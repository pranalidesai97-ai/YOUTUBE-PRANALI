#!/usr/bin/env python3
"""Quick 540p review cut of the EDL (cuts + review captions + placeholder slates).

Not the final render: no audio clean-up, no graphics, fast low-quality encode.
Each EDL item is rendered on its own (accurate seek, exact frame count) and the
pieces are joined with the concat demuxer, so memory stays flat.
Usage: render_review.py SOURCE edl.json captions.srt FONT_DIR OUT.mp4
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

FPS = 30
FADE = 0.012
VENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p", "-r", str(FPS)]


def ff(args):
    subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-v", "error", "-y", *args], check=True)


def render_item(n, it, src, font_dir, work):
    out = os.path.join(work, f"v{n:04d}.mp4")
    if it["type"] == "src":
        frames = round((it["out"] - it["in"]) * FPS)
        ff(["-ss", f"{it['in']:.4f}", "-i", src, "-map", "0:v:0", "-vf", "scale=960:540,fps=30",
            "-frames:v", str(frames), *VENC, "-an", out])
    else:
        label = it.get("title") or it["name"].replace("_", " ")
        if it["name"].startswith("title_"):
            label = f"{it['name'][-1]}. {label}"
        label = label.replace("'", "’").replace(":", "\\:")
        ff(["-f", "lavfi", "-i", f"color=c=0xF4EFE6:s=960x540:r={FPS}:d={it['dur']}",
            "-vf", f"drawtext=fontfile={font_dir}/InstrumentSerif-Regular.ttf:text='{label}':"
                   "fontcolor=0x3A2A3B:fontsize=44:x=(w-tw)/2:y=(h-th)/2",
            "-frames:v", str(round(it["dur"] * FPS)), *VENC, out])
    return out


def main():
    src, edl_path, srt, font_dir, out = sys.argv[1:6]
    tl = json.load(open(edl_path))["timeline"]
    work = out + ".parts"
    os.makedirs(work, exist_ok=True)

    with ThreadPoolExecutor(max_workers=3) as ex:
        parts = list(ex.map(lambda p: render_item(p[0], p[1], src, font_dir, work), enumerate(tl)))
    lst = os.path.join(work, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))

    # audio: one light audio-only graph (cards get silence)
    g = []
    for n, it in enumerate(tl):
        if it["type"] == "src":
            a, b = it["in"], it["out"]
            d = b - a
            f = min(FADE, d / 4)
            g.append(f"[0:a:0]atrim=start={a:.4f}:end={b:.4f},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d={f:.4f},afade=t=out:st={d - f:.4f}:d={f:.4f}[a{n}];")
        else:
            g.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={it['dur']}[a{n}];")
    g.append("".join(f"[a{n}]" for n in range(len(tl))) + f"concat=n={len(tl)}:v=0:a=1[aout]")
    gp = os.path.join(work, "audio.txt")
    open(gp, "w").write("\n".join(g))
    wav = os.path.join(work, "audio.wav")
    ff(["-vn", "-i", src, "-filter_complex_script", gp, "-map", "[aout]", "-c:a", "pcm_s16le", wav])

    style = ("FontName=Poppins Medium,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H66000000,"
             "BorderStyle=1,Outline=0.6,Shadow=0.8,Alignment=2,MarginV=30")
    ff(["-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
        "-vf", f"subtitles=filename={srt}:fontsdir={font_dir}:force_style='{style}'",
        "-map", "0:v", "-map", "1:a", *VENC, "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out])


if __name__ == "__main__":
    main()
