#!/usr/bin/env python3
"""Render every graphic the final timeline needs (PNG layers, cards, B-roll frames).

Usage: make_assets.py edl.json gfx_timeline.json OUT_DIR [T0 T1]
(GFX_FONT_DIR for gfx.py; BRAND_FONT_DIR for the opening, reminder and end screen in brand_gfx.py)
With T0/T1 only assets touching that output window are built (test renders).
Writes OUT_DIR/manifest.json describing each asset for render_final.py.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brand_gfx  # noqa: E402
import gfx  # noqa: E402

BROLL = {"fairytale_film": gfx.broll_fairytale, "budget_sheet": gfx.broll_budget,
         "advice_bubbles": gfx.broll_advice_bubbles, "calendar_thirty": gfx.broll_calendar_thirty,
         "phone_scroll": gfx.broll_phone_scroll, "advice_noise": gfx.broll_advice_noise,
         "signpost_choices": gfx.broll_signpost_choices}
CUED = {"advice_bubbles", "calendar_thirty", "phone_scroll", "advice_noise", "signpost_choices"}


def fmt_ts(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def main():
    edl_path, tl_path, out = sys.argv[1:4]
    win = (float(sys.argv[4]), float(sys.argv[5])) if len(sys.argv) > 5 else (0, 1e9)
    edl = json.load(open(edl_path))
    items = json.load(open(tl_path))
    os.makedirs(out, exist_ok=True)
    touch = lambda a, b: a < win[1] and b > win[0]  # noqa: E731
    pages, manifest = {}, {"cards": {}, "items": []}

    # full-frame cards from the EDL
    titles = [c for c in edl["timeline"] if c["type"] == "card" and c["name"].startswith("title_")]
    for c in edl["timeline"]:
        if c["type"] != "card" or not touch(c["out_start"], c["out_start"] + c["dur"]):
            continue
        if c["name"].startswith("title_"):
            pages[c["name"]] = gfx.title_card(int(c["name"][-1]), c["title"])
        elif c["name"] == "chapter_menu":
            pages[c["name"]] = gfx.chapter_menu(["5 lessons I learned", "in my twenties"],
                                                [(t["title"], fmt_ts(t["out_start"])) for t in titles])
        elif c["name"] == "end_screen":
            # animated Champagne Editorial outro (frames, opaque); BRAND_FONT_DIR must be set
            d = os.path.join(out, "end_screen_frames")
            brand_gfx.render_frames(brand_gfx.CF_end(), c["dur"], d, alpha=False)
            manifest.setdefault("card_frames", {})[c["name"]] = os.path.join(d, "f%05d.png")
            continue
        manifest["cards"][c["name"]] = os.path.join(out, c["name"] + ".png")

    for it in items:
        if not touch(it["t0"], it["t1"]):
            continue
        m = {"id": it["id"], "type": it["type"], "t0": it["t0"], "t1": it["t1"], "layers": []}
        if it["type"] == "notes":
            for name, doc in gfx.notes_layers(it["heading"], [x["text"] for x in it["items"]]).items():
                pages[f"{it['id']}_{name}"] = doc
            m["layers"].append({"png": f"{it['id']}_head.png", "t": it["t0"]})
            m["layers"] += [{"png": f"{it['id']}_item{i}.png", "t": x["t"]} for i, x in enumerate(it["items"])]
        elif it["type"] == "keywords":
            for i, x in enumerate(it["items"]):
                pages[f"{it['id']}_{i}"] = gfx.keyword_layer(x["text"], *x["xy"])
                m["layers"].append({"png": f"{it['id']}_{i}.png", "t": x["t"], "t_end": x["t"] + 2.0})
        elif it["type"] == "pullquote":
            pages[it["id"]] = gfx.quote_layer(it["text"])
            m["layers"].append({"png": f"{it['id']}.png", "t": it["t0"]})
        elif it["type"] == "pip":
            for name, doc in gfx.pip_layers(it["heading"], [x["text"] for x in it["bullets"]]).items():
                pages[f"{it['id']}_{name}"] = doc
            pages["pip_mask"] = gfx.pip_mask()
            m["layers"].append({"png": f"{it['id']}_bg.png", "t": it["t0"]})
            m["layers"] += [{"png": f"{it['id']}_b{i}.png", "t": x["t"]} for i, x in enumerate(it["bullets"])]
            m["pip_box"] = gfx.PIP_BOX
        elif it["type"] == "corner_card":
            pages[it["id"]] = gfx.corner_card(it["text"])
            m["layers"].append({"png": f"{it['id']}.png", "t": it["t0"]})
        elif it["type"] == "anim":
            make, _ = brand_gfx.ANIM[it["asset"]]
            d = os.path.join(out, f"{it['id']}_frames")
            brand_gfx.render_frames(make(), it["t1"] - it["t0"], d, alpha=True)
            m["frames"] = os.path.join(d, "f%05d.png")
        elif it["type"] == "broll":
            if it["asset"] not in BROLL:
                print(f"MISSING B-roll asset '{it['asset']}' for {it['id']} - not built")
                continue
            d = os.path.join(out, f"{it['id']}_frames")
            dur = it["t1"] - it["t0"]
            doc = BROLL[it["asset"]](dur, it["cues"]) if it["asset"] in CUED else BROLL[it["asset"]](dur)
            gfx.render_frames(doc, dur, d)
            m["frames"] = os.path.join(d, "f%05d.png")
        manifest["items"].append(m)

    gfx.render(pages, out)
    for m in manifest["items"]:
        for layer in m["layers"]:
            layer["png"] = os.path.join(out, layer["png"])
    manifest["pip_mask"] = os.path.join(out, "pip_mask.png")
    json.dump(manifest, open(os.path.join(out, "manifest.json"), "w"), indent=1)
    print(f"{len(pages)} graphics pages, {sum(1 for m in manifest['items'] if 'frames' in m)} animated clips")


if __name__ == "__main__":
    main()
