#!/usr/bin/env bash
# Recreate the audio inputs of the final mix in $2 (deterministic):
#   music_full.wav (original music v2, seed 7, 660 s), sfx/{pop,swish,swell}.wav, roomtone.wav (source 274.5 s, 3 s)
# Usage: tools/setup_audio.sh SOURCE.mp4 OUT_DIR
set -euo pipefail
SRC="${1:?source}"; OUT="${2:?out dir}"; mkdir -p "$OUT"
HERE="$(cd "$(dirname "$0")" && pwd)"
python3 "$HERE/compose_music.py" 660 "$OUT/music_full.wav" 7
python3 "$HERE/make_sfx.py" "$OUT/sfx"
ffmpeg -nostdin -v error -y -ss 274.5 -t 3 -i "$SRC" -map 0:a:0 -ac 2 -ar 48000 \
  -af "afade=t=in:d=0.15,afade=t=out:st=2.85:d=0.15" "$OUT/roomtone.wav"
echo 274.5 > "$OUT/roomtone_start"
echo "audio inputs ready in $OUT"
