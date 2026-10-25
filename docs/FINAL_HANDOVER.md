# Final handover: "5 Life Lessons I Wish I Knew Earlier"

The talking-head edit is finished. The opening/Subscribe/end-screen redesign is waiting on the creator's choices.
Everything below was verified on 2026-10-24 (checksums re-read, files listed, data re-built and compared byte for byte).
No video was rendered, overwritten, deleted or uploaded while this handover was written.

---

## 1. Ground rules from the creator (still in force)

The creator's instructions, quoted:

- "Do not modify, overwrite or delete the original file."
- "Do not upload the footage to an external service without my permission." / "do not upload the footage to GitHub or another external website"
- "Do not use paid services or consume credits without asking me first."
- "Do not publish or share the video."
- "Do not speed up the speaker's voice or alter playback speed."
- "Keep the current final export safe and don't upload my video externally."
- "The existing five lesson title cards, captions, approved cuts, B-roll and audio are already approved; don't redesign or alter them without asking me first."
- "Do not invent a creator name; confirm it with me before displaying it."
  - The creator has now given it: **Pranali Desai**, handle **@heyPranali**. Use exactly these spellings.
- Captions: never guess uncertain speech; ask.
- Always make a short test before a full render, and wait for approval.

Working practice:

- No video files go into git.
- QC contact sheets with stills are already committed; keep them small.
- Videos reach the creator only through in-session file cards.
  - The limit is about 400 MiB per file.
  - The 720p previews play on the creator's tablet.

---

## 2. Where everything is

| What | Location |
|---|---|
| Repository | `https://github.com/pranalidesai97-ai/YOUTUBE-PRANALI`, cloned at `/home/user/YOUTUBE-PRANALI` |
| Working branch | `claude/talking-head-video-edit-djp9i3`. Develop and push only here. No PR has been opened. |
| Last commit before this handover | `2b06f2e` Design system for opening title, Subscribe reminder and end screen (3 directions) |
| Media working folder (**ephemeral**) | `/tmp/claude-0/-home-user-YOUTUBE-PRANALI/286ac342-9da4-571b-b536-e601329738e9/scratchpad`, called `$S` below. This belongs to the old session's container. **A new session will not have it.** |

### Source (original footage): unchanged

- **Path:** `$S/src/source_original.mp4`, read-only (`-r--r--r--`).
- **Size:** 2,852,623,060 bytes.
- **SHA-256:** `8608c56f854c28db05e3719eb3698767945d1f0ca7d6340b66c0dc13595d980c`. Re-verified today: matches the download.
- **Format:** HEVC (`hvc1`) 1920×1080, about 30 fps but variable frame rate (avg 29.997); AAC audio; plus two `mett` metadata tracks.
- **Duration:** 987.0 s (16:27.0).
- **Where it comes from:** the creator's Google Drive, file id `1NQAYdsSO12AwiJ4y2TmqecT_eLVoAnot`.
  - It was fetched with `curl` from `https://drive.usercontent.google.com/download?id=<ID>&export=download`, keeping cookies and confirming the large-file warning.
  - The environment's network policy had to allow `drive.usercontent.google.com`; the creator allowed it once.
  - The original was never written to.

### Final export: one MP4, delivered to the creator in two parts

| File (all in `$S/final/`) | Bytes | SHA-256 |
|---|---|---|
| `Lessons_from_my_twenties_FINAL_1080p30.mp4` (**the master, one file**) | 498,491,992 (475 MiB) | `22764d28c19a6b2c2d3868f7d82129307a77d49dbc60ef85b9fb791b9b3d5887` |
| `parts/Lessons_FINAL_1080p30_part1of2.mp4` (0:00–5:27.8) | 244,463,628 | `2b256c4379d8f9aaf7de4f605323d3e46729ff3a97ee6ac354411477b5c8f5f2` |
| `parts/Lessons_FINAL_1080p30_part2of2.mp4` (5:27.8–10:52.6) | 254,029,824 | `5e5464530b6a4c43bc4827d6a854622a53a3415000ef663849a1520872a30700` |
| `Lessons_from_my_twenties_720p_preview.mp4` (viewing copy only) | 83,160,035 | `eb2c84cf759b530028776d2b0949bfd9c4a9395823babc36e09ddc57f597bef7` |

