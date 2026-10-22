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
        _font_face("Hand", "caveat/package/files/caveat-latin-500-normal.woff2", 500),
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
.hand{{font-family:'Hand',cursive}}
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


# ---------------------------------------------------------------------------
# Layered overlays: one transparent PNG per element so each can ease in on its
# own spoken cue while earlier elements stay perfectly still.

NOTES_X, NOTES_Y, NOTES_W = 1290, 150, 540


def notes_layers(heading, items):
    """{'head': html, 'item0': html, ...} - same layout, one element visible per layer."""
    p = PALETTE

    def doc(show):
        lis = "".join(
            f"<div style='margin-bottom:24px;visibility:{'visible' if show == f'item{i}' else 'hidden'}'>"
            f"{_bold(it)}</div>" for i, it in enumerate(items))
        head_vis = "visible" if show == "head" else "hidden"
        return page(f"""
          <div class="abs" style="left:{NOTES_X}px;top:{NOTES_Y}px;width:{NOTES_W}px">
            <div class="serif" style="visibility:{head_vis};display:inline-block;background:{p['tag_bg']};
              color:{p['ink_soft']};font-size:40px;line-height:1.1;padding:12px 20px;
              box-shadow:0 2px 10px rgba(58,42,59,.10)">{html.escape(heading)}</div>
            <div class="serif" style="margin-top:30px;color:{p['ink']};font-size:50px;line-height:1.1;
              text-shadow:0 1px 2px rgba(255,255,255,.35)">{lis}</div>
          </div>""")
    out = {"head": doc("head")}
    for i in range(len(items)):
        out[f"item{i}"] = doc(f"item{i}")
    return out


def keyword_layer(text, x, y):
    return page(f"""<div class='abs sans' style='left:{x}px;top:{y}px;font-size:46px;font-weight:700;
      color:#fff;text-shadow:0 2px 10px rgba(30,20,30,.55),0 0 2px rgba(30,20,30,.4)'>{html.escape(text)}</div>""")


def quote_layer(text):
    """Text only; the dim + blur of the A-roll is done in ffmpeg."""
    return page(f"""<div class="abs" style="inset:0;background:radial-gradient(ellipse at center,
      rgba(0,0,0,0) 40%,rgba(0,0,0,.42) 100%)"></div>
      <div class="abs sans" style="left:260px;right:260px;top:0;bottom:0;display:flex;align-items:center;
      justify-content:center;text-align:center;color:#fff;font-size:58px;line-height:1.25;font-weight:400;
      padding-bottom:110px"><div>{_bold(text)}</div></div>""")


PIP_BOX = (1180, 110, 620, 827)   # x, y, w, h of the speaker picture-in-picture


def pip_layers(heading, bullets):
    """Card background (paper, heading, empty PiP frame) + one layer per bullet."""
    p = PALETTE
    x, y, w, h = PIP_BOX

    def doc(show):
        lis = "".join(
            f"<div style='margin:0 0 22px 0;visibility:{'visible' if show == f'b{i}' else 'hidden'}'>"
            f"&ndash; {_bold(b)}</div>" for i, b in enumerate(bullets))
        bg = show == "bg"
        frame = (f"<div class='abs' style='left:{x - 2}px;top:{y - 2}px;width:{w + 4}px;height:{h + 4}px;"
                 f"border-radius:32px;box-shadow:0 10px 28px rgba(58,42,59,.20);background:{p['ink']}'></div>"
                 if bg else "")
        return page(f"""{frame}<div class="abs serif" style="left:150px;top:200px;width:930px;color:{p['ink']}">
            <div style="font-size:62px;color:{p['ink_soft']};margin-bottom:38px;line-height:1.1;
              visibility:{'visible' if bg else 'hidden'}">{html.escape(heading)}</div>
            <div style="font-size:48px;line-height:1.18">{lis}</div></div>""", opaque=bg)
    out = {"bg": doc("bg")}
    for i in range(len(bullets)):
        out[f"b{i}"] = doc(f"b{i}")
    return out


def pip_mask():
    x, y, w, h = PIP_BOX
    return page(f"<div class='abs' style='left:0;top:0;width:{w}px;height:{h}px;border-radius:30px;background:#fff'></div>")


def corner_card(text):
    p = PALETTE
    return page(f"""<div class="abs sans" style="right:90px;top:80px;max-width:560px;background:#fff;
      border-radius:18px;padding:26px 32px;font-size:34px;line-height:1.3;color:{p['ink']};
      box-shadow:0 10px 30px rgba(30,20,30,.25)">{_bold(text)}</div>""")


