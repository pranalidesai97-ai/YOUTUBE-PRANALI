# Caption flags for review (stage 2)

- **Times:** "Output" times are in the current edit (10:53.9); "source" times are in your original recording.
- **Cue numbers:** these refer to `docs/stage2_captions.srt`.
- **Status:** nothing here has been resolved silently. Every cue below keeps its current text until you choose an option or type a correction.
- **How to reply:** for example, "37–39: A", "71: B", "138: type 'Third is'".

## Needs your confirmation: 16 cues

| # | Cues | Output | Source |
|---|---|---|---|
| 1 | 37, 38, 39 | 00:01:18 | 2:45.5 |
| 2 | 53, 54, 55, 56 | 00:01:50 | 3:20.0 |
| 3 | 69 | 00:02:28 | 4:09.3 |
| 4 | 71 | 00:02:34 | 4:24.3 |
| 5 | 121 | 00:04:07 | 7:02.1 |
| 6 | 130 | 00:04:24 | 7:19.1 |
| 7 | 138 | 00:04:48 | 7:48.9 |
| 8 | 182 | 00:06:12 | 9:37.6 |
| 9 | 226 | 00:07:38 | 11:26.8 |
| 10 | 242 | 00:08:09 | 12:21.0 |
| 11 | 316 | 00:10:31 | 16:06.1 |

### 1. Cues 37, 38, 39: Hindi sentence (Hinglish passage 1)
- **Output time:** 00:01:18
- **Source time:** ≈2:45.5

**Surrounding speech** (previous cues, *flagged cues*, following cues):

> 35  making so many mistakes in our  
> 36  life and we often think like  
> 37  **काश मुझे किसी ने पहले बता**  
> 38  **दिया होता, तो मैं अलग चीज़ें**  
> 39  **करती।**  
> 40  But  
> 41  but still we end up making  

**What the recognisers heard:**

- **Parakeet (English model):** "ka sha macha kisi na pai laba ta diya auta to me alak chi sa karati"
- **Whisper small.en:** "shyamu Chaka Sine Pahele Bata … ta Doma Alapchi Sukharti"
- **Whisper (English mode, translating):** "Kashi, you must tell me before, so I will do a lot of things"
- **Whisper-medium (Hindi), twice:** "तो मैं अलग चीज़े करती।" (end of the sentence only)

**Suggested alternatives** (not applied):

