#!/usr/bin/env python3
"""Stage-2 edit decision list: approved retake removals + natural pause tightening.

Inputs: source video, word-timestamped transcript, cut spec (docs/stage2_cuts.json).
Output: edl.json  - ordered timeline of source ranges and inserted cards
        cuts.csv  - every removal with source timestamps, reason and removed words
Times in the EDL are source seconds snapped to the 30 fps frame grid.

Word timestamps mark word *starts*; actual speech edges are found from the
audio (10 ms RMS + Silero VAD) so no word onset or tail is clipped.
"""
import csv
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clean_talking_head import VAD_STEP, silero_probs  # noqa: E402

SR = 16000
HOP = 0.01
FPS = 30
TAIL_KEEP = 0.12      # silence kept after speech at a join
HEAD_KEEP = 0.08      # silence kept before speech resumes
PAUSE_MID = 0.20      # tightened pause inside a sentence
PAUSE_END = 0.30      # tightened pause after . ? !
MIN_PAUSE = 0.35      # shorter pauses are left as they are
EDGE_MARGIN = 0.04    # keep cut edges this far from removed-word onsets
VAD_GUARD = 0.35      # any frame this speech-like inside a pause -> leave it alone


def snap(t):
    return round(t * FPS) / FPS


class Audio:
    def __init__(self, src):
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", src, "-map", "0:a:0",
                              "-ac", "1", "-ar", str(SR), "-af", "highpass=f=80",
                              "-f", "s16le", "-"], stdout=subprocess.PIPE, check=True).stdout
        x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
        n = int(HOP * SR)
        frames = x[:len(x) // n * n].reshape(-1, n)
        self.db = 10 * np.log10(np.mean(frames ** 2, axis=1) + 1e-12)
        self.total = len(x) / SR
        speech = np.percentile(self.db, 90)
        floor = np.percentile(self.db, 10)
        self.thr = max(speech - 30.0, floor + 4.0)
        self.vad = np.array(silero_probs(src, None, None))

    def quiet(self, t):
        i = int(t / HOP)
        if i >= len(self.db):
            return True
        v = self.vad[min(len(self.vad) - 1, int(t / VAD_STEP))]
        return self.db[i] < self.thr and v < VAD_GUARD

    def speech_end(self, t, limit):
        """First moment after t where >= 60 ms of quiet begins (searching up to limit)."""
        k = t
        while k < limit:
            if all(self.quiet(k + d * HOP) for d in range(6)):
                return k
            k += HOP
        return self.quietest(t, limit)

    def speech_onset(self, t, limit):
        """Last moment before t where >= 60 ms of quiet ends (searching back to limit)."""
        k = t
        while k > limit:
            if all(self.quiet(k - (d + 1) * HOP) for d in range(6)):
                return k
            k -= HOP
        return self.quietest(limit, t)

    def has_gap(self, a, b):
        """True if [a, b] contains >= 60 ms of continuous quiet."""
        k = a
        while k + 0.06 <= b:
            if all(self.quiet(k + d * HOP) for d in range(6)):
                return True
            k += HOP
        return False

    def quietest(self, a, b):
        i, j = int(a / HOP), max(int(a / HOP) + 1, int(b / HOP))
        return (i + int(np.argmin(self.db[i:j]))) * HOP

    def pauses(self, a, b):
        """Quiet runs >= MIN_PAUSE fully inside [a, b]."""
        out, k = [], a
        while k < b:
            if self.quiet(k):
                s = k
                while k < b and self.quiet(k):
                    k += HOP
                if k - s >= MIN_PAUSE and s > a and k < b:
                    out.append((s, k))
            k += HOP
        return out


def main():
    src, transcript, spec_path, out_dir = sys.argv[1:5]
    W = json.load(open(transcript))["words"]
    spec = json.load(open(spec_path))
    au = Audio(src)
    os.makedirs(out_dir, exist_ok=True)

    # 1. approved removals (word index ranges) -> source time ranges
    removed = set()
    removals = []
    for r in spec["remove"]:
        i, j = r["words"]
        removed.update(range(i, j + 1))
        prev_start = W[i - 1]["start"] if i > 0 else None
        nxt_start = W[j + 1]["start"] if j + 1 < len(W) else None
        a = 0.0 if prev_start is None else au.speech_end(prev_start + 0.05, W[i]["start"])
        b = au.total if nxt_start is None else au.speech_onset(nxt_start, W[j]["start"] + 0.05)
        # a join after a sentence end keeps a slightly longer breath
        scale = 1.5 if i > 0 and W[i - 1]["w"].endswith((".", "?", "!")) else 1.0
        if prev_start is not None:
            a = min(a + TAIL_KEEP * scale, b)
        if nxt_start is not None:
            b = max(b - HEAD_KEEP * scale, a)
        # never keep the onset of a removed word (margin survives frame snapping)
        if prev_start is not None:
            a = min(a, W[i]["start"] - EDGE_MARGIN)
        # no pause before the next kept word (continuous speech): cut right up to it,
        # otherwise the tail of the last removed word survives
        if nxt_start is not None and not au.has_gap(W[j]["start"] + 0.05, nxt_start):
            b = au.quietest(W[j]["start"] + 0.06, nxt_start + 0.03)   # the dip between the two words
        removals.append({"id": r["id"], "start": a, "end": b, "reason": r["reason"],
                         "text": " ".join(w["w"] for w in W[i:j + 1])})
    if spec.get("head_before_word") is not None:
        k = spec["head_before_word"]
        b = au.speech_onset(W[k]["start"], 0.0) - HEAD_KEEP * 2
        removals.append({"id": "R1", "start": 0.0, "end": max(0.0, b), "reason": "pre-roll", "text": ""})

    # 2. pause tightening between consecutive kept words
    kept_idx = [k for k in range(len(W)) if k not in removed]
    blocked = sorted((r["start"], r["end"]) for r in removals)
    for x, y in zip(kept_idx, kept_idx[1:]):
        a, b = W[x]["start"], W[y]["start"]
        if y != x + 1 or b - a < MIN_PAUSE:
            continue
        for s, e in au.pauses(a + 0.05, b):
            if any(s < be and e > bs for bs, be in blocked):
                continue
            target = PAUSE_END if W[x]["w"].endswith((".", "?", "!")) else PAUSE_MID
            if e - s <= target + 0.05:
                continue
            cs, ce = s + target * 0.6, e - target * 0.4
            removals.append({"id": "P", "start": cs, "end": ce, "reason": "pause",
                             "text": f"{e - s:.2f}s -> {target:.2f}s"})

    # 3. keep-ranges (frame snapped)
    removals.sort(key=lambda r: r["start"])
    keeps, cur = [], 0.0
    for r in removals:
        a, b = snap(cur), snap(r["start"])
        if b - a >= 2 / FPS:
            keeps.append([a, b])
        cur = max(cur, r["end"])
    a, b = snap(cur), snap(au.total)
    if b - a >= 2 / FPS:
        keeps.append([a, b])

    # 4. timeline with inserted cards (inserted before the given word)
    inserts = sorted(spec["inserts"], key=lambda c: W[c["before_word"]]["start"]
                     if c.get("before_word") is not None else 1e9)
    timeline, ins = [], list(inserts)
    for a, b in keeps:
        while ins and ins[0].get("before_word") is not None and W[ins[0]["before_word"]]["start"] < b:
            t = W[ins[0]["before_word"]]["start"]
            split = snap(au.speech_onset(t, a) - HEAD_KEEP)
            split = max(a, min(split, b))
            if split - a >= 2 / FPS:
                timeline.append({"type": "src", "in": a, "out": split})
            c = ins.pop(0)
            timeline.append({"type": "card", **c})
            a = split
        if b - a >= 2 / FPS:
            timeline.append({"type": "src", "in": a, "out": b})
    timeline += [{"type": "card", **c} for c in ins]

    out_t = 0.0
    for item in timeline:
        item["out_start"] = round(out_t, 4)
        out_t += (item["out"] - item["in"]) if item["type"] == "src" else item["dur"]
    json.dump({"fps": FPS, "timeline": timeline, "duration": out_t}, open(os.path.join(out_dir, "edl.json"), "w"), indent=1)

    with open(os.path.join(out_dir, "cuts.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "reason", "source_start", "source_end", "removed_s", "detail"])
        for r in removals:
            w.writerow([r["id"], r["reason"], ts(r["start"]), ts(r["end"]),
                        f"{r['end'] - r['start']:.2f}", r["text"]])
    rt = [r for r in removals if r["id"] != "P"]
    pz = [r for r in removals if r["id"] == "P"]
    print(f"retake/filler cuts: {len(rt)} ({sum(r['end'] - r['start'] for r in rt):.1f}s); "
          f"pauses tightened: {len(pz)} ({sum(r['end'] - r['start'] for r in pz):.1f}s)")
    print(f"output duration {out_t:.1f}s = {int(out_t // 60)}:{out_t % 60:04.1f}")


def ts(t):
    return f"{int(t // 60)}:{t % 60:06.3f}"


if __name__ == "__main__":
    main()
