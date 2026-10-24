#!/usr/bin/env python3
"""Final render: EDL + graphics + B-roll + captions + music/SFX mix -> MP4.

Usage: render_final.py SOURCE edl.json gfx_timeline.json manifest.json captions.srt
                       jarring.json audio_dir font_dir OUT.mp4 [T0 T1]

Video is rendered in ~30 s chunks straight from the original (one lossy
generation, H.264 CRF 16 / preset slow, BT.709, 1920x1080 @ 30 fps CFR) and the
chunks are joined without re-encoding. Audio is processed as one continuous
track: cut dialogue -> clean-up chain -> + ducked music + SFX -> 2-pass loudnorm.
"""
import json
import os
import re
import subprocess
import sys

FPS = 30
W, H = 1920, 1080
FACE = (0.47, 0.35)          # measured face centre (x, y) as a fraction of the frame
JUMP_SCALE = 1.06
EASE = 5 / FPS               # overlay ease-in
DRIFT = 8                    # px upward drift during the ease
FADE = 0.012                 # audio micro-fade at every cut
AFFTDN_LATENCY = 1200
TARGET_LUFS, TARGET_TP = -16.0, -1.5
MUSIC_GAIN_DB = -14.0        # music bed relative to its -16 LUFS render (=> ~-30 LUFS bed)
SFX_GAIN_DB = {"pop": -30.0, "swish": -27.0, "swell": -29.0}
VENC = ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-g", "60", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
        "-color_range", "tv", "-r", str(FPS)]
RGBA_IN = "scale=out_color_matrix=bt709:out_range=tv,format=yuva420p"
REPAIRS = []                 # filled from docs/stage2_cuts.json "audio_repairs"


def ff(args, quiet=True):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-y"] + (["-v", "error"] if quiet else []) + args
    r = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + " ".join(cmd)[:3000] + "\n" + r.stderr[-3000:])
    return r.stderr


def window_timeline(tl, t0, t1):
    """Clip the timeline to [t0, t1) of output time, keeping out_start global."""
    out = []
    for it in tl:
        dur = (it["out"] - it["in"]) if it["type"] == "src" else it["dur"]
        a, b = it["out_start"], it["out_start"] + dur
        if b <= t0 or a >= t1:
            continue
        c = dict(it)
        lo, hi = max(a, t0), min(b, t1)
        if it["type"] == "src":
            c["in"], c["out"] = it["in"] + (lo - a), it["in"] + (hi - a)
        else:
            c["dur"] = hi - lo
            c["card_offset"] = lo - a
        c["out_start"] = lo
        out.append(c)
    return out


def item_dur(it):
    return (it["out"] - it["in"]) if it["type"] == "src" else it["dur"]


def parse_srt(path):
    cues = []
    for block in open(path, encoding="utf-8").read().strip().split("\n\n"):
        lines = block.split("\n")
        a, b = [x.strip() for x in lines[1].split("-->")]
        sec = lambda s: int(s[:2]) * 3600 + int(s[3:5]) * 60 + float(s[6:].replace(",", "."))  # noqa: E731
        cues.append((sec(a), sec(b), " ".join(lines[2:])))
    return cues


def ass_time(t):
    t = max(0.0, t)
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def write_ass(cues, hidden, c0, c1, path):
    """Chunk-local ASS. Captions are dropped while full-frame cards, notes,
    pull-quotes or PiP cards are on screen (reference rule), kept over B-roll."""
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins Medium,50,&H00FFFFFF,&H00FFFFFF,&H80140A14,&H90000000,0,0,0,0,100,100,0,0,1,1.8,1.6,2,80,80,92,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    for a, b, text in cues:
        segs = [(a, b)]
        for ha, hb in hidden:
            nxt = []
            for x, y in segs:
                if hb <= x or ha >= y:
                    nxt.append((x, y))
                else:
                    if ha > x:
                        nxt.append((x, ha))
                    if hb < y:
                        nxt.append((hb, y))
            segs = nxt
        for x, y in segs:
            x, y = max(x, c0), min(y, c1)
            if y - x >= 0.25:
                ev.append(f"Dialogue: 0,{ass_time(x - c0)},{ass_time(y - c0)},Cap,,0,0,0,,{text}")
    open(path, "w", encoding="utf-8").write(head + "\n".join(ev) + "\n")