**Master specs** (ffprobe and `docs/FINAL_QC_REPORT.md`):

- **Video:** H.264 High, yuv420p, BT.709, 1920×1080, 16:9, **30/1 constant frame rate**, **19,577 frames**, 652.567 s (**10:52.6**). Encoded with x264 CRF 16, preset slow, keyframe every 60 frames; about 5.85 Mb/s.
- **Audio:** AAC-LC, 48 kHz stereo, 256 kb/s target (252 kb/s measured), 652.566 s.
- **Container:** faststart (`moov` before `mdat`).

**Delivery status:**

- The single master file **could not be sent**, because the in-session file limit is about 400 MiB.
- The creator received:
  - **part 1 and part 2**, joined with stream copy, where video is bit-identical to the master and the audio is 2 AAC frames (about 43 ms) short at the split;
  - the **720p preview**;
  - `FINAL_captions.srt`, `FINAL_cut_list.csv`, `ASSETS_AND_LICENSES.md` and `FINAL_QC_REPORT.md`.
- The single 1080p master exists only in `$S`. When the old container is reclaimed, it is gone. It can be rebuilt exactly as described in section 7: equivalent output, though x264 may not be byte-identical.

**QC status: passed.** See `docs/FINAL_QC_REPORT.md`, `docs/FINAL_qc_report.json` and the `docs/FINAL_qc_*.jpg/png` sheets.

- 0 decode errors and no black frames. The only stills are the cards and the intended illustration holds in B5/B7.
- Loudness −16.0 LUFS integrated, LRA 4.3 LU, true peak −1.5 dBTP; no dropouts.
- Audio sync 0.0–±0.5 ms at 12 points; picture within ±1 frame (the resolution of that measurement).
- All 5 Devanagari cues render correctly.

---

## 3. What is approved and locked (don't change without asking)

### Cuts

- **Spec:** `docs/stage2_cuts.json` (29 removals) produces `docs/stage2_edl.json`.
  - The human-readable list is `docs/FINAL_cut_list.csv`: pre-roll, retakes and every tightened pause, in source timestamps.
- **Removed:** `R2 R3+R4 R5 R7 R9 R10 R11 R13 F1 R16 R17 F2 R18 R19 R21 R22 R23 R24 R26 R27 R28 R29 R30 R32 R33 R34 R12a R20 R31`.
- **Kept on the creator's decision:** R6, R8, R14, R15, R25.
  - R12: only the off-camera exchange was removed.
  - R20 was removed as a redundant repeat; R31 was tightened.
- **Pauses:** only pauses over 0.35 s were tightened, to 0.20 s mid-sentence and 0.30 s at sentence ends (a 1.5× breath is kept after a sentence end).
  - Silero VAD guards every cut; 12 ms micro-fades at each cut.
  - The edit starts with the original opening line ("Hi everyone, welcome to my channel").
- **Audio repair:** a bell-like "ting" at source 253.12–253.39 s is attenuated (gain 0.03, about −30 dB), with no timing change. It is in `audio_repairs` in the cuts file.
- **Speed:** no speed change anywhere.
- **Jump cuts:** the 16 most visible jump cuts (`docs/data/jarring_cuts.json`) get a gentle 106% punch-in centred on the face.

### Timeline

| Output time | Item |
|---|---|
| 0:00 | Original opening line |
| 1:03.87 | Chapter menu (6 s) |
| 1:09.87 | Title 1 "Don't Wait to Be Rescued" (3 s) |
| 3:43.57 | Title 2 "Take Control of Your Finances" |
| 4:45.07 | Title 3 "Find Your Happiness and a Creative Outlet" |
| 6:29.97 | Title 4 "Know Yourself" |
| 7:55.13 | Title 5 "Learn to Make Your Own Decisions" |
| 10:42.57–10:52.57 | Current clean end screen (10 s, no channel name) |

