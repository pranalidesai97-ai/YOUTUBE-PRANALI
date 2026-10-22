# Reference Editing-Style Specification

**Source analysed:** "10 High-Maintenance Beauty things…" (talking-head listicle, 23:10, supplied at 256×144 / 30 fps / AAC stereo).
**Purpose:** a transferable style prompt for editing a *different* talking-head video. Copy the editing *language* described here, not the content, footage, music, logos or graphics.

## 0. How this was measured (and how far to trust it)

Everything below comes from inspecting the file itself:

| Method | What it gave |
|---|---|
| Contact sheets, one frame every 2 s, covering the whole video | Structure, every overlay type, and where each one appears |
| Frame grids at 5–10 fps around 25 key events | How animations enter and exit, and how long each layout stays up |
| Per-frame scene-change scores (ffmpeg) plus visual checks on a random sample | Cut cadence |
| Face tracking on every frame (YuNet detector) | Framing sizes, punch-ins and reframes |
| Frame-brightness runs | Exact in/out times of cream cards and dark pull-quotes |
| Pixel sampling | *Approximate* colours (heavily compressed, so ±10–15 % per channel) |
| EBU R128 loudness, 100 ms RMS, silence detection, spectrograms | Loudness, leftover pauses, music/SFX evidence |
| Local speech-to-text (Whisper small.en) | Speaking rate and how speech relates to graphics |

Confidence labels used throughout:
- **High**: clearly visible or measured repeatedly.
- **Medium**: consistent but inferred from low-resolution or indirect data.
- **Low**: plausible estimate. Verify, or treat as a free choice.

Timestamps are `m:ss` in the reference file and are accurate to roughly ±0.2 s.

---

## A. Summary of the style

A **calm, polished, "aesthetic-educational" listicle** that is still very tightly cut. The look is soft and editorial: a cream paper colour, a condensed serif, brown ink and warm-lit A-roll. That softness hides an aggressive pace:

- **Every pause is cut out.** No silence in the video is longer than about 0.4 s, and the median remaining gap is 0.17 s. The delivery runs at about **215–220 words per minute**, against roughly 150–170 for natural speech.
- **Something visual changes about every 1.2–2.2 s.** That might be a jump cut, B-roll, a text pop or a card. Plain jump cuts in the A-roll come roughly every 2–3 s.
- **Jump cuts stay visible.** The camera is locked off and almost every cut keeps the same framing. Nothing tries to hide the cuts; the small head jumps are part of the native YouTube look.
- **Motion design is almost static.** Graphics *pop* in on hard cuts and sync to the spoken word. They do not fly, bounce or spin. The energy comes from the timing, not the motion.
- **Graphics show information.** Most graphics are typeset notes: section title cards, side "notes" lists, cream info cards with a picture-in-picture (PiP) of the speaker, and dimmed pull-quotes. They summarise, structure or emphasise what is being said.
- **Rough screen-time split (measured):**

  | Layout | Share of runtime |
  |---|---|
  | Talking head (including about 1–2 min with side notes) | ≈ 67 % |
  | B-roll and inset clips | ≈ 14–19 % |
  | Dark pull-quote overlays | ≈ 8 % |
  | Full cream cards (titles, menu, PiP info cards) | ≈ 6–9 % |

- **The structure is a strict, repeated template.** Each list item runs: title card → explanation on A-roll → personal proof in B-roll → a summarising notes overlay → one or two pull-quotes → (optional) a cream PiP card with facts and costs → back to the A-roll → next title card.

Style label: **educational listicle × lifestyle-vlog B-roll × minimal editorial typography.** It is not cinematic: there are no grades, transitions or music swells. It is not hyper-kinetic either: there are no zoom-whooshes or meme inserts.

---

## 1. Overall editing style

