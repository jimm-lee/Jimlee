# Heavyweight Hills: campaign intros (voice-led)

## Finished: two 30 s intros (`videos/`)

| File | Length | Story |
|---|---|---|
| `Heavyweight-Hills-Intro-A-30s.mp4` | 28.8 s | **The challenge.** "Just because I haven't posted it doesn't mean I haven't been doing it" over the night road climb and the rain → the vest at night → up (feet, the dirt track) / down (the grass slope, the steep path) → "30 kilos on my back" walking selfie → a map pin for every day (Day 1–8, 4 hills) → "Heavyweight Hills" over the terraces → summit selfie → "this one is visible" on the vest in full view → "Go on, look after yourself" over the harbour |
| `Heavyweight-Hills-Intro-B-30s.mp4` | 31.0 s | **The why** (Nov 9 re-record). "So why bother?" over the beard coming off (IMG_3220, captions on the dark jersey below the faces) → "Why do Movember?" over the map pulling back to every hill so far → "Last year my uncle made the irreversible decision that ended up shattering both sides of our family" over the harbour, the night path, the surf, the rain → "in the last three months I've lost two grandparents" on the night roads → "So for me, putting on this vest is a sign of strength" on the vest selfies → "There's always a way out, and you need to be strong enough to ask" → James saying "Go on, look after yourself" over the Mount at night, the closing rows appearing word by word with his voice |

Clips used: IMG_3220–3290 (launch footage, re-supplied) and IMG_3313–3430 (Nov 4–8). Captions move up to 300 px over
3276, where James's head sits high in frame (`HIGH_FACE` in `build_intros.py`); nothing is captioned over a face.

1080×1920, 30 fps, H.264 + AAC 256k, voice only (about −15 LUFS, peak −1.5 dBFS); music is added afterwards, ducked
under the voice. House style from the `hero-edit` skill: no grade, real speed, Bebas Neue captions that spell out
letter by letter **in time with the voice** (Whisper word timings), no name card. Captions are 1–2 words at a time (3 at most), each arriving with its first spoken word and staying until the next (at least 0.45 s), with the impact words in green: the phrasing is the `chunks` spec in `build_intros.py`.

**Map:** the Day 3 & 4 recap map (OpenStreetMap, credited on screen). Pins from the clips' GPS and the earlier recaps:
Mount Drury (1, 2, 4, 5, 8 Nov), 3rd Avenue (3 Nov), 17th Avenue, Tauranga (6 Nov: IMG_3373/3377/3389) and
Cliff Road, Tauranga (7 Nov: IMG_3401/3402/3404). Day list: `DAYS` in `build_intros.py`.

**Rebuild:** clips in `clips/` (edit copies of the IMG_33xx/34xx originals: `fps=30,scale=1080:1920:…crop`, SDR so no
tone-map), voice with `voiceover/stitch_vo.py intro-a m1=… m2=… m3=…` / `intro-b m4=Movember_4.m4a o=New_Recording_10.m4a`, word timings into `voiceover/words-<intro>.json`,
then `python3 build_intros.py`, `om render intro-a --silent`, and mux the voice (`loudnorm=I=-14:TP=-1.5`).

---

# Full-length voice-over plan (65 s)

The intro piece for James's Movember 2026 campaign: his own voice-over, stitched from three voice memos, laid over
the vest footage from `projects/heavyweight-hills/`. Unlike the silent 10–15 s hero edits, the voice drives this one:
about **68 s**, 1080×1920, 30 fps, house caption style from the `hero-edit` skill (Bebas Neue, letter-by-letter, one
green word, no name card, closes on "Go on, look after yourself").

Raw memos, the stitched voice and the clips are **not committed** (public repo; see `.gitignore`).

## Voice-over (`voiceover/`)

