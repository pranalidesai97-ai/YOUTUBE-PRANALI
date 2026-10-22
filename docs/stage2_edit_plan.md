# Stage 2 edit plan: "Lessons from my twenties"

Status: **proposal, waiting for approval. Nothing has been rendered.**
Style guide: the reference editing-style specification you supplied (pasted in chat; there was no
`reference_editing_spec.md` file in the repo or session).

All timestamps are **source** times in the original file (`m:ss`, about ±0.3 s). Final output times
get calculated after the cuts are approved.

---

## 1. Source check

| Item | Value |
|---|---|
| File | Original phone recording from Google Drive (2.85 GB). Checksum verified, read-only, never modified |
| Duration | **16:27.0** (987.0 s) |
| Video | HEVC Main, **1920×1080**, 16:9, yuv420p, BT.709 limited range, 30 fps nominal (avg 29.998, near-CFR), ≈22 Mb/s |
| Audio | AAC-LC stereo, 48 kHz, 256 kb/s; speech peaks ≈ −13 dBFS, very low noise floor (≈ −67 dBFS) |
| Framing | Locked-off camera. Face centre x ≈ 47 %, y ≈ 35 %; face height ≈ 27 % of frame (wider than the reference's ≈40 %). Busy desk/shelf/lamp on the left; **empty ivory wall on the right third** |
| Set palette | Ivory wall, deep-plum top, brass lamp glow, white marble desk |
| Language | English, with two short Hindi/Hinglish passages (2:40, 4:15) |

**"Cleaned source video":** a full stage-1 render was never made. Only the 90 s test section
(3:00–4:30) was rendered and sent for review. I recommend **not** rendering stage 1 on its own:
stage 2 will render once, straight from the original, applying the stage-1 audio clean-up, the cuts
and all graphics in a single encode. That gives one generation of compression instead of two.

Output keeps the source **1920×1080, 16:9, 30 fps**. The reference's 256×144 resolution is ignored.

---

## 2. Global decisions, including where this edit departs from the reference

| Topic | Reference | Proposal for your video | Why |
|---|---|---|---|
| Pauses | Every gap cut to 0.10–0.25 s | Gaps trimmed to **≈0.18 s mid-sentence, ≈0.30 s at sentence ends**. **Needs your OK**, because stage 1 used 0.5 s | The approved style is tight. Runtime barely changes (≈9.3 vs 9.6 min of speech); the feel does |
| Pace | ≈216 wpm | ≈150–155 wpm (your natural rate) | Reaching 216 needs a speed-up, which stage 1 ruled out |
| Retakes | Best take only | **Removed only after you approve the list in Section 4** | As you asked |
| Fillers ("uh", "um", "okay") | Mostly removed | Remove the 34 standalone ones that sit between phrases; keep any welded inside a word | Removing those is safe; the welded ones could clip words |
| Notes overlay | ≈1.2× punch-in, text in the left third, white text | **No punch-in**. Text sits on the empty **right-hand wall** in **dark plum** | Your 1080p source would be upscaled (soft) by a 1.2× zoom. The empty space already exists on the right, and white text would not read on the light wall |
| Jump-cut softening | Optional 100/108 % alternation | Only at the most jarring cuts: **106 %** scale, Lanczos resample, centred on the face | 6 % upscaling is not visibly soft at 1080p; more would be |
| Master framing | Face ≈40 % of height | Keep 100 % (face ≈27 %) | A global punch-in would soften the whole video |
| B-roll | 15–20 % of runtime, personal proof clips | **None available.** Slots are marked in Section 3 if you want to shoot them. No stock footage without your permission | Would require licensing or paid stock |
| Music / SFX | Faint bed at most; no SFX | **None** | Matches the reference's voice-led feel and the stage-1 brief |
| Transitions | Hard cuts only | Hard cuts. Overlays ease in over 5 frames (opacity plus 8 px drift); floating labels fade out over 12 frames | Within the spec's allowance |
| Audio | −19.1 LUFS measured; spec asks for −16 | Stage-1 chain: gentle denoise (latency-compensated), de-click, light EQ, 2:1 compression, **−16 LUFS / −1.5 dBTP**, 12 ms micro-fades at every cut, room tone under title cards | Already validated on the test section |

### Graphics palette, taken from your set

| Role | Colour | Source |
|---|---|---|
| paper | `#F4EFE6` | Ivory wall, lifted |
| ink | `#3A2A3B` | Plum top |
| ink_soft | `#6E5A6B` | |
| tag_bg | `#EFEBE3` | |
| accent | `#8C6E84` | Dusty mauve |
| highlight | `#E3B04B` | Brass lamp |
| end gradient | `#EBD9C6` → `#C9B2C6` → `#9E8BB0` | |

### Fonts

All fonts are SIL Open Font License (free to use), fetched from npm `@fontsource`:

| Role | Font |
|---|---|
| Titles, notes, cards | Instrument Serif |
| Pull-quotes, keyword labels | Inter |
| Captions | Poppins Medium |
| Hook script | Great Vibes |

The style frames (`style_frames.jpg`) show each preset on real frames from your video.

---

## 3. Proposed timeline

Structure taken from the transcript: hook → intro → chapter menu → **5 lessons** → wrap-up → end screen.
Estimated final runtime: **≈10–10.5 min** (≈9.3–9.6 min of speech, plus ≈30 s of cards and end screen).

**Key** to the "Visual" column:
- **TC** = title card (3.0 s, hard cut, room tone, no captions)
- **NO** = notes overlay on the right wall
- **PQ** = dimmed pull-quote: A-roll at ≈35 % brightness, blur sigma 9, vignette; Inter with **bold** keywords
- **KW** = floating keyword labels
- **PiP** = ivory card with the speaker picture-in-picture
- **J106** = 106 % softening scale on a jarring jump cut
- **[B-roll?]** = an optional slot if you supply footage

Captions are **on** everywhere except during TC, menu, NO, PQ, PiP, the end screen and the first ≈8 s.

| # | Source | Content | Visual | Notes |
|---|---|---|---|---|
| H1 | 6:57–7:03 | "Whoever is paying for you is going to control your life…" | **Cold open**, no captions, serif lower text in gold: *paying → control* | Flash-forward soundbite (option A, see Q3) |
| H2 | 14:06–14:14 | "If you are taking 10 decisions… eight will go right" | A-roll, no captions | Flash-forward 2 |
| H3 | 0:09.9–0:14.4 | "So if you are in your twenties right now, I think my video will definitely help you." | A-roll; captions start | Hook line |
| I1 | 1:06.8–1:16 | "Hi everyone, welcome to my channel… navigate our life in our 20s" (final clean take) | A-roll; split lockup *"in your* ***twenties***" (sans plus gold script), right of the head | Spec 3.9 |
| I2 | 1:16–1:40 | relationships, finances, mental health, physical health… seek advice | **KW** on each spoken word (1:24–1:33), then captions | Spec 3.7 |
| I3 | 1:40–1:50 + 2:14–2:34 | "We forget how to look into our inner self" + "I'm going to be thirty next year… lessons…" | A-roll; **PQ** at 1:44: "We forget to look **inward**." | Retakes R3–R4 removed |
| M | (insert) | Chapter menu, 5 tiles with real output timestamps | Full ivory card, 6 s | Spec 3.2 (5 tiles in one row) |
| L1 | 2:34–2:39 | "So first" | **TC "1. Don't wait to be rescued"** | Title wording: Q4 |
| | 2:39–3:09 | Mistakes are okay; take help when you can | A-roll + captions; Hinglish line 2:40–2:50 needs caption text from you (Q5) | [B-roll?] |
| | 3:41–4:08 | "Take all the help you need, but do not wait for someone to rescue you…" | **PQ** at 3:41: "Take all the help you need, but **don't wait** to be **rescued**." | |
| | 4:15–4:28 | Prince Charming from childhood movies (Hinglish) | A-roll; caption text from you (Q5) | [B-roll? old film/fairy-tale imagery you own] |
| | 4:43–5:17 | As women we're told what to do; parents, partners; "the narrative that has been fed to you" | A-roll; **NO "Who decides for you?"**: parents · partner · "someone will rescue you" (≈4:49–5:05) | |
| | 5:14–5:17 + 5:38–5:58 | "It is up to you to change this narrative… take charge of your life… emotional slump" | **PQ** at 5:44: "**Take charge** of your life." | |
| | 6:28–6:35 | "…not completely dependent on people around you" | A-roll | Off-camera chat (R12) removed |
| L2 | 6:36–6:43 | "Second thing I would like to say is…" | **TC "2. Take control of your finances"** (cut on "is", card, then "take control of your finances") | |
| | 6:47–7:20 | Handle your finances; "whoever is paying for you…"; investment, budgeting, stock market | **PQ** at 6:57 (same line as cold open; use one or the other, Q3). **NO "Learn the basics"**: investing · budgeting · stock market · personal finance (≈7:13–7:22) | [B-roll? budgeting app / notebook] |
| | 7:20–7:35 | "Many YouTube videos… start educating yourself early" | A-roll + captions | |
| L3 | 7:48–7:56 | "[Third is] find where your happiness lies" | **TC "3. Find your happiness"** | ASR heard "Tourism" here; please confirm the word (Q5) |
| | 7:58–8:42 | Scrolling is consumption; you need a creative outlet | **PQ** at 8:14: "Have a **creative outlet**, not just a feed." | |
| | 8:42–9:20 | crochet, baking, singing, dancing, YouTube, pottery, journaling, workshops, reading clubs | **KW** on each word 8:42–8:56, then **NO "Try"**: pottery · perfume workshops · reading clubs · journaling (≈9:07–9:20) | [B-roll? your crochet/journal/baking] |
| | 9:20–9:57 | Pen-and-paper exercise: what do I do when I'm bored? | **PiP card "Write it down"**: What do I do when I'm bored? / Am I just scrolling? / Am I creating something? (pops on cue) | [B-roll? pen and paper] |
| L4 | 9:58–10:05 | "Next is…" | **TC "4. Know yourself first"** | |
| | 10:05–10:58 | People's advice; clear the noise; know yourself first; filter it | **PQ** at 10:20: "Clear the **noise**. **Know yourself** first." | |
| | 10:58–11:12 | Advice based on their own experience | **PQ** at 11:02: "Their advice comes from **their** life, not **yours**." | 2 PQs ≈40 s apart (Q6) |
| | 11:15–11:48 | Know your values, ethics, non-negotiables, boundaries | **NO "Know your"**: values · ethics · non-negotiables · boundaries (in the style frame) | |
| L5 | 12:05–12:20 | "Everything eventually points to decision making…" | **TC "5. Learn to make decisions"** before 12:05 | |
| | 12:20–13:11 | Indian parents decide for us, then partners; trip / degree / city / purchases | **KW** trip · degree · city · buy or not (≈12:52–13:08) | [B-roll? travel, college] |
| | 13:25–13:46 | Waiting for others' decisions drops your confidence | **PQ** at 13:30: "Waiting for approval **drops your confidence**." | |
| | 13:49–14:25 | Decisions can go wrong; 10 decisions → 2 wrong, 8 right → confidence for 50 more | **PiP card "Decisions build confidence"** (in the style frame), bullets on cue | |
| | 14:25–15:34 | Lose confidence and courage; another video on decision making; take advice, then decide | A-roll; small comment prompt "Want a video on decision making? **Comment below**" (3 s, top-right) at 14:47 | Instead of a related-video card (no such video yet) |
| W | 15:43–15:46 + 16:04–16:19 | "That's it for this video… be confident, be bold… speak your heart out. Thank you. Love you guys." | **PQ** pair: "Be **confident**. Be **bold**." → "Don't shy away from **speaking your heart**." Then CTA A-roll, 1-word caption "Bye!" | |
| E | (insert) | End screen, 10 s | Gradient, sparkles, circle photo, "Watch this next" (empty zone right), Subscribe pill, channel name | Needs channel name and credits (Q7) |

**Density check, about 10 min:**

| Element | Count | Share of runtime |
|---|---|---|
| Pull-quotes | 11 | ≈8 % (≈1 per 55 s) |
| Notes overlays | 4 | ≈10 % |
| PiP cards | 2 | |
| Title cards | 5 | ≈4 % with the menu |
| Keyword moments | 3 | |

The longest plain A-roll stretch is about 35 s. Without B-roll, graphics carry most of the pattern breaks. If you shoot even 6–8 short clips for the [B-roll?] slots, it moves much closer to the reference.

---

## 4. Likely retakes and repeated sentences

**Proposed for removal; not removed until you approve.** The "keep" column is the take I'd use.
The full list is also in `stage2_retakes.csv`.

| # | Source range (≈) | What's there | Proposal | Confidence |
|---|---|---|---|---|
| R1 | 0:00–0:09.6 | Pre-roll before first line | Remove | High |
| R2 | 0:14.5–1:06.6 | **Five aborted intros** ("Hi everyone, welcome…" ×6, "in today's top uh", "we are going to discussing…") | Keep the 1:06.8 take only | High |
| R3 | 1:49.5–2:14.0 | "we forget how to navigate / we f– we forget how to / um / Okay, good one / I'm going to be thirty next year / and um" | Keep "We forget how to look into our inner self", then the 2:14 take | High |
| R4 | 2:14.0–2:15.0 | "I'm going to, I'm going to be thirty" stutter | Trim to one "I'm going to" | High |
| R5 | 2:34.4–2:39.5 | "Okay. So first… uh" | Replaced by the title card | High |
| R6 | 3:09.4–3:41.0 | "Actually." + first attempt: "don't wait for someone to rescue you… as a kid… kingdom… no Prince Charming… yeah… okay so um" | Keep the 3:41 restatement; the Prince Charming idea returns at 4:15 | **Medium**: listen, as it may hold a line you like |
| R7 | 3:56–4:01 | "Don't be completely depend on anyone. Dependent on—" | Keep "don't be completely dependent on anyone to rescue you" | High |
| R8 | 4:08.6–4:14.6 | "Okay, be your pillow(?). Uh" | Remove | **Low**: maybe "be your own pillar", which could be intentional |
| R9 | 4:14.6–4:21 | "From childhood we um, from childhood we have seen movies. Um…" | Keep the last "from childhood we have seen movies…" | High |
| R10 | 4:28–4:47 | "We often as women we are always told to do told / As women we are often told to, as women…" | Keep "As women, we are often told what to do, what not to do" | High |
| R11 | 5:17.4–5:38.4 | "…because. / It is up here to change this narrative. / So that you don't wait. / For someone to" | Keep "But it is up to you to change this narrative", then the 5:38 take | High |
| R12 | 5:58.0–6:28.4 | **Off-camera exchange** ("Three, do you want? No. No…") + "So take charge of your life or so / take charge of your life / and uh" | Remove all; resume at "and see to it that you are not completely dependent…" | High |
| R13 | 6:36.0–6:41.5 | "Okay. Second I would like to see is—" | Keep "second thing I would like to say is…" | High |
| R14 | 7:35.5–7:52.0 | "Okay." + 12 s gap + "Tourism(?)" | Remove; the title card replaces it | Medium: the word may be "Third is" |
| R15 | 7:52.6–7:54.3 | "Find your happiness, find where…" | Keep "Find where your happiness lies" | Medium (could be emphasis) |
| R16 | 8:17.9–8:26.6 | "Because as female you have so much creativity inside you. Which…" | Keep the 8:26 take ("We have so much creativity inside you…") | High |
| R17 | 8:34.9–8:37.0 | "The thing that can help you is. The thing that can help you is…" | Keep the second | High |
| R18 | 9:32.6–9:39.8 | "Is it just uh it j– is it is it that…" + "At Witz(?)" | Keep "Is it that I'm just watching YouTube?" | High |
| R19 | 9:58.0–10:05.2 | "Next is the / We have people around us." | Title card, then "We have people around us who often…" | High |
| R20 | 10:29.6–10:34.8 | "It's just absolutely important for you to know yourself first and" (repeats the previous sentence) | Remove | **Medium**: may be intentional emphasis |
| R21 | 10:58.1–10:59.6 | "Often what happens is often people…" | Keep "Often people will tell you…" | High |
| R22 | 11:11.5–11:15.5 | "So / So know your values" | One "So" | High |
| R23 | 11:38.5–11:42.2 | "you would know if that advice suits you" (2nd time) | Remove the duplicate | High |
| R24 | 11:48.5–12:04.8 | "Um / And whatever we have discussed until now, everything eventually / needs to / And whatever" | Keep the 12:05 take | High |
| R25 | 12:19.5–12:22.0 | "as a female we as… Oh." | Trim to "…because Indian parents often take decisions for you" | Medium |
| R26 | 13:11.5–13:25.0 | "Sometimes even what? / Okay. So even basic even for and it / and continuing so," | Remove; resume "you start waiting for other people to take decisions…" | High |
| R27 | 13:46.2–13:49.6 | "Mm-hmm. So that" | Remove | High |
| R28 | 13:52–13:54 | "sometimes your decision, sometimes your decisions" | Keep the second | High |
| R29 | 14:34.8–14:42.8 | "So learn learn decision making. It is a" | Keep the 14:42 take | High |
| R30 | 15:02.6–15:08.3 | "Obviously, take advice and the" | Keep the 15:08 take | High |
| R31 | 15:17.6–15:21.4 | "they know you. Better. They they also know you better." | Keep "they know you better" | Medium |
| R32 | 15:34.6–15:43.8 | "That's it." + gap | Keep only the 15:43 "That's it for this video" | High |
| R33 | 15:46–16:03.8 | "I hope you have a great life, your great twenties and um whatever uh mistakes other people do I uh / And" | Keep the 16:03.8 take | High |
| R34 | 16:20.5–end | "Okay." + tail | Remove | High |

Removing all of these drops ≈400 of 1,828 words (≈4.3 min of the 16.5 min). Every cut snaps to word
boundaries (Parakeet timestamps), is double-checked against the voice detector, and gets the same
12 ms audio micro-fade as stage 1.

---

## 5. Captions

- Generated from the local transcript: phrase cues of 3–6 words / ≤35 characters, one line, instant swap.
  Poppins Medium 42 px, white, soft shadow, baseline at 91 % height. Hidden during cards, quotes,
  notes and PiP cards.
- **You proofread first:** I'll send an `.srt` before burning anything in. Known recognition problems: the Hinglish lines at 2:40 and 4:15, "Tourism", "be your pillow", "Very oddly" (11:26, probably "very early"), "At Witz".
- Delivered **burned in** (per the spec) **and** as a separate `.srt` for YouTube's own caption track.

---

## 6. Processing requirements

| Step | Tool (all local, free, nothing uploaded) | Time on this 4-core machine |
|---|---|---|
| Transcript and word timing | sherpa-onnx + NVIDIA Parakeet TDT 0.6B (done) | 2 min |
| Cut list (retakes + pauses), frame-snapped | Python + Silero VAD | < 1 min |
| Graphics (≈45 PNG overlays/cards + end-screen sparkle sequence) | `tools/gfx.py` → headless Chromium | ≈5 min |
| Captions | ASS subtitles, burned in by ffmpeg/libass | — |
| Composite and encode | ffmpeg, rendered in ≈1-min chunks with identical settings, then joined without re-encoding (stream-copy concat) | ≈60–75 min |
| QC | Black/frozen-frame scan, loudness, A/V sync cross-correlation at start/middle/end, review clips | ≈5 min |

Peak scratch disk ≈6 GB; RAM < 4 GB. Before the full render: one **≈90 s test render containing every element type** (title card, notes, PQ, PiP, KW, captions).

---

## 7. Output quality settings

| Setting | Value |
|---|---|
| Container | MP4, `+faststart` |
| Video | H.264 High, **1920×1080, 30 fps CFR**, yuv420p, BT.709 tags kept, **CRF 16, preset slow**, keyframe every 2 s |
| Scaling | Only on J106 shots (Lanczos) and the PiP (downscale) |
| Audio | AAC-LC 192 kb/s, 48 kHz stereo, −16 LUFS integrated, −1.5 dBTP |
| Expected size | ≈0.6–0.8 GB for ≈10 min (≈6 Mb/s; the test section came out at 6.2 Mb/s) |
| Generations | One encode from the original HEVC; no lossy intermediates |

*Correction:* my earlier "≈6.7 GB" estimate for the stage-1 full render was wrong by a factor of 10. That render would have been ≈0.7 GB.

---

## 8. Decisions needed from you

1. **Retakes:** approve Section 4 (or list the numbers to keep). Please listen to R6, R8, R15 and R20.
2. **Pause length:** reference-tight (0.18 s / 0.30 s) as proposed, or a softer 0.25 s / 0.40 s?
3. **Cold open:** A) the two flash-forward soundbites (H1, H2), then the hook line; or B) start directly on the hook line at 0:09.9.
4. **Title wording** for the 5 lessons (Section 3).
5. **Caption text** for the Hinglish lines (2:40, 4:15) and the uncertain words, or leave those lines uncaptioned.
6. **Graphics density:** keep 11 pull-quotes, or fewer?
7. **End screen:** channel name and credits text. Is it OK to use a still of you for the circle photo?
8. **B-roll:** do you have, or want to shoot, clips for any [B-roll?] slot?