Overlays, from `docs/stage2_gfx_timeline.json`, which is generated from the phrase-anchored plan in `docs/stage2_graphics.json`:

- **Keyword labels:**
  - KW1 0:26 (relationships, finances, mental health, physical health)
  - KW2 5:25 (crocheting … journaling)
- **B-roll:** B1 0:36, B2 0:48, B3 2:33, B4 3:53, B5 4:54 (phone), B6 6:33, B7 8:37 (signpost).
  - All are original illustrated pages on a dark plum backdrop, so the captions stay legible.
- **Pull-quotes:** PQ1 2:10, PQ2 3:14, PQ3 4:03, PQ4 5:09, PQ5 7:17, PQ6 10:18, PQ7 10:32, PQ7b 10:35. Wording is approved.
- **Notes overlays:** NO1 2:43, NO2 4:21, NO3 7:28.
- **Picture-in-picture:** PIP1 5:59 "Write it down" and PIP2 9:26 "Decisions build confidence". `PIP_BOX` = (1180,110,620,826).
- **Corner card:** CC1 9:53 "Want a video on decision making? Comment below".

### Captions

- **Files:** `docs/FINAL_captions.srt`, 317 cues, UTF-8.
- **Style:** clean verbatim. Fillers and cut-off fragments are dropped; "hi" is kept; "20s" is spelled "twenties".
- **Hindi:** Hindi lines are written in **Devanagari**, set in `docs/stage2_caption_overrides.json`. The 5 Hindi cues are burned in with libass `shaping=complex`.
- **Review:** all flagged words were resolved with the creator over 4 rounds (`docs/stage2_caption_flags_review.md`).
- **Burn-in:** captions are burned into the video. The same SRT can also be uploaded to YouTube.

### Graphics style

The current lesson cards, overlays and B-roll come from `tools/gfx.py`.

- **Fonts:** Instrument Serif, Poppins, Great Vibes and Noto Sans Devanagari.
- **Colours:** a warm plum/rose palette.
- **Status:** approved. The redesign below must not touch them.

### Music, SFX and mix

All original and generated locally; see `docs/ASSETS_AND_LICENSES.md`.

- **Music:** `compose_music.py 660 out.wav 7`, v2. The chime-like notes of v1 are removed. It sits at −14 dB relative to its −16 LUFS render, about 18 dB under the voice. It is ducked with `sidechaincompress` (threshold 0.015, ratio 6, attack 40 ms, release 450 ms), fades in over 1.5 s and out over the last 3 s.
- **SFX:** pop −30 dB, swish −27 dB, swell −29 dB, used sparingly on cards and inserts.
- **Dialogue chain:**
  - highpass 70 Hz
  - `afftdn nr=10 nf=-67` (1200-sample latency compensated)
  - `adeclick`
  - EQ −1.5 dB @ 250 Hz, +1.5 dB @ 3.5 kHz
  - 2:1 compressor (threshold −22 dB)
  - two-pass `loudnorm` to −16 LUFS / −1.5 dBTP
- **Room tone:** 3 s from source 274.5 s, filling the cards.

---

## 4. The redesign: opening title, Subscribe reminder and end screen (open)

### Visual direction requested

Elegant, aesthetic, Pinterest/editorial-inspired.

- **Palette:** warm ivory, dusty rose, plum, sage and champagne gold.
- **Type:** sophisticated serif typography.
- **Decoration:** delicate botanical illustrations, tasteful stickers and paper textures.
- **Motion:** restrained.
- **Avoid:** anything basic, childish or funky.

### Three directions

The design system is `tools/brand_gfx.py`; its palette is the `C` dict.

| | Name | Fonts | Opening | Reminder | End screen |
|---|---|---|---|---|---|
| **A** | Pressed Garden | Cormorant Garamond + Manrope | Torn-edge ivory card, double gold border, watercolour garden-rose bouquets, gold "5" | Paper luggage tag on a gold string | Ivory paper, corner bouquets, "Watch next" on a rose mat with washi tape |
| **B** | Scrapbook Journal | Playfair Display + Montserrat | Torn notebook page on rose paper, circled gold "5", "note to self" sticker, doodled stars | Torn notebook strip with heart sticker | Collage board, "Watch next" in a snapshot frame |
| **C** | Champagne Editorial | Playfair Display + Montserrat (+ Cormorant) | Thin gold frame, ivory haze over the wall (not the face), fine-line gold florals | Ivory pill with rose wax seal | Deep plum, gold frames, sage ribbon |

