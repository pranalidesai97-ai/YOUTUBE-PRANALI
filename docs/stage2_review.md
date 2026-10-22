# Stage 2: review before the final render

Status: **review cut and captions ready for proofreading. Graphics shortlist proposed. Final render not started.**
Times are **output** times in `review_cut_540p.mp4` unless marked "src" (original file).

## 1. What was cut

| | Count | Removed |
|---|---|---|
| High-confidence retakes / restarts / redundant takes | 25 (+ pre-roll R1) | ≈282 s |
| Standalone fillers (isolated "Uh" src 7:56, mid-list "um" src 8:47) | 2 | ≈4 s |
| Pauses tightened (to 0.20 s mid-sentence / 0.30 s at sentence end) | 89 | ≈58 s |

- **Runtime:** 16:27 → **11:13.9**, including 6 s chapter menu, 5 × 3 s title cards and the 10 s end screen.
- **Cut list:** every removal, with source timestamps and the exact words removed, is in `stage2_cuts.csv`. The decisions behind it are in `stage2_cuts.json`.
- **Pause rules:**
  - A pause only shrinks if it is longer than 0.35 s, is quiet throughout, and contains nothing the voice detector rates as possible speech.
  - Breaths louder than room tone stay in.
  - Pauses shorter than 0.35 s are left alone.
  - No speed change anywhere.
- **Word boundaries:** cut points are set from the audio itself (10 ms resolution), not only the transcript, so no word onset or tail is clipped.

### Held for your review (left in, unchanged)

| ID | src | Output | What to listen for |
|---|---|---|---|
| R6 | 3:09–3:41 | ≈1:41–2:09 | First attempt at "don't wait for someone to rescue you", plus the Prince Charming / kingdom lines (partly Hinglish) |
| R8 | 4:08–4:14 | ≈2:27–2:32 | "Okay, be your pillow(?)": maybe "be your own pillar" |
| R12 | 5:58–6:28 | ≈3:27–3:44 | Off-camera conversation ("Three, do you want? No. No…") plus "So take charge of your life, or so / take charge of your life / and uh" |
| R14 | 7:35–7:52 | ≈4:57–5:02 | "Okay." + "Tourism(?)". The 12 s silence was tightened; the "Okay." is kept. The title card sits right before "Tourism" (probably "Third is") |
| R15 | 7:52 | ≈5:02 | "Find your happiness, find where your happiness lies" |
| R20 | 10:29–10:34 | ≈7:09 | Second "It's just absolutely important for you to know yourself first" |
| (medium) R25 | 12:19 | ≈8:32 | "as a female we as… Oh. Indian parents…" |
| (medium) R31 | 15:17–15:21 | ≈10:33 | "they know you. Better. They they also know you better." |
| (note) | src 1:16 | 0:16 | "If you are in your twenties, I am sure this video is definitely going to help you" repeats the thought of your opening line at 0:00 (both kept) |

## 2. Captions: please proofread

- **`captions_review.srt`:** every uncertain word is shown as `[?word?]`. The review cut has these burned in, so you can check them in context.
- **`captions_flags.csv`:** the 40 flagged cues with output times and reasons.
- **Style:** clean verbatim. Your words exactly as spoken, Hinglish kept, minus "uh/um" and cut-off word fragments. Sentence case, phrase by phrase.
- **Hinglish passages:** written in Roman script, **not translated**. These are reconstructions; no local model could transcribe the Hindi reliably, so please correct them.
  - 1:18 (src 2:45): *"kaash mujhe kisi ne pehle bata diya hota, toh main alag cheez karti."*
  - 2:34 (src 4:21): *"…ki Prince Charming aayega humare liye, but aisa nahi hota."*
- **Likely misrecognitions** (suggested fix in brackets):
  - "At Witz" (**Netflix?**, already applied, still flagged)
  - "Tourism" (Third is?)
  - "Very oddly" (very early?)
  - "somewhat other way" (some or the other way?)
  - "a person. personal financing"
  - "be your pillow"
- **Two caption files:** `captions.srt` is the clean version for YouTube's caption track. The burned-in version will hide captions wherever a title card, notes overlay, pull-quote or picture-in-picture card is on screen.
- **How to send corrections:** edit the text in `captions_review.srt` (keep the numbers and times), or just list `cue number → correct text`.

## 3. Lesson titles

| # | Title | Card at | Transcript check |
|---|---|---|---|
| 1 | Don't Wait to Be Rescued | 1:10 | ✅ matches "do not wait for someone to rescue you" |
| 2 | Take Control of Your Finances | 3:56 | ✅ her exact words |
| 3 | Build Happiness and Creative Outlets | 4:58 | ⚠ You say "**find** your happiness / find where your happiness lies" and "have a creative outlet". "Build" shifts it slightly; the transcript suggests *"Find Your Happiness and a Creative Outlet"* |
| 4 | Know Yourself | 6:43 | ✅ "know yourself first … filter out the noise" |
| 5 | Make Better Decisions | 8:12 | ⚠ Your point is learning to make **your own** decisions, and that "sometimes your decisions will go wrong, and that's absolutely okay". "Better" implies decision quality; the transcript suggests *"Learn to Make Your Own Decisions"* |