def end_screen_clean():
    """No channel name or logo (none confirmed): Subscribe + 'Watch next' placeholder zone."""
    p = PALETTE
    g = p["end_grad"]
    return page(f"""<div class="abs" style="inset:0;background:linear-gradient({g[0]},{g[1]},{g[2]})"></div>
      <div class="abs serif" style="left:150px;top:300px;font-size:92px;color:{p['ink']};line-height:1.05">
        Thank you<br>for watching</div>
      <div class="abs sans" style="left:150px;top:600px;border:3px solid {p['ink']};border-radius:44px;
        padding:16px 46px;color:{p['ink']};font-size:38px;font-weight:600;letter-spacing:4px">SUBSCRIBE</div>
      <div class="abs" style="left:1000px;top:250px;width:770px;height:433px;border-radius:22px;
        border:3px dashed rgba(255,255,255,.85)"></div>
      <div class="abs script" style="left:1010px;top:150px;font-size:76px;color:#fff">Watch this next</div>""",
                opaque=True)


# ---------------------------------------------------------------------------
# Original illustrated B-roll. Each page exposes window.setT(t) (seconds);
# render_frames() steps it at 30 fps and screenshots every frame.

def _ease(js_t):
    return f"(1-Math.pow(1-Math.min(1,Math.max(0,{js_t})),3))"


def broll_fairytale(dur):
    """'From childhood we have seen movies: Prince Charming will come…' - a film frame
    holding a storybook castle under a night sky. No added words."""
    p = PALETTE
    stars = "".join(f"<circle class='st' cx='{x}' cy='{y}' r='{r}' fill='#FFF4D6' data-p='{ph}'/>"
                    for x, y, r, ph in [(180, 90, 2.4, 0), (320, 160, 1.8, 1.3), (460, 70, 2.2, 2.1),
                                        (900, 110, 2, .6), (1050, 60, 2.6, 1.7), (1240, 150, 1.8, .2),
                                        (1380, 80, 2.2, 2.6), (640, 180, 1.6, 1.1), (1500, 200, 2, .9)])
    holes = "".join(f"<rect x='{40 + i * 110}' y='14' width='54' height='30' rx='6' fill='{p['paper']}' opacity='.85'/>"
                    f"<rect x='{40 + i * 110}' y='786' width='54' height='30' rx='6' fill='{p['paper']}' opacity='.85'/>"
                    for i in range(15))
    castle = f"""
      <g fill='#2B1F2C'>
        <rect x='640' y='430' width='360' height='240'/>
        <rect x='590' y='360' width='90' height='310'/><rect x='960' y='360' width='90' height='310'/>
        <rect x='760' y='300' width='120' height='370'/>
        <polygon points='590,360 635,270 680,360'/><polygon points='960,360 1005,270 1050,360'/>
        <polygon points='760,300 820,190 880,300'/>
        <rect x='600' y='345' width='14' height='18'/><rect x='630' y='345' width='14' height='18'/>
        <rect x='660' y='345' width='14' height='18'/>
        <path d='M790 670 v-70 a30 30 0 0 1 60 0 v70z' fill='#3E2E40'/>
      </g>
      <g fill='{p['highlight']}' opacity='.9'>
        <rect x='805' y='340' width='30' height='40' rx='15'/><rect x='617' y='420' width='26' height='34' rx='13'/>
        <rect x='987' y='420' width='26' height='34' rx='13'/>
      </g>
      <line x1='820' y1='190' x2='820' y2='150' stroke='#2B1F2C' stroke-width='5'/>
      <path id='flag' d='M822 152 q30 8 52 0 l0 26 q-22 8 -52 0z' fill='{p['highlight']}'/>"""
    crown = f"""<g id='crown' transform='translate(1180 250)'>
        <path d='M0 70 L10 10 L45 45 L70 0 L95 45 L130 10 L140 70 Z' fill='{p['highlight']}'/>
        <rect x='0' y='70' width='140' height='18' rx='4' fill='#C9932F'/>
        <circle cx='10' cy='10' r='8' fill='#F6D27A'/><circle cx='70' cy='0' r='9' fill='#F6D27A'/>
        <circle cx='130' cy='10' r='8' fill='#F6D27A'/></g>"""
    return page(f"""
      <div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 35%,#4A3A4E 0%,#2E2232 70%,#241B27 100%)"></div>
      <div id="cam" class="abs" style="left:230px;top:60px;width:1460px;height:739px;transform-origin:50% 50%">
        <svg viewBox="0 0 1640 830" width="1460" height="739" style="border-radius:24px;overflow:hidden;
          box-shadow:0 18px 50px rgba(0,0,0,.45)">
          <defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stop-color="#2E2240"/><stop offset=".6" stop-color="#6E5A86"/>
            <stop offset="1" stop-color="#C9A9B8"/></linearGradient></defs>
          <rect width="1640" height="830" fill="url(#sky)"/>
          <circle cx="1330" cy="190" r="70" fill="#FFF1C9" opacity=".95"/>
          <circle cx="1355" cy="175" r="62" fill="#5E4C76" opacity=".55"/>
          {stars}
          <path d="M0 640 Q300 560 620 640 T1250 630 T1640 600 V830 H0Z" fill="#4A3A55"/>
          {castle}{crown}
          <path d="M0 700 Q400 650 820 700 T1640 690 V830 H0Z" fill="#35283F"/>
          <rect width="1640" height="58" fill="#1E1620"/><rect y="772" width="1640" height="58" fill="#1E1620"/>
          {holes}
        </svg></div>
      <script>
      window.setT = function(t) {{
        const k = t / {dur};
        document.getElementById('cam').style.transform = 'scale(' + (1 + 0.06 * k) + ')';
        document.querySelectorAll('.st').forEach(s => {{
          s.setAttribute('opacity', 0.45 + 0.55 * Math.abs(Math.sin(t * 2.2 + (+s.dataset.p))));
        }});
        document.getElementById('crown').setAttribute('transform',
          'translate(1180 ' + (250 + 10 * Math.sin(t * 1.6)) + ') rotate(' + (4 * Math.sin(t * 1.1)) + ' 70 40)');
        document.getElementById('flag').setAttribute('transform', 'skewY(' + (4 * Math.sin(t * 5)) + ')');
      }};
      </script>""")