All artwork is original SVG, drawn in code; no stock images were used. All fonts are SIL OFL.

### Preview files

These are **not in the repo**, because the opening and reminder previews contain stills of the footage. They live in `$S/design/out/`:

- `A_opening.png`, `A_reminder.png`, `A_end.png`, `A_end_guides.png`, and the same four files for `B_*` and `C_*`;
- `A_board.jpg`, `B_board.jpg` and `C_board.jpg`: the three boards sent to the creator, each with 4 panels;
- `phone_size_check.jpg`.

The backgrounds are frames from the master: `$S/design/bg_opening.jpg` at 2.2 s and `$S/design/bg_reminder.jpg` at 91 s.

To regenerate the previews (stills only, no video):

```bash
ffmpeg -ss 2.2 -i FINAL.mp4 -frames:v 1 -q:v 2 design/bg_opening.jpg
ffmpeg -ss 91  -i FINAL.mp4 -frames:v 1 -q:v 2 design/bg_reminder.jpg
cd tools && BRAND_FONT_DIR=$FONTS/brand python3 - <<'EOF'
import brand_gfx as b
pages = {}
for k, (name, op, rem, end) in b.DIRECTIONS.items():
    pages[f"{k}_opening"] = op(bg="../design/bg_opening.jpg")
    pages[f"{k}_reminder"] = rem(bg="../design/bg_reminder.jpg")
    pages[f"{k}_end"] = end()
    pages[f"{k}_end_guides"] = end(guides=True)
b.render(pages, "../design/out")   # prints "fonts loaded N/N" per page; all must load
EOF
```

The boards are 2×2 montages of those four PNGs.

### Plan for each piece

Proposed to the creator, not yet confirmed.

**Opening title**
- **When:** 0:00–0:04, over the first spoken line ("Hi everyone, welcome to my channel").
- **Where:** on the empty wall to the right of the face; never over the face or the captions.
- **Text:** "5 Life Lessons / I Wish I Knew Earlier", subtitle "A little wisdom for a more independent life".
- **Motion:** gentle fade and drift in, a few pixels; out by 0:04.

**Subscribe reminder**
- **When:** shown once, about 5 s, near 1:30, top right.
- **Fit:** it must not overlap any graphic. Nearest are the chapter menu and title 1 (ending at 1:12.9) and the gap before PQ1 at 2:09.9, so the window is clear.
- **Style:** subtle, no bounce, no flashing.

**End screen (outro)**
- **Length:** 15–20 s; 18 s is proposed, replacing the current 10 s card. YouTube allows 5–20 s. The video becomes about 8 s longer (10:52.6 → about 11:00.6).
- **Closing line:** "Until next time, be confident, be bold, and keep choosing yourself." This is based on the creator's own closing words and needs approval.
- **Keep clear for YouTube's real end-screen elements,** which are added in YouTube Studio and never baked in:
  - "Video" element `WATCH_BOX` = (x 1030, y 250, w 760, h 428), 16:9;
  - "Subscribe" circle `SUB_CIRCLE` = centre (430, 812), radius 104.
- **Check:** the `*_end_guides.png` previews show these zones as dashed boxes. The guides are preview-only.

### Decisions still needed from the creator

1. **Direction:** A, B or C, or a mix (e.g. A's opening with C's end screen).
2. **Creator name:** "Pranali Desai" and "@heyPranali" are now confirmed by the creator. Nothing in the current previews shows them yet; ask *where* they should appear, for example under the opening title, on the reminder ("Subscribe to @heyPranali") or on the end screen.
3. **Decorative wording** (written by Claude, not yet approved): "with love & gratitude", "a little series", "note to self", "for more gentle lessons", "for more life lessons", and the closing line above. Keep, change or remove each one.
4. **Timings:** confirm opening 0:00–0:04, the reminder once at about 1:30 top-right for about 5 s, and an 18 s end screen.
5. **Polish already planned:** make the smallest labels (17–20 px) one step larger, since the phone-size check showed they are borderline.

