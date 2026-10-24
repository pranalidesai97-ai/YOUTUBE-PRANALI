import json, subprocess, sys, os
S = sys.argv[1]; FD = sys.argv[2]; OUT = sys.argv[3]
W = json.load(open(S + "/plan/transcript.json"))["words"]
segs = [i for i in json.load(open(S + "/stage2/edl.json"))["timeline"] if i["type"] == "src"]
def out_t(t):
    for g in segs:
        if g["in"] <= t < g["out"]:
            return g["out_start"] + t - g["in"]
def f(t): return f"{int(t // 60)}:{t % 60:04.1f}" if t is not None else "removed"
def idx(word, near):
    return min((i for i, w in enumerate(W) if w["w"].lower().strip(".,?") == word), key=lambda i: abs(W[i]["start"] - near))
sw, tr, vo, g20 = idx("somewhat", 421.7), idx("tourism", 468.7), idx("very", 686.4), idx("20", 966.0)
items = [
 ("item01_cues37-39_mujhe", "Item 1 · cues 37–39 · 'मुझे'", "Is the second word मुझे?  (sentence: काश मुझे किसी ने पहले बता दिया होता…)", 312, 327, (314, 315)),
 ("item02_cues53-56_R6", "Item 2 · cues 53–56 · R6", "A: …come to the kingdom   B: …Prince Charming will come to rescue you", 383, 395, None),
 ("item03_cue69_R8", "Item 3 · cue 69 · R8", "A: be your pillow   B: be your pillar   C: be your own pillar", 455, 458, None),
 ("item05_cue121", "Item 5 · cue 121", "A: somewhat other way   B: some or the other way   C: some other way", sw - 3, sw + 2, (sw, sw + 2)),
 ("item07_cue138_R14", "Item 7 · cue 138 · R14", "A: Tourism   B: Third is", tr, tr, None),
 ("item09_cue226", "Item 9 · cue 226", "A: Very oddly   B: very early", vo, vo + 1, None),
 ("item11_cue315_was316", "Item 11 · cue 315 (was 316)", "A: you have great 20 years   B: your great twenties", g20 - 3, g20 + 1, None),
]
rows = []
for name, title, opts, i, j, hl in items:
    a = W[i]["start"] - 1.5
    b = min(W[j]["end"], W[j]["start"] + 0.8) + 1.5
    h0, h1 = (W[hl[0]]["start"], min(W[hl[1] - 1 if hl[1] > hl[0] + 1 else hl[1]]["end"], W[hl[1]]["start"] + 0.8)) if hl else (W[i]["start"], min(W[j]["end"], W[j]["start"] + 0.8))
    if hl and hl == (314, 315): h0, h1 = W[314]["start"] - 0.05, W[315]["start"]
    loc = f"source {f(W[i]['start'])}  ·  output {f(out_t(W[i]['start']))}"
    ts = lambda x: f"0:00:{x:05.2f}"
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: T,Poppins Medium,34,&H00FFFFFF,&H00FFFFFF,&H00000000,&H9A1E1620,0,0,0,0,100,100,0,0,3,14,0,8,30,30,24,1
Style: O,Poppins Medium,28,&H00FFFFFF,&H00FFFFFF,&H00000000,&H9A1E1620,0,0,0,0,100,100,0,0,3,12,0,2,30,30,26,1
Style: H,Poppins Medium,30,&H004BB0E3,&H00FFFFFF,&H00000000,&HB01E1620,0,0,0,0,100,100,0,0,3,12,0,5,30,30,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,{ts(0)},{ts(b - a + 1)},T,,0,0,0,,{title}\\N{{\\fs24}}{loc}
Dialogue: 0,{ts(0)},{ts(b - a + 1)},O,,0,0,0,,{opts}
Dialogue: 1,{ts(h0 - a)},{ts(h1 - a + 0.15)},H,,0,0,0,,{{\\pos(1060,300)}}●  flagged words now
"""
    ap = os.path.join(OUT, name + ".ass"); open(ap, "w", encoding="utf-8").write(ass)
    out = os.path.join(OUT, name + ".mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", S + "/src/source_original.mp4",
                    "-map", "0:v:0", "-map", "0:a:0", "-vf", f"fps=30,scale=1280:720:flags=lanczos,ass=filename={ap}:fontsdir={FD}:shaping=complex",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-profile:v", "high",
                    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", out], check=True)
    rows.append((name, title, f(W[i]['start']), f(out_t(W[i]['start'])), round(a, 2), round(b, 2), " ".join(w["w"] for w in W[i:j + 1])))
json.dump(rows, open(os.path.join(OUT, "clips.json"), "w"), ensure_ascii=False, indent=1)
for r in rows: print(r)
