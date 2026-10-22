#!/usr/bin/env python3
"""First-pass clean-up of a talking-head video.

- Removes clearly unnecessary pauses (> MIN_GAP seconds) but keeps a natural
  pause and padding around every word, so word onsets/tails are never cut.
- Leaves borderline gaps (low-level sound that might be quiet speech) uncut
  and flags them for review.
- Gentle audio clean-up: high-pass, light FFT denoise, mild de-click, gentle
  EQ, light compression, two-pass EBU R128 loudness normalisation.
- Frame-accurate cuts (re-encode, H.264 CRF 16 + AAC), original resolution,
  frame rate, pixel format and colour tags preserved. No speed changes.
- Never modifies the source file.

Usage:
  clean_talking_head.py SOURCE OUTDIR [--test-start S --test-duration D]
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys
from fractions import Fraction

MIN_GAP = 0.8          # only gaps longer than this are candidates
PAD_BEFORE_CUT = 0.30  # silence kept after the end of speech (word tail, breath)
PAD_AFTER_CUT = 0.20   # silence kept before speech resumes (word onset)
LONG_GAP = 2.0         # gaps this long keep a slightly longer pause
LONG_GAP_EXTRA = 0.25
MIN_REMOVAL = 0.30     # don't bother with tiny removals (rhythm > seconds saved)
WINDOW = 0.05          # analysis window, seconds
FADE = 0.012           # audio micro-fade at every cut, seconds (prevents clicks)
TARGET_LUFS = -16.0
TARGET_TP = -1.5
TARGET_LRA = 11.0


def run(cmd, capture=True):
    r = subprocess.run(cmd, stdout=subprocess.PIPE if capture else None,
                       stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd)}\n{r.stderr[-3000:]}")
    return r


def probe(path):
    r = run(["ffprobe", "-v", "error", "-show_format", "-show_streams",
             "-of", "json", path])
    return json.loads(r.stdout)


def describe(info):
    lines = []
    fmt = info["format"]
    lines.append(f"container: {fmt.get('format_name')}  duration: "
                 f"{float(fmt['duration']):.3f}s  bitrate: "
                 f"{int(fmt.get('bit_rate', 0)) // 1000} kb/s")
    for s in info["streams"]:
        if s["codec_type"] == "video":
            lines.append(
                f"video #{s['index']}: {s['codec_name']} {s.get('profile', '')} "
                f"{s['width']}x{s['height']} {s.get('pix_fmt')} "
                f"r_frame_rate={s['r_frame_rate']} avg={s['avg_frame_rate']} "
                f"color={s.get('color_space')}/{s.get('color_primaries')}/"
                f"{s.get('color_transfer')}/{s.get('color_range')} "
                f"rotation={s.get('side_data_list', [{}])[0].get('rotation', 0) if s.get('side_data_list') else 0}")
        elif s["codec_type"] == "audio":
            lines.append(
                f"audio #{s['index']}: {s['codec_name']} {s['sample_rate']} Hz "
                f"{s.get('channels')}ch {s.get('channel_layout', '')} "
                f"{int(s.get('bit_rate', 0) or 0) // 1000} kb/s")
        else:
            lines.append(f"other #{s['index']}: {s['codec_type']} {s.get('codec_name')}")
    return "\n".join(lines)


def rms_series(path, start, dur):
    """Per-window RMS level (dBFS) of the first audio stream."""
    sr = 48000
    n = int(sr * WINDOW)
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-v", "error"]
    if start is not None:
        cmd += ["-ss", str(start), "-t", str(dur)]
    cmd += ["-i", path, "-map", "0:a:0", "-ac", "1", "-ar", str(sr),
            "-af", f"highpass=f=80,asetnsamples=n={n}:p=0,"
                   "astats=metadata=1:reset=1:measure_overall=RMS_level:measure_perchannel=none,"
                   "ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-",
            "-f", "null", "-"]
    out = run(cmd).stdout
    levels = []
    for m in re.finditer(r"RMS_level=(-?[\d.]+|-inf)", out):
        v = m.group(1)
        levels.append(-120.0 if v == "-inf" else max(-120.0, float(v)))
    return levels


def percentile(vals, p):
    s = sorted(vals)
    return s[min(len(s) - 1, int(p / 100 * len(s)))]


def find_gaps(levels):
    floor = percentile(levels, 10)
    speech = percentile(levels, 90)
    thr = min(floor + 10.0, speech - 25.0)
    thr = max(thr, floor + 4.0)
    gaps, i = [], 0
    while i < len(levels):
        if levels[i] < thr:
            j = i
            while j < len(levels) and levels[j] < thr:
                j += 1
            s, e = i * WINDOW, j * WINDOW
            if e - s > MIN_GAP:
                gaps.append((s, e, max(levels[i:j])))
            i = j
        else:
            i += 1
    return gaps, floor, speech, thr


def plan_cuts(gaps, thr, total):
    """Return (removals, flagged) in source-relative seconds."""
    removals, flagged = [], []
    for s, e, peak in gaps:
        g = e - s
        keep = PAD_BEFORE_CUT + PAD_AFTER_CUT + (LONG_GAP_EXTRA if g >= LONG_GAP else 0)
        if s <= 0.0 or e >= total - WINDOW:
            # leading/trailing silence: keep a short natural head/tail
            keep = 0.5
        cs, ce = s + PAD_BEFORE_CUT, e - PAD_AFTER_CUT
        if s <= 0.0:
            cs, ce = 0.0, e - 0.5
        elif e >= total - WINDOW:
            cs, ce = s + 0.5, total
        if ce - cs < MIN_REMOVAL:
            continue
        # borderline content inside the gap (soft speech / mumble / trailing
        # word) -> don't cut, flag it
        if peak > thr - 3.0:
            flagged.append((s, e, peak, "low-level sound inside gap; may be quiet speech"))
            continue
        removals.append((cs, ce, s, e, g, keep))
    return removals, flagged


def snap(t, fps):
    return float(round(Fraction(t) * fps) / fps)


def keep_segments(removals, total, fps):
    segs, cur = [], 0.0
    for cs, ce, *_ in removals:
        a, b = snap(cur, fps), snap(cs, fps)
        if b - a > 1 / float(fps):
            segs.append((a, b))
        cur = ce
    a, b = snap(cur, fps), snap(total, fps)
    if b - a > 1 / float(fps):
        segs.append((a, b))
    return segs


def audio_chain(floor_db):
    nf = max(-80, min(-20, round(floor_db)))
    return ("highpass=f=70:p=2,"
            f"afftdn=nr=10:nf={nf}:tn=1:om=o,"
            "adeclick=w=55:o=75:a=2:t=8,"
            "equalizer=f=250:t=q:w=1.0:g=-1.5,"
            "equalizer=f=3500:t=q:w=1.2:g=1.5,"
            "acompressor=threshold=-22dB:ratio=2:attack=15:release=250:makeup=1:knee=6")


def build_graph(segs, achain, loudnorm):
    lines = []
    n = len(segs)
    for i, (a, b) in enumerate(segs):
        lines.append(f"[0:v:0]trim=start={a:.6f}:end={b:.6f},setpts=PTS-STARTPTS[v{i}];")
        d = b - a
        fade = min(FADE, d / 4)
        lines.append(f"[0:a:0]atrim=start={a:.6f}:end={b:.6f},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d={fade:.4f},afade=t=out:st={d - fade:.6f}:d={fade:.4f}[a{i}];")
    lines.append("".join(f"[v{i}][a{i}]" for i in range(n)) +
                 f"concat=n={n}:v=1:a=1[vc][ac];")
    lines.append(f"[ac]{achain},{loudnorm}[aout]")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("outdir")
    ap.add_argument("--test-start", type=float)
    ap.add_argument("--test-duration", type=float, default=90.0)
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--preset", default="slow")
    ap.add_argument("--plan-only", action="store_true")
    args = ap.parse_args()

    src = os.path.abspath(args.source)
    os.makedirs(args.outdir, exist_ok=True)
    out_dir = os.path.abspath(args.outdir)
    # outputs are always named cleaned_*; refuse anything that could touch the source
    if os.path.basename(src).startswith("cleaned_") and os.path.dirname(src) == out_dir:
        sys.exit("source lives in the output folder with an output-style name; pick another outdir")
    info = probe(src)
    print(describe(info))
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    if a is None:
        sys.exit("source has no audio stream")
    fps = Fraction(v["r_frame_rate"])
    if Fraction(v["avg_frame_rate"] or "0/1") not in (fps, 0):
        print(f"WARNING: r_frame_rate {v['r_frame_rate']} != avg_frame_rate "
              f"{v['avg_frame_rate']} (possible VFR source; output is CFR at r_frame_rate)")

    full = float(info["format"]["duration"])
    start = args.test_start
    total = min(args.test_duration, full - start) if start is not None else full
    tag = f"test_{int(start)}s" if start is not None else "full"

    levels = rms_series(src, start, total)
    gaps, floor, speech, thr = find_gaps(levels)
    removals, flagged = plan_cuts(gaps, thr, total)
    segs = keep_segments(removals, total, fps)
    off = start or 0.0

    print(f"noise floor {floor:.1f} dBFS, speech {speech:.1f} dBFS, "
          f"silence threshold {thr:.1f} dBFS")
    print(f"gaps > {MIN_GAP}s detected: {len(gaps)}; removed: {len(removals)}; "
          f"flagged/left uncut: {len(flagged)}")

    base = os.path.join(out_dir, f"cleaned_{tag}")
    with open(base + "_cutlist.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["#", "action", "gap_start", "gap_end", "gap_len_s",
                    "removed_start", "removed_end", "removed_s", "pause_kept_s", "note"])
        rows = [(r[2], "removed", r) for r in removals] + [(x[0], "flagged", x) for x in flagged]
        for k, (_, kind, r) in enumerate(sorted(rows, key=lambda t: t[0]), 1):
            if kind == "removed":
                cs, ce, s, e, g, keep = r
                w.writerow([k, "removed", ts(s + off), ts(e + off), f"{g:.2f}",
                            ts(cs + off), ts(ce + off), f"{ce - cs:.2f}", f"{keep:.2f}", ""])
            else:
                s, e, peak, note = r
                w.writerow([k, "kept (review)", ts(s + off), ts(e + off), f"{e - s:.2f}",
                            "", "", "0", f"{e - s:.2f}", f"{note} (peak {peak:.1f} dBFS)"])
    kept = sum(b - a for a, b in segs)
    print(f"planned output duration {kept:.2f}s (source {total:.2f}s, "
          f"removed {total - kept:.2f}s)")
    if args.plan_only:
        return

    achain = audio_chain(floor)
    inp = ["-ss", str(start), "-t", str(total)] if start is not None else []

    # pass 1: loudness measurement on the cut + cleaned audio
    g1 = build_graph(segs, achain, f"loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:"
                                   f"LRA={TARGET_LRA}:print_format=json")
    gp = base + "_graph1.txt"
    open(gp, "w").write(g1.replace(";\n[ac]", ";\n[vc]nullsink;\n[ac]"))
    r = run(["ffmpeg", "-nostdin", "-hide_banner", *inp, "-i", src,
             "-filter_complex_script", gp, "-map", "[aout]", "-f", "null", "-"])
    m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    ln = (f"loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:LRA={TARGET_LRA}:"
          f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
          f"offset={m['target_offset']}:linear=true,aresample=48000")

    # pass 2: render
    g2 = build_graph(segs, achain, ln)
    gp2 = base + "_graph2.txt"
    open(gp2, "w").write(g2)
    color = []
    for key, opt in (("color_primaries", "-color_primaries"), ("color_transfer", "-color_trc"),
                     ("color_space", "-colorspace"), ("color_range", "-color_range")):
        if v.get(key) and v[key] != "unknown":
            color += [opt, v[key]]
    pix = v.get("pix_fmt", "yuv420p")
    if pix not in ("yuv420p", "yuvj420p", "yuv422p", "yuv444p", "yuv420p10le"):
        pix = "yuv420p"
    out = base + ".mp4"
    run(["ffmpeg", "-nostdin", "-hide_banner", "-y", *inp, "-i", src,
         "-filter_complex_script", gp2, "-map", "[vc]", "-map", "[aout]",
         "-c:v", "libx264", "-crf", str(args.crf), "-preset", args.preset,
         "-pix_fmt", pix, "-r", str(fps), "-fps_mode", "cfr", *color,
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         "-map_metadata", "0", "-movflags", "+faststart", out], capture=False)
    print(f"wrote {out}")


def ts(t):
    h, rem = divmod(t, 3600)
    mnt, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(mnt):02d}:{s:06.3f}"


if __name__ == "__main__":
    main()
