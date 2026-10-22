#!/usr/bin/env bash
# Quality check of a cleaned export: stream info, black/frozen frames,
# loudness, A/V duration match, and 10 s review clips from start/middle/end.
set -euo pipefail
OUT="$1"
DIR="$(dirname "$OUT")"; NAME="$(basename "$OUT" .mp4)"

ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels,duration \
  -show_entries format=duration -of compact "$OUT"

echo "--- black frames / frozen frames (none expected) ---"
ffmpeg -nostdin -hide_banner -i "$OUT" -map 0:v:0 \
  -vf "blackdetect=d=0.04:pix_th=0.05,freezedetect=n=0.001:d=1.0" -f null - 2>&1 \
  | grep -E "black_start|freeze_start" || echo "none"

echo "--- loudness (EBU R128) ---"
ffmpeg -nostdin -hide_banner -i "$OUT" -map 0:a:0 -af ebur128=peak=true -f null - 2>&1 \
  | sed -n '/Summary:/,$p' | grep -E "I:|LRA:|Peak:"

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")
for pos in start middle end; do
  case $pos in
    start) SS=0 ;;
    middle) SS=$(python3 -c "print(max(0, $DUR/2 - 5))") ;;
    end) SS=$(python3 -c "print(max(0, $DUR - 10))") ;;
  esac
  ffmpeg -nostdin -v error -y -ss "$SS" -i "$OUT" -t 10 -c copy "$DIR/${NAME}_qc_${pos}.mp4"
done
echo "review clips: $DIR/${NAME}_qc_{start,middle,end}.mp4"
