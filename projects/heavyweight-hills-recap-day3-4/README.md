# Heavyweight Hills — Day 3 & 4 recap (Movember 2026)

| File | Length | Notes |
|---|---|---|
| `videos/Heavyweight-Hills-Day3-4-Recap.mp4` | 32.3 s | 1080×1920, H.264 + AAC 256k, −14 LUFS, true peak −1.7 dBFS. House style (`brand/`), synthwave score like the rest of the series. |

## Structure

| Time | Section | Footage |
|---|---|---|
| 0–2.5 s | Hook: "DAY 3 & 4" | IMG_3304 (golden light on the Mount Drury terraces) |
| 2.5–12.3 s | Map: Tauranga + Mount Maunganui → 3rd Avenue, 5 summits → fly to Mount Drury, 2 summits on the usual track + 2 up the steeper north-east face (white) | OpenStreetMap |
| 12.3–16.8 s | Day 3 · 3rd Avenue (Tue 3 Nov, night): In the rain. 5 summits. By night. | IMG_3286, IMG_3292, IMG_3290 |
| 16.8–22.8 s | Day 4 · Mount Drury (Wed 4 Nov): 4 summits. The steep way. Burning the calves. Running for Movember. | IMG_3306, IMG_3327, IMG_3315, IMG_3317 |
| 22.8–32.3 s | The ask and end card, as in the launch, with James's launch voice-over lines | IMG_3330, IMG_3276 (blurred) |

## Map and routes

`map-build/build_map34.py` merges the Mount Maunganui Overpass extract with OpenStreetMap API tiles for Tauranga
(bbox −37.705,176.150 → −37.612,176.215) into `film/assets/map/map.json` + `land.png`.

- **3rd Avenue** (OSM way 28502068): from the harbour end (≈5 m) up to the crest near the western end (≈16.7 m),
  about 500 m — heights from the NZ 8 m DEM via OpenTopoData (`map-build/ave_profile.json`). James's clips are
  geotagged on this stretch.
- **Mount Drury, usual track**: north entrance up the winding gravel track (OSM way 574736364) to the summit.
- **Mount Drury, steeper slope**: the direct grass track up the north-east face (OSM way 574736365), where IMG_3327
  was filmed.

Map data © OpenStreetMap contributors (ODbL), credited on screen; elevation: LINZ NZ 8 m DEM via OpenTopoData.

## Rebuilding

Same as the Day 1 & 2 recap: clips in `film/assets/clips/`, voice track from the launch voice-over (22.0–25.0 s
placed at 22.8 s, 26.0–28.9 s at 27.0 s), `index.html` = `template.html` with `map.json` injected, then `om sound`,
`om render` and the voice-forward mix (side-chain ducking, two-pass loudnorm −14 LUFS, limiter).
