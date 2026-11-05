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

**Captions:** the hook line plays as chunks of 2–3 words on a single row. Words pop in one at a time (0.14 s apart),
each chunk holds for reading time (0.35 s + 0.28 s per word) and then clears. Chunks are split with `|` in
`HOOK_15` / `HOOK_10` in `build.py`; `*word*` marks the green word. The 10 s cut's last chunk sits lower, in the sand,
so it doesn't cover James on the dune.

**Ending:** no name card (James: it read as forced promotion). Both edits close on **"Go on, look after yourself"**
(`OUTRO` in `build.py`, *yourself* in green), centred over the open sea and fading out with the picture.

**Type:** Bebas Neue caps, letter-spacing .035em, thickened with a 3 px same-colour stroke (Bebas has one weight), white
with the brand's subtle down-right shadow.

**Green words:** bold #75FF78 with a thin (2.5 px) outline in dark cherry **#990F3D** (James's pick, option B in
`cherry-shades.jpg`), then the subtle shadow. Change `CHERRY` in `build.py`.

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