def broll_budget(dur):
    """'As a woman, you should know how to handle your finances' - a budget card
    whose bars fill in; rupee amounts left blank (no invented numbers)."""
    p = PALETTE
    rows = [("Income", .92, p["ink"]), ("Expenses", .58, p["accent"]),
            ("Savings", .26, p["highlight"]), ("Investments", .18, "#7E9C8A")]
    bars = "".join(f"""
      <div style="display:flex;align-items:center;margin:0 0 46px 0">
        <div class="serif" style="width:330px;font-size:54px;color:{p['ink']}">{name}</div>
        <div style="flex:1;height:44px;background:#E6DED2;border-radius:22px;overflow:hidden">
          <div class="bar" data-w="{w}" data-d="{i * .35}" style="height:100%;width:0;background:{c};border-radius:22px"></div>
        </div></div>""" for i, (name, w, c) in enumerate(rows))
    return page(f"""
      <div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 35%,#4A3A4E 0%,#2E2232 70%,#241B27 100%)"></div>
      <div id="card" class="abs" style="left:330px;top:70px;width:1260px;height:740px;background:#FFFDF8;
        border-radius:28px;box-shadow:0 22px 60px rgba(0,0,0,.40);padding:60px 86px;box-sizing:border-box">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:50px">
          <div class="hand" style="font-size:96px;color:{p['ink']}">My money</div>
          <div class="serif" style="width:120px;height:120px;border-radius:50%;background:{p['highlight']};
            color:#fff;font-size:80px;display:flex;align-items:center;justify-content:center">&#8377;</div>
        </div>{bars}</div>
      <script>
      window.setT = function(t) {{
        document.querySelectorAll('.bar').forEach(b => {{
          const k = {_ease("(t - 0.25 - (+b.dataset.d)) / 1.1")};
          b.style.width = (100 * (+b.dataset.w) * k) + '%';
        }});
        const c = {_ease("t / 0.5")};
        const card = document.getElementById('card');
        card.style.transform = 'translateY(' + (24 * (1 - c)) + 'px) scale(' + (1 + 0.025 * t / {dur}) + ')';
        card.style.opacity = Math.min(1, 0.2 + c);
      }};
      </script>""")


def render_frames(doc, dur, out_dir, fps=30):
    """Step window.setT through the clip and save PNG frames f00000.png..."""
    from playwright.sync_api import sync_playwright
    os.makedirs(out_dir, exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080})
        pg.set_content(doc)
        pg.evaluate("document.fonts.ready")
        for i in range(int(round(dur * fps))):
            pg.evaluate(f"window.setT({i / fps})")
            pg.screenshot(path=os.path.join(out_dir, f"f{i:05d}.png"))
        b.close()
