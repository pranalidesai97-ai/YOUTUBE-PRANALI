#!/usr/bin/env python3
"""Flag transcript words where two recognisers disagree.

Usage: asr_crosscheck.py transcript.json whisper_segments.json OUT_flags.json
Parakeet words (transcript.json) are aligned per segment against a Whisper
transcript of the same audio; words in replaced/deleted spans are flagged with
Whisper's alternative so they can be proofread.
"""
import difflib
import json
import re
import sys

NUM = {"twenties": "20s", "thirties": "30s", "ten": "10", "two": "2", "eight": "8", "fifty": "50",
       "thirty": "30", "twenty": "20"}
FILLERS = {"uh", "um", "mm", "hmm", "mmhmm", "okay", "ok"}


def norm(w):
    w = re.sub(r"[^a-z0-9']", "", w.lower().replace("-", ""))
    return NUM.get(w, w)


def main():
    tr, wh, out = sys.argv[1:4]
    W = json.load(open(tr))["words"]
    segs = json.load(open(wh))
    flags = []
    for sg in segs:
        idx = [k for k, w in enumerate(W) if sg["start"] <= w["start"] < sg["end"]]
        a = [norm(W[k]["w"]) for k in idx]
        b = [norm(x) for x in sg["text"].split()]
        b = [x for x in b if x]
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op in ("replace", "delete"):
                span = [k for k in idx[i1:i2] if norm(W[k]["w"]) not in FILLERS]
                alt = " ".join(sg["text"].split()[j1:j2]) if op == "replace" else "(not heard)"
                # Whisper silently drops disfluencies, so "not heard" is not evidence of an error
                if span and op == "replace":
                    flags.append({"words": [span[0], span[-1]],
                                  "note": f"second recogniser heard: {alt}"})
    json.dump({"flag": flags}, open(out, "w"), indent=1)
    print(f"{len(flags)} disagreements flagged")


if __name__ == "__main__":
    main()
