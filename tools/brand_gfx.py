#!/usr/bin/env python3
"""Editorial / stationery design system for the opening title, Subscribe reminder and end screen.

All imagery is original: SVG illustrations with painterly filters (watercolour petals,
pressed flowers, fine-line gold botanicals, paper grain, torn and deckled edges, washi tape,
ribbons, stickers, wax seal). Fonts are OFL (Cormorant Garamond, Playfair Display, Manrope,
Montserrat) from npm @fontsource, embedded as base64.

Three directions: A "Pressed Garden", B "Scrapbook Journal", C "Champagne Editorial".
Each exposes opening(), reminder(), end_screen() -> HTML (1920x1080).
"""
import base64
import html
import math
import os
import random

FONT_DIR = os.environ.get("BRAND_FONT_DIR", "")

C = {
    "ivory": "#F8F2E9", "paper": "#FBF7F1", "cream": "#F1E7DA",
    "rose": "#D8A9A6", "rose_deep": "#C38C8E", "rose_pale": "#EED6D2",
    "plum": "#5E4256", "plum_deep": "#3F2B3A", "plum_soft": "#86677D",
    "sage": "#A9B8A0", "sage_deep": "#7F9376", "sage_pale": "#D5DECF",
    "gold": "#C5A46D", "gold_light": "#E6D3A6", "gold_deep": "#A8834A",
    "ink": "#3B2C36",
}

# YouTube end-screen element zones (kept clear in every design)
WATCH_BOX = (1030, 250, 760, 428)        # x, y, w, h  (16:9)
SUB_CIRCLE = (430, 812, 104)             # cx, cy, r


# ----------------------------------------------------------------------------- fonts
def _ff(family, rel, weight, style="normal"):
    data = base64.b64encode(open(os.path.join(FONT_DIR, rel), "rb").read()).decode()
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:{style};"
            f"src:url(data:font/woff2;base64,{data}) format('woff2');}}")


def fonts():
    out = []
    for w in (300, 400, 500, 600):
        for st in ("normal", "italic"):
            out.append(_ff("Cormorant", f"cormorant-garamond/package/files/cormorant-garamond-latin-{w}-{st}.woff2", w, st))
    for w in (400, 500, 600):
        for st in ("normal", "italic"):
            out.append(_ff("Playfair", f"playfair-display/package/files/playfair-display-latin-{w}-{st}.woff2", w, st))
    for w in (300, 400, 500, 600):
        out.append(_ff("Manrope", f"manrope/package/files/manrope-latin-{w}-normal.woff2", w))
    for w in (400, 500, 600):
        out.append(_ff("Montserrat", f"montserrat/package/files/montserrat-latin-{w}-normal.woff2", w))
    return "".join(out)


_FONTS = None


def page(body, bg=None, opaque=False, bg_color=None):
    global _FONTS
    if _FONTS is None:
        _FONTS = fonts()
    bgcss = ""
    if bg:
        data = base64.b64encode(open(bg, "rb").read()).decode()
        bgcss = f"background:url(data:image/jpeg;base64,{data}) center/cover;"
    elif opaque:
        bgcss = f"background:{bg_color or C['ivory']};"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{_FONTS}
html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;{bgcss if bgcss else 'background:transparent;'}}}
.abs{{position:absolute}} svg{{position:absolute;left:0;top:0;overflow:visible}}
.corm{{font-family:'Cormorant',serif;font-variant-numeric:lining-nums}} .play{{font-family:'Playfair',serif;font-variant-numeric:lining-nums}}
div{{text-wrap:balance}}
.man{{font-family:'Manrope',sans-serif}} .mont{{font-family:'Montserrat',sans-serif}}
</style></head><body>{body}</body></html>"""


# ----------------------------------------------------------------------------- svg defs
def defs():
    g = C
    return f"""<defs>
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{g['gold_deep']}"/><stop offset=".45" stop-color="{g['gold_light']}"/>
    <stop offset="1" stop-color="{g['gold']}"/></linearGradient>
  <radialGradient id="petalRose" cx=".5" cy=".85" r=".9">
    <stop offset="0" stop-color="#F6E1DD"/><stop offset=".55" stop-color="{g['rose']}"/><stop offset="1" stop-color="{g['rose_deep']}"/></radialGradient>
  <radialGradient id="petalBlush" cx=".5" cy=".85" r=".9">
    <stop offset="0" stop-color="#FFF6F1"/><stop offset=".6" stop-color="#F0D3CC"/><stop offset="1" stop-color="#D9AFA9"/></radialGradient>
  <radialGradient id="petalIvory" cx=".5" cy=".85" r=".9">
    <stop offset="0" stop-color="#FFFDF8"/><stop offset=".7" stop-color="#F3E9DA"/><stop offset="1" stop-color="#DCCBB2"/></radialGradient>
  <radialGradient id="petalPlum" cx=".5" cy=".85" r=".9">
    <stop offset="0" stop-color="#C9AEC0"/><stop offset=".6" stop-color="{g['plum_soft']}"/><stop offset="1" stop-color="{g['plum']}"/></radialGradient>
  <linearGradient id="leafSage" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{g['sage_deep']}"/><stop offset="1" stop-color="{g['sage']}"/></linearGradient>
  <radialGradient id="seal" cx=".4" cy=".35" r=".8">
    <stop offset="0" stop-color="#D9AAB0"/><stop offset=".6" stop-color="{g['rose_deep']}"/><stop offset="1" stop-color="#9F6B72"/></radialGradient>
  <radialGradient id="plumGlow" cx=".38" cy=".42" r=".85">
    <stop offset="0" stop-color="#77566E"/><stop offset=".6" stop-color="{g['plum']}"/><stop offset="1" stop-color="{g['plum_deep']}"/></radialGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 .33  0 0 0 0 .26  0 0 0 0 .22  0 0 0 .55 -.18"/></filter>
  <filter id="mottle" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".004" numOctaves="3" seed="9"/>
    <feColorMatrix values="0 0 0 0 .55  0 0 0 0 .42  0 0 0 0 .38  0 0 0 .5 -.18"/></filter>
  <filter id="deckle" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency=".05" numOctaves="4" seed="11" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="9" xChannelSelector="R" yChannelSelector="G"/></filter>
  <filter id="fiber" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency=".09" numOctaves="3" seed="17" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="5" xChannelSelector="R" yChannelSelector="G"/></filter>
  <filter id="wc" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="3" seed="2" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="6" result="d"/>
    <feGaussianBlur in="d" stdDeviation=".7" result="b"/>
    <feTurbulence type="fractalNoise" baseFrequency=".55" numOctaves="2" seed="5" result="g"/>
    <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -.9 1.25" result="ga"/>
    <feComposite in="b" in2="ga" operator="in"/></filter>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
    <feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#3B2C36" flood-opacity=".22"/></filter>
  <filter id="shadowSoft" x="-20%" y="-20%" width="140%" height="150%">
    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#3B2C36" flood-opacity=".2"/></filter>
  <pattern id="ruled" width="40" height="38" patternUnits="userSpaceOnUse">
    <line x1="0" y1="37" x2="40" y2="37" stroke="{g['sage']}" stroke-width="1.2" opacity=".55"/></pattern>
  <pattern id="dots" width="34" height="34" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.6" fill="{g['plum_soft']}" opacity=".18"/></pattern>
  <pattern id="stripeRose" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <rect width="16" height="16" fill="{g['rose']}"/><rect width="7" height="16" fill="#F6E4E1" opacity=".7"/></pattern>
  <pattern id="dotSage" width="18" height="18" patternUnits="userSpaceOnUse">
    <rect width="18" height="18" fill="{g['sage']}"/><circle cx="9" cy="9" r="3" fill="#F3F5EE" opacity=".8"/></pattern>
  <pattern id="plainGold" width="10" height="10" patternUnits="userSpaceOnUse">
    <rect width="10" height="10" fill="{g['gold_light']}"/></pattern>
