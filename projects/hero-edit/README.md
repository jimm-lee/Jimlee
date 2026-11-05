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
| 04 Payoff | 9.5–13 dune run (half speed) → sun on the sea | 6.0–8.5 dune run → sea |
| 05 Linger | 13–15 golden-hour selfie, turns to camera; JAMES / **LEAHY** over the sky | 8.5–10 same |
| Hook line | "The ordinary days are quietly building / the **extraordinary** life you've always imagined." (aspiration: saves, profile visits) | "Your comfort zone can quietly become / the most **expensive** place you ever live." (challenging belief: comments) |

Each hook line is split into two blocks so it can be read at this pace. **Type:** Bebas Neue caps, tight spacing (.01em), thickened with a 3 px same-colour stroke (Bebas has one weight),
white with #75FF78 on one word and the brand's subtle down-right shadow (James's choice for hero edits, Nov 2026;
see `bebas-sample.jpg`).

**Look:** no grade. The iPhone HLG footage is only converted to SDR (Hable tone-map) so it plays with correct colours;
no extra contrast, saturation, vignette or flashes. The dune run is the 60 fps original at half speed.

**For the music:** every cut sits on a 0.5 s grid, so a 120 BPM track (or 60 BPM half-time) starting at 0 s lines up.
The linger (and the name) starts at 13.0 s (15 s cut) / 8.5 s (10 s cut); the payoff at 9.5 s / 6.0 s is where the drop should land.

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
