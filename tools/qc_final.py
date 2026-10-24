#!/usr/bin/env python3
"""Technical QC of the final export.

Usage: qc_final.py FINAL.mp4 SOURCE edl.json gfx_timeline.json captions.srt OUT_DIR
Writes OUT_DIR/qc_report.json plus contact sheets (PNG/JPG) for visual review.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def grab(path, t, size=None, gray=False):
    vf = [f"scale={size[0]}:{size[1]}"] if size else []
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{max(0, t):.4f}", "-i", path, "-frames:v", "1"]
    if gray:
        cmd += ["-vf", ",".join(vf + ["format=gray"]), "-f", "rawvideo", "-"]
        return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.uint8).astype(float)
    out = os.path.join(OUT, "_f.png")
    subprocess.run(cmd + (["-vf", ",".join(vf)] if vf else []) + ["-y", out], check=True)
    return Image.open(out).convert("RGB")


def sheet(name, shots, cols=3, w=640):
    h = w * 9 // 16
    rows = (len(shots) + cols - 1) // cols
    img = Image.new("RGB", (cols * w, rows * (h + 30)), "white")
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    for n, (label, t) in enumerate(shots):
        x, y = (n % cols) * w, (n // cols) * (h + 30)
        img.paste(grab(FINAL, t).resize((w, h)), (x, y + 30))
        d.text((x + 6, y + 8), f"{label}  @ {int(t // 60)}:{t % 60:05.2f}", fill="black")
    p = os.path.join(OUT, name)
    img.save(p, quality=85)
    return p


def main():
    global FINAL, OUT
    FINAL, src, edl_p, gfx_p, srt_p, OUT = sys.argv[1:7]
    os.makedirs(OUT, exist_ok=True)
    edl = json.load(open(edl_p))
    gfx = json.load(open(gfx_p))
    rep = {"file": FINAL, "size_bytes": os.path.getsize(FINAL)}

    pr = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", FINAL]).stdout)
    v = next(s for s in pr["streams"] if s["codec_type"] == "video")
    a = next(s for s in pr["streams"] if s["codec_type"] == "audio")
    rep["video"] = {k: v.get(k) for k in ("codec_name", "profile", "level", "width", "height", "sample_aspect_ratio",
                                          "display_aspect_ratio", "pix_fmt", "r_frame_rate", "avg_frame_rate",
                                          "nb_frames", "duration", "bit_rate", "color_space", "color_primaries",
                                          "color_transfer", "color_range")}
    rep["audio"] = {k: a.get(k) for k in ("codec_name", "profile", "sample_rate", "channels", "channel_layout",
                                          "bit_rate", "duration")}
    rep["format_duration"] = float(pr["format"]["duration"])
    rep["expected_duration"] = edl["duration"]
    rep["expected_frames"] = round(edl["duration"] * 30)
    with open(FINAL, "rb") as f:
        head = f.read(4_000_000)
    m = re.search(rb"x264 - core \d+.*?options: (.*?)\x00", head, re.S)
    opts = m.group(1).decode(errors="replace") if m else ""
    rep["x264"] = {k: (re.search(rf"\b{k}=([^ ]+)", opts) or [None, None])[1] for k in ("crf", "rc", "keyint", "ref", "subme", "me", "bframes")}
    rep["faststart"] = head.find(b"moov") < head.find(b"mdat")

    dec = run(["ffmpeg", "-v", "error", "-i", FINAL, "-f", "null", "-"])
    rep["decode_errors"] = [l for l in dec.stderr.splitlines() if l.strip()][:20]

    det = run(["ffmpeg", "-hide_banner", "-i", FINAL, "-an", "-vf",
               "blackdetect=d=0.04:pix_th=0.05,freezedetect=n=0.001:d=1.0", "-f", "null", "-"]).stderr
    rep["black"] = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", det)
    fs = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", det)]
    fe = [float(x) for x in re.findall(r"freeze_end: ([\d.]+)", det)]
    cards = [(c["name"], c["out_start"], c["out_start"] + c["dur"]) for c in edl["timeline"] if c["type"] == "card"]
    freezes = []
    for s_, e_ in zip(fs, fe + [rep["format_duration"]] * (len(fs) - len(fe))):
        card = next((c[0] for c in cards if c[1] - 0.2 <= s_ <= c[2] and e_ <= c[2] + 0.2), None)
        freezes.append({"start": s_, "end": e_, "explained_by": card})
    rep["freezes"] = freezes

    loud = run(["ffmpeg", "-hide_banner", "-i", FINAL, "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    summ = loud[loud.rfind("Summary:"):]
    rep["loudness"] = {"I_LUFS": float(re.search(r"I:\s+(-?[\d.]+)", summ).group(1)),
                       "LRA": float(re.search(r"LRA:\s+(-?[\d.]+)", summ).group(1)),
                       "true_peak_dBFS": float(re.search(r"Peak:\s+(-?[\d.]+)", summ).group(1))}
    sil = run(["ffmpeg", "-hide_banner", "-i", FINAL, "-vn", "-af", "silencedetect=noise=-55dB:d=0.25", "-f", "null", "-"]).stderr
    rep["audio_dropouts_below_-55dB_over_0.25s"] = re.findall(r"silence_start: ([\d.]+)", sil)

    # sync: picture vs source frame, and audio vs source audio, on many A-roll segments
    segs = [i for i in edl["timeline"] if i["type"] == "src" and i["out"] - i["in"] > 1.5]
    covered = [(g["t0"], g["t1"]) for g in gfx if g["type"] in ("broll", "pip", "pullquote")]
    segs = [s for s in segs if not any(a_ - 0.2 < s["out_start"] + (s["out"] - s["in"]) / 2 < b_ + 0.2 for a_, b_ in covered)]
    pick = [segs[int(k * (len(segs) - 1) / 11)] for k in range(12)]
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-map", "0:a:0", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    sx = np.frombuffer(raw, np.int16).astype(float)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", FINAL, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    fx = np.frombuffer(raw, np.int16).astype(float)
    sync = []
    for s in pick:
        mid = (s["out"] - s["in"]) / 2
        ot, st = s["out_start"] + mid, s["in"] + mid
        a_img = grab(FINAL, ot, (320, 180), True)
        errs = {o: float(np.abs(a_img - grab(src, st + o / 30, (320, 180), True)).mean()) for o in (-2, -1, 0, 1, 2)}
        x = sx[int((st - 0.6) * 16000):int((st + 0.6) * 16000)]
        best = None
        for lag in range(-480, 481, 4):
            y = fx[int((ot - 0.6) * 16000) + lag:int((ot - 0.6) * 16000) + lag + len(x)]
            c = float(np.dot(x, y) / np.sqrt(np.dot(x, x) * np.dot(y, y) + 1e-9))
            if best is None or c > best[0]:
                best = (c, lag)
        sync.append({"output_t": round(ot, 2), "picture_offset_frames": min(errs, key=errs.get),
                     "audio_offset_ms": round(best[1] / 16, 1), "audio_corr": round(best[0], 2)})
    rep["sync"] = sync

    # visual sheets
    T = rep["format_duration"]
    rep["sheets"] = {}
    rep["sheets"]["start_end"] = sheet("qc_start_end.jpg", [("start", 0.5), ("start", 3.0), ("start", 8.0),
                                                           ("end screen", T - 9.0), ("end screen", T - 2.0), ("last frame", T - 0.05)])
    tr = []
    for name, t0, t1 in cards:
        tr += [(f"before {name}", t0 - 0.2), (name, t0 + 1.0), (f"after {name}", t1 + 0.3)]
    rep["sheets"]["transitions"] = sheet("qc_chapter_transitions.jpg", tr)
    br = []
    for g in gfx:
        if g["type"] == "broll":
            br += [(f"{g['id']} in", g["t0"] + 0.2), (f"{g['id']} mid", (g["t0"] + g["t1"]) / 2), (f"{g['id']} out", g["t1"] + 0.2)]
    rep["sheets"]["broll"] = sheet("qc_broll_inserts.jpg", br)
    gr = [(g["id"], (g["t0"] + g["t1"]) / 2 if g["type"] != "keywords" else g["t1"] - 1.0) for g in gfx
          if g["type"] in ("notes", "pullquote", "pip", "corner_card", "keywords")]
    rep["sheets"]["graphics"] = sheet("qc_graphics.jpg", gr, cols=4, w=480)
    rep["sheets"]["throughout"] = sheet("qc_every_minute.jpg", [(f"{m} min", m * 60 + 30) for m in range(int(T // 60) + 1) if m * 60 + 30 < T], cols=4, w=480)

    # Hindi captions: full-resolution crops of the caption area while each Devanagari cue is up
    cues = []
    for b in open(srt_p, encoding="utf-8").read().strip().split("\n\n"):
        L = b.split("\n")
        if re.search("[\u0900-\u097F]", " ".join(L[2:])):
            ts_ = L[1].split(" --> ")[0]
            t = int(ts_[:2]) * 3600 + int(ts_[3:5]) * 60 + float(ts_[6:].replace(",", "."))
            cues.append((" ".join(L[2:]), t + 0.25))
    crops = [grab(FINAL, t).crop((260, 900, 1660, 1060)) for _, t in cues]
    img = Image.new("RGB", (1400, 160 * len(crops)), "black")
    for n, c in enumerate(crops):
        img.paste(c, (0, n * 160))
    p = os.path.join(OUT, "qc_hindi_captions.png")
    img.save(p)
    rep["sheets"]["hindi_captions"] = p
    rep["hindi_cues"] = cues
    json.dump(rep, open(os.path.join(OUT, "qc_report.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: rep[k] for k in ("video", "audio", "format_duration", "expected_duration", "expected_frames",
                                          "x264", "faststart", "decode_errors", "black", "freezes", "loudness",
                                          "audio_dropouts_below_-55dB_over_0.25s", "sync")}, indent=1))


if __name__ == "__main__":
    main()
