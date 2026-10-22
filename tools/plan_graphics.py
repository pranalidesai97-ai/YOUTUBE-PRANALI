#!/usr/bin/env python3
"""Resolve the phrase-anchored graphics plan to output times.

Usage: plan_graphics.py transcript.json edl.json graphics.json OUT.json
Every anchor [phrase, approx_source_s] is matched against the word list
(punctuation-insensitive, nearest to the approximate time) and mapped through
the EDL. Anchors on removed words are reported as errors, never guessed.
"""
import json
import re
import sys

READ_PAD = 0.5


def norm(w):
    return re.sub(r"[^a-z0-9'-]", "", w.lower())


def main():
    tr, edl_path, plan_path, out_path = sys.argv[1:5]
    W = json.load(open(tr))["words"]
    segs = [i for i in json.load(open(edl_path))["timeline"] if i["type"] == "src"]
    nw = [norm(w["w"]) for w in W]

    def to_out(t):
        for s in segs:
            if s["in"] <= t < s["out"]:
                return s["out_start"] + t - s["in"]
        return None

    def find(anchor):
        phrase, near = anchor
        q = [norm(x) for x in phrase.split()]
        hits = [i for i in range(len(W) - len(q)) if nw[i:i + len(q)] == q]
        if not hits:
            raise SystemExit(f"anchor not found: {anchor}")
        i = min(hits, key=lambda k: abs(W[k]["start"] - near))
        return i, i + len(q) - 1

    def start_of(anchor):
        i, _ = find(anchor)
        t = to_out(W[i]["start"])
        if t is None:
            raise SystemExit(f"anchor on a removed word: {anchor}")
        return round(t, 3)

    def end_of(anchor):
        _, j = find(anchor)
        t = to_out(min(W[j]["end"], W[j]["start"] + 0.8) - 0.01)
        if t is None:
            raise SystemExit(f"anchor on a removed word: {anchor}")
        return round(t + 0.01, 3)

    out = []
    for it in json.load(open(plan_path))["items"]:
        r = dict(it)
        if it["type"] == "keywords":
            for k in r["items"]:
                k["t"] = start_of(k["at"])
            r["t0"] = r["items"][0]["t"]
            r["t1"] = r["items"][-1]["t"] + 2.0
        elif it["type"] in ("notes", "pip"):
            key = "items" if it["type"] == "notes" else "bullets"
            for k in r[key]:
                k["t"] = start_of(k["at"])
            r["t0"] = start_of(it["start"]) if "start" in it else r[key][0]["t"]
            r["t1"] = end_of(it["end"]) + READ_PAD
        elif it["type"] == "pullquote":
            r["t0"] = start_of(it["start"])
            r["t1"] = max(end_of(it["end"]) + READ_PAD, r["t0"] + it.get("min", 2.5))
        elif it["type"] in ("broll", "corner_card"):
            r["t0"] = start_of(it["start"])
            r["t1"] = r["t0"] + it["dur"]
        out.append(r)
    out.sort(key=lambda r: r["t0"])
    for a, b in zip(out, out[1:]):
        if b["t0"] < a["t1"] and not (a["type"] == "broll" or b["type"] == "broll"):
            print(f"WARNING overlap {a['id']} {a['t0']:.1f}-{a['t1']:.1f} / {b['id']} {b['t0']:.1f}")
    json.dump(out, open(out_path, "w"), indent=1, ensure_ascii=False)
    for r in out:
        print(f"{r['id']:5s} {r['type']:11s} {int(r['t0'] // 60)}:{r['t0'] % 60:05.2f} - {int(r['t1'] // 60)}:{r['t1'] % 60:05.2f}")


if __name__ == "__main__":
    main()