Caption now: **काश मुझे किसी ने पहले बता दिया होता, तो मैं अलग चीज़ें करती।**
- Well supported: काश · किसी ने · पहले · बता दिया होता · तो मैं अलग चीज़ें करती
- **Least certain: मुझे** (only Parakeet's "macha" hints at it). Possible alternatives: मुझे / मुझको / *(no word)*
- Also possible: चीज़ें vs चीज़

### 2. Cues 53, 54, 55, 56: R6 (kept for your review)
- **Output time:** 00:01:50
- **Source time:** ≈3:20.0

**Surrounding speech** (previous cues, *flagged cues*, following cues):

> 51  You know, as a kid also,  
> 52  we have  
> 53  **As a kid,**  
> 54  **also,**  
> 55  **I think we'll**  
> 56  **have to come to the kingdom.**  
> 57  Which never happens.  
> 58  There is no Prince Charming  

**What the recognisers heard:**

- **Parakeet:** "As a kid, also, I think we'll have to come to the kingdom."
- **Whisper small.en:** "…movies are very good. I think Prince Chama will … and rescue you."
- **Whisper turbo:** "…प्रंच शामन विल कम रस्क्यू यू" ("Prince Charming will come rescue you", in Devanagari)

**Suggested alternatives** (not applied):

- **A:** keep as is: "As a kid, also, I think we'll have to come to the kingdom."
- **B:** "As a kid also, … Prince Charming will come to rescue you." (two recognisers support "Prince Charming will come… rescue you"; the words in between are unclear and may be Hindi)
- **C:** you type the line as you said it

### 3. Cue 69: R8 (kept for your review)
- **Output time:** 00:02:28
- **Source time:** ≈4:09.3

**Surrounding speech** (previous cues, *flagged cues*, following cues):

> 67  Don't be completely dependent on  
> 68  anyone to rescue you.  
> 69  **Okay, be your pillow.**  
> 70  From childhood we have seen movies  
> 71  Prince Charming आके हमें बचाएगा,  

**What the recognisers heard:**

- **Parakeet:** "Okay, be your pillow."
- **Whisper small.en:** "Okay, be your pillow."

Both recognisers independently heard "pillow", so the sound is close to that word; the meaning is what's unclear.

**Suggested alternatives** (not applied):

- **A:** "Okay, be your pillow." (as recognised)
- **B:** "Okay, be your own pillar."
- **C:** "Okay, be your pillar."

### 4. Cue 71: Hindi sentence (Hinglish passage 2)
- **Output time:** 00:02:34
- **Source time:** ≈4:24.3

**Surrounding speech** (previous cues, *flagged cues*, following cues):

> 69  Okay, be your pillow.  
> 70  From childhood we have seen movies  
> 71  **Prince Charming आके हमें बचाएगा,**  
> 72  but ऐसा नहीं होता।  
> 73  As women, we are often told  

**What the recognisers heard:**

- **Parakeet:** "…movies charming a key hammer, but as a nahi hotta."
- **Whisper-medium (Hindi):** "…प्रिंश शामिंग के हमें बच्छा आएगा"
- **Whisper (English mode, translating):** "where someone will be charming, but it doesn't happen"

**Suggested alternatives** (not applied):

Caption now: **Prince Charming आके हमें बचाएगा,** / next cue **but ऐसा नहीं होता।** ("but ऐसा नहीं होता" is well supported)
- **A:** Prince Charming आके हमें बचाएगा
- **B:** Prince Charming हमें बचाने आएगा
- **C:** Prince Charming आएगा, हमें बचाएगा
- Also unclear: whether a "ki/कि" comes before "Prince"

### 5. Cue 121: Finances sentence
- **Output time:** 00:04:07
- **Source time:** ≈7:02.1

**Surrounding speech** (previous cues, *flagged cues*, following cues):

> 119  Whoever is paying for you is  
> 120  going to control your life in  
> 121  **somewhat other way.**  
> 122  So don't let other people have  
> 123  that control over you.  

**What the recognisers heard:**

- **Parakeet:** "…going to control your life in somewhat other way."
- **Whisper small.en:** "…going to control your life in some more other way."

**Suggested alternatives** (not applied):

- **A:** "in somewhat other way" (as recognised)
- **B:** "in some or the other way"
- **C:** "in some other way"

### 6. Cue 130: Finances list
- **Output time:** 00:04:24
- **Source time:** ≈7:19.1

**Surrounding speech** (previous cues, *flagged cues*, following cues):

> 128  Know what is investment,  
> 129  know what is budgeting,  
> 130  **stock market, a person.**  
> 131  Personal financing.  
> 132  There are many YouTube videos that  

**What the recognisers heard:**

- **Parakeet:** "Know what is investment, know what is budgeting, stock market, a person. personal financing."
- **Whisper small.en:** "…know what is budgeting, stock market, a person."

Both recognisers heard "a person.", so something like it was spoken. Whether it's a false start is your call.

**Suggested alternatives** (not applied):

- **A:** keep "a person." (verbatim)
- **B:** drop "a person." from the caption only (it sounds like a false start of "personal"; the audio stays as is)

### 7. Cue 138: R14 (kept for your review)
- **Output time:** 00:04:48
- **Source time:** ≈7:48.9

**Surrounding speech** (previous cues, *flagged cues*, following cues):

> 136  Start educating yourself on finances.  
> 137  Okay.  
> 138  **Tourism.**  
> 139  Find your happiness find where your  
> 140  happiness lies.  

**What the recognisers heard:**

- **Parakeet:** "Tourism."
- **Whisper:** "TODISM"

**Suggested alternatives** (not applied):

- **A:** "Tourism." (as recognised)
- **B:** "Third is," (fits the list: second lesson → third lesson)
- **C:** remove this caption

### 8. Cue 182: Scrolling question
- **Output time:** 00:06:12
- **Source time:** ≈9:37.6

**Surrounding speech** (previous cues, *flagged cues*, following cues):

> 180  Is it that I'm just scrolling?  
> 181  Is it that I'm just watching YouTube?  
> 182  **Netflix?**  
> 183  Or am I actually doing something creative?  
> 184  So write down what creative things  

**What the recognisers heard:**

- **Parakeet:** "At Witz"
- **Whisper small.en:** "Netflix" (clearly)

**Suggested alternatives** (not applied):

- **A:** "Netflix?" (applied, unconfirmed)
- **B:** you type the word

### 9. Cue 226: Know-your-values sentence
- **Output time:** 00:07:38
- **Source time:** ≈11:26.8

**Surrounding speech** (previous cues, *flagged cues*, following cues):

> 224  know your boundaries.  
> 225  Try to implement them in your life.  
> 226  **Very oddly.**  
> 227  So that whenever someone is trying  
> 228  to tell you is is trying  

**What the recognisers heard:**

- **Parakeet:** "Try to implement them in your life. Very oddly."
- **Whisper small.en:** "very oddly."

Both recognisers heard "very oddly". "Very early" is only my reading of the sense, not something either model heard.

**Suggested alternatives** (not applied):

- **A:** "Very oddly." (as recognised)
- **B:** "very early." (fits "implement them in your life very early")

### 10. Cue 242: R25 (kept for your review)
- **Output time:** 00:08:09
- **Source time:** ≈12:21.0

**Surrounding speech** (previous cues, *flagged cues*, following cues):

> 240  because  
> 241  as a female we as  
> 242  **Oh.**  
> 243  Indian parents often take decisions  
> 244  for you from childhood.  

**What the recognisers heard:**

- **Parakeet:** "…because as a female we as… Oh. Indian parents often take decisions for you…"
- **Whisper:** "Awesome."

**Suggested alternatives** (not applied):

- **A:** keep "Oh."
- **B:** drop "Oh." from the caption only (it may be a sound, not a word)

### 11. Cue 316: Closing line
- **Output time:** 00:10:31
- **Source time:** ≈16:06.1

**Surrounding speech** (previous cues, *flagged cues*, following cues):

> 314  That's it for this video.  
> 315  I hope you have a great life,  
> 316  **you have great 20 years.**  
> 317  Be confident, be bold.  
> 318  Do not shy away from speaking  

**What the recognisers heard:**

- **Parakeet:** "I hope you have a great life, you have great 20 years."
- **Whisper small.en:** "I hope you have a great life, your great 20 years."

**Suggested alternatives** (not applied):

- **A:** "you have great 20 years" (as recognised)
- **B:** "your great twenties"
- **C:** "you have a great twenties"

## Checked and left as is (second recogniser misheard)

| Cue | Time | Caption | Note |
|---|---|---|---|
| 25 | 00:00:47 | to be thirty next year. | Parakeet's word fits the sentence; second recogniser heard 13; second recogniser heard two years. |
| 26 | 00:00:48 | So I'll be entering my thirties | Parakeet's word fits the sentence; second recogniser heard two years. |
| 40 | 00:01:22 | But | Parakeet's word fits the sentence; second recogniser heard Hauta Doma Alapchi Sukharti" |
| 48 | 00:01:41 | Actually. | real word (stray), second recogniser output was noise |
| 58 | 00:02:00 | There is no Prince Charming | Parakeet text is right; Whisper misheard ('Mooji Renshami') |
| 59 | 00:02:04 | Yeah. | Parakeet's word fits the sentence; second recogniser heard [MUS |
| 72 | 00:02:35 | but ऐसा नहीं होता। | Well supported (Parakeet "but as a nahi hotta" plus Whisper-medium). Belongs to item 4: confirm it together with cue 71. |
| 103 | 00:03:28 | So take charge of your life | Parakeet's word fits the sentence; second recogniser heard chance |
| 112 | 00:03:48 | say is take control of your finances. | Parakeet's word fits the sentence; second recogniser heard see |
| 157 | 00:05:24 | Crocheting, try baking, | Parakeet's word fits the sentence; second recogniser heard Crouching |
| 160 | 00:05:32 | anything creative. | Parakeet's word fits the sentence; second recogniser heard you need to |
| 161 | 00:05:33 | Try a pottery class, | Parakeet's word fits the sentence; second recogniser heard glass, |
| 168 | 00:05:44 | Yeah. | Parakeet's word fits the sentence; second recogniser heard (clap |
| 177 | 00:06:02 | do when I'm bored, | Parakeet's word fits the sentence; second recogniser heard Then |
| 178 | 00:06:04 | when I'm free, | Parakeet's word fits the sentence; second recogniser heard and |
| 206 | 00:07:01 | Take advice. | Parakeet's word fits the sentence; second recogniser heard advices. |
| 229 | 00:07:43 | to give you an advice. | Parakeet's word fits the sentence; second recogniser heard a device. |
| 230 | 00:07:45 | You would know if that advice | Parakeet's word fits the sentence; second recogniser heard device |
