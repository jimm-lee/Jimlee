# Hero edits (Nov 2026)

Two silent hero edits (1080×1920, H.264, no audio track; James adds the music).

Built on James's montage brief, using the **transformation** formula (open on a challenge, build through effort,
pay off with the breakthrough) and the five-act timing: hook ~15 % → connection ~20 % → build ~30 % → payoff ~20 % →
linger ~15 %, alternating intimacy/scale, stillness/movement and dark/light.

| | 15 s | 10 s |
|---|---|---|
| 01 Hook | 0–2.5 ice bath, lowering in and the splash | 0–2.0 ice bath |
| 02 Connection | 2.5–5.5 coast from above (world) → Movember walk (human) | 2.0–3.5 coast → Movember walk |
| 03 Build | 5.5–9.5 sauna · rodeo · fight night · dragon boats · geyser · Split Apple Rock (1 s → 0.5 s cuts) | 3.5–6.0 sauna · rodeo · fight night · geyser · dragon boats |
| 04 Payoff | 9.5–12 dune run (half speed) → golden-hour selfie, turns to camera | 6.0–7.5 dune run → selfie |
| 05 Linger | 12–15 the open sea at sunset, slow push; **"Go on, look after yourself"** word by word, fade to black | 7.5–10 same |
| Hook line | "The ordinary days are quietly building / the **extraordinary** life you've always imagined." (aspiration: saves, profile visits) | "Your comfort zone can quietly become / the most **expensive** place you ever live." (challenging belief: comments) |

**20 s cut** (`videos/Hero-Edit-20s.mp4`, `film-20/`): the original clips plus 13 new ones (jellyfish, Aoraki/Mt Cook, the
Wānaka tree, Clay Cliffs, river gorge, vintage town, pad work, beach run, dusk beach, brunch, oysters, seafood,
candlelit table). Hook: the glowing jellyfish under "Some places **stay** with you long after you've physically left
them behind." (0–3 s) → connection (Mt Cook, Wānaka tree, pad work, 3–7 s) → build (11 shots, 1 s then 0.5 s cuts,
7–13 s) → payoff (dune run, beach run, golden selfie, 13–17 s) → linger on the dusk sea with "Go on, look after
yourself" (17–20 s). More structures for this footage: `COMPOSITIONS.md`.

**The escape** (`videos/Hero-Edit-Escape-15s.mp4`, `film-escape/`): 15 more clips. Opens on gridlocked motorway traffic
under "Being busy isn't the same thing as building a life you're **proud** of.", breaks into the ice tub, open land,
buskers, a rugby crowd, bars, river, yachts and a misty jetty, pays off on a sunrise wave and the golden selfie, and
lingers on a sunrise over the sea with "Go on, look after yourself".

**Captions:** the hook line plays as chunks of 2–3 words on a single row. Words arrive **as if read aloud** and
spell out letter by letter across each word's whole spoken time (0.22 s + 0.06 s per letter, 0.32–0.85 s; 0.25 s fade
per letter). A chunk holds about 0.35 s after its last letter, then the next chunk starts straight away: no gap
between captions. The final shot is 4 s so the closing line (second row following straight on from the first)
completes about a second before the 0.6 s fade.

**Ending:** no name card (James: it read as forced promotion). Both edits close on **"Go on, look after yourself"**
(`OUTRO` in `build.py`, *yourself* in green), centred over the open sea and fading out with the picture.

**Type:** Bebas Neue caps, letter-spacing .035em, thickened with a 3 px same-colour stroke (Bebas has one weight), white
with the brand's subtle down-right shadow.

**Green words:** bold #75FF78 with the same subtle down-right shadow as the white type, **no outline** (James, Nov
2026; cherry and pastel-yellow outlines were tried and dropped).

**Look:** no grade. The iPhone HLG footage is only converted to SDR (Hable tone-map) so it plays with correct colours;
no extra contrast, saturation, vignette or flashes. The dune run is the 60 fps original at half speed.

**For the music:** every cut sits on a 0.5 s grid, so a 120 BPM track (or 60 BPM half-time) starting at 0 s lines up.
The linger (open sea, closing line, fading to black over the last 0.8 s) starts at 12.0 s (15 s cut) / 7.5 s (10 s cut); the payoff at 9.5 s / 6.0 s is where the drop should land.

## Rebuilding

Clips are not committed. Make edit copies (clip names in `build.py` are the IMG numbers):

```sh
SDR="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv"
ffmpeg -i IMG_XXXX.mov -an -vf "$SDR,fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 18 -g 15 clips/XXXX.mp4
# dune run, half speed from the 60 fps original:
ffmpeg -i IMG_9661.mov -an -vf "$SDR,setpts=2*PTS,fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 18 -g 15 clips/9661_slow.mp4
```

Copy them into `film-15/assets/clips/` and `film-10/assets/clips/`, edit `build.py`, then
`python3 build.py && om render film-15 --silent && om render film-10 --silent`.


## Caption edits (`plans/`, `build_plans.py`)

Ten caption-led edits (10–15 s) from James's caption list, staged as storyboards in `plans/storyboard-1.jpg` and
`-2.jpg`, rendered one at a time after approval into `videos/captions/`.

| # | Caption | Status |
|---|---|---|
| 1 | My camera roll since moving to the other side of the world. | rendered (second pass, with spiral): `videos/captions/01-Camera-Roll-15s.mp4` |
| 2 | POV: You actually took the leap. | rendered (second pass): `videos/captions/02-Took-The-Leap-10s.mp4` |
| 3 | A little look at what life looks like 18,000km from home. | rendered (second pass, with spiral): `videos/captions/03-18000km-From-Home-15s.mp4` |
| 4 | Turns out, there's a lot of life outside your comfort zone. | rendered for review (grid framework + grid spiral): `videos/captions/04-Comfort-Zone-15s.mp4` |
| 5 | Somewhere between getting lost and finding yourself. | rendered (mirror on the hook, iris into the linger; vest-free sauna payoff): `videos/captions/05-Getting-Lost-15s.mp4` |
| 6 | Three years, one big decision, and a camera roll full of memories. | rendered (impact frame intro, photo stack): `videos/captions/06-Three-Years-15s.mp4` |
| 7–10 | see `build_plans.py` | second pass planned; rendering one at a time |

Second pass (Nov 6): all ten re-sequenced from the full library (77 clips): each clip in at most two edits, no shot
pair repeated, unique hook / payoff / linger. Captions moved down to y 520 (upper third, not too high). Shots with
faces are kept out from under the captions.

**Caption edits, closing:** "GO ON," and "LOOK AFTER YOURSELF" sit as two stacked rows that both stay up; the linger
shot is 3.5 s (15 s cuts) so the full line holds about a second before a 0.6 s fade. The dune run (9661) plays at real
speed in the caption edits (James didn't want it slowed); `clips/9661.mp4` is the real-speed copy.
