#!/usr/bin/env python3
"""Graphics templates for the stage-2 edit (HTML/CSS rendered by headless Chromium).

Every preset renders a 1920x1080 PNG: transparent for overlays, opaque for
full-frame cards. Passing `bg` (an image path) composites it over a still for
style frames. Palette is derived from the set (ivory wall, plum top, brass lamp).
"""
import base64
import html
import os
import re

FONT_DIR = os.environ.get("GFX_FONT_DIR", "")

PALETTE = {
    "paper": "#F4EFE6",      # ivory, lifted from the wall
    "ink": "#3A2A3B",        # deep plum, from the top
    "ink_soft": "#6E5A6B",
    "tag_bg": "#EFEBE3",
    "accent": "#8C6E84",     # dusty mauve
    "highlight": "#E3B04B",  # brass lamp gold
    "on_video": "#FFFFFF",
    "end_grad": ["#EBD9C6", "#C9B2C6", "#9E8BB0"],
}


def _font_face(family, path, weight=400, style="normal"):
    p = os.path.join(FONT_DIR, path)
    data = base64.b64encode(open(p, "rb").read()).decode()
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};font-style:{style};"
            f"src:url(data:font/woff2;base64,{data}) format('woff2');}}")


def _fonts():
    return "".join([
        _font_face("Serif", "fontsource-instrument-serif-5.3.0/package/files/instrument-serif-latin-400-normal.woff2"),
        _font_face("Serif", "fontsource-instrument-serif-5.3.0/package/files/instrument-serif-latin-400-italic.woff2", style="italic"),
        _font_face("Caption", "fontsource-poppins-5.3.0/package/files/poppins-latin-500-normal.woff2", 500),
        _font_face("Script", "fontsource-great-vibes-5.3.0/package/files/great-vibes-latin-400-normal.woff2"),
    ])


def _bold(text, color=None):
    """**word** -> bold (or coloured) span."""
    t = html.escape(text)
    style = f"font-weight:700;color:{color}" if color else "font-weight:700"
    return re.sub(r"\*\*(.+?)\*\*", rf"<span style='{style}'>\1</span>", t)


def page(body, bg=None, bg_filter="", opaque=False):
    p = PALETTE
    bg_css = ""
    if bg:
        data = base64.b64encode(open(bg, "rb").read()).decode()
        bg_css = (f"#bg{{position:absolute;inset:0;background:url(data:image/jpeg;base64,{data})"
                  f" center/cover;filter:{bg_filter}}}")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{_fonts()}
html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;
  background:{p['paper'] if opaque else 'transparent'}}}
{bg_css}
.abs{{position:absolute}}
.serif{{font-family:'Serif',serif}}
.sans{{font-family:'Inter',sans-serif}}
.cap{{font-family:'Caption',sans-serif;font-weight:500}}
.script{{font-family:'Script',cursive}}
</style></head><body>{'<div id="bg"></div>' if bg else ''}{body}</body></html>"""


def title_card(number, title):
    p = PALETTE
    return page(f"""<div class="abs serif" style="inset:0;display:flex;align-items:center;
      justify-content:center;font-size:84px;color:{p['ink']}">{number}. {html.escape(title)}</div>""",
                opaque=True)


def chapter_menu(title_lines, items):
    p = PALETTE
    tiles = "".join(
        f"""<div style="background:{p['accent']};border-radius:10px;padding:22px 24px;
            display:flex;flex-direction:column;justify-content:space-between;height:230px">
            <div class="serif" style="font-size:40px;line-height:1.1;color:#FFF8F0">{i + 1}. {html.escape(name)}</div>
            <div class="sans" style="font-size:22px;color:#F3E6EE;text-align:right">{ts}</div></div>"""
        for i, (name, ts) in enumerate(items))
    return page(f"""
      <div class="abs serif" style="top:150px;left:0;right:0;text-align:center;font-size:66px;
        line-height:1.15;color:{p['ink']}">{'<br>'.join(html.escape(t) for t in title_lines)}</div>
      <div class="abs" style="left:154px;right:154px;top:470px;display:grid;
        grid-template-columns:repeat({len(items)},1fr);gap:28px">{tiles}</div>""", opaque=True)


def notes(heading, items, side="right", bg=None):
    """Key-point list on the empty wall (right third) - no reframe needed."""
    p = PALETTE
    x = "left:1290px" if side == "right" else "left:170px"
    lis = "".join(f"<div style='margin-bottom:24px'>{_bold(it)}</div>" for it in items)
    return page(f"""
      <div class="abs" style="{x};top:150px;width:520px">
        <div class="serif" style="display:inline-block;background:{p['tag_bg']};color:{p['ink_soft']};
          font-size:38px;line-height:1.1;padding:12px 18px">{html.escape(heading)}</div>
        <div class="serif" style="margin-top:30px;color:{p['ink']};font-size:44px;line-height:1.12">{lis}</div>
      </div>""", bg=bg)