Titles are used exactly as you gave them unless you choose otherwise.

## 4. Pull-quotes: shortlist of 7 (down from 11)

All quotes use **your own words** (trimmed only), so the meaning can't drift. **Bold** = emphasised words.

| # | Output | Quote | Why it earns a quote |
|---|---|---|---|
| PQ1 | 2:10 | "Take all the help you need, but **do not wait** for someone to **rescue** you." | Thesis of lesson 1 |
| PQ2 | 3:14 | "**Take charge** of your life." | The action for lesson 1 |
| PQ3 | 4:16 | "Whoever is **paying** for you is going to **control** your life." | Strongest line of lesson 2 |
| PQ4 | 5:21 | "It is absolutely important to have a **creative outlet**." | Thesis of lesson 3 |
| PQ5 | 7:34 | "People will tell you what to do based on **their own experiences**." | Key insight of lesson 4 |
| PQ6 | 10:39 | "Definitely listen to them, **and then** take the decision." | Resolves lesson 5 (advice vs. deciding) |
| PQ7 | 10:53 | "Be **confident**. Be **bold**." → "Do not shy away from **speaking your heart** out." | The closing message (one 2-step quote) |

**Dropped**, with reasons:
- 0:40 "We forget to look inward": a paraphrase in the intro, with keywords already there.
- 7:02 "Clear the noise, know yourself first": the "Know your…" notes 43 s later say the same thing.
- 9:17 "Waiting for approval drops your confidence": the decisions-and-confidence picture-in-picture card covers it.
- A separate second wrap-up quote: merged into PQ7.

Spacing is about one quote every 60–90 s, with none closer than 45 s.

## 5. Other graphics (restrained; all hard-cut in, 5-frame ease, nothing decorative)

| Output | Element | Content (on spoken cue) |
|---|---|---|
| 0:26 | Keyword labels | relationships · finances · mental health · physical health, white Inter Bold on the wall, each popping on its word |
| 1:04 | Chapter menu (6 s) | 5 tiles with real timestamps |
| 2:43 | Notes, right wall | **"Who decides for you?"** parents · partner · "someone will rescue you" |
| 4:34 | Notes, right wall | **"Learn the basics"** investment · budgeting · stock market · personal finance |
| 5:37 | Keyword labels | crocheting · baking · singing · dancing · pottery · journaling |
| 6:11 | Picture-in-picture card | **"Write it down"** What do I like to do when I'm bored? / Am I just scrolling? / Or am I doing something creative? |
| 7:45 | Notes, right wall | **"Know your"** values · ethics · non-negotiables · boundaries |
| 8:55 | Keyword labels | a trip · a degree · where to travel · which city to live in |
| 9:44 | Picture-in-picture card | **"Decisions build confidence"** Take 10 decisions / maybe 2 go wrong / 8 go right / those 8 give you confidence for the next 50 |
| 10:11 | Small top-right card, 3 s | "Want a video on decision making? **Comment below**" |
| 11:04 | End screen (10 s) | Gradient, circle photo, "Watch this next" zone, Subscribe. Channel name still needed |

- **Changes from the plan:**
  - The split "in your twenties" lockup at 0:06 is dropped as decorative.
  - The "creative outlets" notes overlay becomes keyword labels, because a spoken list of 7 short nouns is better as labels than a 7-line column.
- **Zooms:** the subtle **106%** alternate framing goes only on the most visually jarring jump cuts. 17 of 111 joins qualify; those already covered by a graphic are skipped. There are no other zooms; notes sit on the empty wall at 100%.
- **Placement checks:** notes and keyword placement will be checked frame by frame against your hand gestures in the test render.

## 6. Sync and quality checks on the review cut

- **Duration:** video and audio are both 673.900 s, matching the cut list exactly.
- **Frame alignment:** spot checks at the start and middle are exact. Near the end it's within **1 frame (33 ms)**, caused by the source's slightly variable frame rate, which is below perceptible lip-sync error. The final render re-checks this.
- **What the review cut leaves out:** it's 540p, fast-encoded, and has **no audio clean-up and no graphics**. The final render applies the stage-1 audio chain and full quality.

## 7. Next steps after your answers

1. **Captions:** apply your corrections.
2. **Held sections:** cut or keep R6 / R8 / R12 / R14 / R15 / R20 (plus R25 / R31) as you decide.
3. **Titles and graphics:** use your choices for titles 3 and 5 and confirm the pull-quote shortlist.
4. **End screen:** add your channel name.
5. **Test render:** about 90 s of full quality with every element type.
6. **Full render:** about 60–75 min.
