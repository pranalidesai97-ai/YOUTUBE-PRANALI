#!/usr/bin/env python3
"""Local word-timestamped transcript (sherpa-onnx + NVIDIA Parakeet TDT).

Speech is chunked at pauses with the Silero VAD so each chunk is <= 25 s,
then every chunk is transcribed offline. Nothing leaves the machine.

Usage: transcribe.py SOURCE MODEL_DIR OUT.json
Output: {"words": [{"w", "start", "end"}], "segments": [{"start", "end", "text"}]}
(times in source seconds)
"""
import json
import os
import subprocess
import sys

import numpy as np
import sherpa_onnx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clean_talking_head import VAD_STEP, silero_probs  # noqa: E402

SR = 16000
MAX_CHUNK = 25.0
MERGE_GAP = 0.6
EDGE_PAD = 0.25


def chunks(probs, total):
    speech, i = [], 0
    while i < len(probs):
        if probs[i] >= 0.5:
            j = i
            while j < len(probs) and probs[j] >= 0.35:
                j += 1
            speech.append([i * VAD_STEP, j * VAD_STEP])
            i = j
        else:
            i += 1
    merged = []
    for s, e in speech:
        if merged and s - merged[-1][1] < MERGE_GAP and e - merged[-1][0] <= MAX_CHUNK:
            merged[-1][1] = e
        else:
            merged.append([s, e])
    out = []
    for s, e in merged:
        # split anything still too long at the least speech-like frame
        while e - s > MAX_CHUNK:
            a, b = int((s + MAX_CHUNK * 0.5) / VAD_STEP), int((s + MAX_CHUNK) / VAD_STEP)
            k = a + int(np.argmin(probs[a:b]))
            out.append([s, k * VAD_STEP])
            s = k * VAD_STEP
        out.append([s, e])
    return [(max(0.0, s - EDGE_PAD), min(total, e + EDGE_PAD)) for s, e in out]


def main():
    src, model, out_path = sys.argv[1:4]
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", src, "-map", "0:a:0",
                          "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         stdout=subprocess.PIPE, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    total = len(x) / SR
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=os.path.join(model, "encoder.int8.onnx"),
        decoder=os.path.join(model, "decoder.int8.onnx"),
        joiner=os.path.join(model, "joiner.int8.onnx"),
        tokens=os.path.join(model, "tokens.txt"),
        model_type="nemo_transducer", num_threads=4)
    words, segments = [], []
    for n, (s, e) in enumerate(chunks(silero_probs(src, None, None), total)):
        st = rec.create_stream()
        st.accept_waveform(SR, x[int(s * SR):int(e * SR)])
        rec.decode_stream(st)
        r = st.result
        seg_words = []
        for tok, t in zip(r.tokens, r.timestamps):
            t = s + float(t)
            if tok.startswith(" ") or tok.startswith("▁") or not seg_words:
                seg_words.append({"w": tok.strip().lstrip("▁"), "start": round(t, 3)})
            else:
                seg_words[-1]["w"] += tok
        for k, w in enumerate(seg_words):
            nxt = seg_words[k + 1]["start"] if k + 1 < len(seg_words) else e - EDGE_PAD
            w["end"] = round(min(nxt, w["start"] + 1.0), 3)
        words += seg_words
        segments.append({"start": round(s, 3), "end": round(e, 3), "text": r.text.strip()})
        print(f"{n:4d} {s:8.2f}-{e:8.2f} {r.text.strip()[:90]}", flush=True)
    json.dump({"words": words, "segments": segments}, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main()