def pull_quote(text, bg=None):
    """Text layer only; the dim/blur of the A-roll is done in ffmpeg (or CSS for stills)."""
    vign = ("<div class='abs' style='inset:0;background:radial-gradient(ellipse at center,"
            "rgba(0,0,0,0) 45%,rgba(0,0,0,.45) 100%)'></div>") if bg else ""
    return page(f"""{vign}<div class="abs sans" style="left:260px;right:260px;top:430px;text-align:center;
      color:#fff;font-size:54px;line-height:1.25;font-weight:400">{_bold(text)}</div>""",
                bg=bg, bg_filter="blur(9px) brightness(.36)")


def pip_card(heading, bullets, pip_img=None, pip_crop=(0.30, 0.05, 0.62, 0.95)):
    """Ivory card, speaker PiP (3:4, rounded) on the right, bullets on the left."""
    p = PALETTE
    pip = ""
    if pip_img:
        data = base64.b64encode(open(pip_img, "rb").read()).decode()
        x0, y0, x1, y1 = pip_crop
        w = (x1 - x0)
        pip = (f"<div class='abs' style='left:1180px;top:110px;width:620px;height:827px;"
               f"border-radius:30px;overflow:hidden;box-shadow:0 8px 24px rgba(58,42,59,.18)'>"
               f"<div style='width:100%;height:100%;background:url(data:image/jpeg;base64,{data});"
               f"background-size:{100 / w:.1f}% auto;background-position:{x0 / (1 - w) * 100:.1f}% {y0 * 100:.0f}%'></div></div>")
    lis = "".join(f"<div style='margin:0 0 18px 0'>&ndash; {_bold(b)}</div>" for b in bullets)
    return page(f"""{pip}<div class="abs serif" style="left:150px;top:200px;width:920px;color:{p['ink']}">
        <div style="font-size:58px;color:{p['ink_soft']};margin-bottom:34px;line-height:1.1">{html.escape(heading)}</div>
        <div style="font-size:44px;line-height:1.2">{lis}</div></div>""", opaque=True)


def keywords(words_xy, bg=None):
    spans = "".join(f"<div class='abs sans' style='left:{x}px;top:{y}px;font-size:44px;font-weight:700;"
                    f"color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.35)'>{html.escape(w)}</div>"
                    for w, x, y in words_xy)
    return page(spans, bg=bg)


def caption(text, bg=None):
    return page(f"""<div class="abs cap" style="left:0;right:0;top:960px;text-align:center;color:#fff;
      font-size:42px;text-shadow:0 1px 4px rgba(0,0,0,.6)">{html.escape(text)}</div>""", bg=bg)


def end_screen(avatar_img=None, channel=""):
    p = PALETTE
    g = p["end_grad"]
    av = ""
    if avatar_img:
        data = base64.b64encode(open(avatar_img, "rb").read()).decode()
        av = (f"<div class='abs' style='left:250px;top:170px;width:400px;height:400px;border-radius:50%;"
              f"border:8px solid #fff;background:url(data:image/jpeg;base64,{data}) 47% 30%/260% auto'></div>")
    stars = "".join(f"<div class='abs' style='left:{x}px;top:{y}px;color:#fff;font-size:{s}px;opacity:.85'>&#10022;</div>"
                    for x, y, s in [(120, 90, 40), (760, 140, 28), (1700, 80, 36), (980, 620, 24),
                                    (1820, 900, 30), (90, 860, 26), (700, 940, 34), (1500, 520, 22)])
    return page(f"""<div class="abs" style="inset:0;background:linear-gradient({g[0]},{g[1]},{g[2]})"></div>{stars}{av}
      <div class="abs script" style="left:1150px;top:120px;font-size:84px;color:#fff">Watch this next</div>
      <div class="abs serif" style="left:250px;top:640px;font-size:60px;color:{p['ink']}">{html.escape(channel)}</div>
      <div class="abs sans" style="left:250px;top:760px;border:3px solid #fff;border-radius:40px;padding:14px 40px;
        color:#fff;font-size:36px;font-weight:600;letter-spacing:3px">SUBSCRIBE</div>""", opaque=True)


def render(pages, out_dir):
    """pages: {name: html}. Writes <out_dir>/<name>.png (alpha preserved)."""
    from playwright.sync_api import sync_playwright
    os.makedirs(out_dir, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        for name, doc in pages.items():
            pg.set_content(doc)
            pg.evaluate("document.fonts.ready")
            pg.screenshot(path=os.path.join(out_dir, name + ".png"), omit_background=True)
        b.close()