`stitch_vo.py` cuts the selects from the three memos (Movember_1/2/3.m4a), level-matches the takes, joins them with
short breaths and normalises to −16 LUFS. Result: 65.4 s. `vo_cues.json` has where each select sits;
`captions.json` has every caption chunk with word-level timings (Whisper `small.en`, then hand-chunked).

| Time | Take | Line | Why this take |
|---|---|---|---|
| 0.3–10.2 | 2 | "I'm a little late to the whole Movember conversation, but this year we're still taking on a challenge. Just because I haven't posted it doesn't mean I haven't been doing it." | Cleanest opener, and the "haven't posted it" line is the hook |
| 10.7–13.4 | 1 | "30 kilo weight vest, same as last year," | Tightest version (takes 2 and 3 stumble on "30 kilos, 30 kilo") |
| 13.6–25.1 | 2 | "so walking up the hill, walking down the hill obviously, 30 kilos on my back, at least one hill every day for the whole month of Movember, and calling it Heavyweight Hills." | Only take with up/down, which gives the edit its rhythm |
| 25.7–30.4 | 3 | "It's a physical challenge, but as always, there's a bigger reason behind it." | Take 1 restarts mid-line |
| 30.7–39.9 | 3 | "It's a memory of someone special. I lost my uncle last year, and in the last three months, I've lost two grandparents." | Only take that names who; the heart of the piece |
| 40.2–46.0 | 2 | "And it's there to help raise awareness for men's health, men's mental health specifically," | |
| 46.4–50.4 | 1 | "because we all carry weight, just some of it is invisible." | The strongest line across all three memos |
| 51.0–59.3 | 1 | "So the weight vest is there to help symbolize the weight that men hold on their shoulders, except this time it's visible." | Only take that explains the vest |
| 59.9–64.5 | 3 | "So this month, let's make sure no one has to carry that weight alone." | "that weight" ties back to the vest |

Left out: "heavy as shit" (take 2), "Heavyweight Hills" said twice and "the mountain towering area" (take 3).

## Shot map

Clip names are the IMG numbers (as in `projects/heavyweight-hills/README.md` and `hero-edit/COMPOSITIONS.md`).
Captions run the whole voice-over in 2–3 word chunks at `top: 520px`; ⚠ marks where a face could sit under the caption
(reframe or slide the clip so the caption clears it).

| Time | Part | Shot | Voice / caption (green word) | Notes |
|---|---|---|---|---|
| 0.0–1.2 | Spiral | Opening spiral: 3-frame flashes of the vest clips, landing on 2654 | — | `spiral=True` |
| 1.2–4.6 | **Hook** | 2654 lying on the track in the vest with the Movember bottle | "late to the whole *Movember* conversation" | Unexpected image to stop the scroll |
| 4.6–7.6 | Hook | 3266 POV walk in the vest, binning rubbish | "we're still taking on a *challenge*" | |
| 7.6–10.6 | Hook | 3292 night walk (the "by night" street) | "haven't *posted* it… haven't been *doing* it" | Proof it's been happening off-camera |
| 10.6–13.6 | Connection | 3267 "30 KG" selfie, vest in full view | "*30* kilo weight vest, same as last year" | ⚠ face low in frame, caption sits on the sky |
| 13.6–15.3 | **Build** | 3324 UP: path under the tree branch | "walking *up* the hill" | Cut on "up" |
| 15.3–17.4 | Build | 3313 DOWN: grass slope | "walking *down* the hill, obviously" | Cut on "down" |
| 17.4–19.3 | Build | 3276 walking selfie, from 0.35 s | "*30* kilos on my back" | ⚠ |
| 19.3–22.9 | Build | 0.5 s cuts: 3325 REPEAT · 3269 by day · 3286 in the rain · 3292 by night · 2524 vest walk · 3225 into the low sun · 3246 summit | "at least one hill *every* day for the whole month of *Movember*" | The montage: every day, every weather |
| 22.9–25.6 | **Payoff** | 3244 the terraces, wide | "and calling it *Heavyweight* Hills" | Title moment; the music drop goes here |
| 25.6–30.6 | Turn | 3262 open hilltop, slow | "a physical challenge… a *bigger* reason behind it" | Pace drops: long shots from here |
| 30.6–35.2 | Reflect | 3269 harbour from the top, the figure sitting alone | "a memory of someone *special*. I lost my *uncle*" | No faces; let it breathe |
| 35.2–40.2 | Reflect | 3225 vest selfie walking into the low sun (from behind or the sun-flare part) | "two *grandparents*" | Pick a section without the smile |
| 40.2–46.4 | Reason | 3220 the shave (Movember start), then 2153 golden-hour selfie, turns to camera at 4.6 s | "raise *awareness*… men's *mental* health" | ⚠ 3220 has two faces mid-frame |
| 46.4–48.6 | Line | 2524 Movember vest walk | "because we all carry *weight*" | |
| 48.6–51.0 | Line | 3286 rainy empty street, no one in shot | "just some of it is *invisible*" | The empty frame is the point |
| 51.0–55.6 | Vest | 3276 walking selfie (back half), vest straps on the shoulders | "the weight that men hold on their *shoulders*" | Second use of 3276; different section |
| 55.6–59.9 | Vest | 3267 "30 KG" selfie (second half) | "except this time it's *visible*" | Hard cut on "visible" |
| 59.9–64.5 | Close | 3290 night selfie, the wave to camera | "let's make sure no one has to carry that weight *alone*" | Warmest moment, he invites you in |
| 64.5–68.5 | **Linger** | 3269 / 3262 open view, slow push | **"GO ON, / LOOK AFTER *YOURSELF*"**, fade to black | 4 s hold, 0.6 s fade |

