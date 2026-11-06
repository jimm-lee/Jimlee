# Heavyweight Hills — Day 1 & 2 recap (Movember 2026)

| File | Length | Notes |
|---|---|---|
| `videos/Heavyweight-Hills-Day1-2-Recap.mp4` | 29.5 s | 1080×1920, H.264 + AAC 256k, −14 LUFS, true peak −1.4 dBFS. House style (`brand/`). |

## Structure

| Time | Section | Footage |
|---|---|---|
| 0–2.5 s | Hook: "DAY 1 & 2" | Mount Drury – Hopukiore sign photo (James) |
| 2.5–9.5 s | Animated map: Mount Maunganui → Mount Drury → route drawn → marker climbs it 3 times | OpenStreetMap |
| 9.5–14 s | Day 1 stats: 1.64 km · 27 min · peak 130 bpm (Apple Watch workout, 1 Nov, 7:24 pm) | IMG_3231, IMG_3244, IMG_3246 |
| 14–20 s | Day 2: Same hill. Same 30 kg. Still going. | IMG_3260, IMG_3264, IMG_3261, IMG_3267 |
| 20–29.5 s | The ask and end card, as in the launch video, with James's launch voice-over lines | IMG_3262, IMG_3276 (blurred) |

## Map

`map-build/build_map.py` turns an OpenStreetMap extract of Mount Maunganui (bbox −37.672,176.150 → −37.612,176.215,
fetched via the Overpass API) into `film/assets/map/map.json` (SVG paths: coastline, parks, bush, beaches, roads,
paths, the Mount Drury Reserve outline and the walking route) and `land.png` (land filled from the coastline).
The route follows the reserve's tracks matched to James's workout map: north entrance → winding gravel track → summit
→ grass track and steps → south end.

Map data © OpenStreetMap contributors, available under the Open Database License (ODbL);
the attribution is shown on screen during the map section. `map.json` is a derived database under the ODbL.

## Rebuilding

Clips go in `film/assets/clips/` (1080×1920, 30 fps, H.264, no audio — same recipe as the launch project), the sign
photo at `film/assets/sign.jpg`, and the voice track at `film/assets/voice.wav`: launch voice-over 22.0–25.0 s placed
at 20.0 s and 26.0–28.9 s placed at 24.0 s. `index.html` is `template.html` with `map.json` injected. Then `om sound`,
`om render`, and the same voice-forward mix as the launch: music side-chain ducked under the voice, two-pass
`loudnorm` to −14 LUFS, limiter at about −1.6 dBFS.
