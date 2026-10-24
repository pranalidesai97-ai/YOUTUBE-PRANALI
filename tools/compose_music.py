#!/usr/bin/env python3
"""Original background music, synthesised from scratch (no samples, no external assets).

Calm, warm lo-fi bed for a talking-head video: 78 BPM, D major,
Dmaj9 - Bm9 - Gmaj9 - A7sus4. Soft felt-piano keys (no octave-up chime voicing) and a soft pad throughout;
a round sub bass and a very light brushed hat join in alternate 16-bar sections.
Being generated here, the track is an original work with no third-party licence.

Usage: compose_music.py DURATION_S OUT.wav [SEED]
"""
import sys

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
BPM = 78
BEAT = 60 / BPM
BAR = 4 * BEAT

# MIDI voicings (low to high) and bass roots
CHORDS = [
    ([62, 66, 69, 73, 76], 38),   # Dmaj9
    ([59, 62, 66, 69, 73], 35),   # Bm9
    ([55, 59, 62, 66, 69], 31),   # Gmaj9
    ([57, 62, 64, 67, 71], 33),   # A7sus4(9)
]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lowpass(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)


def keys_note(f, dur, vel, rng):
    n = int(dur * SR)
    t = np.arange(n) / SR
    det = 1 + rng.normal(0, 0.0007)
    # felt-piano tone: soft attack, few overtones and a low-pass, so notes don't ring like bells
    tone = (np.sin(2 * np.pi * f * det * t) + 0.16 * np.sin(4 * np.pi * f * t) * np.exp(-t * 5)
            + 0.03 * np.sin(6 * np.pi * f * t) * np.exp(-t * 9))
    env = (1 - np.exp(-t / 0.018)) * np.exp(-t / 0.85)
    return lowpass(vel * tone * env, 1800)


def pad_chord(notes, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for m in notes[:4]:
        for d in (-0.12, 0.0, 0.12):   # cents-ish detune
            f = hz(m) * 2 ** (d / 12)
            out += np.sin(2 * np.pi * f * t + d * 7) + 0.15 * np.sin(4 * np.pi * f * t)
    env = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.0).clip(0)
    return 0.05 * lowpass(out, 1400) * env


def reverb(x, rng, seconds=2.6, wet=0.28):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = rng.normal(0, 1, (2, n)) * np.exp(-t / 0.55)
    ir = np.stack([lowpass(i, 5000) for i in ir])
    ir /= np.sqrt(np.sum(ir ** 2, axis=1, keepdims=True))
    y = np.stack([fftconvolve(x[c], ir[c])[:x.shape[1]] for c in range(2)])
    return (1 - wet) * x + wet * y


def main():
    dur = float(sys.argv[1])
    out = sys.argv[2]
    rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 7)
    n = int((dur + 4) * SR)
    mix = np.zeros((2, n))

    def add(sig, t0, pan=0.0):
        i = int(t0 * SR)
        j = min(n, i + len(sig))
        if i >= n:
            return
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        mix[0, i:j] += sig[:j - i] * l
        mix[1, i:j] += sig[:j - i] * r

    bars = int(dur / BAR) + 2
    # broken-chord rhythm per bar: (beat offset, voice index)
    patterns = [[(0, 0), (1.5, 2), (2, 3), (3, 1), (3.5, 4)],
                [(0, 1), (1, 3), (2.5, 2), (3, 4)]]
    for b in range(bars):
        notes, root = CHORDS[b % 4]
        t0 = b * BAR
        section_b = (b // 16) % 2 == 1
        add(pad_chord(notes, BAR + 1.0), t0, 0.0)
        for off, v in patterns[(b // 4) % 2]:
            jitter = rng.normal(0, 0.012)
            vel = 0.11 * (0.75 + 0.25 * rng.random())
            add(keys_note(hz(notes[v]), 2.6, vel, rng), t0 + off * BEAT + jitter,
                pan=(v - 2) * 0.18)
        if section_b:
            for off in (0, 2.5):
                k = np.arange(int(1.4 * SR)) / SR
                bass = 0.14 * np.sin(2 * np.pi * hz(root) * k) * np.minimum(1, k / 0.02) * np.exp(-k / 0.9)
                add(bass, t0 + off * BEAT)
            for off in (0.5, 1.5, 2.5, 3.5):
                k = int(0.05 * SR)
                hat = rng.normal(0, 1, k) * np.exp(-np.arange(k) / (0.012 * SR))
                hat = sosfilt(butter(2, 7000, "high", fs=SR, output="sos"), hat)
                add(0.012 * hat, t0 + off * BEAT + rng.normal(0, 0.008), pan=0.3)

    mix = reverb(mix, rng)
    mix = np.stack([lowpass(c, 9500) for c in mix])
    t = np.arange(n) / SR
    mix *= np.minimum(1, t / 2.5)                         # fade in
    mix *= np.clip((dur + 0.5 - t) / 3.0, 0, 1)            # fade out at the end
    mix = mix[:, :int(dur * SR)]
    mix *= 10 ** (-18 / 20) / (np.sqrt(np.mean(mix ** 2)) + 1e-9)   # ~ -18 dBFS RMS
    peak = np.max(np.abs(mix))
    if peak > 0.9:
        mix *= 0.9 / peak
    from scipy.io import wavfile
    wavfile.write(out, SR, (mix.T * 32767).astype(np.int16))


if __name__ == "__main__":
    main()
