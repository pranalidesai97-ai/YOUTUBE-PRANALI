#!/usr/bin/env bash
# Rebuild every font the pipeline uses (all SIL OFL, from npm @fontsource) into $1.
#   $1/                      fontsource packages (gfx.py / brand_gfx.py read woff2 from here)
#   $1/ttf/                  TTFs for libass captions: Poppins Latin+Devanagari merged, Noto Sans Devanagari, Instrument Serif
#   $1/brand/                Cormorant Garamond, Playfair Display, Manrope, Montserrat (design system)
# Usage: tools/setup_fonts.sh /path/to/fonts      (then GFX_FONT_DIR=$1, BRAND_FONT_DIR=$1/brand)
set -euo pipefail
D="${1:?font dir}"; mkdir -p "$D/ttf" "$D/brand"
cd "$D"
for p in instrument-serif poppins great-vibes noto-sans-devanagari inter caveat; do
  npm pack -q "@fontsource/$p@5.3.0" >/dev/null; f=$(ls fontsource-$p-*.tgz | head -1)
  dir="${f%.tgz}"; [ "$p" = caveat ] && dir=caveat; mkdir -p "$dir"; tar xzf "$f" -C "$dir"
done
cd brand
for p in cormorant-garamond playfair-display manrope montserrat; do
  npm pack -q "@fontsource/$p@5.3.0" >/dev/null; mkdir -p "$p"; tar xzf fontsource-$p-*.tgz -C "$p"
done
cd ..
python3 - "$D" <<'PY'
import glob, os, sys
from fontTools.ttLib import TTFont
from fontTools.merge import Merger
D = sys.argv[1]
pop = glob.glob(f"{D}/fontsource-poppins-*/package/files")[0]
for w, name in (("500", "Medium"), ("600", "SemiBold")):
    parts = []
    for sub in ("latin", "latin-ext", "devanagari"):
        f = TTFont(f"{pop}/poppins-{sub}-{w}-normal.woff2"); f.flavor = None
        out = f"{pop}/poppins-{sub}-{w}-normal.ttf"; f.save(out); parts.append(out)
    Merger().merge(parts).save(f"{D}/ttf/Poppins-{name}-Full.ttf")
f = TTFont(glob.glob(f"{D}/fontsource-noto-sans-devanagari-*/package/files/noto-sans-devanagari-devanagari-500-normal.woff2")[0]); f.flavor = None
f.save(f"{D}/ttf/NotoSansDevanagari-Medium.ttf")
f = TTFont(glob.glob(f"{D}/fontsource-instrument-serif-*/package/files/instrument-serif-latin-400-normal.woff2")[0]); f.flavor = None
f.save(f"{D}/ttf/InstrumentSerif-Regular.ttf")
print("fonts ready:", sorted(os.listdir(f"{D}/ttf")))
PY
# gfx.py expects these exact folder names
for p in instrument-serif poppins great-vibes; do d=$(ls -d fontsource-$p-*/ | head -1); [ -e "fontsource-$p-5.3.0" ] || ln -s "${d%/}" "fontsource-$p-5.3.0"; done
