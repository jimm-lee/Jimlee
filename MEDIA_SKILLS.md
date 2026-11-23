# Media Editing Skills — Compiled Reference

Three Claude Code skills for local audio, motion-graphics and video work, compiled into one file.
The live, individually-loadable versions are in `.claude/skills/`; this file is the portable copy.

| Skill | Tool | What it does | Licence |
|---|---|---|---|
| [voicestudio-editor](#1-voicestudio-editor) | [VoiceStudio](https://github.com/debpalash/VoiceStudio) v0.5.7 | Speech generation, voice cloning/conversion, transcripts, dubbing, audiobooks, loudness | AGPL-3.0 (models vary) |
| [huashu-motion](#2-huashu-motion) | [huashu-motion](https://github.com/alchaincyf/huashu-motion) v0.3.1 (`52467f9`) | Motion graphics, launch videos and explainers as editable HTML+GSAP code | MIT |
| [concat-editor](#3-concat-editor) | [Concat](https://github.com/jub0t/Concat) v0.2.8 | Timeline video editing via its built-in MCP server | AGPL-3.0 |

**Pipeline:** VoiceStudio (voice-over, captions, dubs) → huashu-motion (intros, overlays, explainers) → Concat (final cut and export).

## House style (all videos)

Every video uses James's house style in `brand/` (see `brand/README.md` and `brand/house-style.css`):
**Merienda Black** titles (CAPS for title words, sentence case for spoken lines), **#75FF78** green on one or two
key words, white everything else, Outfit for small labels, and a subtle down-right shadow on all type. Keep text
above y 1440 (Instagram UI). Copy the fonts from `brand/fonts/`. Don't fall back to Anton/Inter or yellow accents.

## Contents

0. [Reinstall in a fresh environment](#0-reinstall-in-a-fresh-environment)
1. [voicestudio-editor](#1-voicestudio-editor)
2. [huashu-motion](#2-huashu-motion)
3. [concat-editor](#3-concat-editor)

---

## 0. Reinstall in a fresh environment

The programs, drivers and models are not stored in the repo. These steps rebuild them (Linux x86_64, as verified; see each project's README for macOS/Windows).

### Ultimate Vocal Remover models (audio-separator)

[Ultimate Vocal Remover](https://github.com/Anjok07/ultimatevocalremovergui) is a desktop (Tk) app; in a headless
session use its model runner, [audio-separator](https://github.com/nomadkaraoke/python-audio-separator) (same UVR
models, MIT):

```sh
pip install "audio-separator[cpu]" audioread        # ~3 GB with PyTorch; add [gpu] on CUDA
audio-separator take.wav -m denoise_mel_band_roformer_aufr33_sdr_27.9959.ckpt --output_format WAV   # hiss / noise
audio-separator take.wav -m UVR-DeEcho-DeReverb.pth --output_format WAV                           # room echo
audio-separator -l --list_filter vocals                                                            # all models
```

CPU speed here: Mel-Roformer denoise ~6 min per minute of audio, VR De-Echo ~1 min per minute. On James's Nov 2026
voice memos both removed almost nothing (−66 / −77 dB): the recordings are dry and quiet, and breaths count as voice
to these models. Breathing is handled by `projects/heavyweight-hills-hero/voiceover/clean_take.py`; reach for UVR
when a take has wind, traffic, music or a roomy echo under it.

### VoiceStudio backend (~6 GB with one TTS model)

```sh
git clone --depth 1 https://github.com/debpalash/VoiceStudio.git ~/vendor/VoiceStudio
cd ~/vendor/VoiceStudio
OMNIVOICE_TORCH_VARIANT=cpu bun run setup:api     # omit the variable on a CUDA machine
bun scripts/dev-backend.mjs &                      # serves http://localhost:3900
until curl -s localhost:3900/health | grep -q '"ok"'; do sleep 3; done

# Commercial-friendly TTS engine (Apache-2.0) — the one chosen in this workspace
curl -X POST localhost:3900/engines/sidecar/voxcpm2/install
curl -X POST localhost:3900/models/install -H 'Content-Type: application/json' -d '{"repo_id":"openbmb/VoxCPM2"}'
curl -X POST localhost:3900/engines/select -H 'Content-Type: application/json' -d '{"family":"tts","backend_id":"voxcpm2"}'
```

The default `k2-fsa/OmniVoice` weights are **non-commercial**; James accepted the licence on 2026-11-05. Use `engine=omnivoice-subprocess` (in-process OmniVoice clashes with VoxCPM2). Speech-to-text (transcription, captions) needs a Whisper model (`Systran/faster-whisper-large-v3`, 2.9 GB), not yet installed.

### huashu-motion

Already vendored in the repo at `vendor/huashu-motion/` (the skill is a symlink into it), so nothing to download. It needs Node ≥ 22, FFmpeg and a Chrome/Chromium (`OM_CHROME=/path` if not auto-found). Check with:

```sh
.claude/skills/huashu-motion/bin/om doctor
```

Do not use `npx huashu-motion`: npm only publishes 0.1.1.

### Concat

```sh
V=0.2.8
curl -LO https://github.com/jub0t/Concat/releases/download/v$V/Concat-$V-linux-x86_64.deb
curl -LO https://github.com/jub0t/Concat/releases/download/v$V/SHA256SUMS
grep linux-x86_64.deb SHA256SUMS | sha256sum -c -
sudo apt install ./Concat-$V-linux-x86_64.deb          # → /usr/bin/concat
sudo apt install mesa-vulkan-drivers libvulkan1       # only on machines without a GPU
```

macOS: `/Applications/Concat.app/Contents/MacOS/concat` — update `.mcp.json` to that path.
The repo's `.mcp.json` registers `concat --mcp` for Claude Code.

### Shared helper: `vs_check.sh`

Used by all three skills to verify any rendered audio/video (lives at `.claude/skills/voicestudio-editor/scripts/vs_check.sh`):

```bash
#!/usr/bin/env bash
# Verify a VoiceStudio output: format, duration, peak and integrated loudness.
set -euo pipefail
f="${1:?usage: vs_check.sh <audio-or-video-file>}"
[ -s "$f" ] || { echo "ERROR: $f missing or empty" >&2; exit 1; }
if head -c 1 "$f" | grep -q '[{<]'; then echo "ERROR: $f looks like a text/JSON error body:" >&2; head -c 300 "$f" >&2; exit 1; fi
ffprobe -v error -show_entries format=format_name,duration:stream=codec_type,codec_name,sample_rate,channels -of default=nw=1 "$f"
ffmpeg -hide_banner -nostats -i "$f" -af volumedetect -f null - 2>&1 | grep -E 'mean_volume|max_volume' | sed 's/.*\] //'
ffmpeg -hide_banner -nostats -i "$f" -af ebur128 -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | sed 's/^ *//' || true
```

---

## 1. voicestudio-editor

> **When to use:** Master editing skill for VoiceStudio (debpalash/VoiceStudio) — the local, open-source voice studio. Covers speech generation and re-takes, voice cloning/design/conversion, transcript and subtitle editing, video dubbing (translate, per-segment re-voice, timing fit, QC, mixing, hardsub/karaoke export), audiobook/story production with chapters and pauses, DSP effect presets, loudness, and batch jobs, all via the local REST API on port 3900. Use when the user wants to edit, re-voice, dub, subtitle, master, or assemble audio/video with VoiceStudio.
>
> Source: `.claude/skills/voicestudio-editor/SKILL.md`

# VoiceStudio Master Editor

Drive a running VoiceStudio backend to edit speech, video dubs and long-form audio.
Everything runs locally. Model downloads, cloud translation providers and remote
backends require the user's explicit consent.

**Base URL:** `http://localhost:3900` (honor `OMNIVOICE_PORT` / the user's configured address).
**Contract source of truth:** `GET /openapi.json` on the running version (~312 paths in v0.5.7).
Endpoints below were verified against v0.5.7; re-check the schema if the version differs.

### 0. Preflight (always)

```sh
curl -s localhost:3900/health          # {"status":"ok"} — "starting" means wait; poll, don't restart
curl -s localhost:3900/setup/status    # models_ready + missing[] — TTS needs k2-fsa/OmniVoice (or another engine)
curl -s localhost:3900/engines/tts     # engines + expression_caps (emotion / direction / tags)
curl -s localhost:3900/profiles        # saved voices — never invent profile IDs
curl -s localhost:3900/tools/effects   # DSP presets
curl -s localhost:3900/media-tools/status  # ffmpeg/ffprobe/yt-dlp
```

- Missing model → tell the user what and how big; download only with consent.
- Not running and a source checkout exists → `bun run setup:api` once, then `bun run dev:api`
  (backend only) or `bun run dev` (desktop). Never install a second copy.
- 401/403 → auth is configured; ask for credentials, never disable auth.
- 403 `model_licence_required` → the model's licence has not been accepted. Show the user
  `GET /models/licenses/details/{repo_id}` (the default OmniVoice weights are **non-commercial**,
  CC-BY-NC + Higgs Audio 2 + Meta Llama 3 tokenizer terms) and accept via `POST /models/licenses/accept`
  **only on their explicit say-so**. Never accept on the user's behalf.
- **Commercial-friendly engines** (Apache-2.0/MIT per `GET /models` → `license_info.license_category`):
  VoxCPM2 (clone + design), CosyVoice 3 (needed for `keep_delivery`), MOSS-TTS-Nano, KittenTTS, GPT-SoVITS.
  Install: `POST /engines/sidecar/{engine}/install` + `POST /models/install {"repo_id":…}`,
  then `POST /engines/select {"family":"tts","backend_id":"voxcpm2"}` (or pass `engine=` per request).
  The user chose this route over OmniVoice's non-commercial weights. VoxCPM2 is the active engine in this
  workspace (CPU: ~2.5 min for a 5 s take, 48 kHz mono).

Pick the right tool for the edit:

| Goal | Endpoint family | Section |
|---|---|---|
| Fix/redo one line of speech | `POST /generate` | 1 |
| Change who is speaking (keep words) | `POST /convert` | 2 |
| Clean up, normalize, master a clip | `/tools/*`, effect presets | 3 |
| Edit a video's transcript/subtitles | `/dub/upload` → transcribe → sync/import | 4 |
| Translate + dub a video | `/dub/translate` → `/dub/generate` | 5 |
| Export video/audio/stems/subs | `/dub/download*`, `/dub/srt|vtt|ass` | 6 |
| Long-form narration, chapters | `/audiobook*`, `/longform/*` | 7 |
| Many items / languages | `/batch/*` | 8 |

### 1. Speech takes and re-takes — `POST /generate` (multipart form)

Key fields: `text` (required), `profile_id`, `language`, `instruct` (style), `speed` (1.0),
`seed` (pin for reproducible re-takes), `num_step`, `guidance_scale` (2.0), `duration`
(force target length in seconds), `effect_preset` (default `broadcast`), `wav_bits` (16/24/32),
`denoise` (true), `max_chunk_chars` (800), `crossfade_ms` (50), `pronounce` (lexicon on),
`emo_text`/`emo_alpha`/`emo_vector` (engines with graded emotion only), `engine`, `stream`.

```sh
curl --fail-with-body -s localhost:3900/generate \
  -F text='Every voice has a story. [pause 0.5s] Let'\''s tell yours.' \
  -F profile_id=$PROFILE -F seed=42 -F effect_preset=podcast -F wav_bits=24 -o take.wav
```

Editing rules:
- **Re-take a single word/line**: same `profile_id` + `seed`, change only the text or one knob.
  Changing several knobs at once makes the difference undiagnosable.
- **Fit to a slot** (ADR / replacing a line in a video): set `duration` to the slot length,
  or use `POST /tools/rate-fit` to rewrite text to fit first.
- **Pauses**: `[pause]` (350 ms), `[pause 500ms]`, `[pause 1.5s]`, max 10 s — works on every engine.
- **Reactions** `[laughter]`, `[sigh]`, `[breath]` only on engines whose `expression_caps.tags`
  list them. Unknown tags are spoken literally — never paste ElevenLabs-style `[excited]` tags.
- **Pronunciation**: fix with the lexicon, not misspellings —
  `GET/POST/PUT/DELETE /pronunciation`, preview with `POST /pronunciation/test`.
- History: `GET /history`, star keepers with `PUT /history/{id}/starred`.
- Shortcut for simple TTS: OpenAI-compatible `POST /v1/audio/speech` (JSON `model`, `voice`, `input`, `response_format`).

### 2. Voice conversion / cloning / design

- **Convert** `POST /convert` (form): `audio`, `profile_id`, `match_duration` (true), `language`,
  `keep_delivery`. `keep_delivery=true` preserves timing, pauses and intonation (needs CosyVoice 3
  installed; clips >28 s are split at pauses; >10 min refused). Default re-transcribes and re-speaks.
- **Clone** `POST /profiles` with a clean reference (5–20 s, one speaker, no music). The reference's
  *delivery* is copied, not just timbre — a flat reference gives flat output.
  Replace reference audio via `PUT /profiles/{id}/audio`; freeze a good take with `POST /profiles/{id}/lock`.
- **Design** from text: `POST /design/describe`.
- Only clone voices the user is authorized to use; consent/attestation endpoints exist on profiles.

### 3. Clean-up, loudness and DSP

- `POST /tools/normalize-speech` (form `audio` WAV ≤64 MiB, `target_dbfs` −24…−1, default −2) →
  peak-normalized WAV. *Verified: −38.1 dB peak → −2.7 dB at target −3.*
- Effect presets (`effect_preset` on `/generate` and on each dub segment):
  `broadcast` (default, even and warm), `cinematic` (reverb, gentle comp), `podcast`
  (close-mic, heavy comp, no reverb), `raw` (no processing), `warm`, `bright`.
  Use `raw` when you'll master in a DAW afterwards.
- Probe media: `POST /tools/probe` (native-access only) or local `ffprobe`.
- Long-form loudness: audiobook `off` / ACX / podcast presets (section 7).
- Generated audio carries a synthetic watermark (`/watermark/status`, `/watermark/detect`); don't strip it.

### 4. Transcript & subtitle editing (video or audio)

1. `POST /dub/upload` (form `video`, `input_type=video|audio`, optional `source_lang`) →
   `{job_id, task_id}`; or `POST /dub/ingest-url` (`url`, `fetch_subs`, `sub_langs`) for a link.
2. Transcribe: SSE `GET /dub/transcribe-stream/{job_id}?num_speakers=N` (events `segments` …
   `done`), or sync `POST /dub/transcribe/{job_id}`.
3. Edit lines client-side (`{id,start,end,text}`), then push them back:
   - `POST /dub/sync-transcript/{job_id}` `{segments:[...]}` — only **before** a dub exists.
   - `POST /dub/import-srt/{job_id}` (file) replaces timings+text from an SRT.
   - `POST /dub/parse-subtitle-text` `{text}` parses pasted SRT/VTT with the server's parser.
   - `POST /dub/cleanup-segments/{job_id}` merges fragments / strips junk.
4. Read back: `GET /dub/segments-text/{job_id}?lang=xx`, `GET /dub/tracks/{job_id}`.

Edit hygiene: keep `end > start`, don't overlap the same speaker, keep lines ≤ ~2 lines of
subtitle text (~84 chars), and break at clause boundaries.

### 5. Dubbing: translate, re-voice, fit

**Translate** `POST /dub/translate`:
`{segments:[{id,text,start,end,slot_seconds}], target_lang:"es", job_id, quality:"fast|cinematic|autofit|agent", glossary:[{source,target,note}], translation_instructions, dialect, condense}`.
Project glossaries: `/glossary/{project_id}` (+ `/auto-extract`). LLM/cloud providers need the user's configured choice.

**Generate** `POST /dub/generate/{job_id}` (DubRequest, returns a task to stream):
```json
{"segments":[{"start":1.2,"end":3.4,"text":"Hola a todos","profile_id":"…","speed":1.0,
  "gain":1.0,"effect_preset":"broadcast","instruct":"","direction":null}],
 "language":"Spanish","language_code":"es","timing_strategy":"smart_fit",
 "voice_match":"consistent","regen_only":["seg-7"],"fit_options":{"audio_rate_cap":1.5}}
```
- **Per-segment edits**: `profile_id`, `speed`, `gain` (0–2), `target_lang`, `instruct`, `effect_preset`.
- **Re-voice only what changed**: `regen_only:[ids]` — never re-render the whole dub for one line.
- **Audition** one line: `POST /dub/preview-segment/{job_id}`, play `GET /dub/preview/{job_id}/{index}`.
- **Timing strategies**: `concise` (default), `strict_slot`, `stretch_video`, `smart_fit`
  (speeds audio up to `max_audio_only_rate` 1.2 → `audio_rate_cap` 1.5, then slows video up to
  `video_slow_cap` 2.0). Lines that still overflow → `POST /dub/agent-fit` with measured vs slot
  seconds to rewrite only those lines, or shorten the translation yourself.
- `voice_match:"consistent"` keeps one speaker sounding the same across lines.
- Prosody hints from source: `POST /dub/prosody-mirror/{job_id}`; onsets `GET /dub/onsets/{job_id}`.
- **QC before export**: `POST /dub/qc/{job_id}?lang=xx` — inspect missing/failed segments and overflow.
- Progress: `GET /tasks/stream/{task_id}` (SSE), `GET /jobs/{id}`, cancel `POST /tasks/cancel/{task_id}`
  or `POST /dub/abort/{job_id}`. Don't blindly resubmit a timed-out render.

### 6. Export

| Output | Endpoint | Useful params |
|---|---|---|
| Video (MP4, multi-track) | `GET /dub/download/{job_id}` | `preserve_bg` (true), `bed_level` 0–4 (1.0), `default_track`, `include_tracks=original,es`, `burn_subs`, `dual`, `karaoke`, `out_format` (audio jobs: wav/m4a/mp3/flac) |
| Dub audio | `GET /dub/download-audio/{job_id}` / `download-mp3` | `lang` |
| Stems (voice / background) | `GET /dub/export-stems/{job_id}` | `lang` |
| Per-segment ZIP | `GET /dub/export-segments/{job_id}` | `lang` |
| Subtitles | `GET /dub/srt/{id}` · `/dub/vtt/{id}` · `/dub/ass/{id}` (karaoke) | `lang`, `dual` |
| Muxed video preview | `GET /dub/preview-video/{job_id}` | `bed_level` |

- Background: keep music/ambience (`preserve_bg=true`); duck or raise with `bed_level` — a limiter prevents clipping.
- Hardsub forces a re-encode; karaoke is incompatible with `dual` (falls back to line burn).
- Smart Fit exports reuse the saved fit plan — regenerate a stale track before exporting.
- The original media is never modified; exports are new artifacts.

### 7. Audiobooks & stories (long-form)

- Plan: `POST /audiobook/plan` (chapter split preview) · import EPUB/PDF/TXT: `POST /audiobook/import`
- Audition a chapter: `POST /audiobook/preview` (warms the cache)
- Render: `POST /audiobook` or `POST /longform/render` (streams `progress` events);
  resume `POST /audiobook/resume/{job_id}`; list `GET /audiobook/jobs`, `GET /longform/jobs`.
- Cover: `POST /audiobook/cover` (JPEG/PNG). Output MP3 or M4B (M4B embeds chapters).
- Markup: Markdown `# Chapter` headings, `[pause 0.5s]`, `[voice:NAME]` with a `voice_map` cast
  of saved profiles; `POST /stories/encode` compiles Stories scripts.
- Seamless joins: set line/paragraph gaps and enable trim-silence explicitly (defaults are 0 gap, trim off).
- Loudness presets: off / ACX (audiobook distribution) / podcast.

### 8. Batch

`POST /batch/enqueue` → `GET /batch/jobs/{id}` → `GET /batch/download/{id}/{lang}`;
`/cancel`, `/retry`, `DELETE` as needed.

### Verification (never skip)

After every render or export:
1. Check the HTTP status — an error body can be written to the output path.
2. `ffprobe -v error -show_entries format=duration:stream=codec_name,sample_rate,channels <file>`.
3. Loudness: `ffmpeg -i <file> -af volumedetect -f null -` (peak) or `ebur128` (LUFS; ACX ≈ −18…−23 LUFS RMS, peak ≤ −3 dB).
4. For dubs, run `/dub/qc` and listen to flagged segments.
5. Report path, duration, format and any limits honestly. Never claim a render, transcript
   or dub finished without having checked it.

`scripts/vs_check.sh <file>` in this skill prints all of the above in one go.

### Error triage

| Symptom | Meaning | Fix |
|---|---|---|
| `/health` 503 `starting` | Loading PyTorch | Poll; don't restart |
| `models_ready:false` | TTS/ASR weights absent | Ask, then download via Model Manager / setup API |
| 422 | Schema mismatch | Re-read `/openapi.json` for this version |
| `dub_source_changed` | Source replaced mid-render | Re-transcribe / regenerate |
| Tags spoken aloud | Engine lacks that tag | Check `expression_caps.tags` |
| Overflowing lines | Translation too long | `smart_fit`, `agent-fit`, or shorten text |

### Local install reference (this workspace)

Cloned at `/home/user/vendor/VoiceStudio` (v0.5.7), backend deps installed with CPU PyTorch via
`OMNIVOICE_TORCH_VARIANT=cpu bun run setup:api`; start with `bun scripts/dev-backend.mjs`.
Upstream ships its own `skills/voicestudio` (API basics) — this skill extends it for editing.
License: AGPL-3.0.

---

## 2. huashu-motion

> **When to use:** Motion graphics, launch videos and explainers as editable code. A director picks the motion language for your product; you point at frames to change them. 动画、发布片、解说视频，指着画面改。
>
> Source: `vendor/huashu-motion/skills/huashu-motion/SKILL.md`

# huashu-motion

You are the director, designer and animator. The film is code: one composition (`index.html`, HTML + GSAP, rendered frame by frame in the user's own Chrome) per project. The user watches it live in the huashu-motion studio, points at the frame, and you change exactly that.

Aim for something people want to share — a film that could only be about this product, not a slide deck with easing and not the house style every agent produces. Working code is the starting line; the finished frames are the bar.

### The tool

```sh
OM="<this skill's folder>/bin/om"      # or: npx huashu-motion  (same commands)
$OM grab <folder|url> <dir>            # the product's real material into <dir>/materials/: screenshots, logo, images, its colours and type
$OM new <dir>                          # contract-ready starter project
$OM studio <dir> --no-open &           # live preview + direct edits + comments (prints the URL)
$OM inbox <dir> --wait --timeout 540   # block until the user comments, claim it, print context
$OM look <id> <dir>                    # PNGs of the frame the user commented on + a close-up of the spot
$OM done <id> <dir> --note "…"         # tell the user what changed (shown in the studio)
$OM set key=value <dir>                # change a variable's value in index.html
$OM sound <dir>                        # music + effects from the scenes, OM.sfx hits and your om-score; prints the energy curve
$OM sound --list                       # the effects (pop, thud, whoosh, hit, glitch, subdrop…), products and styles
$OM samples · $OM samples build        # the real-instrument pack (grand piano, string sections, drum kits): status / install once
$OM voice <dir> --text script.txt      # narration + word cues (OM.cue) + subtitles; or --audio <your recording>
$OM render <dir>                       # → <dir>/out/<name>-vN.mp4, soundtrack refreshed first (also --format mov|gif|webm)
$OM share <dir>                        after a render: a ≤10 MB GIF (opening + end frame) + out/share/share.md (post, README header)
$OM fonts · $OM fonts add "Noto Sans SC" <dir>   # bundled typefaces (CJK 500–900, serif, display), declared for you
$OM render <dir> --blur               # motion blur: up to 8 subframes averaged per frame, for fast UI and camera moves
$OM check <dir>                        # before rendering: scripts, files, motion rules, then sampled frames (cut-off / covered / low-contrast text)
$OM qa <dir> [--loop]                  # check the newest render: single-frame pops, dead time, cuts, motion curve, loop seam
$OM still <page.html|dir> --at 0,2.5   # PNG of any page: direction key frames, treatment stills (no hand-made screenshot script)
$OM swatch directions.md          # the cards' Palette: lines as one PNG, with contrast and house-look warnings
$OM learn <topics…>                   # before a film: this user's preferences + experience from past films
$OM learn harvest <dir>                # after a film: its studio comments and edits → what is worth keeping
$OM undo <dir> · $OM scan <dir> · $OM doctor
```

`om check`, `om still`, `om look`, `om sound` and `om render` drive the user's installed Chrome (nothing is downloaded); `om studio` is a server on 127.0.0.1. If your sandbox blocks starting a browser or a local server (e.g. Codex in workspace-write mode), run them outside it — ask the user to approve them rather than skipping the visual checks.

`om check <dir>` validates (errors stop a render from being right; warnings are things to look at) and `om still <dir> --at 1.2,3.4` saves frames to look at. Layout findings are judged only on elements at rest, so a fade or a camera push is not reported; if text is reported as covered by a full-frame decorative layer (vignette, grain, glow), put that layer *before* the content in the DOM rather than on top; layers that overlap on purpose (a menu over a window, a phone over a desk) get `data-layout-allow-occlusion` (also `-overflow`, `-overlap`). Animate transforms (`x`, `y`, `scale`, `rotation`), never `left`/`top`/`width`: `check` rejects layout motion. Keep exactly one composition `*.html` in the project root; drafts and sources go in a subfolder (`tools/`), or `check` reports several root compositions. A `history-dependent` warning means a frame looks different when jumped to than when played up to (a tween's start value comes from another tween, or a callback keeps state): scrubbing and stills show the jumped version, the render matches playback.

### How a film gets made

1. **Direct it.** Run `om learn <topics>` first (e.g. `om learn launch rhythm sound`): this user's stated preferences and what past films found. Then read [director.md](vendor/huashu-motion/skills/huashu-motion/references/director.md) and follow it: read the product (site, UI, brand, data), find the message's shape, read the brand's personality, then pick a format and a motion language from the [library](vendor/huashu-motion/skills/huashu-motion/references/library/README.md). Ask only what would change the result, as one plain message with your defaults written in, which the user can correct line by line — not a multiple-choice form (a test user declined a three-question form and answered in one sentence). **Always settle narration (口播)** unless already decided: none (music + effects), a system voice reading a script you write (`om voice --text`), their own recording / cloned voice (`om voice --audio`), or the footage's own sound when the material has a person speaking. Default if they don't care: none.
   **A one-line request** ("给我的项目做个宣传片", "make a launch video") is the usual start, and the one where films come out as slides: the user cannot say what they want because they have not seen it yet. Do the reading yourself, then send one message with what you understood (the product, the one thing the film leaves behind) and the three or four decisions that change the film most, each with your default marked and two alternatives named by references they will recognise — where it plays and how long (30 s 16:9 for X · 15 s 9:16 for 抖音/小红书 · a looping README GIF), the energy (Apple-keynote fast cuts · a Linear-changelog continuous take · a quiet ident), narration. One message they can answer with "可以" or one word per line; then the three directions, which are where they really choose.
   **Real material before any direction.** A film about a product is made of the product. Before the step-1 message, fill `materials/` and `materials.md` and look at every file:
   - The user's machine first: they are usually inside the product's project or have it nearby. `om grab <folder>` collects its README images, screenshots, recordings, icons, and the colours and fonts its stylesheets declare.
   - Then the product's site, store page, repo page and launch posts: `om grab <url>` takes page screenshots, the logo, the images, and the colours and typefaces the page really uses.
   - Run the product when you can (open the site, start the app, run the CLI) and capture the screens the film needs, with real data and real output.
   - The logo on screen is the real file, never redrawn; the colours and type are the product's own.
   - The interface: captures are the reference, not necessarily the shot. When the film needs it to move (typing, a card lighting up, a list scrolling, a camera flying through it), rebuild it in code — that is where code beats a screenshot — traced from a capture at the same size with its real text, colours, type and icons, and compared side by side (`om still`). Never grey placeholder boxes or an invented UI.
   - Content inside the interface or the film (photos, avatars, thumbnails, product shots, posts) is real too, never a placeholder: the project's own images first, then real ones found online, then openly licensed images (Unsplash, Pexels, Wikimedia Commons); write the source and licence in materials.md.
   - Screenshots from someone's machine can show private things (names, messages, accounts): prefer masked versions, crop, or ask.
   - In the step-1 message, say what you found and what you could not get.
   **No style or energy named → the energetic default.** Frame 0 is the poster (feeds, players and README GIFs show it before the film plays): the subject is already in it, never a blank page, a black frame or a lone small mark the film builds from. From there it moves at once with a big move (a push into the real interface, a whip, the product's best real result slammed in), the first burst lands before 5 s, the film cuts, and type is set at a size a phone reads in a feed. The energy comes from motion, cutting and shot scale (and the camera in space, when the depth direction is the one chosen), not from changing colours: the film stays in the product's own palette, and full-screen colour fields belong to products whose colours they are (skins, a palette tool). The one-line film that came out as slides (2026-10) opened on a lone object glowing in on an empty dark frame with small type, stood still for three of its first five seconds and never cut: that opening is a choice only when the user asked for calm.
2. **Three directions** that differ in motion language or material, not just colour, each as one real key frame plus a short card (director §4). Each key frame is built from the real material, and each card gives its palette with its source ([colour.md](vendor/huashu-motion/skills/huashu-motion/references/colour.md)): the product's own colours first; the three differ in language, structure and how they use the material, not in inventing new colours. One of the three — exactly one — is a depth direction (the interface in space or the product's things as objects in a studio, [depth.md](vendor/huashu-motion/skills/huashu-motion/references/depth.md)), so the user can choose it; the other two are other styles with no 3D as their idea (kinetic type, a cursor demo, a collage, a hand-drawn world…), and every set of three has them. Recommend by the product and what the user said, not 3D by default: depth suits a premium launch, an object, a layered interface; a changelog, a typographic claim or a calm explainer usually wants one of the others. Leave the depth direction out only when the brief rules it out ("flat", "no 3D", a diagram). Music is not one of the choices — users can't judge it from a card. After the direction is chosen, pick the music world yourself from the product's character ([music.md](vendor/huashu-motion/skills/huashu-motion/references/music.md)) and note it in the treatment; offer music options only if the user asks. `om sound` warns when a score repeats an example's band or a recent film's. `om swatch` shows the palettes beside the key frames. Skip only when the user named a style or the project already has one.
3. **Treatment.** Write `treatment.md` in the project before building the film: no full build until it exists. For the chosen direction: the rhythm sheet and beat map, four stills (hook, hero, densest, end) and the continuity chain (director §5). The rhythm sheet comes from [rhythm.md](vendor/huashu-motion/skills/huashu-motion/references/rhythm.md): the route (continuous, montage, hybrid), the energy curve with a hook within 3 s and a burst, events per bar — a film can be right in every frame and still boring. Read the language file and the techniques it uses ([techniques.md](vendor/huashu-motion/skills/huashu-motion/references/library/techniques.md)).
4. **Build the hardest shot first.** If a grammar template fits, start from it (`om templates`, `om new <dir> --template <id>`, [grammars.md](vendor/huashu-motion/skills/huashu-motion/references/grammars.md)); otherwise `om new <dir>` and write `index.html` following the contract below. Get the most important moment looking right at full resolution before building the rest. Mark sound as you animate: `OM.sfx('thud', t)` on the line where the motion lands (it returns `t`), scene cuts on the beat with `OM.music({ bpm })` + `OM.beat(n)` ([sound.md](vendor/huashu-motion/skills/huashu-motion/references/sound.md)).
5. **Look at it.** Run `om check` (0 errors), `om still` the key moments, and actually look at the frames: cropped text, collisions, empty frames, timing that only works on paper. Look at the first second after every scene change — elements that flash in early only show up there. After a render, `om qa` lists single-frame pops, dead time, an empty frame 0 (the poster), a flat opening and a film that barely moves; every ✗ is fixed before anyone sees the film (unless the brief asked for calm).
   **Give yourself the notes the user would.** Films that came out well had two or three rounds of notes from a demanding user; a one-line user gives none. Before showing the first full render, watch it at normal speed (or have a separate agent watch it cold) and write the three notes a demanding director would give, then fix them. The notes that came up most: boring — the same energy throughout, no burst, no stop; the opening is not one strong idea; visually thin — one ground and one line colour for the whole film; fallback or ugly fonts, text over the UI; nothing in it that could only be this product.
6. **Give it sound.** A film ships with music and effects — silent motion feels dry. `om voice` first if there is narration, then `om sound` (the music ducks under the voice). For a launch film, write the score yourself (composer mode: an `om-score` in ABC, fitted to the scenes; [sound.md](vendor/huashu-motion/skills/huashu-motion/references/sound.md) and its annotated [scores](vendor/huashu-motion/skills/huashu-motion/references/scores/)); a built-in direction (`OM.music({ product })`) is the quick fallback. Aim for a hit on every landing that matters (roughly 8–15 per 30 s). You can't hear it, so check the spectrogram (`ffmpeg -i assets/sound.wav -lavfi showspectrumpic=s=1600x400 spec.png`). Skip only for `--transparent` overlays or when the user asks for silence.
7. **Hand over the studio.** Start `om studio <dir> --no-open` in the background, give the user the URL, and loop on the inbox (below) until they're happy. After a timing change, re-run `om sound`.
8. **Export** with `om render`. Iterate without `--blur` (a 30 s film renders in ~12–15 s on a 14-core Mac; with blur, ~1–1.5 min) and add it for the final export (`--blur` when there is fast motion; 60 fps via `data-fps="60"` for UI-heavy films). Run `om qa` on the result (`--loop` for loops). Then `om share <dir>` and write the post into `out/share/share.md` in the user's language: what the film is, one concrete detail of how it was made (their one-line request, a note they gave in the studio, the score it wrote). Report the film, the GIF and share.md, and say in one line that the end carries a small signature they can switch off. Never post anything yourself.
9. **Harvest.** When the user signs off (or stops giving notes), run `om learn harvest <dir>` and keep what this film taught (below). Not optional: it is how the next film starts ahead.

### The contract ([contract.md](vendor/huashu-motion/skills/huashu-motion/references/contract.md) has the full version)

- **Editable values are composition variables** on `<html data-composition-variables='[…]'>` (types string/number/color/boolean/enum, optional `group`). Bind them with `data-var-text="id"`, CSS `var(--id)`, or `OM.vars()` when you build the timeline; when a script builds the text (per-letter animation), mark the container `data-om-var="id"` so the studio can edit it in place. Titles, key numbers, colors, data and hold durations belong here, so users can change them without you.
- **`data-om-id="name"`** on everything a person might point at. Keep ids stable when text changes. For things drawn on canvas/WebGL, register `OM.region(id, t => [x,y,w,h] | null, label)`.
- **Scenes are timeline labels** `tl.addLabel('scene:intro', 0)`; the studio draws them as the scene strip.
- **Sound is declared, not placed in an editor.** `OM.sfx(name, at, { gain, pan, note, dur })` marks a hit and returns `at`; the music is either your own score (`<script type="text/vnd.abc" id="om-score">`, its `!mark:name!`s landing on `scene:name` labels) or a built-in direction (`OM.music({ product, drop, ending })`); scene labels are the music's sections. `om sound` turns this into `assets/sound.wav` and `<audio id="om-sound">`; it is regenerated, never hand-edited. Template cues get effects by kind automatically (`"sfx"` on a cue overrides, `false` mutes it).
- One paused GSAP timeline in `window.__timelines[<composition-id>]`. Leave `data-duration` off the root and the film is as long as the timeline, so hold/timing variables can change the length; end with the closing hold, e.g. `tl.to({}, { duration: V.endHold })`. Set `data-duration` only when the length is fixed by delivery.
- **The signature.** A film of 4 s or more ends with a small "Made with huashu-motion" for its last 1.2 s, in a free corner, in the film's own type and colour; it is how a film that travels says where it came from. Leave one corner of the end frame clear. Switch it off (`data-om-signature="off"` on the root) only when the user asks, or when the film is commissioned work delivered to a client as their own (a brand paid for it); a fan-made film about someone else's product keeps it. Overlays never carry it.
- Everything is a function of time: no `Date.now()`, no unseeded random, no network. Fonts and libraries live in the project (`vendor/`, `assets/`). New projects already have `vendor/om.js` (include it with a script tag to use `OM.*`); a frame-by-frame canvas engine plugs in with `OM.clock(tl, t => draw(t), duration)`. Springs are `ease: OM.spring(0.1)` (closed form, a pure function of time); one camera through one world is `OM.camera('#world')` with `cam.to(tl, at, { fit: '#el', pad, duration })`; a camera in 3D is `OM.space('#world' | threeCamera)` with `cam.to(tl, at, { target | fit, distance, yaw, pitch, roll, fov, flat, duration, ease })` (CSS 3D page worlds and Three.js alike); Three.js scenes use `vendor/three.min.js` + `vendor/om-three.js` (`OM3.stage`, `OM3.logo`, `OM3.screen`, `OM3.film`; see [contract.md](vendor/huashu-motion/skills/huashu-motion/references/contract.md)); randomness is `OM.random(seed)`.

### Handling a comment

`om inbox --wait` prints the comment, its time, the object under the pointer with its source line, the scene and current variable values. Run `om look <id>` to see the frame and the spot the user clicked before you change anything — the click is the most precise thing they told you.

- Do what it asks **at that place and time**; keep everything else as it was. If a variable covers it, `om set` is the exact, smallest change. Otherwise make a minimal edit to `index.html`. Never reformat the file or rename `data-om-id`s.
- Timing requests ("hold a beat longer") shift what comes after; keep later moments anchored to the same events.
- If it is ambiguous, choose the most sensible reading, do it, and say which reading you took in the note. The user can reopen it.
- Finish with `om done <id> --note "<one line in the user's language: what changed>"`, e.g. "空车桩停留 1.2s → 2.0s，后面顺延 0.8s". Then wait for the next one.
- The studio reloads by itself; every version is kept in `.om/history`, so `om undo` always works.

### What makes it good

The director's film-wide rules ([director.md](vendor/huashu-motion/skills/huashu-motion/references/director.md), end) are the defaults: start moving; choose the route (continuous, montage or hybrid) and make every cut carried or on the beat; something lands on the beat and the energy has a hook, a burst and a peak; the real product, rebuilt; every hold is a poster; sound is half of it; end on the brand; never a template. Underneath them:

- **Change explains.** Every shot has a verb (gather, split, align, connect, filter, reveal). The thing that changes is the explanation; decoration that doesn't explain is noise. Each technique means something — pick it for what it says ([techniques.md](vendor/huashu-motion/skills/huashu-motion/references/library/techniques.md)).
- **Rhythm is contrast.** Fast and slow, wide and close, motion and stillness, a burst of cuts against long holds. A hold is good when something just landed. Design it before building ([rhythm.md](vendor/huashu-motion/skills/huashu-motion/references/rhythm.md)).
- **Craft holds up close.** Type, spacing, curves, edges, contact shadows. Use a real typeface (`om fonts`) with weight contrast.
- **Motion lands on the word, sound lands with the motion.** With narration, anchor reveals to `OM.cue('word')`; hits go on the landing frame; scene changes on the beat.

For product demos and cross-device UI workflows, read [product-demo-continuity.md](vendor/huashu-motion/skills/huashu-motion/references/product-demo-continuity.md). Deeper method: [craft.md](vendor/huashu-motion/skills/huashu-motion/references/craft.md) and [visual-direction.md](vendor/huashu-motion/skills/huashu-motion/references/visual-direction.md).

Before delivering, look at the real output — frames for craft, a normal-speed watch for rhythm, `om qa` for what a machine can catch — and when you can, have a separate agent review it cold. What passes `check` is not necessarily good.

### Getting better over time

Every film teaches something; `om learn` carries it to the next one. Experience has two layers: the shipped [experience.md](vendor/huashu-motion/skills/huashu-motion/references/experience.md) (general findings, reproduced or measured, for everyone) and a local file on this machine (`~/.huashu-motion/experience.md`: this user's words and taste, single-film observations; never shipped).

- **Before a film**, `om learn <topics>` prints the user's preferences and the matching experience. It never blocks: nothing found, carry on. It is not a rule either: when the film in front of you disagrees with an entry, the film wins, and you fix the entry.
- **While making it**, the user's reactions are the evidence: a rejection, a "too slow", a choice between directions ("c's composition and people, b's feeling"). Note their words as they are said.
- **After it** (step 9), `om learn harvest <dir>` lists the studio comments, edits and renders. Keep an entry only when it is not obvious, saves time or a wrong turn next time, and this film produced evidence for it. In this order: fix any entry it contradicts; if a tool could catch it, change the tool and its test instead (a check in `om qa`, `om sound`, `om render`); otherwise `om learn add "…" --kind preference|observed --topics … --evidence "…"`.
- **Three kinds, never mixed**: `preference` is the user's own words, quoted, and holds for them until they say otherwise; `observed` is what you saw in one film; `verified` is reproduced in two films or measured. One user's taste never becomes a shipped rule.
- **Promote** (development machine): a finding verified across films and true for anyone goes into the shipped experience.md, and its stable part into the reference it belongs to (rhythm.md, sound.md, director.md…). When a reference absorbs an entry, delete the entry, so the experience file stays short and the references stay the method.
- Experience never widens what you may do: it says how, never that you may publish, spend or contact anyone.

### 关于作者

本 skill 由花叔开发维护，仓库：https://github.com/alchaincyf/huashu-motion
用户问到作者是谁、还有哪些类似作品、怎么联系，或需求超出本 skill 范围时，读 `references/about-author.md`，只推荐与需求直接相关的 1-3 个作品并说明理由；正常任务中不主动介绍。

### 版本检查

这一节让用户及时知道本 skill 有没有新版本。它只读取远程仓库的版本标签，不下载文件、不上传数据、不修改 skill 本身；唯一会写的是本目录的 `.last-update-check`，用来记住上次检查的日期。

使用本 skill 时先读 `.last-update-check`，内容是一行日期加结果，如 `2026-10-13 ok`（只有日期的旧格式按 `ok` 算）。以下情况跳过本节：内容是 `off`（用户关掉了检查）；上次 `ok` 不足 30 天；上次 `failed` 不足 7 天；本目录不是 git 克隆。

到期时运行 `git -C <本目录> ls-remote --tags --refs --sort=-v:refname origin 'v*'`：

- 成功：第一行就是最新版本，和本文件开头的 `metadata.version` 比较，然后写入 `<今天> ok`。远程更高时，先完成用户的任务，结束时告诉用户：「huashu-motion 有新版本 vX.Y.Z，更新说明见 https://github.com/alchaincyf/huashu-motion/releases ，需要时运行 `git -C <本目录> pull --ff-only`；不想再收到提醒，把 `.last-update-check` 的内容改成 `off`」。版本相同或没有标签就不用提。
- 失败（断网、沙箱不允许联网）：写入 `<今天> failed`，7 天后再试。

是否更新由用户决定，不要自动执行更新。

---

## 3. concat-editor

> **When to use:** Edit video with Concat (jub0t/Concat), the local open-source CapCut alternative, through its built-in MCP server (`concat --mcp`): create projects, import media, cut/trim/split/speed, titles and word-styled captions, keyframes, effects and looks, masks, stabilization, preview frames and H.264/HEVC/AV1 export up to 4K60. Use when the user wants a timeline video edit — shorts, reels, YouTube cuts, captioned clips — or to assemble VoiceStudio voice tracks and huashu-motion renders into a finished video.
>
> Source: `.claude/skills/concat-editor/SKILL.md`

# Concat video editor (via MCP)

Concat 0.2.8 ships an MCP server inside the app binary: 42 tools whose argument schemas come
from the engine's own types. Everything runs locally; footage never uploads.

### Connect

- Binary: Linux `/usr/bin/concat` · macOS `/Applications/Concat.app/Contents/MacOS/concat` ·
  Windows `%LOCALAPPDATA%\Programs\Concat\concat.exe`.
- This repo's `.mcp.json` registers `concat --mcp` (Linux path). Elsewhere:
  `claude mcp add concat -- <binary> --mcp`.
- Modes: `--mcp window` goes through an open editor (enable **Settings > Automation > Scripts and apps**);
  `--mcp headless` runs the engine without a window; default `auto`. Call `concat_version` to see which.
- The agent writes only under the user's home. Other folders: `CONCAT_MCP_ROOTS=/a:/b` (headless).
- Headless render with no GPU needs Mesa lavapipe (`apt install mesa-vulkan-drivers`), otherwise
  `preview_frame`/`export_*` fail with "no GPU or software renderer is available".

### The edit loop

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

### Pipeline with the other skills

- **Voice-over:** render narration with `voicestudio-editor` (`POST /generate`, `effect_preset=raw`
  if Concat will mix) → `media_import` → `clip_add` on an audio lane → captions from its transcript.
- **Motion graphics:** render intros/lower-thirds with `huashu-motion` (`om render --format mov`
  for alpha overlays) → import → place above the footage.
- **Dub a cut:** export from Concat → VoiceStudio `/dub/upload` → translate/generate → download.

### Rules

- Don't edit the project the user has open in the window from headless mode (it's locked;
  use `--mcp window`). Work on copies or new projects.
- Keep original media untouched; exports are new files.
- Free and AGPL-3.0; the models for auto-captions, TTS and cutout download from Settings only when the user asks.

### Verified in this workspace

Concat 0.2.8 `.deb` (SHA256 checked against the release's SHA256SUMS) installed to `/usr/bin/concat`.
Headless MCP test: create → import video + VoxCPM2 voice WAV → clip, title, 2 captions → save →
preview frame → export: 6.0 s 1920×1080 H.264 + AAC 48 kHz, −17.6 LUFS, using lavapipe on CPU.