</defs>"""


# ----------------------------------------------------------------------------- elements
def _rng(seed):
    return random.Random(seed)


def paper_fill(x, y, w, h, color, filt="deckle", rot=0, shadow=True, grain=True):
    """A sheet of paper with deckled edges and grain."""
    cx, cy = x + w / 2, y + h / 2
    sh = ' filter="url(#shadow)"' if shadow else ""
    gr = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#grain)" opacity=".9"/>'
          if grain else "")
    return (f'<g transform="rotate({rot} {cx} {cy})"><g{sh}><g filter="url(#{filt})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/></g></g>'
            f'<g clip-path="none">{gr}</g></g>')


def torn_sheet(x, y, w, h, color, side="bottom", rot=0, seed=1, amp=14, fill_pattern=None, shadow=True):
    """Paper with one hand-torn edge (jagged + fibrous white core) and deckled others."""
    r = _rng(seed)
    pts = [(x, y), (x + w, y)]
    if side == "bottom":
        edge = [(x + w - i * w / 28, y + h + r.uniform(-amp, amp) * (0.6 + 0.4 * math.sin(i))) for i in range(29)]
        pts = [(x, y), (x + w, y)] + edge
    elif side == "top":
        edge = [(x + i * w / 28, y + r.uniform(-amp, amp)) for i in range(29)]
        pts = edge + [(x + w, y + h), (x, y + h)]
    elif side == "right":
        edge = [(x + w + r.uniform(-amp, amp), y + i * h / 24) for i in range(25)]
        pts = [(x, y)] + edge + [(x, y + h)]
    else:
        edge = [(x + r.uniform(-amp, amp), y + h - i * h / 24) for i in range(25)]
        pts = [(x + w, y), (x + w, y + h)] + edge
    poly = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    cx, cy = x + w / 2, y + h / 2
    sh = ' filter="url(#shadow)"' if shadow else ""
    fill2 = f'<polygon points="{poly}" fill="url(#{fill_pattern})"/>' if fill_pattern else ""
    return (f'<g transform="rotate({rot} {cx} {cy})"><g{sh}>'
            f'<g filter="url(#fiber)"><polygon points="{poly}" fill="#FFFDF9" transform="translate(0 0) scale(1)"/></g>'
            f'<polygon points="{poly}" fill="{color}" transform="translate({cx} {cy}) scale(.992) translate({-cx} {-cy})"/>'
            f'{fill2}</g>'
            f'<polygon points="{poly}" filter="url(#grain)" opacity=".85"/></g>')


def petal_path(r):
    return (f"M0 0 C{r * .38:.1f} {-r * .22:.1f} {r * .42:.1f} {-r * .82:.1f} 0 {-r:.1f} "
            f"C{-r * .42:.1f} {-r * .82:.1f} {-r * .38:.1f} {-r * .22:.1f} 0 0Z")


def flower(cx, cy, r, grad="petalRose", n=6, rot=0, center="gold", seed=1, opacity=1.0):
    rg = _rng(seed)
    petals = "".join(
        f'<path d="{petal_path(r * rg.uniform(.88, 1.06))}" fill="url(#{grad})" '
        f'transform="rotate({rot + i * 360 / n + rg.uniform(-6, 6):.1f})" opacity=".93"/>'
        for i in range(n))
    dots = "".join(f'<circle cx="{math.cos(a) * r * .2:.1f}" cy="{math.sin(a) * r * .2:.1f}" r="{r * .035:.1f}" '
                   f'fill="{C["plum"]}" opacity=".7"/>' for a in [k * 0.9 for k in range(7)])
    ctr = (f'<circle r="{r * .17:.1f}" fill="{C["gold"]}"/>{dots}' if center == "gold"
           else f'<circle r="{r * .15:.1f}" fill="{C["plum_soft"]}"/>')
    return (f'<g transform="translate({cx} {cy})" opacity="{opacity}"><g filter="url(#wc)">{petals}</g>{ctr}</g>')


def leaf(x, y, length, angle, fill="url(#leafSage)", vein=True, width=.2):
    L, W = length, length * width
    d = f"M0 0 C{L * .3:.1f} {-W:.1f} {L * .72:.1f} {-W:.1f} {L:.1f} 0 C{L * .72:.1f} {W:.1f} {L * .3:.1f} {W:.1f} 0 0Z"
    v = (f'<path d="M{L * .06:.1f} 0 L{L * .9:.1f} 0" stroke="#EEF2EA" stroke-width="1.3" opacity=".6"/>' if vein else "")
    return f'<g transform="translate({x} {y}) rotate({angle})"><g filter="url(#wc)"><path d="{d}" fill="{fill}"/></g>{v}</g>'


def sprig(x, y, s=1.0, rot=0, palette=("petalRose", "petalBlush"), seed=3):
    """Pressed-flower spray: curved stem, leaves, two or three blooms and buds."""
    r = _rng(seed)
    stem = (f'<path d="M0 0 C40 -70 30 -150 90 -230 S170 -330 150 -400" fill="none" stroke="{C["sage_deep"]}" '
            f'stroke-width="3.2" stroke-linecap="round" opacity=".85"/>'
            f'<path d="M60 -170 C100 -190 140 -200 180 -240" fill="none" stroke="{C["sage_deep"]}" stroke-width="2.4" opacity=".8"/>'
            f'<path d="M35 -90 C10 -130 -20 -150 -60 -170" fill="none" stroke="{C["sage_deep"]}" stroke-width="2.2" opacity=".8"/>')
    leaves = (leaf(30, -60, 70, -40) + leaf(48, -120, 64, 210) + leaf(95, -235, 60, -30) + leaf(125, -300, 58, 200)
              + leaf(140, -205, 50, -15) + leaf(-20, -150, 52, 200))
    blooms = (flower(150, -400, 44, palette[0], 6, r.uniform(0, 40), seed=seed)
              + flower(182, -244, 30, palette[1], 5, r.uniform(0, 40), seed=seed + 1)
              + flower(-62, -172, 26, palette[0], 5, r.uniform(0, 40), seed=seed + 2))
    buds = "".join(f'<g transform="translate({bx} {by}) rotate({ba})"><g filter="url(#wc)"><path d="{petal_path(16)}" fill="url(#{palette[1]})"/></g></g>'
                   for bx, by, ba in ((110, -330, 30), (5, -105, -40)))
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" opacity=".96">{stem}{leaves}{buds}{blooms}</g>'


def fineline(x, y, s=1.0, rot=0, color="url(#gold)", width=1.6, flip=False, cls=""):
    """Gold fine-line botanical: stem, outlined leaves, a bloom and buds."""
    fx = -1 if flip else 1
    p = []
    p.append("M0 0 C10 -80 -15 -160 20 -250 S80 -380 70 -460")
    for lx, ly, la, ll in ((5, -70, -35, 70), (0, -140, 210, 62), (35, -235, -30, 66), (45, -320, 200, 60), (70, -400, -25, 52)):
        W = ll * .22
        p.append(f"M{lx} {ly} c{ll * .3 * math.cos(math.radians(la)):.1f} {ll * .3 * math.sin(math.radians(la)) - W:.1f} "
                 f"{ll * .7 * math.cos(math.radians(la)):.1f} {ll * .7 * math.sin(math.radians(la)) - W:.1f} "
                 f"{ll * math.cos(math.radians(la)):.1f} {ll * math.sin(math.radians(la)):.1f}")
        p.append(f"M{lx} {ly} c{ll * .3 * math.cos(math.radians(la)):.1f} {ll * .3 * math.sin(math.radians(la)) + W:.1f} "
                 f"{ll * .7 * math.cos(math.radians(la)):.1f} {ll * .7 * math.sin(math.radians(la)) + W:.1f} "
                 f"{ll * math.cos(math.radians(la)):.1f} {ll * math.sin(math.radians(la)):.1f}")
    bloom = "".join(f'<path d="{petal_path(34)}" transform="translate(70 -470) rotate({a})" fill="none"/>' for a in range(0, 360, 60))
    buds = ('<path d="M20 -250 C 50 -270 70 -300 66 -330" fill="none"/><ellipse cx="66" cy="-340" rx="9" ry="14" fill="none"/>'
            '<path d="M0 -140 C -30 -170 -40 -200 -36 -230" fill="none"/><ellipse cx="-36" cy="-240" rx="8" ry="13" fill="none"/>')
    paths = "".join(f'<path d="{d}" fill="none"/>' for d in p)
    return (f'<g class="{cls}" transform="translate({x} {y}) rotate({rot}) scale({fx * s} {s})" stroke="{color}" '
            f'stroke-width="{width / s:.2f}" stroke-linecap="round" stroke-linejoin="round">{paths}{bloom}{buds}'
            f'<circle cx="70" cy="-470" r="6" fill="{color}" stroke="none"/></g>')


def sparkle(x, y, s, color=None, op=1.0, cls="tw"):
    c = color or C["gold"]
    d = (f"M0 {-s} C{s * .12:.1f} {-s * .12:.1f} {s * .12:.1f} {-s * .12:.1f} {s} 0 C{s * .12:.1f} {s * .12:.1f} "
         f"{s * .12:.1f} {s * .12:.1f} 0 {s} C{-s * .12:.1f} {s * .12:.1f} {-s * .12:.1f} {s * .12:.1f} {-s} 0 "
         f"C{-s * .12:.1f} {-s * .12:.1f} {-s * .12:.1f} {-s * .12:.1f} 0 {-s}Z")
    return f'<path class="{cls}" d="{d}" transform="translate({x} {y})" fill="{c}" opacity="{op}"/>'


def doodle_star(x, y, s, color=None, width=2.4, rot=0, seed=5):
    r = _rng(seed)
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36 + rot)
        rr = s if i % 2 == 0 else s * .45
        rr *= r.uniform(.93, 1.07)
        pts.append(f"{x + rr * math.cos(a):.1f},{y + rr * math.sin(a):.1f}")
    pts.append(pts[0])
    return (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color or C["gold"]}" stroke-width="{width}" '
            f'stroke-linejoin="round" stroke-linecap="round"/>')


def washi(x, y, w, h, rot, pattern="stripeRose", opacity=.82):
    zig = 7
    top = [(x + i * w / 12, y) for i in range(13)]
    right = [(x + w + (zig if i % 2 else 0), y + i * h / 6) for i in range(7)]
    bottom = [(x + w - i * w / 12, y + h) for i in range(13)]
    left = [(x - (zig if i % 2 else 0), y + h - i * h / 6) for i in range(7)]
    poly = " ".join(f"{a:.1f},{b:.1f}" for a, b in top + right + bottom + left)
    return (f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})" opacity="{opacity}" filter="url(#shadowSoft)">'
            f'<polygon points="{poly}" fill="url(#{pattern})"/><polygon points="{poly}" filter="url(#grain)"/></g>')


def ribbon(x, y, w, h, text, color=None, text_color="#FFFDF8", font="man", size=19, spacing=".32em", rot=0):
    c = color or C["rose_deep"]
    n = h * .45
    body = f"{x},{y} {x + w},{y} {x + w - n},{y + h / 2} {x + w},{y + h} {x},{y + h} {x + n},{y + h / 2}"
    return (f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})" filter="url(#shadowSoft)">'
            f'<polygon points="{body}" fill="{c}"/><polygon points="{body}" filter="url(#grain)" opacity=".6"/>'
            f'<line x1="{x + n + 6}" y1="{y + 6}" x2="{x + w - n - 6}" y2="{y + 6}" stroke="#fff" stroke-opacity=".35" stroke-dasharray="3 4"/>'
            f'<line x1="{x + n + 6}" y1="{y + h - 6}" x2="{x + w - n - 6}" y2="{y + h - 6}" stroke="#fff" stroke-opacity=".35" stroke-dasharray="3 4"/>'
            f'</g>'
            f'<foreignObject x="{x}" y="{y}" width="{w}" height="{h}" transform="rotate({rot} {x + w / 2} {y + h / 2})">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="{font}" style="height:{h}px;display:flex;align-items:center;'
            f'justify-content:center;color:{text_color};font-size:{size}px;letter-spacing:{spacing};font-weight:500;'
            f'text-transform:uppercase">{html.escape(text)}</div></foreignObject>')


def wax_seal(cx, cy, r, seed=8):
    rg = _rng(seed)
    pts = " ".join(f"{cx + (r + rg.uniform(-4, 5)) * math.cos(a):.1f},{cy + (r + rg.uniform(-4, 5)) * math.sin(a):.1f}"
                   for a in [i * 2 * math.pi / 26 for i in range(26)])
    return (f'<g filter="url(#shadowSoft)"><polygon points="{pts}" fill="url(#seal)"/></g>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .7:.1f}" fill="none" stroke="#F2D6D6" stroke-opacity=".55" stroke-width="2"/>'
            f'{sparkle(cx, cy, r * .42, "#F8E6E4", .9, "")}')


def sticker(cx, cy, r, fill, text, text_color="#FFFDF8", font="corm", size=24, italic=True, rot=0):
    return (f'<g transform="rotate({rot} {cx} {cy})"><g filter="url(#shadowSoft)">'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 7}" fill="#FFFDF9"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/></g>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" filter="url(#grain)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r - 7}" fill="none" stroke="#FFFDF8" stroke-opacity=".55" stroke-dasharray="2 4"/></g>'
            f'<foreignObject x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" transform="rotate({rot} {cx} {cy})">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="{font}" style="width:{2 * r}px;height:{2 * r}px;display:flex;'
            f'align-items:center;justify-content:center;text-align:center;color:{text_color};font-size:{size}px;line-height:1.05;'
            f'font-style:{"italic" if italic else "normal"};font-weight:500">{text}</div></foreignObject>')


def gold_frame(x, y, w, h, gap=8, width=1.6, color="url(#gold)", corners=True):
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{color}" stroke-width="{width}"/>'
           f'<rect x="{x + gap}" y="{y + gap}" width="{w - 2 * gap}" height="{h - 2 * gap}" fill="none" stroke="{color}" stroke-width="{width * .6}"/>')
    if corners:
        for cx, cy in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
            out += f'<rect x="{cx - 5}" y="{cy - 5}" width="10" height="10" fill="{C["gold"]}" transform="rotate(45 {cx} {cy})"/>'
    return out



def garden_rose(cx, cy, r, palette="rose", rot=0, seed=1):
    """Layered garden rose: three rings of cupped petals, darker heart, watercolour edges."""
    rg = _rng(seed)
    cols = {"rose": ("#F4DCD8", "#E2B6B2", "#C98F92", "#A86F78"),
            "blush": ("#FFF3EE", "#F2D6CF", "#DDB2AA", "#C08F8C"),
            "ivory": ("#FFFDF7", "#F4EADB", "#E2CFB3", "#C7AE8C"),
            "plum": ("#D8C0CF", "#B396AA", "#8C6C83", "#634A5D")}[palette]
    out = []
    for ring, (n, rr, sz, col) in enumerate(((9, .62, .55, cols[1]), (7, .4, .45, cols[2]), (5, .2, .34, cols[3]))):
        for i in range(n):
            a = rot + i * 360 / n + rg.uniform(-10, 10) + ring * 17
            px, py = math.cos(math.radians(a)) * r * rr, math.sin(math.radians(a)) * r * rr
            out.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{r * sz * .62:.1f}" ry="{r * sz * .48:.1f}" '
                       f'transform="rotate({a + 90:.1f} {px:.1f} {py:.1f})" fill="{col}" opacity=".9"/>')
    out.insert(0, f'<circle r="{r * .95:.1f}" fill="{cols[0]}" opacity=".95"/>')
    out.append(f'<path d="M{-r * .12:.1f} 0 a{r * .12:.1f} {r * .1:.1f} 0 1 1 {r * .2:.1f} {r * .04:.1f}" fill="none" '
               f'stroke="{cols[3]}" stroke-width="{max(1.2, r * .03):.1f}" opacity=".8"/>')
    return f'<g transform="translate({cx} {cy})" filter="url(#shadowSoft)"><g filter="url(#wc)">{"".join(out)}</g></g>'


def eucalyptus(x, y, length, angle, s=1.0, seed=2):
    """Stem of round eucalyptus leaves in dusty sage."""
    rg = _rng(seed)
    leaves = []
    for i in range(7):
        t = i / 6
        px = length * t
        side = 1 if i % 2 else -1
        rr = (16 - 7 * t) * s
        leaves.append(f'<ellipse cx="{px:.1f}" cy="{side * rr * 1.05:.1f}" rx="{rr * 1.05:.1f}" ry="{rr:.1f}" '
                      f'fill="{rg.choice(["#A9B8A0", "#9DAE95", "#B7C4AE", "#8FA187"])}" opacity=".95"/>')
    return (f'<g transform="translate({x} {y}) rotate({angle})"><path d="M0 0 L{length:.1f} 0" stroke="{C["sage_deep"]}" '
            f'stroke-width="{2.2 * s:.1f}"/><g filter="url(#wc)">{"".join(leaves)}</g></g>')


def filler(x, y, s=1.0, color="#FFFDF8", seed=4):
    """Baby's-breath style filler: a fine branching stem with tiny blossoms."""
    rg = _rng(seed)
    out = [f'<path d="M0 0 C{8 * s} {-30 * s} {-6 * s} {-60 * s} {4 * s} {-90 * s}" stroke="{C["sage_deep"]}" stroke-width="1.4" fill="none"/>']
    for i in range(14):
        a = rg.uniform(-150, -30)
        d = rg.uniform(30, 95) * s
        bx, by = math.cos(math.radians(a)) * d * .5, math.sin(math.radians(a)) * d
        out.append(f'<path d="M0 {by * .5:.1f} L{bx:.1f} {by:.1f}" stroke="{C["sage_deep"]}" stroke-width=".9" opacity=".7"/>'
                   f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{rg.uniform(3, 5.5) * s:.1f}" fill="{color}" stroke="{C["gold_light"]}" stroke-width=".6"/>')
    return f'<g transform="translate({x} {y})">{"".join(out)}</g>'


def bouquet(x, y, s=1.0, rot=0, mood="rose", seed=10):
    """A tucked corner arrangement: garden roses, cosmos, eucalyptus, leaves, filler, sparkles."""
    pal = {"rose": ("rose", "blush", "petalRose", "petalBlush"),
           "ivory": ("ivory", "blush", "petalIvory", "petalBlush"),
           "plum": ("plum", "blush", "petalPlum", "petalBlush")}[mood]
    g = (eucalyptus(-20, 10, 230, -150, 1.0, seed) + eucalyptus(10, 0, 210, -40, .9, seed + 1)
         + leaf(-10, -10, 120, -115) + leaf(20, -6, 110, -70) + leaf(0, 0, 100, -165)
         + filler(-70, -40, 1.1, seed=seed) + filler(90, -30, .9, "#F6E8E3", seed=seed + 2)
         + flower(-95, -95, 40, pal[2], 7, 15, seed=seed + 3) + flower(120, -110, 30, pal[3], 6, 5, seed=seed + 4)
         + garden_rose(10, -80, 62, pal[0], 10, seed=seed + 5) + garden_rose(-60, -10, 42, pal[1], 40, seed=seed + 6)
         + garden_rose(78, -20, 36, pal[1], 70, seed=seed + 7)
         + sparkle(150, -170, 9) + sparkle(-150, -150, 7, op=.8))
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">{g}</g>'


def svg(content, w=1920, h=1080):
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{defs()}{content}</svg>'


def text(x, y, w, inner, align="center", extra=""):
    return f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;text-align:{align};{extra}">{inner}</div>'


TITLE_1, TITLE_2 = "5 Life Lessons", "I Wish I Knew Earlier"
SUBTITLE = "A little wisdom for a more independent life"
CLOSING = "Until next time, be confident, be bold, and keep choosing yourself."


# ============================================================================= A: Pressed Garden
def _divider(color, width=240, glyph="&#10022;"):
    return (f'<div style="margin:24px auto;width:{width}px;display:flex;align-items:center;gap:14px">'
            f'<span style="flex:1;height:1px;background:{color}"></span><span style="color:{color};font-size:18px">{glyph}</span>'
            f'<span style="flex:1;height:1px;background:{color}"></span></div>')


def A_opening(bg=None):
    c = C
    x, y, w, h = 1312, 118, 520, 650
    art = (torn_sheet(x, y, w, h, c["paper"], "bottom", rot=-1.4, seed=21, amp=11)
           + f'<g transform="rotate(-1.4 {x + w / 2} {y + h / 2})">'
             f'<rect x="{x + 24}" y="{y + 24}" width="{w - 48}" height="{h - 66}" fill="none" stroke="url(#gold)" stroke-width="1.4"/>'
             f'<rect x="{x + 31}" y="{y + 31}" width="{w - 62}" height="{h - 80}" fill="none" stroke="url(#gold)" stroke-width=".7"/></g>'
           + washi(x - 30, y + 18, 150, 40, -36, "dotSage")
           + bouquet(x + w - 6, y + 40, .78, 205, "rose", seed=11)
           + bouquet(x + w - 30, y + h + 10, .52, -20, "ivory", seed=21)
           + sparkle(x + 70, y + 110, 11) + sparkle(x + 92, y + 138, 6, op=.8) + sparkle(x + w - 80, y + h - 130, 9, op=.85))
    t = text(x + 30, y + 92, w - 60,
             f'<div class="corm" style="font-size:168px;line-height:.78;font-style:italic;font-weight:500;color:{c["gold"]}">5</div>'
             f'<div class="corm" style="font-size:70px;line-height:1;font-weight:500;color:{c["plum"]};margin-top:30px">Life Lessons</div>'
             f'<div class="corm" style="font-size:46px;line-height:1.15;font-style:italic;color:{c["rose_deep"]};margin-top:4px">I wish I knew earlier</div>'
             + _divider(c["gold"]) +
             f'<div class="man" style="font-size:23px;letter-spacing:.09em;color:{c["sage_deep"]};font-weight:500;line-height:1.5;padding:0 34px">{SUBTITLE}</div>',
             extra="transform:rotate(-1.4deg)")
    return page(svg(art) + t, bg=bg)


def A_reminder(bg=None):
    c = C
    x, y, w, h = 1432, 66, 390, 176
    shape = f"M{x} {y + 34} L{x + 42} {y} L{x + w} {y} L{x + w} {y + h} L{x + 42} {y + h} L{x} {y + h - 34} Z"
    art = (f'<path d="M{x + 26} {y + h / 2} C{x - 40} {y + 20} {x + 20} {y - 50} {x + 120} {y - 34}" fill="none" '
           f'stroke="{c["gold_deep"]}" stroke-width="2.2" opacity=".85"/>'
           + f'<g transform="rotate(-3.5 {x + w / 2} {y + h / 2})"><g filter="url(#shadowSoft)"><g filter="url(#deckle)">'
             f'<path d="{shape}" fill="{c["paper"]}"/></g></g><path d="{shape}" filter="url(#grain)"/>'
             f'<circle cx="{x + 28}" cy="{y + h / 2}" r="10" fill="none" stroke="{c["gold"]}" stroke-width="2.2"/>'
             f'<rect x="{x + 56}" y="{y + 14}" width="{w - 70}" height="{h - 28}" fill="none" stroke="url(#gold)" stroke-width="1.1"/></g>'
           + garden_rose(x + w - 6, y + h - 8, 30, "rose", 20, seed=7) + eucalyptus(x + w - 20, y + h - 4, 90, 150, .7, seed=3)
           + sparkle(x + 74, y + 30, 9))
    t = text(x + 58, y + 34, w - 72,
             f'<div class="corm" style="font-size:60px;font-style:italic;font-weight:500;color:{c["plum"]};line-height:1">Subscribe</div>'
             f'<div class="man" style="font-size:20px;letter-spacing:.1em;color:{c["sage_deep"]};margin-top:12px;font-weight:500">for more gentle lessons</div>',
             extra="transform:rotate(-3.5deg)")
    return page(svg(art) + t, bg=bg)


def A_end(guides=False):
    c = C
    bx, by, bw, bh = WATCH_BOX
    sx, sy, sr = SUB_CIRCLE
    art = (f'<rect width="1920" height="1080" fill="{c["ivory"]}"/><rect width="1920" height="1080" filter="url(#mottle)"/>'
           f'<rect width="1920" height="1080" filter="url(#grain)"/>'
           + bouquet(70, 1085, 1.05, 32, "rose", seed=31)
           + bouquet(1905, 18, .82, 200, "ivory", seed=41)
           + bouquet(1890, 1070, .7, -38, "rose", seed=51)
           + torn_sheet(bx - 46, by - 46, bw + 92, bh + 92, c["rose_pale"], "right", rot=1.1, seed=41, amp=10)
           + f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#FFFCF7"/>'
           + gold_frame(bx - 14, by - 14, bw + 28, bh + 28, 7)
           + washi(bx - 74, by - 36, 176, 42, -32, "stripeRose") + washi(bx + bw - 96, by + bh - 4, 176, 42, -32, "dotSage")
           + f'<circle cx="{sx}" cy="{sy}" r="{sr + 18}" fill="#FFFCF7" filter="url(#shadowSoft)"/>'
           + f'<circle cx="{sx}" cy="{sy}" r="{sr + 10}" fill="none" stroke="url(#gold)" stroke-width="1.6"/>'
           + f'<circle cx="{sx}" cy="{sy}" r="{sr + 18}" fill="none" stroke="url(#gold)" stroke-width=".8"/>'
           + sparkle(sx + 150, sy - 120, 12) + sparkle(sx + 176, sy - 94, 6, op=.8) + sparkle(880, 120, 10, op=.85))
    t = (text(170, 132, 780,
              f'<div class="man" style="font-size:20px;letter-spacing:.34em;color:{c["sage_deep"]};text-transform:uppercase;font-weight:500">with love &amp; gratitude</div>'
              f'<div class="corm" style="font-size:146px;line-height:.92;font-style:italic;font-weight:500;color:{c["plum"]};margin-top:20px">Thank you</div>'
              f'<div class="corm" style="font-size:80px;line-height:1.05;font-weight:400;color:{c["plum"]}">for watching</div>'
              f'<div style="width:130px;height:1px;background:{c["gold"]};margin:30px 0 24px"></div>'
              f'<div class="corm" style="font-size:36px;font-style:italic;line-height:1.3;color:{c["rose_deep"]};max-width:660px">{CLOSING}</div>',
              align="left")
         + text(bx, by - 96, bw, f'<div class="corm" style="font-size:46px;font-style:italic;color:{c["plum"]}">watch next</div>')
         + text(sx + sr + 46, sy - 40, 440,
                f'<div class="corm" style="font-size:52px;font-style:italic;color:{c["plum"]};line-height:1">Subscribe</div>'
                f'<div class="man" style="font-size:20px;letter-spacing:.1em;color:{c["sage_deep"]};margin-top:10px;font-weight:500">for more life lessons</div>',
                align="left"))
    return page(svg(art) + t + (guides_overlay() if guides else ""), opaque=True)


# ============================================================================= B: Scrapbook Journal
def B_opening(bg=None):
    c = C
    x, y, w, h = 1318, 150, 510, 560
    art = (torn_sheet(x - 26, y - 14, w + 34, h + 34, c["rose_pale"], "right", rot=3.4, seed=51, amp=12)
           + torn_sheet(x + 8, y + 12, w - 16, h - 16, c["paper"], "top", rot=-2.0, seed=52, amp=10, fill_pattern="ruled")
           + f'<g transform="rotate(-2 {x + w / 2} {y + h / 2})"><line x1="{x + 58}" y1="{y + 22}" x2="{x + 58}" y2="{y + h - 6}" '
             f'stroke="{c["rose"]}" stroke-width="1.4" opacity=".65"/></g>'
           + washi(x - 30, y + 2, 150, 40, -38, "stripeRose") + washi(x + w - 150, y + h - 26, 170, 40, -28, "dotSage")
           + bouquet(x + w - 4, y + h + 6, .5, -24, "rose", seed=61)
           + sticker(x + w - 30, y + 30, 64, c["sage_deep"], "note<br>to self", size=29, rot=10)
           + doodle_star(x + 104, y + 58, 20, rot=8) + sparkle(x + 30, y + h - 60, 10)
           + f'<g transform="rotate(-2 {x + w / 2} {y + h / 2})"><ellipse cx="{x + 150}" cy="{y + 196}" rx="66" ry="74" fill="none" '
             f'stroke="{c["gold"]}" stroke-width="2.8" stroke-dasharray="390 30" transform="rotate(-12 {x + 150} {y + 196})"/></g>')
    t = text(x + 88, y + 118, w - 130,
             f'<div style="display:flex;align-items:flex-end;gap:18px">'
             f'<span class="play" style="font-size:136px;line-height:.84;font-style:italic;color:{c["plum"]};width:122px;text-align:center">5</span>'
             f'<span class="play" style="font-size:56px;line-height:1.02;color:{c["plum"]};font-weight:500;padding-bottom:6px">Life<br>Lessons</span></div>'
             f'<div class="play" style="font-size:44px;font-style:italic;color:{c["rose_deep"]};margin-top:34px;line-height:1.15">I wish I knew earlier</div>'
             f'<div class="mont" style="font-size:22px;letter-spacing:.04em;color:{c["plum_soft"]};margin-top:30px;line-height:1.55;font-weight:500">{SUBTITLE}</div>',
             align="left", extra="transform:rotate(-2deg)")
    return page(svg(art) + t, bg=bg)


def B_reminder(bg=None):
    c = C
    x, y, w, h = 1440, 76, 370, 150
    art = (torn_sheet(x, y, w, h, c["paper"], "bottom", rot=-3, seed=71, amp=8, fill_pattern="ruled")
           + washi(x + 120, y - 20, 130, 36, 4, "stripeRose")
           + sticker(x + w - 6, y + h - 4, 40, c["rose_deep"], "&#9825;", size=36, italic=False, rot=-8)
           + doodle_star(x + 32, y + 40, 13, seed=12) + sparkle(x + w - 40, y + 26, 8))
    t = text(x + 54, y + 30, w - 80,
             f'<div class="play" style="font-size:52px;font-style:italic;color:{c["plum"]};line-height:1">subscribe</div>'
             f'<div class="mont" style="font-size:20px;letter-spacing:.04em;color:{c["sage_deep"]};margin-top:12px;font-weight:500">for more life lessons</div>',
             align="left", extra="transform:rotate(-3deg)")
    return page(svg(art) + t, bg=bg)


def B_end(guides=False):
    c = C
    bx, by, bw, bh = WATCH_BOX
    sx, sy, sr = SUB_CIRCLE
    art = (f'<rect width="1920" height="1080" fill="{c["cream"]}"/><rect width="1920" height="1080" fill="url(#dots)"/>'
           f'<rect width="1920" height="1080" filter="url(#mottle)"/><rect width="1920" height="1080" filter="url(#grain)"/>'
           + torn_sheet(96, 120, 820, 540, c["rose_pale"], "right", rot=-2.4, seed=81, amp=12)
           + torn_sheet(130, 150, 760, 490, c["paper"], "bottom", rot=1.3, seed=82, amp=10, fill_pattern="ruled")
           + washi(104, 130, 176, 42, -28, "dotSage") + washi(790, 600, 176, 42, -24, "stripeRose")
           + bouquet(60, 1088, .95, 28, "rose", seed=91) + bouquet(1906, 22, .78, 200, "ivory", seed=93)
           + f'<g filter="url(#shadow)"><rect x="{bx - 26}" y="{by - 26}" width="{bw + 52}" height="{bh + 120}" fill="#FFFDF9" transform="rotate(1.6 {bx + bw / 2} {by + bh / 2})"/></g>'
           + f'<rect x="{bx - 26}" y="{by - 26}" width="{bw + 52}" height="{bh + 120}" filter="url(#grain)" transform="rotate(1.6 {bx + bw / 2} {by + bh / 2})"/>'
           + f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{c["ivory"]}"/>'
           + washi(bx + bw / 2 - 84, by - 52, 168, 42, -3, "stripeRose")
           + sticker(bx + bw + 4, by + bh + 64, 62, c["plum_soft"], "watch<br>next", size=30, rot=12)
           + f'<circle cx="{sx}" cy="{sy}" r="{sr + 16}" fill="#FFFDF9" filter="url(#shadowSoft)"/>'
           + f'<circle cx="{sx}" cy="{sy}" r="{sr + 9}" fill="none" stroke="{c["rose_deep"]}" stroke-width="2.2" stroke-dasharray="6 7"/>'
           + doodle_star(sx + 150, sy - 126, 20, rot=10, seed=3) + doodle_star(sx + 190, sy - 84, 10, seed=6)
           + sparkle(1010, 150, 9, op=.85))
    t = (text(200, 214, 650,
              f'<div class="play" style="font-size:118px;line-height:.98;font-style:italic;color:{c["plum"]}">Thank you</div>'
              f'<div class="mont" style="font-size:28px;letter-spacing:.34em;text-transform:uppercase;color:{c["rose_deep"]};margin-top:18px;font-weight:500">for watching</div>'
              f'<div class="play" style="font-size:33px;font-style:italic;line-height:1.45;color:{c["plum_soft"]};margin-top:40px;max-width:600px">{CLOSING}</div>',
              align="left", extra="transform:rotate(1.3deg)")
         + text(sx + sr + 44, sy - 38, 440,
                f'<div class="play" style="font-size:48px;font-style:italic;color:{c["plum"]};line-height:1">subscribe</div>'
                f'<div class="mont" style="font-size:20px;letter-spacing:.04em;color:{c["sage_deep"]};margin-top:10px;font-weight:500">for more life lessons</div>',
                align="left"))
    return page(svg(art) + t + (guides_overlay() if guides else ""), opaque=True)


# ============================================================================= C: Champagne Editorial
def C_opening(bg=None):
    c = C
    veil = ('<div class="abs" style="left:1210px;top:0;width:710px;height:1080px;'
            'background:linear-gradient(90deg,rgba(248,242,233,0) 0%,rgba(248,242,233,.66) 22%,rgba(248,242,233,.74) 100%)"></div>')
    art = (gold_frame(36, 36, 1848, 1008, 9, 1.4, corners=False)
           + fineline(1838, 1016, .74, -8, flip=True) + fineline(1748, 1030, .48, 12)
           + sparkle(1810, 130, 12) + sparkle(1786, 156, 6, op=.8) + sparkle(1380, 196, 8, op=.8))
    t = text(1330, 150, 520,
             f'<div class="mont" style="font-size:20px;letter-spacing:.42em;text-transform:uppercase;color:{c["gold_deep"]};font-weight:500">a little series</div>'
             f'<div class="play" style="font-size:150px;line-height:.9;font-style:italic;color:{c["gold_deep"]};margin-top:18px">5</div>'
             f'<div class="play" style="font-size:74px;line-height:1.02;color:{c["plum"]};font-weight:500;margin-top:16px">Life Lessons</div>'
             f'<div class="play" style="font-size:48px;line-height:1.15;color:{c["plum"]};font-style:italic">I Wish I Knew Earlier</div>'
             + _divider(c["gold_deep"], 220) +
             f'<div class="corm" style="font-size:36px;font-style:italic;line-height:1.25;color:{c["plum_soft"]};padding:0 40px">{SUBTITLE}</div>')
    return page(veil + svg(art) + t, bg=bg)


def C_reminder(bg=None):
    c = C
    x, y, w, h = 1376, 84, 450, 112
    art = (f'<g filter="url(#shadowSoft)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{c["paper"]}" opacity=".97"/></g>'
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" filter="url(#grain)"/>'
           f'<rect x="{x + 7}" y="{y + 7}" width="{w - 14}" height="{h - 14}" rx="{h / 2 - 7}" fill="none" stroke="url(#gold)" stroke-width="1.3"/>'
           + wax_seal(x + 60, y + h / 2, 38) + fineline(x + w - 26, y + h + 8, .24, 22))
    t = text(x + 116, y + 18, w - 150,
             f'<div class="play" style="font-size:46px;font-style:italic;color:{c["plum"]};line-height:1">Subscribe</div>'
             f'<div class="mont" style="font-size:17px;letter-spacing:.16em;text-transform:uppercase;color:{c["gold_deep"]};margin-top:8px;font-weight:500">for more life lessons</div>',
             align="left")
    return page(svg(art) + t, bg=bg)


def C_end(guides=False):
    c = C
    bx, by, bw, bh = WATCH_BOX
    sx, sy, sr = SUB_CIRCLE
    art = (f'<rect width="1920" height="1080" fill="url(#plumGlow)"/><rect width="1920" height="1080" filter="url(#grain)" opacity=".7"/>'
           + gold_frame(40, 40, 1840, 1000, 10, 1.4, corners=False)
           + fineline(96, 1032, .78, 4) + fineline(196, 1040, .5, -16, flip=True)
           + fineline(1836, 1032, .62, -6, flip=True)
           + f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#4A3446" opacity=".55"/>'
           + gold_frame(bx - 16, by - 16, bw + 32, bh + 32, 8, 1.4)
           + f'<circle cx="{sx}" cy="{sy}" r="{sr + 12}" fill="none" stroke="url(#gold)" stroke-width="1.6"/>'
           + f'<circle cx="{sx}" cy="{sy}" r="{sr + 20}" fill="none" stroke="url(#gold)" stroke-width=".8"/>'
           + wax_seal(sx + sr + 4, sy - sr + 6, 32)
           + sparkle(930, 130, 12, c["gold_light"]) + sparkle(955, 156, 6, c["gold_light"], .8)
           + ribbon(bx + bw / 2 - 170, by + bh + 44, 340, 56, "watch next", c["sage_deep"], size=20, spacing=".26em"))
    t = (text(150, 136, 820,
              f'<div class="mont" style="font-size:20px;letter-spacing:.42em;text-transform:uppercase;color:{c["gold_light"]};font-weight:500">with gratitude</div>'
              f'<div class="play" style="font-size:134px;line-height:1;font-style:italic;color:#F8EFE6;margin-top:22px">Thank you</div>'
              f'<div class="mont" style="font-size:30px;letter-spacing:.36em;text-transform:uppercase;color:{c["gold_light"]};margin-top:14px;font-weight:500">for watching</div>'
              f'<div class="corm" style="font-size:38px;font-style:italic;line-height:1.32;color:#EADBD3;margin-top:38px;max-width:660px">{CLOSING}</div>',
              align="left")
         + text(sx + sr + 50, sy - 36, 440,
                f'<div class="play" style="font-size:46px;font-style:italic;color:#F8EFE6;line-height:1">Subscribe</div>'
                f'<div class="mont" style="font-size:17px;letter-spacing:.16em;text-transform:uppercase;color:{c["gold_light"]};margin-top:9px;font-weight:500">for more life lessons</div>',
                align="left"))
    return page(svg(art) + t + (guides_overlay() if guides else ""), opaque=True)


# ============================================================================= C final (approved direction)
# Animated versions of C. Each page exposes window.setT(t) (seconds) and is stepped frame by frame
# by render_frames(). Motion is restrained: fades with a few px of drift, gold lines drawn on,
# a wax seal settling, slow sparkle. Elements carry data-in (start, s), data-d (duration, s) and
# data-kind: "fade" (default), "draw" (stroke draw-on), "seal" (settle) or "tw" (twinkle).
CREATOR, HANDLE = "Pranali Desai", "@heyPranali"
FINAL_SUBTITLE = "Things I wish someone had told me in my twenties."
REMINDER_LINE = "for more life lessons"
OPENING_DUR, REMINDER_DUR, END_DUR = 5.0, 4.8, 18.0

_ANIM_JS = """
<script>
const E = x => { x = Math.min(1, Math.max(0, x)); return 1 - Math.pow(1 - x, 3); };
const SM = x => { x = Math.min(1, Math.max(0, x)); return x * x * (3 - 2 * x); };
const els = [...document.querySelectorAll('[data-in]')];
els.forEach(el => {
  if (el.dataset.kind === 'draw')
    el.querySelectorAll('path,ellipse,rect,circle,line,polyline').forEach(p => {
      if (p.getAttribute('fill') && p.getAttribute('fill') !== 'none' && !p.getAttribute('stroke')) return;
      const L = p.getTotalLength(); p.style.strokeDasharray = L + ' ' + L; p.dataset.len = L; });
});
const tws = [...document.querySelectorAll('.tw')];
window.setT = function (t) {
  for (const el of els) {
    const a = +el.dataset.in, d = +(el.dataset.d || 0.8), k = E((t - a) / d), kind = el.dataset.kind || 'fade';
    if (kind === 'fade') { el.style.opacity = k; el.style.transform = 'translateY(' + ((1 - k) * +(el.dataset.dy || 10)).toFixed(2) + 'px)'; }
    else if (kind === 'draw') {
      el.style.opacity = Math.min(1, k * 4);
      el.querySelectorAll('[data-len]').forEach(p => p.style.strokeDashoffset = (1 - SM((t - a) / d)) * p.dataset.len);
    } else if (kind === 'seal') {
      el.style.opacity = Math.min(1, k * 2.5);
      el.style.transform = 'scale(' + (1.12 - 0.12 * k).toFixed(4) + ') rotate(' + (-8 * (1 - k)).toFixed(2) + 'deg)';
    }
  }
  tws.forEach((s, i) => { const ph = i * 1.7;
    s.style.opacity = (0.45 + 0.55 * (0.5 + 0.5 * Math.sin(t * 1.6 + ph))).toFixed(3); });
  const root = document.getElementById('root'), T = +root.dataset.dur, out = +(root.dataset.out || 0.6);
  root.style.opacity = (1 - SM((t - (T - out)) / out)).toFixed(4);
};
window.setT(0);
</script>"""


def _a(t, d=0.8, kind="fade", dy=10):
    return f'data-in="{t}" data-d="{d}" data-kind="{kind}" data-dy="{dy}"'


def _g(inner, t, d=0.8, kind="fade", origin=None):
    o = (f' style="transform-box:fill-box;transform-origin:center"' if kind == "seal" else "")
    return f'<g {_a(t, d, kind)}{o}>{inner}</g>'


def _anim_page(body, dur, out=0.6, opaque=False, bg=None):
    # bg (a still) is for preview stills only; the video pages are transparent overlays
    doc = page(f'<div id="root" data-dur="{dur}" data-out="{out}" style="position:absolute;inset:0">{body}</div>',
               bg=bg, opaque=opaque, bg_color=C["plum_deep"])
    return doc.replace("</body>", _ANIM_JS + "</body>")


def CF_opening(bg=None):
    c = C
    veil = (f'<div class="abs" {_a(0.0, 0.9, dy=0)} style="left:1190px;top:0;width:730px;height:1080px;'
            'background:linear-gradient(90deg,rgba(248,242,233,0) 0%,rgba(248,242,233,.70) 21%,rgba(248,242,233,.80) 100%)"></div>')
    art = svg(_g(gold_frame(36, 36, 1848, 1008, 9, 1.4, corners=False), 0.15, 1.6, "draw")
              + _g(fineline(1846, 1018, .66, -8, flip=True), 0.5, 2.2, "draw")
              + _g(fineline(1770, 1034, .42, 12), 0.8, 2.0, "draw")
              + _g(sparkle(1812, 128, 12, cls="tw") + sparkle(1788, 154, 6, op=.8, cls="tw")
                   + sparkle(1372, 168, 8, op=.8, cls="tw"), 0.9, 0.8))
    L = 1316
    t = (text(L, 112, 548, f'<div class="play" {_a(0.35, 0.9)} style="font-size:150px;line-height:.9;font-style:italic;color:{c["gold_deep"]}">5</div>')
         + text(L, 262, 548,
                f'<div class="play" {_a(0.55, 0.9)} style="font-size:80px;line-height:1.02;color:{c["plum"]};font-weight:500">Life Lessons</div>'
                f'<div class="play" {_a(0.75, 0.9)} style="font-size:54px;line-height:1.15;color:{c["plum"]};font-style:italic">I Wish I Knew Earlier</div>')
         + text(L, 432, 548, f'<div {_a(1.0, 0.9, dy=0)}>{_divider(c["gold_deep"], 220)}</div>')
         + text(L, 506, 548,
                f'<div class="corm" {_a(1.15, 0.9)} style="font-size:42px;font-style:italic;line-height:1.22;color:{c["plum_soft"]};'
                f'font-weight:500;padding:0 30px">{html.escape(FINAL_SUBTITLE)}</div>')
         + text(L, 650, 548,
                f'<div {_a(1.45, 0.9)}>'
                f'<div style="width:46px;height:1px;background:{c["gold_deep"]};margin:0 auto 18px"></div>'
                f'<div class="play" style="font-size:38px;font-style:italic;color:{c["plum"]};line-height:1.1">{html.escape(CREATOR)}</div>'
                f'<div class="mont" style="font-size:26px;letter-spacing:.08em;color:{c["gold_deep"]};margin-top:8px;font-weight:500">'
                f'{html.escape(HANDLE)}</div></div>'))
    return _anim_page(veil + art + t, OPENING_DUR, 0.7, bg=bg)


def CF_reminder(bg=None):
    c = C
    x, y, w, h = 1290, 80, 556, 126
    pill = (f'<g filter="url(#shadowSoft)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{c["paper"]}" opacity=".97"/></g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" filter="url(#grain)"/>')
    art = svg(_g(pill, 0.0, 0.6)
              + _g(f'<rect x="{x + 7}" y="{y + 7}" width="{w - 14}" height="{h - 14}" rx="{h / 2 - 7}" fill="none" '
                   f'stroke="url(#gold)" stroke-width="1.4"/>', 0.2, 1.3, "draw")
              + _g(wax_seal(x + 66, y + h / 2, 42), 0.35, 0.7, "seal")
              + _g(fineline(x + w - 58, y + h - 6, .2, 24), 0.6, 1.4, "draw")
              + _g(sparkle(x + w - 30, y + 18, 8, cls="tw"), 0.9, 0.6))
    t = text(x + 128, y + 18, w - 160,
             f'<div class="play" {_a(0.45, 0.7, dy=6)} style="font-size:52px;font-style:italic;color:{c["plum"]};line-height:1">Subscribe</div>'
             f'<div class="mont" {_a(0.7, 0.7, dy=6)} style="font-size:22px;letter-spacing:.13em;text-transform:uppercase;color:{c["gold_deep"]};'
             f'margin-top:9px;font-weight:600">{REMINDER_LINE}</div>',
             align="left")
    return _anim_page(art + t, REMINDER_DUR, 0.55, bg=bg)


def CF_end(guides=False):
    c = C
    bx, by, bw, bh = WATCH_BOX
    sx, sy, sr = SUB_CIRCLE
    base = svg(f'<rect width="1920" height="1080" fill="url(#plumGlow)"/><rect width="1920" height="1080" filter="url(#grain)" opacity=".7"/>')
    art = svg(_g(gold_frame(40, 40, 1840, 1000, 10, 1.4, corners=False), 0.1, 1.8, "draw")
              + _g(fineline(96, 1032, .78, 4) + fineline(196, 1040, .5, -16, flip=True), 0.6, 2.6, "draw")
              + _g(fineline(1836, 1032, .62, -6, flip=True), 0.9, 2.4, "draw")
              + _g(fineline(1822, 66, .38, 176), 1.1, 2.2, "draw")
              + _g(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#4A3446" opacity=".55"/>', 0.9, 0.9)
              + _g(gold_frame(bx - 16, by - 16, bw + 32, bh + 32, 8, 1.4), 1.0, 1.4, "draw")
              + _g(f'<circle cx="{sx}" cy="{sy}" r="{sr + 12}" fill="none" stroke="url(#gold)" stroke-width="1.6"/>'
                   f'<circle cx="{sx}" cy="{sy}" r="{sr + 20}" fill="none" stroke="url(#gold)" stroke-width=".8"/>', 1.3, 1.4, "draw")
              + _g(wax_seal(sx + sr + 4, sy - sr + 6, 34), 2.1, 0.8, "seal")
              + _g(sparkle(930, 130, 12, c["gold_light"], cls="tw") + sparkle(955, 156, 6, c["gold_light"], .8, cls="tw")
                   + sparkle(1790, 760, 8, c["gold_light"], .8, cls="tw"), 1.4, 0.8)
              + _g(ribbon(bx + bw / 2 - 180, by + bh + 44, 360, 60, "watch next", c["sage_deep"], size=24, spacing=".26em"), 1.8, 0.8))
    t = (text(150, 128, 820,
              f'<div class="mont" {_a(0.4)} style="font-size:24px;letter-spacing:.4em;text-transform:uppercase;color:{c["gold_light"]};font-weight:500">'
              f'with love &amp; gratitude</div>'
              f'<div class="play" {_a(0.65, 1.0)} style="font-size:138px;line-height:1;font-style:italic;color:#F8EFE6;margin-top:22px">Thank you</div>'
              f'<div class="mont" {_a(0.95)} style="font-size:32px;letter-spacing:.36em;text-transform:uppercase;color:{c["gold_light"]};margin-top:14px;font-weight:500">'
              f'for watching</div>'
              f'<div {_a(1.5, 1.0)} style="margin-top:40px">'
              f'<div class="corm" style="font-size:27px;font-style:italic;letter-spacing:.06em;color:{c["gold_light"]};opacity:.9">&mdash; note to self</div>'
              f'<div class="corm" style="font-size:44px;font-style:italic;line-height:1.28;color:#EADBD3;margin-top:6px;max-width:700px;font-weight:500">'
              f'{CLOSING}</div></div>',
              align="left")
         + text(sx + sr + 50, sy - 62, 460,
                f'<div {_a(1.9)}><div class="play" style="font-size:52px;font-style:italic;color:#F8EFE6;line-height:1">Subscribe</div>'
                f'<div class="mont" style="font-size:22px;letter-spacing:.14em;text-transform:uppercase;color:{c["gold_light"]};margin-top:10px;font-weight:600">'
                f'{REMINDER_LINE}</div>'
                f'<div class="mont" style="font-size:26px;letter-spacing:.08em;color:#F8EFE6;margin-top:14px;font-weight:500">'
                f'{html.escape(HANDLE)}</div></div>',
                align="left"))
    # the backdrop stays put; only the artwork and text fade out over the last second
    doc = _anim_page(art + t + (guides_overlay() if guides else ""), END_DUR, 1.0, opaque=True)
    return doc.replace('<div id="root"', base + '<div id="root"', 1)


def render_frames(doc, dur, out_dir, fps=30, alpha=True, start=0, stop=None):
    """Step window.setT through the page and save f00000.png... (alpha kept for overlays)."""
    from playwright.sync_api import sync_playwright
    os.makedirs(out_dir, exist_ok=True)
    n = int(round(dur * fps))
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        pg.set_content(doc)
        st = pg.evaluate("""async () => { await Promise.allSettled([...document.fonts].map(f => f.load()));
             await document.fonts.ready; const f = [...document.fonts];
             return [f.filter(x => x.status === 'loaded').length, f.length]; }""")
        if st[0] != st[1]:
            raise SystemExit(f"fonts failed to load ({st[0]}/{st[1]})")
        for i in range(start, n if stop is None else min(n, stop)):
            pg.evaluate(f"window.setT({i / fps})")
            pg.screenshot(path=os.path.join(out_dir, f"f{i:05d}.png"), omit_background=alpha)
        b.close()
    return n


ANIM = {"opening": (CF_opening, OPENING_DUR), "subscribe": (CF_reminder, REMINDER_DUR)}


def guides_overlay():
    """Where YouTube's own end-screen elements go (preview only, never rendered)."""
    bx, by, bw, bh = WATCH_BOX
    sx, sy, sr = SUB_CIRCLE
    lab = "font-family:Manrope;font-size:20px;font-weight:600;color:#fff;letter-spacing:.06em"
    return (f'<div class="abs" style="left:{bx}px;top:{by}px;width:{bw}px;height:{bh}px;background:rgba(30,30,30,.55);'
            f'border:3px dashed #fff;box-sizing:border-box;display:flex;align-items:center;justify-content:center;{lab}">'
            f'YouTube "Video" element (placed in YouTube Studio)</div>'
            f'<div class="abs" style="left:{sx - sr}px;top:{sy - sr}px;width:{2 * sr}px;height:{2 * sr}px;border-radius:50%;'
            f'background:rgba(30,30,30,.55);border:3px dashed #fff;box-sizing:border-box;display:flex;align-items:center;'
            f'justify-content:center;text-align:center;{lab};font-size:15px">YouTube<br>Subscribe<br>element</div>')


DIRECTIONS = {
    "A": ("Pressed Garden", A_opening, A_reminder, A_end),
    "B": ("Scrapbook Journal", B_opening, B_reminder, B_end),
    "C": ("Champagne Editorial", C_opening, C_reminder, C_end),
}


def render(pages, out_dir):
    from playwright.sync_api import sync_playwright
    os.makedirs(out_dir, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        for name, doc in pages.items():
            pg.set_content(doc)
            # load every embedded face explicitly, then confirm none failed before capturing
            st = pg.evaluate("""async () => { const r = await Promise.allSettled([...document.fonts].map(f => f.load()));
                 await document.fonts.ready;
                 const faces = [...document.fonts];
                 return {loaded: faces.filter(f => f.status === 'loaded').length, total: faces.length,
                         failed: faces.filter(f => f.status !== 'loaded').map(f => f.family + ' ' + f.weight + ' ' + f.style)}; }""")
            pg.wait_for_timeout(150)
            pg.screenshot(path=os.path.join(out_dir, name + ".png"), omit_background=True)
            print(name, f"fonts loaded {st['loaded']}/{st['total']}", "FAILED: " + ", ".join(st["failed"]) if st["failed"] else "")
        b.close()