def render_chunk(n, items, overlays, cues, hidden, jumps, src, font_dir, mask, work):
    c0 = items[0]["out_start"]
    c1 = items[-1]["out_start"] + item_dur(items[-1])
    args, g, k = [], [], 0
    for i, it in enumerate(items):
        frames = round(item_dur(it) * FPS)
        if it["type"] == "src":
            # seek half a frame early: the source is VFR with frames ~20 ms off the 1/30 s grid,
            # so this picks the frame *nearest* the cut point instead of the next one
            args += ["-ss", f"{max(0.0, it['in'] - 0.5 / FPS):.4f}", "-t", f"{item_dur(it) + 0.5:.4f}", "-i", src]
            chain = f"[{k}:v:0]fps={FPS},trim=end_frame={frames},setpts=N/{FPS}/TB"
            if it.get("jump"):
                cw, ch = round(W / JUMP_SCALE / 2) * 2, round(H / JUMP_SCALE / 2) * 2
                cx, cy = round(FACE[0] * W - FACE[0] * cw), round(FACE[1] * H - FACE[1] * ch)
                chain += f",crop={cw}:{ch}:{cx}:{cy},scale={W}:{H}:flags=lanczos"
            g.append(chain + ",format=yuv420p,setsar=1" + f"[s{i}]")
        else:
            args += ["-loop", "1", "-framerate", str(FPS), "-i", it["png"]]
            g.append(f"[{k}:v]{RGBA_IN.replace('yuva420p', 'yuv420p')},trim=end_frame={frames},"
                     f"setpts=N/{FPS}/TB,setsar=1[s{i}]")
        k += 1
    g.append("".join(f"[s{i}]" for i in range(len(items))) + f"concat=n={len(items)}:v=1:a=0[base0]")
    cur = "base0"

    def lt(t):  # global -> chunk-local time
        return t - c0

    for o in overlays:
        a, b = max(o["t0"], c0), min(o["t1"], c1)
        if b <= a:
            continue
        en = f"between(t,{lt(a):.3f},{lt(b):.3f})"
        if o["type"] == "pullquote":
            g.append(f"[{cur}]split[pq_a{k}][pq_b{k}];[pq_b{k}]gblur=sigma=9,lutyuv=y=val*0.36:u=128+(val-128)*0.8:"
                     f"v=128+(val-128)*0.8[pq_d{k}];[pq_a{k}][pq_d{k}]overlay=enable='{en}'[pq_o{k}]")
            cur = f"pq_o{k}"
        if o["type"] == "broll":
            start = round((a - o["t0"]) * FPS)
            args += ["-framerate", str(FPS), "-start_number", str(start), "-i", o["frames"]]
            g.append(f"[{k}:v]{RGBA_IN.replace('yuva420p', 'yuv420p')},setpts=PTS-STARTPTS+{lt(a):.3f}/TB[br{k}];"
                     f"[{cur}][br{k}]overlay=enable='{en}':eof_action=pass[bro{k}]")
            cur = f"bro{k}"
            k += 1
            continue
        if o["type"] == "pip":
            x, y, w, h = o["pip_box"]
            cw = round(0.42 * H * 3 / 4 / 2) * 2 * 2
            ch = round(cw * 4 / 3 / 2) * 2
            cx, cy = round(FACE[0] * W - cw / 2), max(0, round(FACE[1] * H - ch * 0.36))
            args += ["-loop", "1", "-framerate", str(FPS), "-i", o["layers"][0]["png"],
                     "-loop", "1", "-framerate", str(FPS), "-i", mask]
            g.append(f"[{cur}]split[pp_a{k}][pp_b{k}];[pp_b{k}]crop={cw}:{ch}:{cx}:{cy},scale={w}:{h}:flags=lanczos,"
                     f"format=yuva420p[pp_c{k}];[{k + 1}:v]{RGBA_IN},crop={w}:{h}:0:0,alphaextract[pp_m{k}];"
                     f"[pp_c{k}][pp_m{k}]alphamerge[pp_r{k}];[{k}:v]{RGBA_IN.replace('yuva420p', 'yuv420p')}[pp_bg{k}];"
                     f"[pp_bg{k}][pp_r{k}]overlay={x}:{y}:shortest=1[pp_card{k}];"
                     f"[pp_a{k}][pp_card{k}]overlay=enable='{en}':shortest=0:eof_action=pass[pp_o{k}]")
            cur = f"pp_o{k}"
            k += 2
            layers = o["layers"][1:]
        else:
            layers = o["layers"]
        for L in layers:
            la = max(L["t"], a)
            lb = min(L.get("t_end", b), b)
            if lb <= la:
                continue
            args += ["-loop", "1", "-framerate", str(FPS), "-i", L["png"]]
            ease_from = lt(L["t"])
            fade = (f",fade=t=in:st={ease_from:.3f}:d={EASE:.3f}:alpha=1" if L["t"] >= c0 else "")
            if "t_end" in L and L["t_end"] <= b:
                fade += f",fade=t=out:st={lt(lb) - 0.4:.3f}:d=0.4:alpha=1"
            y_expr = (f"'{DRIFT}*max(0,1-(t-{ease_from:.3f})/{EASE:.3f})'" if L["t"] >= c0 else "0")
            g.append(f"[{k}:v]{RGBA_IN},setpts=PTS-STARTPTS{fade}[ly{k}];"
                     f"[{cur}][ly{k}]overlay=x=0:y={y_expr}:enable='between(t,{lt(la):.3f},{lt(lb):.3f})':"
                     f"eof_action=pass[lo{k}]")
            cur = f"lo{k}"
            k += 1

    ass = os.path.join(work, f"c{n:03d}.ass")
    write_ass(cues, hidden, c0, c1, ass)
    # 'ass' with complex shaping: the 'subtitles' filter falls back to simple shaping here,
    # which breaks Devanagari conjuncts and pre-base matras (verified on a test frame)
    g.append(f"[{cur}]ass=filename={ass}:fontsdir={font_dir}:shaping=complex,format=yuv420p[vout]")
    gp = os.path.join(work, f"c{n:03d}.graph")
    open(gp, "w").write(";\n".join(g))
    out = os.path.join(work, f"c{n:03d}.mp4")
    ff(args + ["-filter_complex_script", gp, "-map", "[vout]", "-frames:v", str(round((c1 - c0) * FPS)),
               *VENC, "-an", out])
    return out