### 1.1 Visual identity and tone
- **Palette:** warm cream (#FEF2D6, approx.), dark espresso-brown text (#4E3821 sampled, probably darker in the master, around #3A2618), dusty-rose tiles (#976563, approx.) and warm gold accents (#E5AC60, approx.). The A-roll itself is warm-toned: a tungsten lamp, a plant, a beige arch and a peach top. The graphics palette is clearly chosen *to match the set*. Confidence: High for the palette relationships, Low for exact values.
- **Tone:** friendly, confiding and slightly witty ("I am a **sunscreen stan** now :)"). The text sounds like the speaker's own notes, not like advertising.
- **Energy:** high information density with low visual aggression.

### 1.2 How attention is held
1. **Pause removal and jump cuts** keep the speech flowing with no dead air (High).
2. **A pattern break every 10–40 s.** B-roll, a pull-quote, a notes overlay or a card arrives often enough that the plain A-roll rarely runs longer than about 30–40 s unbroken (High).
3. **Structure is always visible.** A chapter menu at 0:59.6, then a numbered title card for each of the 10 items, and persistent sub-labels such as "1. Whey Protein" inside multi-part sections. Viewers always know where they are (High).
4. **Text is revealed progressively.** List items appear one by one exactly when they are spoken, so viewers keep reading along (High).
5. **Dimmed pull-quotes** take the punchline out of the speech, darken the frame and put the line in the centre. It works like a "pay attention" beat (High).
6. **Personal proof B-roll.** The speaker doing the routine (selfie clips, bathroom, product-in-hand shots) makes the claims believable (High).

### 1.3 Balance of footage types
Talking head is the backbone. The speaker is fully replaced by B-roll for 1–20 s blocks, with a median of about 5 s. She also appears **inside** graphics: a PiP in cream cards, and a dimmed background behind pull-quotes and vertical inset clips. Full-screen graphics with no speaker at all are only the section title cards (2–4 s), the chapter menu (6.7 s), the "You put in" card (about 9 s, which later gains a speaker inset) and the end screen (about 10 s).

### 1.4 How the style changes by part of the video

| Part | Reference time | Treatment |
|---|---|---|
| Cold-open hook | 0:00–0:20 | The densest, most decorative part. **No captions for the first 8 s.** A collage of tilted photo clusters with gold script labels ("Hair", "Skin", "Nails", "Outfits") pops in one per spoken word. Fast flashback selfie B-roll follows (0:10–0:16) with serif overlay text ("Months in advance"), then a two-sided split label ("To become *Low Maintenance*" / "Being *High Maintenance*"). |
| Thesis and disclaimer | 0:20–0:59 | A cream concept card ("You put in" → Time · Money · Discipline icons pop in on each word, then a vertical speaker clip joins). The first pull-quote is in **serif with gold keywords** ("None of the things discussed in the video are **mandatory**"). Floating white labels (lasers, facials, colored hair, manicured nails) pop in around her head. Selfie B-roll montage. |
| Chapter menu | 0:59.6–1:06.3 | Full cream card with a 2 × 5 grid of rose tiles, each showing an item name and its timestamp. Held 6.7 s. |
| Body (10 items) | 1:06–22:17 | The repeating template described in Section F. Pull-quotes switch to a **clean sans with bold keywords**. Captions run continuously. Graphics stay informational. |
| Wrap-up | 22:17–23:00 | Three dimmed pull-quotes close together (the "moral" of the video), then a fast A-roll call to action (CTA), a waving goodbye and a "Bye" caption. |
| End screen | 23:00.5–23:10.5 | Hard cut to a pastel gradient (peach → lilac → periwinkle) with twinkling sparkles, a circular photo with sticker text, a handwritten "Watch this next" with an arrow pointing at an *empty area* (left for the platform's end-screen element), an outlined "SUBSCRIBE" button and small credits text. Elements animate in over about 0.5–1 s. |

---

## 2. Cuts and pacing

### 2.1 Frequency and motivation
- **About 810 visual change events in 23 min.** About 170 are hard scene changes. The rest are mostly same-framing jump cuts, plus text pops and gestures; a visual check of a random sample found that about ⅔ were real jump cuts. That works out to roughly **one A-roll jump cut every 2–3 s** (Medium). Per-minute density stays between 21 and 60 events across the whole video, so the pace is fairly steady (High).
- **Visual change interval by section:**

  | Section | Seconds per change |
  |---|---|
  | Intro | 1.4 |
  | Items 3, 4, 5 (most B-roll-heavy) | 1.2–1.5 |
  | Item 9 (longer B-roll and pull-quote holds) | 3.5 |
  | Outro | 1.4 |

  The pace follows content type: demonstrations and lists get faster, and a reflective explanation is allowed to breathe.
- **What motivates a cut:**
  1. removing a pause, breath, "um" or false start;
  2. a new sentence or thought;
  3. the start of a graphic, because graphics enter *on* cuts;
  4. a B-roll insert that illustrates the noun just spoken.

### 2.2 Pauses, retakes and mistakes
- **Pauses:** silence detection at −38 dB finds only about 10 short gaps per minute. Median 0.17 s, 90th percentile 0.27 s, and only **one gap longer than 0.4 s** in the whole video. Every breath gap is trimmed to about 0.1–0.25 s (High).
- **Retakes:** only the best take is kept. Repeated sentences and fumbles are removed at the cut (High; the full transcript contains no immediately repeated 3–4-word phrases). Small verbal fillers are *sometimes* kept when they add personality ("uh", "you know"). They are not scrubbed robotically (Medium).
- **Speech rate after editing:** about 216 wpm (Medium; about 4,960 ASR words over the full 23 min).

### 2.3 Visible jump cuts and how they are softened
- The camera is static and the framing is constant, so most jump cuts show a **small head or hand jump**. They are left visible on purpose (High).
- Ways they are softened when needed:
  - **A text pop on the same frame as the cut.** The eye goes to the new text.
  - **A cut to B-roll** while the voice-over continues.
  - **A cut to a dimmed pull-quote** (the speaker continues underneath).
  - **A reframe** (≈1.2× punch-in with the subject shifted right) when a notes overlay arrives.
  - Possibly a subtle alternate framing (≈1.05–1.1×) at some cuts (Low–Medium; face-size data shows a secondary cluster, but it is hard to separate from leaning).

### 2.4 Shot duration vs content
- A-roll segments: most last **0.5–4 s**. Very short fragments under 0.5 s are common where single words were tightened (Medium).
- B-roll blocks: median **≈5 s**, typical range 3–10 s, maximum about 20 s (supplement montage 17:30–17:50) (Medium–High).
- Section title cards: **2.2–4.3 s**, typically about 3 s (High; measured: 1:06.3, 4:42.8, 6:32.3, 9:47.9, 12:18.6, 14:07.6, 15:29.8, 17:06.2, 20:20.4, 21:12.3).
- Pull-quotes: **2.1–7.6 s**, median **4.0 s**. Back-to-back quotes can form a 10–14 s block (High; 24 detected).
- Cream PiP info cards: 7–40 s, staying up while the bullet points are read out (High).

### 2.5 Cut types
- **Hard cuts everywhere.** No dissolves, wipes, whip-pans or zoom transitions were seen between any shots or graphics (High).
- **Cuts land mid-sentence** into B-roll and back (an "L-cut" feel: the voice runs straight through) (High).
- **"Match" logic is semantic, not graphic:** the B-roll matches the *spoken noun* ("shaving" → shaving clip, "tretinoin" → product in hand) (High).
- **Visual interruptions** are the full-screen cream title cards (hard cut in, hard cut out) and dimmed pull-quotes.

---

## 3. Motion graphics (reverse-engineered)

> General rule found in the reference: **graphics appear on a hard cut or as an instant pop (≤ 2 frames), stay completely still, then leave on a hard cut.** At 10 fps no slide, scale or blur entrance is visible on cards, notes, quotes, titles or captions. The only visibly animated elements are the end screen (sparkle twinkle, circle scale-in) and the fade-out of floating labels (≈0.3–0.5 s). Confidence: High for "no large motion", Medium for "instant" (a 1–3 frame fade could be hidden at 144p).

For an original recreation, you may add a **very short ease (4–6 frames, opacity 0→100 % with a 2–4 % upward drift or a 96→100 % scale, ease-out)**. That stays true to the look and removes any harshness. Do not go beyond about 8 frames.

### 3.1 Section title card ("N. Title")
- **Observed:** full-frame cream (#FEF2D6, approx.) with one centred line, for example "4. Doing Nails", in a condensed serif, dark brown, at about 4–5 % cap height (modest, not huge). No icon, no subtitle, no motion. Hard cut in and out. The audio has the speaker's lead-in line *before* the cut and her first sentence *after* it; the card itself is mostly quiet or carries a breath of speech. 2.2–4.3 s.
- **Recreate:** a solid-colour 1920×1080 card using your own brand's "paper" colour. Text: condensed serif (free options: *Gloock*, *Playfair Display SC Condensed*, *Instrument Serif*, *Libre Caslon Condensed*, *Fraunces 72pt condensed*), about 72–84 px at 1080p, centred, letter-spacing 0. Hold for 2.5–3.5 s. Hard cuts.

### 3.2 Chapter menu (overview grid)
- **Observed (0:59.6–1:06.3):** cream card. Two-line serif title at the top ("10 High maintenance things I do / to be low maintenance"), then a **2 rows × 5 columns grid of dusty-rose rounded tiles**. Each tile shows the item name (small serif, top-left) and its timestamp (bottom-right, tiny). Static for 6.7 s, then a hard cut straight to "1. …".
- **Recreate:** a grid with an outer margin of about 8 %, gutters of about 1.5 %, tile corner radius about 6 px at 1080p and a fill in one muted accent colour. Make the timestamps real chapter times. Optional: tiles pop in left-to-right at 2-frame intervals (an enhancement; not observed).

### 3.3 Side "notes" overlay (key-point list over the A-roll)
- **Observed (12 instances, e.g. 2:10, 4:32, 4:45, 5:26, 6:58, 7:22, 7:36, 8:36, 10:02, 10:34, 14:14, 15:52):**
  - **Header tag:** an off-white rectangular label (#EFECE1, approx.) with a 2-line serif heading in muted brown, for example "After Laser hair / reduction". Placed top-left at about x 10 %, y 8–17 %. Square or very slightly rounded corners.
  - **Body:** white serif text, left-aligned, in a column about 25–28 % of frame width under the tag. Numbered ("1. … 2. …") or dash bullets. About 3 short lines per item, with an extra line gap between items. Possibly a faint drop shadow (it reads cleanly on the warm background).
  - **Behaviour:** the overlay arrives **on a cut that also reframes the speaker**: a ≈1.2× punch-in with her face moved right, from x≈48 % to x≈53 %, to clear the left third. Items are added **one at a time as she says them** (instant pop). **Captions are hidden while notes are on screen.** The overlay stays for 5–25 s, then leaves on a cut back to the normal framing.
- **Recreate:** an adjustment layer or reframe of 115–122 % scale, anchored so the subject's eye-line stays about 38 % from the top and the subject moves right. Text box at x = 8–10 %, width ≤ 30 %. Serif about 34–40 px at 1080p for the body and a 30–34 px heading in the tag. Add each item on its spoken cue. Hide captions while it is on.

### 3.4 Dimmed pull-quote
- **Observed (≈25 instances, roughly one every 55 s):** the A-roll keeps running underneath (she is still talking) but is **darkened to about 30–40 % brightness, softly blurred and vignetted**. One or two centred lines of white text sit at about **45 % frame height** (over the face area). Body text uses a clean neo-grotesk sans (Inter or Helvetica-like) in regular weight. **Keywords are set in bold white** ("Laser treatment is **expensive** upfront", "**Retinoids** reward consistency", "A **beautiful smile** is low-maintenance in public…"). The text is often a paraphrase or condensed version of the speech, sometimes a direct quote. Captions are hidden. Hard cut in and out. 2–7.6 s.
- **Intro variant (0:40):** the same dim-and-blur treatment, but the text is in the **condensed serif with gold-yellow keywords** ("None of the things discussed in the video are **mandatory**").
- **Recreate:** duplicate the A-roll, then apply exposure −1.5 to −2 stops (or a black solid at 60–70 % opacity), Gaussian blur of about 6–10 px at 1080p and a soft vignette. Text: sans 44–52 px at 1080p, line length ≤ 45 characters, 2 lines maximum, centred at y ≈ 45 %. Bold the 1–3 words that carry the idea. One quote per idea, held about 0.5 s longer than it takes to read aloud.

### 3.5 Cream info card with speaker PiP
- **Observed (2:37–3:17, 5:42–5:59, 18:06–18:13):** full cream background. **Right:** the speaker PiP as a portrait rounded rectangle (about 3:4) at x 62–94 %, y 10–90 %, corner radius about 5 % of its width, with no visible border. **Left:** a small illustrated or 3D product icon at the top-left (x 3–11 %), then a serif heading in brown ("Results can vary depending on"), dash bullets in smaller dark-brown serif, then more heading and bullet blocks ("Cost", "Frequency", "Costing: In Delhi, 1 full body session ≈ ₹10,000") that **pop in on cue**. One version shows a **research-paper citation block** (title, authors, small metadata) above a plain-language summary with the key phrase in bold ("…shifts with **7 days** of Creatine supplementation"). Captions are hidden. Hard cuts in and out.
- **Recreate:** cream base; PiP from the A-roll cropped to 3:4 around the face, scaled to fill a 560×800 px box at 1080p, radius 24–28 px, optional 0–2 px warm-grey stroke or a soft shadow. Heading serif 40–46 px, bullets 28–32 px, line spacing 1.2, left margin 12 %. Use your *own* drawn icons. Recreate any citation as an original styled block that quotes the real source's title and authors, not as a screenshot of a journal page.

### 3.6 Sub-item persistent label (inside a multi-part section)
- **Observed:** a small white serif label at the top-left (about x 1–4 %, y 2–6 %), for example "1. Whey Protein", "2. Creatine", "3. Collagen", "4. Omega-3", "5. Magnesium", "6. Iron + Vit C", and in the hair section "1. Pre-wash routine … 7. Style properly". It **stays on** over both A-roll and B-roll for the whole sub-part, then swaps instantly to the next number. Captions stay on.
- **Recreate:** serif 30–36 px, white, with a 1–2 px soft shadow at 40 % opacity. Change it on the cut where the new sub-item starts.

### 3.7 Floating keyword labels around the speaker
- **Observed (0:44–0:47):** single words or short phrases in **bold white sans** (lasers, facials, colored hair, manicured nails) pop up at different spots around the head, one per spoken word, about 0.6–0.8 s apart. Each fades out about 2 s later over about 0.3–0.5 s, so 2–3 are visible at once.
- **Recreate:** sans bold 36–44 px. Place them on a loose ring around the head, avoiding the face, at 20–35 % from the frame edges. Pop in on the word, hold 1.8–2.2 s, fade out over 10–14 frames.

### 3.8 Hook collage (photo clusters plus script labels)
- **Observed (0:01.6–0:07.8):** clusters of 2–3 overlapping, slightly **rotated photos** (±5–10°), each cluster placed in a corner: top-left "Hair" at 1.6 s, bottom-right "Skin" at 3.2 s, bottom-left "Nails" at 4.4 s, top-right "Outfits" at 5.6 s. Each has a **gold-yellow script word** overlapping its edge. They pile up while she lists them, then all clear on a cut at about 7.8 s.
- **Recreate:** use only *your own* photos or licensed stock. Cluster width about 25–30 % of the frame, with a white 4–6 px photo border and a soft shadow. Script font (free options: *Great Vibes*, *Allura*, *Pinyon Script*) in gold (#E8B85A-ish), 60–80 px. Pop each cluster in on its word; an optional 6-frame overshoot scale from 90→103→100 % keeps it lively.

### 3.9 Split hook labels (two-sided)
- **Observed (0:16–0:20):** right side: "Being" (white bold sans) above "*High Maintenance*" (gold script). Then, a beat later, the left side: "To become" above "*Low Maintenance*". Both stay up for about 1.5 s, then a cut.
- **Recreate:** a sans-plus-script lockup about 15–18 % of frame width, placed at the upper left and right thirds beside the head. Pop each in on its words.

### 3.10 Concept card with icon reveal
- **Observed (0:20.7–0:29.6):** cream card. "You put in" in dark script is centred, then three **emoji-like icons** with sans labels (Time · Money · Discipline) pop in left-to-right on each spoken word, about 0.4–0.6 s apart. The layout then shifts left to make room for a **portrait clip of the speaker** on the right.
- **Recreate:** use your own icons (flat or 3D renders you are licensed to use). Icons about 70–90 px with labels at 26–30 px. Pop them on the spoken words.

### 3.11 Vertical social-clip inset
- **Observed (1:10–1:15, 1:50–1:53):** a 9:16 clip in a rounded rectangle, **centred** at x 37–63 %, y 7–93 %, over the dimmed and blurred A-roll. Captions stay on. Hard cut in and out. It is used for third-party "reaction or example" clips.
- **Recreate:** only with licensed or your own vertical footage. Radius about 20 px; background at 40–50 % brightness plus blur.

### 3.12 "Related video" card
- **Observed (12:50–12:53):** a white rounded card in the top-right (x 62–96 %, y 8–52 %) that imitates a video tile (thumbnail plus 2-line title plus meta line), shown while she mentions "a video on how to figure out your own haircare routine". Instant pop, about 3 s.
- **Recreate:** an original card showing *your own* earlier video's thumbnail and title. Do not copy any platform's UI exactly; a generic rounded card with a soft shadow is enough.

### 3.13 B-roll step labels / headings
- Same as 3.6, for example "1. Pre-wash routine" during the hair B-roll montage at 12:54–13:08, where each step's clip gets its label.

### 3.14 End screen
- **Observed (23:00.5–23:10.5):** a vertical gradient from peach-pink at the top (#D8A99D, approx.) through lilac (#C4A6C7) to periwinkle at the bottom (#B2A1EC). White 4-point sparkles twinkle (scale and opacity loops of about 1 s, staggered). A circular photo cut-out with sticker-style text pops in with a scale-up over about 0.3 s. Also a small handwritten "Watch this next" with a curved arrow, an outlined "SUBSCRIBE" pill and tiny credits ("Idea, Script & Research…", "Editing by…"). **Large empty zones are left for the platform's end-screen elements.**
- **Recreate:** your own gradient in your palette, with sparkle shapes drawn as vector stars. Pop or stagger elements over 0.5–1 s. Keep the end screen at 10 s or more for platform end-screen compatibility.

---

## 4. Typography and captions

### 4.1 Type families (observed characteristics; exact fonts not identifiable at 144p)

| Role | Observed characteristics | Weight | Colour | Confidence |
|---|---|---|---|---|
| Titles, notes, cards, sub-labels | **Condensed, moderately high-contrast serif** (narrow, tall x-height, editorial) | Regular / Book | Dark brown on cream; white on video | High (class), Low (exact font) |
| Pull-quotes (body sections), floating labels | **Neutral neo-grotesk sans** (Inter / Helvetica-like) | Regular with **Bold** keywords | White | High (class) |
| Captions | **Geometric / humanist sans**, small, with open shapes (Raleway / Montserrat / Poppins-like) | Medium | White / very light warm grey | Medium |
| Decorative (hook only) | **Formal connecting script** | n/a | Gold-yellow (#E5AC60, approx.) or dark brown | High (class) |
| End screen | Handwritten / marker accents plus small sans | n/a | White | Medium |

Hierarchy, from largest to smallest: hook script > chapter-menu title ≈ section title > pull-quote ≈ card heading > notes body ≈ card bullets > captions > tile and credit micro-text.

### 4.2 Layout
- **Captions:** a single line, centred, baseline at about **95 % of frame height** (a small bottom margin of 4–5 %), 3–6 words or roughly 25–35 characters, spanning about 25–40 % of the frame width. **No background box and no outline**; any shadow is too faint to resolve. They read because the bottom of the frame (her top and arms) is mid-dark. For a target video, place them a little higher, at about 90–92 %, to clear platform UI and add a faint shadow for safety.
- **Pull-quotes:** centred block at about 45 % height, 1–2 lines, each line no more than about 45–50 % of the frame width.
- **Notes:** top-left column, x≈8–10 %, width ≤ 30 %, starting at y≈8 %.
- **Cards:** left column at x≈12–58 %, with the PiP on the right.
- **Sub-labels:** at the very top-left corner, close to the edge.

### 4.3 Emphasis
- Bold-weight keywords inside otherwise regular sans (pull-quotes) (High).
- Gold-yellow keywords inside serif (intro only) (High).
- Bold figures in fact cards ("**7 days**") (High).
- Gold script for decorative category words in the hook only (High).
- **Not used:** coloured highlight boxes, underlines, strike-throughs, arrows, circles, or animated highlights (High).

### 4.4 Caption timing and animation
- **Phrase-by-phrase, not word-by-word.** Each phrase replaces the previous one instantly as it is spoken, with no fade, karaoke highlight, bounce or scale (High).
- Line breaks follow the speech rhythm, so phrases often end mid-clause ("becomes offended on" → "behalf of body hair, if you"). The cue is set by duration, not grammar. Phrases change about every 0.6–1.5 s (Medium).
- Sentence case, standard punctuation kept (High).
- **Captions are off** during the first 8 s of the hook, on cream cards, dark pull-quotes, notes overlays and the end screen. They are **on** over plain A-roll, B-roll, vertical insets and sub-labelled sections (High).

---

## 5. Camera framing and zooms

- **Single locked-off camera:** a medium close-up at chest level, eye-line about 33–38 % from the top, subject slightly left of centre (face centre at x≈48 %). The face fills about **40 % of frame height** (measured median; 95 % of A-roll time falls within ±12 %) (High).
- **One deliberate reframe:** about **1.15–1.25× punch-in with the subject shifted right**, used **only** when a notes overlay needs the left third (High). It switches on the same cut as the overlay and reverts when the overlay leaves.
- **Possible secondary framing** of about 1.05–1.1× at some jump cuts (Low–Medium).
- **No keyframed slow push-ins, zoom-punches on emphasis words, whip-zooms or shake** were observed in the A-roll (Medium–High; frame grids show none, and face-size growth inside shots matches natural leaning).
- B-roll comes from a mix of a handheld phone (selfie, POV hands), a tripod at a bathroom mirror, and clinic footage; it is not stabilised into one look.

**Recommendations for the target video** (keep it restrained, as the reference does):
1. Choose one master framing, with the face at 35–42 % of frame height and the eyes on the upper third.
2. Use the ≈1.2× reframe with a lateral shift **only** to make room for side text.
3. If cuts in the A-roll feel too jumpy, alternate between 100 % and 108 % scale on **every other** cut *within the same thought*, never randomly. Return to 100 % at each new section.
4. Use at most one emphasis punch-in (about 1.15×, instant) per 60–90 s, and only on a true punchline. Even that goes beyond the reference, so it is optional.
5. Shoot at 4K if possible, so a 1.2× punch-in still delivers a sharp 1080p frame.

---

## 6. B-roll and supporting imagery

| Kind | Reference examples | Relation to speech | Duration | Speaker visible? |
|---|---|---|---|---|
| Personal selfie / vlog clips | 0:10–0:16, 0:50–0:57, 13:34–13:40, 16:02–16:19 | "Proof" of the routine; shows the result or the process | 2–8 s | Replaced fully (it *is* her) |
| POV hands / product-in-hand | 7:08–7:12, 17:44–18:48 (tubs, bottles) | Shows the exact product named | 2–6 s per product | Replaced fully |
| Mirror / bathroom demos | 7:14, 9:18–9:26, 20:36–20:40 | Demonstrates the technique being described | 2–10 s | Replaced fully |
| Clinic / procedure footage | 0:34–0:38, 5:14–5:21, 14:22–14:37, 21:26–21:31 | Illustrates the treatment that cannot be filmed at home | 4–15 s | Replaced fully |
| Close-up macro (nails, teeth) | 11:18–11:27, 11:56–12:01, 20:42–20:47 | Detail or result shots | 3–8 s | Replaced fully |
| Third-party vertical clips | 1:10–1:15, 1:50–1:53 | Example of "what others say" | 2–5 s | Dimmed behind |

- **Entry and exit:** hard cut, usually mid-sentence, with the voice running through; return to the A-roll on a sentence boundary or on the next point (High).
- **Captions stay on** over B-roll (High).
- **Density:** about 40 B-roll blocks in 23 min (≈1.7 per minute). The most B-roll is in hands-on sections (nails, hair, supplements); opinion-driven stretches (for example item 2's reasoning, or the wrap-up) lean on pull-quotes instead (Medium).
- **Purpose:** credibility and demonstration, never decoration. There is no generic "stock mood" footage.
- *Copyright note:* clinic and third-party clips in the reference are not to be reused. Shoot your own, or use licensed stock or your own screen recordings.

---

## 7. Colour, transitions and sound design

### 7.1 Colour
- **A-roll:** warm white balance (tungsten practical lamp and warm room), moderate contrast, natural-to-slightly-lifted saturation, soft highlights on skin. There is no stylised LUT, teal-orange or crushed blacks. The background is a little darker than the face (Medium; compression limits detail).
- **B-roll:** left mostly as shot, so its colour does *not* match the A-roll exactly (for example, the pink-walled bathroom and white clinic). Unity comes from the graphics, not the grade (Medium).
- **Graphics palette (approximate):**

  | Use | Approximate colour |
  |---|---|
  | Paper / cream | #FEF2D6 |
  | Ink brown | #3A2618–#4E3821 |
  | Muted brown, secondary text | #716249–#7E685C |
  | Tag off-white | #EFECE1 |
  | Rose tile | #976563 |
  | Gold accent | #E5AC60 |
  | White text on video | #FFFFFF |
  | End gradient | #D8A99D → #C4A6C7 → #B2A1EC |

- **Dim treatment:** A-roll pulled to about 30–40 % brightness.

### 7.2 Transitions
- Hard cuts only. Dissolves, slides, whooshes, glitches and light leaks are all absent (High).
- Overlay elements: instant pops; floating labels have about a 0.3–0.5 s fade-out; the end screen has a scale-in and sparkle loops (High / Medium).

### 7.3 Audio
- **Voice:** integrated loudness **−19.1 LUFS**, loudness range (LRA) **5.3 LU**, which is consistent and gently compressed (High; measured on the downloaded file, whose mastering may differ slightly from the original upload).
- **Music bed:** a faint, continuous low-level tonal component is measurable about 20–25 dB under the voice and continues into the end screen. It could be a very quiet music bed, room tone or a codec artefact at this bitrate. **Genre, mood and tempo cannot be assessed.** At most, any music is kept far below the voice and never swells (Low).
- **Sound effects:** none were detectable at the checked events: title cards (4:42.8, 9:47.9), pull-quote entries (3:21.3), notes entries (2:10), hook collage pops (0:01.6–0:05.6) and the chapter menu. There were no broadband whoosh or pop transients beyond speech. Soft ping-like tones at the end screen (about 23:07–23:09) *might* be sparkle SFX or music (Low–Medium). **Conclusion:** the style uses few or no SFX; the edit is driven by the voice.
- **Voice clarity:** voice dominates by 20 dB or more, pauses are cut tight, and there are no competing effects. Any music should be ducked to about −28 to −32 dB below dialogue, or roughly −40 to −45 LUFS short-term under speech.

---

## B. Technique table

| # | Technique | What is observable | Approx. timing / trigger | Visual characteristics | Purpose | How to recreate | Confidence |
|---|---|---|---|---|---|---|---|
| 1 | Pause-free jump cutting | Constant flow, visible micro head-jumps | Every pause or breath; ≈ every 2–3 s | Same framing either side of the cut | Pace, density | Cut all gaps to 0.10–0.25 s; keep the best take; no speed change | High |
| 2 | Section title card | "N. Title" on cream | Start of each list item; 2.2–4.3 s | Centred condensed serif, brown on cream, static | Structure / chapter beat | Solid-colour card plus centred serif; hard cuts | High |
| 3 | Chapter menu grid | 2×5 rose tiles with timestamps | After the hook, before item 1; 6.7 s | Cream bg, serif title, rounded tiles | Promise and roadmap | Grid template; real chapter times | High |
| 4 | Side notes overlay | Tag heading plus white serif list, left third | When an item's key takeaways are spoken; 5–25 s; items pop on cue | Punch-in ≈1.2× with subject shifted right; captions off | Summarise / retain | Reframe plus text column; add items on cue | High |
| 5 | Dimmed pull-quote | Dark, blurred A-roll with centred white text | The key claim or punchline of a beat; ≈ every 55 s; 2–7.6 s | Sans regular plus bold keywords at y≈45 %; captions off | Emphasis, pattern break | Duplicate the clip, darken 60–70 %, blur, vignette, add text | High |
| 6 | Cream PiP info card | Rounded portrait PiP on the right; icon, heading and bullets on the left | Facts, costs, caveats, research; 7–40 s | Bullets pop as spoken; captions off | Deliver dense info without losing the face | Cream bg, 3:4 PiP with 24 px radius, serif hierarchy | High |
| 7 | Sub-item corner label | "2. Creatine" at the top-left | Throughout each sub-part | Small white serif, persistent | Orientation inside long sections | Static text layer that swaps per sub-item | High |
| 8 | Floating keyword labels | Words popping around the head | Each spoken item in a list; ≈0.7 s apart; hold ≈2 s, fade 0.3–0.5 s | Bold white sans, scattered | Visualise a quick list | Pop-in, timed fade-out | High |
| 9 | Hook photo collage | Tilted photo clusters with gold script words | First 8 s; one per spoken category | Corner clusters that pile up | Instant visual promise | Own photos, rotate ±5–10°, script label | High |
| 10 | Split hook lockup | "Being *High Maintenance*" / "To become *Low Maintenance*" | When the thesis contrast is spoken | Sans plus gold script, left and right of the head | Frame the paradox | Two lockups, popped in sequence | High |
| 11 | Concept icon card | "You put in" with Time / Money / Discipline icons | On each spoken word ≈0.5 s apart | Cream, centred, icons pop L→R | Explain the core idea | Own icon set, staggered pops | High |
| 12 | Personal proof B-roll | Selfie, POV and mirror demo clips | The noun or action just spoken; median ≈5 s | Phone footage, mixed grades | Credibility / demonstration | Shoot your own matching inserts | High |
| 13 | Vertical inset clip | 9:16 clip centred over dim A-roll | Referencing other people's content; 2–5 s | Rounded corners, dim / blur bg, captions on | Show an example without leaving the A-roll | Rounded mask plus dim background | High |
| 14 | Related-video card | White tile at the top-right | When another video is mentioned; ≈3 s | Thumbnail plus title, soft shadow | Cross-promotion | Original card graphic | High |
| 15 | Phrase captions | Single-line white text at the bottom | Continuous over A-roll / B-roll; every 0.6–1.5 s | Small geometric sans, no box | Accessibility, retention | Auto-transcribe, 3–6 words per cue, instant swap | High |
| 16 | Notes reframe punch-in | Tighter framing with the subject right | Only with notes overlays | ≈1.15–1.25× | Make room for text | Scale plus position keyframes on the cut (no animation) | High |
| 17 | Alternate jump-cut framing | Slightly tighter shots at some cuts | Sporadic | ≈1.05–1.1× | Soften jump cuts | Alternate 100 / 108 % within a thought | Low–Med |
| 18 | End screen | Pastel gradient, sparkles, circle photo, Subscribe, "Watch this next" | Final ≈10 s | Twinkling sparkles; scale-in over ≈0.3–1 s | CTA / session time | Own gradient plus vector sparkles; leave empty zones | High |
| 19 | Minimal / no SFX | No transients at graphic entries | n/a | n/a | Calm, voice-led | Optional very soft UI ticks at ≤ −30 dB | Medium |
| 20 | Music bed (if any) | Faint continuous low-level tone | Whole video | ≥20 dB under voice | Warmth without distraction | Lo-fi or acoustic bed, ducked hard under the voice | Low |

---

## C. Reusable editing rules (for an editing agent)

1. **Cut every silence** longer than 0.25 s down to 0.10–0.20 s (0.25 s at a sentence end that needs a beat). Never cut inside a word; keep the onset breath only if it is under 0.15 s. Do not speed up the audio.
2. **Keep only the best take** of any repeated sentence. Remove false starts, "wait, let me say that again" and stumbles. Keep fillers only if they read as personality, at most one per minute.
3. **Leave jump cuts visible.** Do not add dissolves or morph cuts. If two consecutive cuts produce a jarring jump, cover the second with B-roll, a text pop or a 100↔108 % framing alternation.
4. **Never leave the plain A-roll unbroken for more than about 30–40 s.** Insert, in priority order: relevant B-roll, a notes overlay, a pull-quote, or a card.
5. **Every list item opens with a full-screen title card** (2.5–3.5 s, hard cut in and out). The item number and name are mandatory.
6. **After the hook, show a chapter menu** listing every item with its real timestamp, held 5–7 s.
7. **Every graphic enters on a hard cut or an instant pop synced to the word that triggers it,** and leaves on a cut. Animate in at most 4–8 frames (a subtle fade, drift or scale). No bounces, slides across the frame or spins.
8. **Reveal list items one at a time** at the moment each is spoken.
9. **Do not show captions and another text block at once.** Turn captions off during title cards, notes overlays, pull-quotes, cream cards and the end screen. Turn them on everywhere else.
10. **Use pull-quotes for the single most important sentence** of a beat, about one per 45–75 s. Paraphrase to 12 words or fewer and bold 1–3 keywords.
11. **Use a notes overlay when the speaker gives 2–4 takeaways, rules or misconceptions.** Reframe ≈1.2× to the right, keep the list in the left third, and add items on cue.
12. **Use a cream PiP card for numbers, costs, frequencies, caveats or research.** Keep the speaker visible in the PiP.
13. **B-roll must show the exact thing being said** (product, action, result). Cut in mid-sentence, cut out on a sentence boundary, and keep captions on.
14. **In multi-part sections, keep a corner sub-label** ("1. …", "2. …") on for the whole sub-part.
15. **Hook (first 8–20 s):** no captions; decorative, layered graphics that visualise the categories the speaker lists; one dense B-roll flash-forward of the payoff.
16. **Colour:** derive a 4-colour graphics palette (paper, ink, accent, secondary accent) from the target video's set and wardrobe, and use it everywhere. Leave the B-roll mostly ungraded, but correct obvious white-balance clashes.
17. **Audio:** dialogue at about −16 LUFS integrated for platform delivery (the reference measures −19.1). Music, if used, ducked 25–30 dB under speech. Sound effects are not required; if used, they must be soft (≤ −30 dB under the voice) and rare.
18. **End with a 10 s end screen** in the palette, with empty zones for platform elements and a subscribe prompt.

---

## D. Motion-graphics and caption presets

Values are for a **1920×1080, 30 fps** timeline. Parameters marked "est." are recreations, not measurements.

```yaml
palette:            # replace with the target video's own palette; keep the relationships
  paper:      "#FEF2D6"   # warm cream (approx. reference)
  ink:        "#3A2618"   # espresso brown (est.)
  ink_soft:   "#756348"   # secondary text
  tag_bg:     "#EFECE1"   # off-white label
  accent:     "#976563"   # dusty rose tiles
  highlight:  "#E5AC60"   # warm gold keywords / script
  on_video:   "#FFFFFF"
  end_grad:   ["#D8A99D", "#C4A6C7", "#B2A1EC"]

fonts:              # stand-ins with similar character; exact reference fonts unknown
  serif_condensed: "Gloock | Instrument Serif | Playfair Display (condensed width) | Libre Caslon Condensed"
  sans_quote:      "Inter | Helvetica Neue | SF Pro"
  sans_caption:    "Raleway Medium | Montserrat Medium | Poppins Medium"
  script:          "Great Vibes | Allura | Pinyon Script"

entry_default:      # applied to every overlay unless stated
  type: pop                 # appears on the cut / on the word
  optional_ease: {frames: 4-6, opacity: [0, 100], translate_y_px: [8, 0], easing: easeOutCubic}  # est.
  exit: hard_cut            # or 4-frame fade

presets:
  title_card:
    bg: paper
    text: {font: serif_condensed, size_px: 80, color: ink, align: center, y: 50%}
    hold_s: 3.0              # range 2.2-4.3
    transition_in_out: hard_cut
    captions: off

chapter_menu:
    bg: paper
    title: {font: serif_condensed, size_px: 64, color: ink, lines: 2, y: 20%}
    grid: {rows: 2, cols: 5, margin: 8%, gutter: 1.5%, tile_color: accent, radius_px: 8}
    tile_text: {font: serif_condensed, size_px: 22, color: "#2B1A10"}
    tile_time: {font: sans_quote, size_px: 16, align: bottom_right}
    hold_s: 6.5
    captions: off

notes_overlay:
    reframe: {scale: 1.20, subject_x: 55-58%, applied_on: cut}
    tag: {bg: tag_bg, padding_px: [10, 14], text: {font: serif_condensed, size_px: 32, color: ink_soft, max_lines: 2}, x: 8%, y: 8%}
    body: {font: serif_condensed, size_px: 36, color: on_video, line_height: 1.15, item_gap_px: 22, width: 28%, shadow: "0 1px 3px rgba(0,0,0,0.35)"}
    reveal: per_item_on_spoken_cue
    hold: until_topic_ends (5-25 s)
    captions: off

pull_quote:
    background: {source: underlying_a_roll, exposure_stops: -1.8, blur_px: 8, vignette: 0.35}
    text: {font: sans_quote, weight: regular, emphasis_weight: bold, size_px: 48, color: on_video, align: center, y: 45%, max_lines: 2, max_chars_per_line: 48}
    hold_s: reading_time + 0.5   # observed 2-7.6, median 4.0
    variant_intro: {font: serif_condensed, emphasis_color: highlight}
    captions: off

pip_info_card:
    bg: paper
    pip: {x: 62-94%, y: 10-90%, aspect: "3:4", radius_px: 26, stroke: none, shadow: "0 6px 18px rgba(60,40,20,0.15)"}   # shadow est.
    icon: {x: 3%, y: 8%, size_px: 90}
    heading: {font: serif_condensed, size_px: 44, color: ink_soft}
    bullets: {font: serif_condensed, size_px: 30, color: ink, prefix: "- ", indent_px: 24}
    reveal: block_by_block_on_cue
    captions: off

sub_label:
    text: {font: serif_condensed, size_px: 34, color: on_video, x: 2%, y: 3%, shadow: "0 1px 2px rgba(0,0,0,0.4)"}
    persists: whole_sub_section
    captions: on

floating_keywords:
    text: {font: sans_quote, weight: bold, size_px: 40, color: on_video}
    placement: ring_around_head, avoid_face
    in: pop_on_word
    hold_s: 2.0
    out: {fade_frames: 12}

hook_collage:
    cluster: {photos: 2-3, rotation_deg: [-10, 10], border_px: 5, shadow: soft, width: 27%}
    label: {font: script, size_px: 72, color: highlight}
    order: TL, BR, BL, TR
    in: pop_on_word  # optional overshoot 90->103->100% over 6 frames (est.)
    clear: all_on_next_cut

vertical_inset:
    frame: {aspect: "9:16", height: 86%, x_center: 50%, radius_px: 22}
    background: {exposure_stops: -1.3, blur_px: 10}
    captions: on

related_video_card:
    box: {x: 62-96%, y: 8-50%, bg: "#FFFFFF", radius_px: 14, shadow: soft}
    hold_s: 3.0

captions:
    font: sans_caption
    size_px: 40            # est.: reference cap-height ~3.5% of frame height
    color: "#FFFFFF"
    stroke: none
    shadow: "0 1px 3px rgba(0,0,0,0.45)"   # add for safety; reference shows none visible
    position_y: 91%        # reference ~95%; raised for platform UI safety
    max_words: 6
    max_chars: 35
    lines: 1
    animation: none        # instant phrase swap, no word highlight
    case: sentence
    hidden_during: [title_card, chapter_menu, notes_overlay, pull_quote, pip_info_card, end_screen, hook_first_8s]

end_screen:
    bg: {gradient: end_grad, direction: top_to_bottom}
    sparkles: {count: 8-12, shape: 4-point_star, loop_s: 1.0, scale: [0.6, 1.0], opacity: [0.4, 1.0], stagger: random}
    avatar_circle: {x: 22%, y: 25%, d: 22%, in: scale 0->100% over 9 frames easeOutBack}
    elements: ["Watch this next" + hand-drawn arrow (top-right), Subscribe outline pill (bottom-left), credits (bottom-right, 16px)]
    reserve_empty_zones_for_platform_end_cards: true
    hold_s: 10
```

---

## E. Decision rules: when to use each tool

| Trigger in the speech | Use | Avoid |
|---|---|---|
| Any pause or breath over 0.25 s, a stumble, or a retake | **Jump cut** | Crossfade or morph cut |
| A new numbered item | **Title card** (hard cut) | Starting the item on the A-roll without a card |
| Speaker names a product, tool, action or visible result | **B-roll** of that exact thing, 2–8 s, captions on | Generic mood stock |
| Speaker refers to someone else's content or trend | **Vertical inset** over dim A-roll | Full-screen third-party footage |
| Speaker lists 2–4 takeaways, steps or misconceptions | **Notes overlay** plus ≈1.2× reframe, items on cue | Captions at the same time |
| Numbers, prices, frequency, eligibility, research | **Cream PiP card** with bullets popping on cue | Dumping all bullets at once |
| The single sentence that sums up the beat, a warning or a punchline | **Pull-quote** (dim plus centred text with bold keywords) | More than one quote per 45 s, except in the wrap-up |
| A rapid spoken list of short nouns | **Floating keyword labels** | Full card for 1-word items |
| A multi-part section | **Corner sub-label** for each part | Removing it during B-roll |
| A mention of another of your own videos | **Related-video card** for 3 s | Leaving it on more than 4 s |
| A pure opinion or reflection stretch with nothing to show | Let the A-roll run (≤ 40 s), break it with one pull-quote | Decorative zooms or random B-roll |
| End of video | Wrap-up pull-quotes, CTA on the A-roll, **end screen 10 s** | Music swell or long goodbye |

Zoom rules: reframe **only** for side text; optional 100/108 % alternation to soften consecutive jump cuts; no zoom on every sentence, no slow push-ins, no zoom transitions.

Transition rules: hard cuts only. A 4–6 frame ease on overlay entry is acceptable; a 10–14 frame fade-out is acceptable for floating labels.

---

## F. Recommended editing sequence (opening hook to ending)

| # | Beat | Target length | Treatment |
|---|---|---|---|
| 1 | **Cold-open hook** | 0:00–0:08 | A-roll, no captions. Layered collage or labels visualising the 3–5 things the video covers, each popping on its spoken word. |
| 2 | **Payoff flash-forward** | 0:08–0:16 | Captions start. 2–4 quick B-roll shots of results or the process (1–2.5 s each). One serif text overlay on the strongest claim. |
| 3 | **Thesis contrast** | 0:16–0:20 | Split lockup (sans plus script) on both sides of the head. |
| 4 | **Concept card** | 0:20–0:30 | Cream card; icons or keywords pop on each word; optional speaker inset. |
| 5 | **Credibility and context** | 0:30–0:40 | A-roll plus 1–2 relevant B-roll shots. |
| 6 | **Disclaimer / framing quote** | about 0:40 | First pull-quote (serif with accent-colour keywords). |
| 7 | **Quick list / why it matters** | 0:42–0:59 | Floating keyword labels, then a short selfie B-roll montage. |
| 8 | **Chapter menu** | about 1:00, 5–7 s | Grid of all items with timestamps. |
| 9 | **Item loop** (repeat for each item) | 1–3.5 min each | (a) title card 2.5–3.5 s; (b) A-roll explanation with jump cuts and captions; (c) B-roll proof on the nouns; (d) notes overlay with reframe for takeaways; (e) 1–2 pull-quotes on the key claim or warning; (f) optional cream PiP card for facts and costs; (g) optional corner sub-labels for multi-part items; (h) a final A-roll line that ends the item, then a hard cut to the next title card. |
| 10 | **Wrap-up** | about 40 s | 2–3 pull-quotes close together carrying the moral, short A-roll CTA ("if you enjoyed it…"), a goodbye gesture with a 1-word caption. |
| 11 | **End screen** | 10 s | Pastel gradient in the palette, sparkle loop, avatar circle, "Watch this next", subscribe prompt, credits; leave zones for platform elements. |

Pacing targets for the target video: one A-roll jump cut every 2–3 s on average; some visual change every 1.5–2.5 s; a pattern break (B-roll, quote, notes or card) at least every 30–40 s; a pull-quote every 45–75 s; B-roll at 15–20 % of runtime; graphics cards at 6–10 %; dimmed quotes at about 8 %.

---

## G. What cannot be established confidently from the low-resolution reference

1. **Exact typefaces.** Only the classes are certain: condensed serif, neo-grotesk sans, geometric caption sans and a formal script.
2. **Exact colour values.** Compression shifts the samples; small text colours are especially unreliable because of antialiasing. Treat all hex values as ±10–15 %.
3. **Sub-100 ms animation details.** Whether "instant" pops actually have a 1–3 frame fade, scale or blur cannot be told at this resolution.
4. **Caption styling details.** Any faint shadow or outline, the exact weight, and the precise font size.
5. **Drop shadows** under notes text, the PiP frame and cards.
6. **Exact zoom percentages.** The ≈1.2× notes reframe is solid. The secondary ≈1.05–1.1× framing is uncertain, because face-size measurements mix zoom with leaning.
7. **Blur radius and darkening** of the pull-quote background. Only an approximate 30–40 % brightness is measurable.
8. **Music:** whether there is a bed at all, plus its genre, tempo and level. The low-bitrate audio leaves only a faint continuous tonal component, which may be an artefact.
9. **Sound effects:** none were detected, but soft, low-level UI sounds (under about −40 dB) would not be distinguishable.
10. **Original mastering.** −19.1 LUFS was measured on the re-encoded download; the original upload may differ.
11. **Exact cut count.** Automatic detection mixes jump cuts with gesture and text-pop changes; only about ⅔ of the sampled weak detections were confirmed cuts.
12. **Colour grading** beyond "warm, natural, moderate contrast". Fine details of skin, highlight roll-off and black level are lost.
13. **Origin and licensing of clinic and third-party B-roll.** Do not reuse any of it; replace it with your own or licensed footage.
14. **Exact screen-time split.** The percentages come from automatic brightness and face classification and are about ±3 % each.