Each vest clip is used at most twice, and never next to the same shot twice. If one technique goes in, use the
`grid` crop flash on 3244 at "Heavyweight Hills" (TECHNIQUES.md); otherwise clean beat cuts.

**Donate link:** no end card (house style). The link goes in the caption and bio:
<https://movember.com/m/15440871?mc=60>. The QR end card from the 30 s launch video can be added if a version
needs one.

## To render

1. Put the edit copies of the clips above in `clips/` (HLG→SDR conversion as in the hero-edit skill).
2. Put the stitched voice in `voice.wav` (`voiceover/stitch_vo.py`).
3. Build the composition with the hero-edit engine, using `captions.json` timings instead of the synthetic
   reading pace, then `om render`, `om qa`, and the voice-forward mix from `projects/heavyweight-hills/README.md`
   (music ducked under the voice, −14 LUFS).

## 10 s promos (`videos/Heavyweight-Hills-Promo-*`)

Built from lines in the Nov 9 voice-over (Movember_4) that the intros don't use. Same engine and caption style
(`build_promos.py` → `promo-*/`; voice: `voiceover/stitch_vo.py promo-<name> m4=… o=…`).

| File | Length | Line | Ends on |
|---|---|---|---|
| `Promo-Invisible-10s.mp4` | 11.5 s | "Because we all carry weight. Sometimes, most of the time even, it's invisible. You don't see it." (vest selfies → night path → the vest's shadow) | James: "Go on, look after yourself" over the harbour |
| `Promo-Lifetime-10s.mp4` | 10.4 s | "Some people hold that weight on their shoulders for a lifetime and don't tell anyone. There's always someone who can relate to your story." (vest at night → night road → people on the steep path) | "your story." over the Mount at night |
| `Promo-The-Stare-10s.mp4` | 11.4 s | "Most of the times I stare at that vest for two minutes before even trying to pick it up, preparing myself for a little bit of suffering." (vest selfies → track → feet → slope) | "of suffering." on the grinning summit selfie |
| `Promo-Needs-To-Change-10s.mp4` | 10.6 s | "So many men hold this weight on their shoulders and don't tell anyone. And that needs to change." (rain → vest at night → night flax → Running for Movember sign) | James: "Go on, look after yourself" over the harbour |
