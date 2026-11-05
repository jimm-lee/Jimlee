# Hero edits (Nov 2026)

Two silent hero edits (1080×1920, H.264, no audio track; James adds the music).

| File | Length | Running order |
|---|---|---|
| `videos/Hero-Edit-15s.mp4` | 15 s | sauna · coast · geyser · rodeo · fight night · ice bath · dune run (slow-mo) · dragon boats · Split Apple Rock · vest selfie · end card on the sunset deck |
| `videos/Hero-Edit-10s.mp4` | 10 s | ice bath · geyser · rodeo · fight night · dune run (slow-mo) · vest selfie · end card |

**Type:** Anton caps, white, with the #75FF78 green on one word (James's choice for hero edits, Nov 2026, from
`font-options.jpg`). End card: JAMES / **LEAHY** with the green rule. No captions during the clips yet: James is
supplying his own lines (add them to `TITLES_15` / `TITLES_10` in `build.py`).

**Look:** no grade. The iPhone HLG footage is only converted to SDR (Hable tone-map) so it plays with correct colours;
no extra contrast, saturation, vignette or flashes. The end shot is darkened (brightness .72) under the name.
The dune run is the 60 fps original at half speed.

**For the music:** every cut sits on a 0.5 s grid, so a 120 BPM track (or 60 BPM half-time) starting at 0 s lines up.
The end card starts at 12.0 s (15 s cut) / 7.0 s (10 s cut).

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
