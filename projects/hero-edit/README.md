# Hero edits (Nov 2026)

Two silent hero edits (1080×1920, H.264, no audio track; James adds the music). House style from `brand/`.
Captions are written in the spirit of James's stoic/strategy quotes rather than describing the footage.

| File | Length | Captions |
|---|---|---|
| `videos/Hero-Edit-15s.mp4` | 15 s | Be still. · You can't control the chaos. · Only your response. · Motivation fades. Discipline stays. · Consistency over applause. · Build it quietly. · end: Do the WORK. / JAMES LEAHY |
| `videos/Hero-Edit-10s.mp4` | 10 s | Motivation fades. Discipline stays. · Control the response. · Consistency over applause. · Build it quietly. · end: Do the WORK. / JAMES LEAHY |

**For the music:** every cut sits on a 0.5 s grid, so a 120 BPM track (or 60 BPM half-time) starting at 0 s lines up.
Big cuts with a white flash frame: 15 s at 2.5, 6.0, 12.0; 10 s at 1.5, 7.0. The end card starts at 12.0 s / 7.0 s.

Look: contrast +10 %, saturation −12 %, vignette, darker end shot; the dune run is the 60 fps original at half speed.

## Rebuilding

Clips are not committed. Make edit copies as in `../say-yes-montage/README.md` (HDR → SDR tone-map), plus the
slow-motion dune run from the 60 fps original:

```sh
ffmpeg -i IMG_9661.mov -an -vf "$TM,setpts=2*PTS,fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 18 -g 15 clips/9661_slow.mp4
```

Copy them into `film-15/assets/clips/` and `film-10/assets/clips/`, edit `build.py`, then
`python3 build.py && om render film-15 --silent && om render film-10 --silent`.
