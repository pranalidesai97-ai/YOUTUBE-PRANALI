#!/usr/bin/env python3
"""Phrase captions in output time from the word transcript and the EDL.

Usage: make_captions.py transcript.json edl.json overrides.json[,more.json] OUT_DIR

overrides.json:
  {"replace": [{"words": [i, j], "text": "...", "flag": "why"}],   # e.g. Hinglish lines
   "flag":    [{"words": [i, j], "note": "..."}]}                   # uncertain words

Writes captions.srt (clean, for YouTube / burn-in) and captions_review.srt,
where flagged text is wrapped in [? ... ?] for proofreading.
"""
import json
import os
import re
import sys

MAX_WORDS = 6
MAX_CHARS = 35
SOFT_MAX_CHARS = 42   # allowed to avoid leaving a 1-word orphan at a sentence end
SPELL = {"20s": "twenties", "20s.": "twenties.", "20s,": "twenties,", "30s": "thirties", "30s.": "thirties."}
FILLERS = {"uh", "um", "uh,", "um,", "mm-hmm.", "mm-hmm", "uh.", "um."}
FRAGMENT = re.compile(r"^[a-z]{1,2}$")   # cut-off word starts ("tr", "ev", "j")
REAL_SHORT = {"a", "i", "is", "it", "in", "on", "to", "of", "or", "so", "be", "we", "my", "me", "do",
              "no", "go", "up", "as", "at", "an", "if", "us", "he", "by", "am", "hi"}
GAP_BREAK = 0.35
LINGER = 0.30
ONSET_SLACK = 0.08    # see to_output()


def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def to_output(t, segs):
    for s in segs:
        if s["in"] <= t < s["out"]:
            return s["out_start"] + t - s["in"]
    # word timestamps come in 80 ms steps: a kept word may be stamped just before the
    # cut point where its audio actually begins
    for s in segs:
        if 0 < s["in"] - t <= ONSET_SLACK:
            return s["out_start"]
    return None


def main():
    tr, edl_path, ov_path, out_dir = sys.argv[1:5]
    W = json.load(open(tr))["words"]
    segs = [i for i in json.load(open(edl_path))["timeline"] if i["type"] == "src"]
    ov = {"replace": [], "flag": []}
    for p in ov_path.split(","):  # several override files may be merged
        if os.path.exists(p):
            d = json.load(open(p))
            ov["replace"] += d.get("replace", [])
            ov["flag"] += d.get("flag", [])

    # tokens: (text, start, end, flagged)
    flagged = {}
    for f in ov.get("flag", []):
        for k in range(f["words"][0], f["words"][1] + 1):
            flagged[k] = f["note"]
    repl = {r["words"][0]: r for r in ov.get("replace", [])}
    skip = set()
    for r in ov.get("replace", []):
        skip.update(range(r["words"][0] + 1, r["words"][1] + 1))

    toks = []
    for k, w in enumerate(W):
        if k in skip:
            continue
        t = to_output(w["start"], segs)
        if t is None:
            continue  # removed in the edit
        if k in repl:
            r = repl[k]
            i, j = r["words"]
            end = to_output(W[j]["end"] - 0.01, segs) or t + 0.6 * (j - i + 1)
            words = r["text"].split()   # empty text = hidden from captions only (audio untouched)
            step = (end - t) / max(1, len(words))
            only = r.get("flag_words")   # flag just these words of an otherwise accepted line
            for n, x in enumerate(words):
                f = r.get("flag", "") if (only is None or x.strip(",.?!।") in only) else ""
                toks.append([x, t + n * step, t + (n + 1) * step, f])
            continue
        bare = w["w"].lower()
        if bare in FILLERS or (FRAGMENT.match(bare) and bare not in REAL_SHORT):
            continue  # clean verbatim: no fillers or cut-off fragments
        e = to_output(min(w["end"], w["start"] + 0.8) - 0.01, segs) or t + 0.4
        toks.append([SPELL.get(w["w"], w["w"]), t, max(e, t + 0.15), flagged.get(k, "")])

    cues, cur = [], []
    for n, tk in enumerate(toks):
        if cur:
            text = " ".join(x[0] for x in cur + [tk])
            gap = tk[1] - cur[-1][2]
            orphan_fix = (re.search(r"[.?!,]$", tk[0]) and len(text) <= SOFT_MAX_CHARS
                          and len(cur) < MAX_WORDS + 1 and gap <= GAP_BREAK)
            if ((len(cur) >= MAX_WORDS or len(text) > MAX_CHARS) and not orphan_fix
                    or gap > GAP_BREAK
                    or re.search(r"[.?!।]$", cur[-1][0])
                    or (re.search(r",$", cur[-1][0]) and len(cur) >= 3)):
                cues.append(cur)
                cur = []
        cur.append(tk)
    if cur:
        cues.append(cur)

    def fmt(n, review):
        out = []
        for x, _, _, f in cues[n]:
            out.append(f"[?{x}?]" if review and f else x)
        s = " ".join(out)
        # sentence case: capitalise only where a sentence starts
        if n == 0 or re.search(r"[.?!।]$", cues[n - 1][-1][0]):
            s = s[0].upper() + s[1:]
        return s

    os.makedirs(out_dir, exist_ok=True)
    for name, review in (("captions.srt", False), ("captions_review.srt", True)):
        with open(os.path.join(out_dir, name), "w") as f:
            for n, cue in enumerate(cues):
                start = cue[0][1]
                nxt = cues[n + 1][0][1] if n + 1 < len(cues) else cue[-1][2] + LINGER
                end = min(cue[-1][2] + LINGER, nxt - 0.001)
                f.write(f"{n + 1}\n{srt_time(start)} --> {srt_time(max(end, start + 0.4))}\n{fmt(n, review)}\n\n")
    import csv
    with open(os.path.join(out_dir, "captions_flags.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cue", "output_time", "caption", "uncertain_words", "note"])
        for n, cue in enumerate(cues):
            notes = sorted({t[3] for t in cue if t[3]})
            if notes:
                w.writerow([n + 1, srt_time(cue[0][1])[:-4], fmt(n, False),
                            " ".join(t[0] for t in cue if t[3]), " | ".join(notes)])
    print(f"{len(cues)} cues, {sum(1 for c in cues if any(t[3] for t in c))} with flagged words")


if __name__ == "__main__":
    main()