---

## 5. Other open questions

- **Single-file 1080p delivery:** the master (475 MiB) is over the 400 MiB card limit. Options for the creator:
  - (a) keep the two parts and join them locally;
  - (b) approve a CRF 18 re-encode under 400 MiB (a second generation, slightly softer);
  - (c) permit another delivery route they choose.

  Uploading anywhere needs their explicit permission.
- **Optional caption tweak:** the "oh" at 1:59; the caption currently reads "Which never happens."
- **Optional graphics tweak:** PQ3 wraps "life." onto its own line.
- **Re-checks:** after the redesign, re-run QC, including the 19,577-frame count, which will change by the extra end-screen length.

---

## 6. Tools (all in `tools/`)

| Script | Purpose |
|---|---|
| `clean_talking_head.py`, `qc_check.sh` | Stage 1 (pause removal + audio chain), kept for reference |
| `transcribe.py SOURCE MODEL_DIR OUT.json` | Parakeet TDT 0.6B v2 word timestamps (sherpa-onnx, local) |
| `whisper_bytes.py` | Whisper decoding with correct UTF-8 (Devanagari) |
| `asr_crosscheck.py tr.json whisper.json OUT.json` | Flags words the two recognisers disagree on |
| `build_edl.py SOURCE tr.json docs/stage2_cuts.json OUT_DIR` | Writes `edl.json` and `cuts.csv` (reads source audio only) |
| `make_captions.py tr.json edl.json overrides.json,flags.json OUT_DIR` | `captions.srt` and the review SRT/CSV |
| `plan_graphics.py tr.json edl.json docs/stage2_graphics.json OUT.json` | Graphics timeline |
| `score_jumps.py SOURCE edl.json OUT.json` | Jump-cut punch-in list |
| `gfx.py`, `make_assets.py edl.json gfx_timeline.json OUT_DIR [T0 T1]` | Approved cards, overlays and B-roll (`GFX_FONT_DIR`) |
| `brand_gfx.py` | Redesign system (`BRAND_FONT_DIR`); not yet wired into the render |
| `compose_music.py`, `make_sfx.py` | Original music and SFX |
| `render_final.py SOURCE edl gfx manifest srt jarring audio_dir font_ttf_dir OUT.mp4 [T0 T1]` | Chunked final render; `RERENDER=i,j` re-renders only those chunks |
| `qc_final.py FINAL SOURCE edl gfx srt OUT_DIR` | Full QC + contact sheets |
| `setup_fonts.sh DIR` | Rebuilds every font, from npm `@fontsource/*@5.3.0` |
| `setup_audio.sh SOURCE OUT_DIR` | Rebuilds music, SFX and room tone |

**Saved data:** `docs/data/` holds the recogniser outputs, so nothing needs re-transcribing:

- `transcript_parakeet.json`
- `whisper_smallen_crosscheck.json`
- `jarring_cuts.json`

**Reproducibility checked today:**

- From the repo data plus the source, `build_edl`, `asr_crosscheck`, `make_captions` and `plan_graphics` reproduce `docs/stage2_edl.json`, `docs/FINAL_captions.srt` and `docs/stage2_gfx_timeline.json` **byte for byte**.
- `setup_audio.sh` reproduces the music, SFX and room tone byte for byte.
- `setup_fonts.sh` reproduces the fonts. The only difference is the timestamp in the `head` table; glyphs and every other table are identical.

---

## 7. Rebuilding in a new session

