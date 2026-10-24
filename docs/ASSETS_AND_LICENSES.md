# Assets and licences (stage 2 edit)

Every external asset used in the edit is listed here. **No stock footage, stock music or stock SFX is used.** The licensed libraries (Pexels, Pixabay, Wikimedia Commons, Free Music Archive, Incompetech, Freesound, Mixkit, Unsplash) are blocked by this environment's network policy.

| Asset | Used for | Source | Licence | Monetised YouTube |
|---|---|---|---|---|
| Original footage | A-roll, picture-in-picture | Your recording (Google Drive file `1NQAYdsSO12AwiJ4y2TmqecT_eLVoAnot`) | Yours | ✅ |
| Background music "Twenties" (78 BPM, D major) | Music bed | **Original**, synthesised from scratch by `tools/compose_music.py` (no samples) | Original work created for this video; no third-party rights | ✅ (no Content ID claims possible) |
| SFX: pop / swish / swell | Notes items and keywords / cards / pull-quotes | **Original**, synthesised by `tools/make_sfx.py` | Original; no third-party rights | ✅ |
| B-roll illustrations (castle film frame, budget card, …) | B-roll inserts | **Original** HTML/SVG illustrations, `tools/gfx.py` | Original; no third-party rights | ✅ |
| Instrument Serif | Titles, notes, cards | npm `@fontsource/instrument-serif` | SIL Open Font License 1.1 | ✅ |
| Poppins (Latin + Devanagari, merged) | Captions | npm `@fontsource/poppins` (Indian Type Foundry) | SIL OFL 1.1 | ✅ |
| Noto Sans Devanagari | Fallback (Devanagari) | npm `@fontsource/noto-sans-devanagari` | SIL OFL 1.1 | ✅ |
| Inter | Pull-quotes, keyword labels | System font package / `@fontsource/inter` | SIL OFL 1.1 | ✅ |
| Great Vibes, Caveat | End-screen script, hand-written labels | npm `@fontsource/great-vibes`, `@fontsource/caveat` | SIL OFL 1.1 | ✅ |

Speech recognition and voice-activity models are used only for analysis; none of their output is published:
- NVIDIA Parakeet TDT 0.6B v2, CC-BY-4.0
- OpenAI Whisper, MIT
- Silero VAD, MIT

All of them ran locally, and no footage was uploaded anywhere.

## Gaps (flagged, not faked)
- **No real B-roll footage.** The reference uses personal-proof clips (selfie, product, demo), about 14–19 % of its runtime. This edit uses **7 original illustrated inserts**, each timed to your own words. Together they run about 40 s, roughly 6 % of the 10:54 runtime:

  | Insert | Output time | Length | What it shows |
  |---|---|---|---|
  | B1 | 0:36 | 3.6 s | "seek help / seek advice from other people": figure with "?", advisers appear |
  | B2 | 0:48 | 3.0 s | "thirty next year": "Next year" calendar, 30 circled |
  | B3 | 2:33 | 5.2 s | Prince Charming / movies: fairy-tale castle in a film frame (approved in test) |
  | B4 | 3:54 | 4.5 s | "handle your finances": budget card (approved in test) |
  | B5 | 4:54 | 5.5 s | "scroll, watch a YouTube video, watch a movie": phone feed → generic video card → clapper (no YouTube branding) |
  | B6 | 6:34 | 4.5 s | "tell us what to do, what not to do": bubbles with ✓ / ✗ |
  | B7 | 8:38 | 13.6 s | "a trip… a degree… where to travel… buy or not… which city": signpost, one arm per choice |

  To get closer to the reference, either:
  - (a) shoot or upload your own short clips (journaling, baking, laptop budgeting, travel), or
  - (b) allow `pexels.com` / `videos.pexels.com` / `cdn.pixabay.com` in the environment's network settings. Both are free libraries with commercial-use licences. I'd still list each clip here before using it.
- **Music is original and synthesised**, not a produced library track. If you'd prefer a YouTube Audio Library track, download one (it needs your YouTube login) and I'll swap it in with the same ducking.
