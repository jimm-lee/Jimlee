# Hero edits (Nov 2026)

Two silent hero edits (1080×1920, H.264, no audio track; James adds the music). House style from `brand/`.
Captions are written in the spirit of James's stoic/strategy quotes rather than describing the footage.

| File | Length | Captions |
|---|---|---|
| `videos/Hero-Edit-15s.mp4` | 15 s | Be still. (sauna) · You can't control the chaos. (geyser, rodeo) · Only your response. (fight night) · Discipline over comfort. (ice bath) · Hard moments reveal strength. (dune, slow-mo) · Build it quietly. · end: Do the WORK. / JAMES LEAHY |
| `videos/Hero-Edit-10s.mp4` | 10 s | Discipline over comfort. · Control the response. · Hard moments reveal strength. · Build it quietly. · end: Do the WORK. / JAMES LEAHY |

**For the music:** every cut sits on a 0.5 s grid, so a 120 BPM track (or 60 BPM half-time) starting at 0 s lines up.
The end card starts at 12.0 s (15 s cut) / 7.0 s (10 s cut).

**Look (v3, after "too filtered, I want contrast"):** the grade is baked into the edit copies, not added in the page:
iPhone HLG → SDR with a Hable tone-map (keeps skies), then an S-curve for deep blacks and +25 % saturation:

```
GRADE="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,curves=all='0/0 0.15/0.08 0.5/0.58 0.8/0.9 1/1',eq=saturation=1.25"
```

No vignette or flash frames; only the end shot is darkened (brightness .72) under the type. The dune run is the
60 fps original at half speed.

## Rebuilding

Clips are not committed. Make edit copies with the grade above (clip names in `build.py` are the IMG numbers):

```sh
ffmpeg -i IMG_XXXX.mov -an -vf "$GRADE,fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 18 -g 15 clips/XXXX.mp4
# dune run, half speed from the 60 fps original:
ffmpeg -i IMG_9661.mov -an -vf "$GRADE,setpts=2*PTS,fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuv420p" \
  -c:v libx264 -preset veryfast -crf 18 -g 15 clips/9661_slow.mp4
```

Copy them into `film-15/assets/clips/` and `film-10/assets/clips/`, edit `build.py`, then
`python3 build.py && om render film-15 --silent && om render film-10 --silent`.