def build_audio(src, items, overlays, cards, audio_dir, work, total, t_off, fade_out=False):
    """Continuous audio for the whole (windowed) timeline."""
    tone = os.path.join(audio_dir, "roomtone.wav")
    g, args = [], ["-vn", "-i", src, "-stream_loop", "-1", "-i", tone]
    for i, it in enumerate(items):
        d = item_dur(it)
        if it["type"] == "src":
            f = min(FADE, d / 4)
            fix = "".join(f",volume={r['gain']}:enable='between(t,{max(0.0, r['start'] - it['in']):.4f},"
                          f"{r['end'] - it['in']:.4f})'"
                          for r in REPAIRS if r["start"] < it["out"] and r["end"] > it["in"])
            g.append(f"[0:a:0]atrim=start={it['in']:.4f}:end={it['out']:.4f},asetpts=PTS-STARTPTS{fix},"
                     f"afade=t=in:d={f:.4f},afade=t=out:st={d - f:.4f}:d={f:.4f}[d{i}]")
        else:
            g.append(f"[1:a]atrim=duration={d:.4f},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d=0.05,afade=t=out:st={max(0, d - 0.05):.4f}:d=0.05[d{i}]")
    g.append("".join(f"[d{i}]" for i in range(len(items))) + f"concat=n={len(items)}:v=0:a=1,"
             "aresample=48000,highpass=f=70:p=2,afftdn=nr=10:nf=-67:tn=1:om=o,"
             f"atrim=start_sample={AFFTDN_LATENCY},asetpts=PTS-STARTPTS,apad=pad_len={AFFTDN_LATENCY},"
             "adeclick=w=55:o=75:a=2:t=8,equalizer=f=250:t=q:w=1.0:g=-1.5,equalizer=f=3500:t=q:w=1.2:g=1.5,"
             "acompressor=threshold=-22dB:ratio=2:attack=15:release=250:makeup=1:knee=6,"
             f"atrim=duration={total:.4f}[dlg]")
    gp = os.path.join(work, "dialogue.graph")
    open(gp, "w").write(";\n".join(g))
    dlg = os.path.join(work, "dialogue.wav")
    ff(args + ["-filter_complex_script", gp, "-map", "[dlg]", "-c:a", "pcm_s24le", dlg])

    # SFX events (output time relative to the window start)
    events = [(c["out_start"], "swish") for c in cards if c["name"] != "end_screen"]
    for o in overlays:
        if o["type"] in ("notes", "keywords"):
            events += [(L["t"], "pop") for L in o["layers"]]
        elif o["type"] == "pullquote":
            events.append((o["t0"], "swell"))
        elif o["type"] in ("pip", "corner_card"):
            events.append((o["t0"], "swish"))
    events = [(t - t_off, s) for t, s in events if 0 <= t - t_off < total]
    args = ["-i", dlg, "-ss", f"{t_off:.3f}", "-t", f"{total:.3f}", "-i", os.path.join(audio_dir, "music_full.wav")]
    end_fade = f",afade=t=out:st={total - 3.0:.3f}:d=3" if fade_out else ""
    g = [f"[1:a]volume={MUSIC_GAIN_DB}dB,afade=t=in:d=1.5{end_fade}[mus]",
         "[0:a]asplit[dl][key]",
         "[mus][key]sidechaincompress=threshold=0.015:ratio=6:attack=40:release=450:knee=4[duck]"]
    mix_in = ["[dl]", "[duck]"]
    for i, (t, s) in enumerate(events):
        args += ["-i", os.path.join(audio_dir, "sfx", s + ".wav")]
        ms = int(t * 1000)
        g.append(f"[{i + 2}:a]volume={SFX_GAIN_DB[s]}dB,adelay={ms}|{ms}[x{i}]")
        mix_in.append(f"[x{i}]")
    g.append("".join(mix_in) + f"amix=inputs={len(mix_in)}:normalize=0:duration=first,"
             f"atrim=duration={total:.4f}[mix]")
    gp = os.path.join(work, "mix.graph")
    open(gp, "w").write(";\n".join(g))
    pre = os.path.join(work, "mix_pre.wav")
    ff(args + ["-filter_complex_script", gp, "-map", "[mix]", "-c:a", "pcm_s24le", pre])
    err = ff(["-i", pre, "-af", f"loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:LRA=11:print_format=json",
              "-f", "null", "-"], quiet=False)
    m = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    final = os.path.join(work, "mix_final.wav")
    ff(["-i", pre, "-af", f"loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:LRA=11:measured_I={m['input_i']}:"
                          f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
                          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
                          f"aresample=48000", "-c:a", "pcm_s24le", final])
    return final, events


