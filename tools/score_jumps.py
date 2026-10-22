#!/usr/bin/env python3
"""Score how visibly the picture jumps at each cut join (mean abs luma diff, 160x90).

Usage: score_jumps.py SOURCE edl.json OUT.json  -> joins in the top 15 % (and >= 6.0)
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np


def main():
    src, edl_path, out = sys.argv[1:4]
    tl = json.load(open(edl_path))["timeline"]

    def grab(t):
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, t):.4f}", "-i", src, "-frames:v", "1",
                            "-vf", "scale=160:90", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
        return np.frombuffer(r.stdout, np.uint8).astype(float)

    def diff(n):
        a, b = tl[n], tl[n + 1]
        if a["type"] != "src" or b["type"] != "src" or abs(a["out"] - b["in"]) < 0.05:
            return None
        return {"tl_index": n + 1, "output_t": b["out_start"], "diff": float(np.abs(grab(a["out"] - 1 / 30) - grab(b["in"])).mean())}

    with ThreadPoolExecutor(4) as ex:
        res = [r for r in ex.map(diff, range(len(tl) - 1)) if r]
    thr = max(6.0, float(np.percentile([r["diff"] for r in res], 85)))
    jar = [r for r in res if r["diff"] >= thr]
    json.dump(jar, open(out, "w"), indent=1)
    print(f"{len(res)} joins, {len(jar)} jarring (>= {thr:.1f})")


if __name__ == "__main__":
    main()
