---
name: concat-editor
description: Edit video with Concat (jub0t/Concat), the local open-source CapCut alternative, through its built-in MCP server (`concat --mcp`): create projects, import media, cut/trim/split/speed, titles and word-styled captions, keyframes, effects and looks, masks, stabilization, preview frames and H.264/HEVC/AV1 export up to 4K60. Use when the user wants a timeline video edit — shorts, reels, YouTube cuts, captioned clips — or to assemble VoiceStudio voice tracks and huashu-motion renders into a finished video.
---

# Concat video editor (via MCP)

Concat 0.2.8 ships an MCP server inside the app binary: 42 tools whose argument schemas come
from the engine's own types. Everything runs locally; footage never uploads.

## House style (all videos)

Every video uses James's house style in `brand/` (see `brand/README.md` and `brand/house-style.css`):
**Merienda Black** titles (CAPS for title words, sentence case for spoken lines), **#75FF78** green on one or two
key words, white everything else, Outfit for small labels, and a subtle down-right shadow on all type. Keep text
above y 1440 (Instagram UI). Copy the fonts from `brand/fonts/`. Don't fall back to Anton/Inter or yellow accents.

## Connect

- Binary: Linux `/usr/bin/concat` · macOS `/Applications/Concat.app/Contents/MacOS/concat` ·
  Windows `%LOCALAPPDATA%\Programs\Concat\concat.exe`.
- This repo's `.mcp.json` registers `concat --mcp` (Linux path). Elsewhere:
  `claude mcp add concat -- <binary> --mcp`.
- Modes: `--mcp window` goes through an open editor (enable **Settings > Automation > Scripts and apps**);
  `--mcp headless` runs the engine without a window; default `auto`. Call `concat_version` to see which.
- The agent writes only under the user's home. Other folders: `CONCAT_MCP_ROOTS=/a:/b` (headless).
- Headless render with no GPU needs Mesa lavapipe (`apt install mesa-vulkan-drivers`), otherwise
  `preview_frame`/`export_*` fail with "no GPU or software renderer is available".

## The edit loop

1. `project_create {location, name, video?}` (1920×1080@30 default) or `project_open {path}`.
   A project is a folder; every other tool takes `path` = that folder.
2. `media_probe` to check files, then `media_import {path, file}` → the new id is `createdId` (`m1`…).
3. `timeline_read {path}` → lanes `T1..T4` (bottom-first) and clip ids. Re-read after structural edits;
   never guess ids.
4. Place and cut:
   - `clip_add {mediaId, trackId, start, ripple?}` · `clips_add_sequence {mediaIds, start}` (montage)
   - `clip_trim {clipId, edge:"start"|"end", delta}` · `clips_split {clipIds, time}` ·
     `clips_move` · `clips_remove {ripple}` · `clip_speed {clipId, speed 0.0625–16}`
   - `clip_update {patch}`: volume (gain), fadeIn/fadeOut, opacity, muted, flips, blend mode…
   - `clip_frame {framing:"fit"|"fill"}` for mixed aspect ratios (e.g. 16:9 source in a 9:16 short:
     `project_set_video {width:1080,height:1920}` then `fill`).
   - `clip_transform` (scale, offsetX/Y as frame fractions, rotation) · `clip_mask` · `clip_stabilize`
5. Words on screen:
   - `title_add {start, duration, style:{content, font…}, above:true}` — without `style.content`
     the title reads "Your text".
   - `captions_add {captions:[{start,end,text}], style}` — one title per cue, one undo step.
     Feed it VoiceStudio transcript segments (`/dub/segments-text`) or an SRT you parsed.
   - `title_style_words` to colour/weight individual words (hook words in shorts).
6. Motion and looks: `keyframe_set {clipId, property, at 0–1, value, ease[4]}` (scale, offsetX/Y,
   rotation, opacity, volume, mask params) · `effects_list` then `effect_layer_add {effectId, start,
   duration}` (e.g. `concat.warm`) · `effect_key_set` · `timeline_background`.
7. Anything else: `edit_apply {command:{op:…}}` (any window edit, or a batch as one undo step);
   `edit_undo` / `edit_redo`.
8. **Look before exporting:** `preview_frame {time, output:"…png", width, height}` at the hook,
   at each title/caption, and at the end. Read the PNG.
9. `project_save` (edits are in memory until then).
10. `export_start {output:"….mp4", codec?:"h264"|"hevc"|"av1", crf?, width?, height?, tenBit?}`
    → `{job}`; `export_wait {job, timeoutSeconds ≤600}` until `state:"done"`
    (`failed`/`cancelled` are terminal too). One export at a time (`Busy`).
11. Verify the file: `.claude/skills/voicestudio-editor/scripts/vs_check.sh out.mp4`
    (codecs, duration, loudness). Report what you checked.

## Pipeline with the other skills

- **Voice-over:** render narration with `voicestudio-editor` (`POST /generate`, `effect_preset=raw`
  if Concat will mix) → `media_import` → `clip_add` on an audio lane → captions from its transcript.
- **Motion graphics:** render intros/lower-thirds with `huashu-motion` (`om render --format mov`
  for alpha overlays) → import → place above the footage.
- **Dub a cut:** export from Concat → VoiceStudio `/dub/upload` → translate/generate → download.

## Rules

- Don't edit the project the user has open in the window from headless mode (it's locked;
  use `--mcp window`). Work on copies or new projects.
- Keep original media untouched; exports are new files.
- Free and AGPL-3.0; the models for auto-captions, TTS and cutout download from Settings only when the user asks.

## Verified in this workspace

Concat 0.2.8 `.deb` (SHA256 checked against the release's SHA256SUMS) installed to `/usr/bin/concat`.
Headless MCP test: create → import video + VoxCPM2 voice WAV → clip, title, 2 captions → save →
preview frame → export: 6.0 s 1920×1080 H.264 + AAC 48 kHz, −17.6 LUFS, using lavapipe on CPU.