def main():
    (src, edl_path, gfx_path, man_path, srt, jar_path, audio_dir, font_dir, out) = sys.argv[1:10]
    win = (float(sys.argv[10]), float(sys.argv[11])) if len(sys.argv) > 11 else None
    edl = json.load(open(edl_path))
    man = json.load(open(man_path))
    # source-time audio repairs (e.g. a stray non-speech sound in a pause), from the cut spec
    spec = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "stage2_cuts.json")
    REPAIRS[:] = json.load(open(spec)).get("audio_repairs", [])
    gfx_tl = {g["id"]: g for g in json.load(open(gfx_path))}
    tl = edl["timeline"]
    t0, t1 = win if win else (0.0, edl["duration"])
    items = window_timeline(tl, t0, t1)
    for it in items:
        if it["type"] == "card":
            it["png"] = man["cards"][it["name"]]

    overlays = []
    for m in man["items"]:
        o = dict(m)
        o.update({k: v for k, v in gfx_tl[m["id"]].items() if k not in o})
        if o["type"] == "broll" and "frames" not in o:
            continue
        overlays.append(o)

    # graphic-covered ranges hide captions; full-frame cards too
    hidden = [(o["t0"], o["t1"]) for o in overlays if o["type"] in ("notes", "pullquote", "pip")]
    hidden += [(c["out_start"], c["out_start"] + item_dur(c)) for c in items if c["type"] == "card"]

    # 106 % framing on jarring jump cuts not covered by a graphic or B-roll
    covered = [(o["t0"], o["t1"]) for o in overlays]
    jar_t = [j["output_t"] for j in json.load(open(jar_path))]
    for it in items:
        if it["type"] == "src" and any(abs(it["out_start"] - t) < 0.05 for t in jar_t) \
                and not any(a - 0.1 <= it["out_start"] <= b for a, b in covered):
            it["jump"] = True

    work = out + ".work"
    os.makedirs(work, exist_ok=True)
    cues = parse_srt(srt)

    chunks, cur = [], []
    for it in items:
        cur.append(it)
        if sum(item_dur(x) for x in cur) >= 30 or len(cur) >= 10:
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    # RERENDER="0,5" re-renders only those chunks and reuses the others already in the work dir
    only = {int(x) for x in os.environ.get("RERENDER", "").split(",") if x.strip()}
    parts = []
    for n, ch in enumerate(chunks):
        done = os.path.join(work, f"c{n:03d}.mp4")
        if only and n not in only and os.path.exists(done):
            parts.append(done)
            continue
        print(f"chunk {n + 1}/{len(chunks)}  {ch[0]['out_start']:.1f}s", flush=True)
        parts.append(render_chunk(n, ch, overlays, cues, hidden, None, src, font_dir, man["pip_mask"], work))
    lst = os.path.join(work, "parts.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))

    total = t1 - t0
    cards = [c for c in items if c["type"] == "card"]
    # the music fades out over the last 3 s when the render reaches the end of the edit
    if only and os.path.exists(os.path.join(work, "mix_final.wav")):   # audio unchanged: reuse it
        audio, events = os.path.join(work, "mix_final.wav"), json.load(open(out + ".render.json"))["sfx_events"]
    else:
        audio, events = build_audio(src, items, overlays, cards, audio_dir, work, total, t0,
                                    fade_out=abs(t1 - edl["duration"]) < 0.01)
    ff(["-f", "concat", "-safe", "0", "-i", lst, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", out])
    # (no -shortest: it drops the last few video frames; both streams are already the same length)
    json.dump({"window": [t0, t1], "sfx_events": events,
               "jump_framing": [it["out_start"] for it in items if it.get("jump")]},
              open(out + ".render.json", "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
