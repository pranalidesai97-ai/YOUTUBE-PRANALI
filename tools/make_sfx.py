#!/usr/bin/env python3
"""Three restrained, original sound effects (synthesised; no samples or licences).

pop   - very soft tick for a list item / keyword appearing
swish - gentle paper-like swish for full-frame cards (titles, menu, PiP card)
swell - airy low swell for a pull-quote dimming in
Usage: make_sfx.py OUT_DIR
"""
import os
import sys

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000


def norm(x, peak_db):
    return x / (np.max(np.abs(x)) + 1e-9) * 10 ** (peak_db / 20)


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    rng = np.random.default_rng(3)

    t = np.arange(int(0.09 * SR)) / SR
    f = 1250 * np.exp(-t * 6)
    pop = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.018)
    pop += 0.15 * sosfilt(butter(2, [2000, 6000], "band", fs=SR, output="sos"),
                          rng.normal(0, 1, len(t))) * np.exp(-t / 0.004)
    sfx = {"pop": norm(pop, -6)}

    t = np.arange(int(0.55 * SR)) / SR
    noise = rng.normal(0, 1, len(t))
    env = np.sin(np.pi * np.clip(t / 0.55, 0, 1)) ** 2
    sw = np.zeros_like(noise)
    for k in range(0, len(t), 480):             # band-pass that sweeps upward
        fc = 900 + 3500 * k / len(t)
        seg = sosfilt(butter(2, [fc * 0.6, fc * 1.4], "band", fs=SR, output="sos"), noise[k:k + 960])
        sw[k:k + 480] = seg[:480]
    sfx["swish"] = norm(sw * env, -6)

    t = np.arange(int(0.8 * SR)) / SR
    sl = sosfilt(butter(2, 900, "low", fs=SR, output="sos"), rng.normal(0, 1, len(t)))
    sl += 0.4 * np.sin(2 * np.pi * 110 * t)
    sfx["swell"] = norm(sl * np.sin(np.pi * t / 0.8) ** 2, -6)

    for name, x in sfx.items():
        st = np.stack([x, x]).T
        wavfile.write(os.path.join(out, name + ".wav"), SR, (st * 32767).astype(np.int16))
    print("wrote", ", ".join(sfx))


if __name__ == "__main__":
    main()
