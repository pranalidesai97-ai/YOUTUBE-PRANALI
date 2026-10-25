# Final export: quality-check report

**File:** `Lessons_from_my_twenties_FINAL_1080p30.mp4`, 498,491,992 bytes (**475 MB**, about 0.5 GB)

**Source:** the original recording, unchanged. It is read-only and its SHA-256 checksum matches the download. The final is a new file; the source and the test renders were not overwritten.

## Format

| Check | Result |
|---|---|
| Resolution / aspect | 1920×1080, SAR 1:1, DAR **16:9** ✅ |
| Frame rate | **30/1 constant** (r = avg = 30/1) ✅ |
| Frames | **19,577 / 19,577** expected ✅ |
| Duration | video 652.567 s · audio 652.566 s (**10:52.6**) ✅ |
| Video codec | H.264 High, yuv420p, BT.709; x264 **crf=16.0**, preset slow (ref=5, subme=8), keyframe every 2 s ✅ |
| Audio codec | **AAC-LC 256 kb/s target** (252 kb/s measured), **48 kHz stereo** ✅ |
| Streaming | `moov` at the front (faststart) ✅ |
| Full decode, start to end | **0 errors** ✅ |

## Picture

| Check | Result |
|---|---|
| Black frames | none ✅ |
| Still stretches | Chapter menu (6 s), 5 title cards (3 s each) and end screen (10 s): intended. Two brief holds inside **B5** (phone, 4:54–4:59) and three inside **B7** (signpost, 8:40–8:45): the illustration pauses between spoken cues, intended. None elsewhere ✅ |
| Graphics present | 7 B-roll inserts, 8 pull-quotes, 3 notes overlays, 2 keyword sets, 2 picture-in-picture cards, corner card, chapter menu, 5 title cards, end screen: all verified on exported frames ✅ |
| Hindi captions | 5 Devanagari cues, rendered with complex shaping. Conjunct and pre-base vowel placement (किसी, मुझे, चीज़ें, नहीं, बचाएगा, ।) verified on the exported frames ✅ |

## Audio

| Check | Result |
|---|---|
| Loudness | −16.0 LUFS integrated, LRA 4.3 LU, true peak −1.5 dBTP ✅ |
| Dropouts / abrupt gaps | none below −55 dB for ≥ 0.25 s ✅ |
| Music under speech | ≈18 dB below the voice on average (measured on the test); ducks automatically; fades out over the last 3 s ✅ |
| Speed | no speed change or time-stretch anywhere ✅ |

## Sync, at 12 points spread through the video

- **Audio vs. original:** 0.0 to ±0.5 ms at every point ✅
- **Picture vs. original:** within ±1 frame. That is the resolution of the measurement against the phone's slightly variable frame timing. Each cut point was separately verified to land within half a frame (≤17 ms) ✅

## Visual review sheets

- `FINAL_qc_start_end.jpg`
- `FINAL_qc_chapter_transitions.jpg`
- `FINAL_qc_broll_inserts.jpg`
- `FINAL_qc_graphics.jpg`
- `FINAL_qc_every_minute.jpg`
- `FINAL_qc_hindi_captions.png`

## Found and fixed during the final checks

1. **Leftover word slivers at three approved cut points**, visible in the captions as "**And** decision making…", "Sometimes **sometimes**…" and "**they they** also…". The cut-edge logic was fixed. All 29 approved removals are now complete, no kept word was lost, and nothing removed came back. Runtime went from 10:53.9 to 10:52.6.
2. **The picture-in-picture cards would not render** (odd 827 px box height); they now use 826 px.
3. **The last 3 frames of the end screen were dropped** when the chunks were joined (ffmpeg `-shortest`). The file was re-joined without re-encoding and now has exactly 19,577 frames.
4. **The caption "Hi" was missing** from "Hi everyone, welcome to my channel." The fragment filter treated it as a cut-off word. Restored; only that 30 s chunk was re-rendered.

## Known, intentional or minor

- **"oh" dropped at 1:59.** The caption reads "Which never happens." as you reviewed it. The spoken "oh" is dropped by the clean-verbatim style; tell me if you'd like it shown.
- **Pull-quote PQ3 (4:03) wraps** its last word "life." onto a second line. Cosmetic only.
- **Chapter menu text is small.** It matches the approved style frame; the tiles carry 1:09 / 3:43 / 4:45 / 6:29 / 7:55.
- **No external footage, music or SFX were used.** See `ASSETS_AND_LICENSES.md`.
- **H.264 level 5.0.** Fine for YouTube and recent tablets; very old devices may only play the 720p preview copy.

---

## v2 master (Champagne Editorial opening, Subscribe reminder, 18 s end screen), 2026-10-24

`Lessons_from_my_twenties_FINAL_v2_1080p30.mp4`: 507,055,596 bytes, SHA-256 `a4111b56832a5ed6a48c58166c09d65a8c52da2fdcb28d530e548799e4887f4d`.
Rendered in one pass from the original (source SHA-256 re-verified). Full data: `docs/FINAL_v2_qc_report.json`; sheets `docs/FINAL_v2_qc_*.jpg`.

| Check | Result |
|---|---|
| Video | H.264 High, 1920×1080, 30/1 CFR, yuv420p BT.709, **19,817 frames** (= EDL 660.567 s), CRF 16, faststart |
| Audio | AAC-LC 48 kHz stereo, 252 kb/s, 660.566 s |
| Decode errors / black frames | none / none |
| Freezes | same as v1 (cards, intended B5/B7 holds) plus the end screen hold |
| Loudness | −16.0 LUFS, LRA 4.5 LU, true peak −1.5 dBTP; no dropouts |
| Sync vs source (12 points) | picture within ±1 frame, audio 0.0 to −0.5 ms |
| Audio continuity | 30,966 AAC packets, 0 timestamp gaps; sample-exact (lag 0, corr 1.0000) against the continuous rendered mix at 21 points incl. 5:26.5–5:29.0 |

The v1 two-part delivery, rejoined by stream copy, sits a constant 1024 samples (21.3 ms) off the mix throughout. That came from the split/join, not the mix. v2 is delivered as one file, split byte-for-byte (`split`, `.001`/`.002`), which rejoins to the identical SHA-256.

---

## v3 master (opening title as a side panel during the greeting), 2026-10-25 — current final

`Lessons_from_my_twenties_FINAL_v3_1080p30.mp4`: 507,899,574 bytes, SHA-256 `456b39e31f077381e6097c1f34e53ceab4339f9dc89ae1120dca36010bb0f831`.
Only render chunk 0 (0:00–0:39.9, which holds the revised opening) was re-rendered from the source; the other 19 chunks and the audio mix are byte-identical to v2.
Full data: `docs/FINAL_v3_qc_report.json`.

| Check | Result |
|---|---|
| Video | H.264 High 1920×1080, 30/1 CFR, **19,817 frames**, faststart |
| Decode errors / black frames | none / none |
| Loudness | −16.0 LUFS, LRA 4.5 LU, true peak −1.5 dBTP; no dropouts |
| Sync vs source (12 points) | picture within ±1 frame, audio −0.5 to +0.2 ms |
| Audio continuity | 0 packet gaps; sample-exact vs the continuous mix and vs v2 (incl. 0:06.5 and 5:27.8) |
| Jump-cut framing | 106 % punch-in at 0:06.4 kept |

Delivered as `.001`/`.002` byte-exact pieces (rejoin verified against the SHA-256) + a 720p preview.