```bash
# 0. tools: ffmpeg 6.1 with libass+harfbuzz, Chromium + Playwright (preinstalled)
pip install --no-deps silero-vad onnxruntime
pip install sherpa-onnx kaldi-native-fbank scipy fonttools brotli opencv-python-headless
cd /home/user/YOUTUBE-PRANALI && git checkout claude/talking-head-video-edit-djp9i3
S=<new scratchpad>
#    (sherpa-onnx models only needed for re-transcribing, from
#     github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/
#     sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8, sherpa-onnx-whisper-small.en|medium|turbo)

# 1. source: re-download from Drive (needs the creator's OK for drive.usercontent.google.com
#    in the network policy). Check the checksum, then make it read-only.
echo "8608c56f854c28db05e3719eb3698767945d1f0ca7d6340b66c0dc13595d980c  $S/src/source_original.mp4" | sha256sum -c
chmod 444 $S/src/source_original.mp4

# 2. fonts + audio inputs
bash tools/setup_fonts.sh $S/fonts
bash tools/setup_audio.sh $S/src/source_original.mp4 $S/stage2/audio

# 3. timeline data
mkdir -p $S/stage2
python3 tools/build_edl.py $S/src/source_original.mp4 docs/data/transcript_parakeet.json docs/stage2_cuts.json $S/stage2
python3 tools/asr_crosscheck.py docs/data/transcript_parakeet.json docs/data/whisper_smallen_crosscheck.json $S/stage2/asr_flags.json
python3 tools/make_captions.py docs/data/transcript_parakeet.json $S/stage2/edl.json docs/stage2_caption_overrides.json,$S/stage2/asr_flags.json $S/stage2
python3 tools/plan_graphics.py docs/data/transcript_parakeet.json $S/stage2/edl.json docs/stage2_graphics.json $S/stage2/gfx_timeline.json
cp docs/data/jarring_cuts.json $S/stage2/   # or: python3 tools/score_jumps.py SOURCE edl.json OUT.json

# 4. graphics assets
GFX_FONT_DIR=$S/fonts python3 tools/make_assets.py $S/stage2/edl.json $S/stage2/gfx_timeline.json $S/stage2/assets_final

# 5. render. ALWAYS do a short test window first (T0 T1 in output seconds) and get approval
python3 tools/render_final.py $S/src/source_original.mp4 $S/stage2/edl.json $S/stage2/gfx_timeline.json \
  $S/stage2/assets_final/manifest.json $S/stage2/captions.srt $S/stage2/jarring_cuts.json $S/stage2/audio \
  $S/fonts/ttf $S/final/OUT.mp4 [T0 T1]

# 6. QC
python3 tools/qc_final.py $S/final/OUT.mp4 $S/src/source_original.mp4 $S/stage2/edl.json \
  $S/stage2/gfx_timeline.json $S/stage2/captions.srt $S/final/qc
```

**Notes:**

- The full render is CPU-heavy: about 22 chunks of 30 s each.
- The render writes `OUT.mp4.work/`, so check disk space first.
- Never use `-shortest` when joining; the renderer already avoids it.
- To split for delivery, use the **segment muxer** with stream copy (`-map 0 -c copy -f segment -segment_times 325.766667 -reset_timestamps 1`). It cuts at the next keyframe, which is how the parts split at 5:27.8. A time-based `-ss/-t` split duplicates frames.

---

## 8. Exact remaining steps

1. **Get the creator's answers** to section 4 ("Decisions still needed") and section 5.
2. **Rebuild the working set** (section 7, steps 1–4). This needs the source re-downloaded with the creator's permission for Drive access.
3. **Apply the design.** Revise `brand_gfx.py` for the chosen direction and wording, add the name/handle where approved, and enlarge the small labels.
4. **Animate the design.** Build animated layers for the opening, reminder and end screen: frame sequences or a PNG with alpha. Use restrained motion: fade, a few pixels of drift, washi/sticker settle, gold line draw-on, slow sparkle.
5. **Wire it into the pipeline.**
   - Add the opening and reminder as overlay items in `docs/stage2_graphics.json`. Anchors: the opening line at 0:00; the reminder near 1:30, clear of other graphics.
   - Replace the `end_screen` insert (currently 10 s, `gfx.end_screen_clean`) with the new 18 s outro in `docs/stage2_cuts.json` `inserts`.
   - Extend room tone and the music tail. The music file is exactly 660.0 s, which is **shorter** than the new output (about 660.6 s). Regenerate it longer, e.g. `compose_music.py 680 music_full.wav 7`, and check by ear that the bed under the approved part still sounds the same, because the length may change the arrangement. Otherwise loop or pad the tail.
