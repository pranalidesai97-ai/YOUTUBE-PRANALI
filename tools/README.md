# Talking-head clean-up (stage 1)

`clean_talking_head.py SOURCE OUTDIR [--test-start S --test-duration D] [--plan-only]`

- Detects gaps > 0.8 s quieter than typical speech level − 30 dB.
- Cross-checks every cut with the Silero voice detector (local ONNX model from the
  `silero-vad` PyPI package + `onnxruntime`; install with `pip install --no-deps silero-vad onnxruntime`).
  Any possible speech (probability >= 0.35) inside a pause → pause kept and flagged.
- Keeps 0.30 s after speech and 0.20 s before speech (0.75 s total for gaps >= 2 s),
  so word tails, onsets and breaths are never cut; no speed changes.
- Gaps containing borderline low-level sound are left uncut and flagged in the cut list.
- Audio: high-pass 70 Hz, light FFT denoise, mild de-click, gentle EQ,
  2:1 compression (25 ms denoiser latency compensated), two-pass loudnorm to -16 LUFS / -1.5 dBTP; 12 ms micro-fades at cuts.
- Video: frame-snapped cuts, H.264 CRF 16 (slow), original resolution/fps/pix_fmt/colour tags, AAC 192k.
- Writes `cleaned_<tag>.mp4` and `cleaned_<tag>_cutlist.csv` (source timestamps). Never touches the source.

`qc_check.sh OUTPUT.mp4` reports streams, black/frozen frames and loudness, and
cuts 10 s review clips from the start, middle and end.