6. **Leave everything else alone:** cuts, captions, lesson cards, B-roll and audio levels.
7. **Test render** of 0:00–0:12, about 1:25–1:40 and the last about 25 s. Send 720p previews and wait for approval.
8. **Full render** to a **new filename**, e.g. `Lessons_from_my_twenties_FINAL_v2_1080p30.mp4`. Never overwrite the current master.
9. **Run `qc_final.py`** and update `docs/FINAL_QC_REPORT.md`. Expect about 19,817 frames for an 18 s end screen; confirm the exact number from the EDL.
10. **Deliver as before:** 720p preview plus 1080p parts under 400 MiB, or the single-file route the creator chose.
11. **Commit** docs and tools (no video) and push to `claude/talking-head-video-edit-djp9i3`.
12. **In YouTube Studio** (creator's job): add the end-screen "Video" and "Subscribe" elements over the reserved zones. Optionally upload `FINAL_captions.srt` as a caption track.

---

## 9. Status update (session 2, 2026-10-24)

- Creator chose **C, Champagne Editorial**, with this wording: title "5 Life Lessons I Wish I Knew Earlier", subtitle "Things I wish someone had told me in my twenties.", "Pranali Desai" + "@heyPranali" on the opening; "A little series" removed; reminder "Subscribe for more life lessons"; end screen "with love & gratitude", "Thank you for watching", closing line approved, small "note to self" label. The "oh" at 1:59 stays unchanged. PQ3 now breaks after "for you".
- Built: `brand_gfx.CF_opening/CF_reminder/CF_end` (animated, `window.setT`), `brand_gfx.render_frames`; overlay type `anim` (alpha frame sequence) and animated cards (`card_frames`) in `make_assets.py`/`render_final.py`; music padded with silence past the approved 660 s file (`apad`), so the bed under the approved edit is unchanged.
- Timeline: OPEN 0:00–0:05, SUB 1:29.48–1:34.28, end screen 18 s from 10:42.57. New duration 660.567 s = **19,817 frames**. EDL, captions and every other graphic are identical to the approved version (verified by diff).
- Previews approved; "@heyPranali" added under Subscribe on the end screen. Full v2 master rendered and QC passed (see `docs/FINAL_QC_REPORT.md`, v2 section). Delivered as two byte-exact pieces (.001/.002) + SHA-256 + join instructions, and a 720p preview. The v1 master and the source were never modified.
- The 43 ms gap only existed between the two delivery parts (segment split at 5:27.8). The new master is rendered as one file with one continuous audio track.

- **Opening revised (requested 2026-10-25):** the title is now a contained side panel (no full-frame border or veil) shown 0:06.53–0:12.03, while the speaker says "Hi everyone, welcome to my channel"; 0:00–0:06.5 is footage only. `render_final.py` no longer lets `anim` overlays cancel a jump-cut punch-in, so the approved 106 % framing at 0:06.4 is kept. Approved; **v3 master rendered, QC passed and delivered** (see `docs/FINAL_QC_REPORT.md`, v3 section). v3 is the current final. The v2 master and the source were not modified.
- **End screen revised (requested 2026-10-25):** the "watch next" box and ribbon are replaced by an arched ivory "Your next chapter / More life lessons soon" panel (`NEXT_ARCH`), with gold borders, fine-line sprigs and rose blooms. It is decorative, not a video slot; only the Subscribe circle (`SUB_CIRCLE`) is reserved. Approved; **v4 master rendered (only the end-screen chunk changed), QC passed and delivered** — see `docs/FINAL_QC_REPORT.md`, v4 section. v4 is the current final; v3, v2 and the source were not modified. Note: YouTube end screens normally need at least one video or playlist element, so a Subscribe-only end screen may not be accepted in Studio; the channel watermark gives a clickable Subscribe instead. YouTube title, description and chapters: `docs/YOUTUBE_UPLOAD.md`.
