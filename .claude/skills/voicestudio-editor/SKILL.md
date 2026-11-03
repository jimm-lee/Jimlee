---
name: voicestudio-editor
description: Master editing skill for VoiceStudio (debpalash/VoiceStudio) — the local, open-source voice studio. Covers speech generation and re-takes, voice cloning/design/conversion, transcript and subtitle editing, video dubbing (translate, per-segment re-voice, timing fit, QC, mixing, hardsub/karaoke export), audiobook/story production with chapters and pauses, DSP effect presets, loudness, and batch jobs, all via the local REST API on port 3900. Use when the user wants to edit, re-voice, dub, subtitle, master, or assemble audio/video with VoiceStudio.
---

# VoiceStudio Master Editor

Drive a running VoiceStudio backend to edit speech, video dubs and long-form audio.
Everything runs locally. Model downloads, cloud translation providers and remote
backends require the user's explicit consent.

**Base URL:** `http://localhost:3900` (honor `OMNIVOICE_PORT` / the user's configured address).
**Contract source of truth:** `GET /openapi.json` on the running version (~312 paths in v0.5.7).
Endpoints below were verified against v0.5.7; re-check the schema if the version differs.

## 0. Preflight (always)

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

## 1. Speech takes and re-takes — `POST /generate` (multipart form)

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

## 2. Voice conversion / cloning / design

- **Convert** `POST /convert` (form): `audio`, `profile_id`, `match_duration` (true), `language`,
  `keep_delivery`. `keep_delivery=true` preserves timing, pauses and intonation (needs CosyVoice 3
  installed; clips >28 s are split at pauses; >10 min refused). Default re-transcribes and re-speaks.
- **Clone** `POST /profiles` with a clean reference (5–20 s, one speaker, no music). The reference's
  *delivery* is copied, not just timbre — a flat reference gives flat output.
  Replace reference audio via `PUT /profiles/{id}/audio`; freeze a good take with `POST /profiles/{id}/lock`.
- **Design** from text: `POST /design/describe`.
- Only clone voices the user is authorized to use; consent/attestation endpoints exist on profiles.

## 3. Clean-up, loudness and DSP

- `POST /tools/normalize-speech` (form `audio` WAV ≤64 MiB, `target_dbfs` −24…−1, default −2) →
  peak-normalized WAV. *Verified: −38.1 dB peak → −2.7 dB at target −3.*
- Effect presets (`effect_preset` on `/generate` and on each dub segment):
  `broadcast` (default, even and warm), `cinematic` (reverb, gentle comp), `podcast`
  (close-mic, heavy comp, no reverb), `raw` (no processing), `warm`, `bright`.
  Use `raw` when you'll master in a DAW afterwards.
- Probe media: `POST /tools/probe` (native-access only) or local `ffprobe`.
- Long-form loudness: audiobook `off` / ACX / podcast presets (section 7).
- Generated audio carries a synthetic watermark (`/watermark/status`, `/watermark/detect`); don't strip it.

## 4. Transcript & subtitle editing (video or audio)

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

## 5. Dubbing: translate, re-voice, fit

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

## 6. Export

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

## 7. Audiobooks & stories (long-form)

- Plan: `POST /audiobook/plan` (chapter split preview) · import EPUB/PDF/TXT: `POST /audiobook/import`
- Audition a chapter: `POST /audiobook/preview` (warms the cache)
- Render: `POST /audiobook` or `POST /longform/render` (streams `progress` events);
  resume `POST /audiobook/resume/{job_id}`; list `GET /audiobook/jobs`, `GET /longform/jobs`.
- Cover: `POST /audiobook/cover` (JPEG/PNG). Output MP3 or M4B (M4B embeds chapters).
- Markup: Markdown `# Chapter` headings, `[pause 0.5s]`, `[voice:NAME]` with a `voice_map` cast
  of saved profiles; `POST /stories/encode` compiles Stories scripts.
- Seamless joins: set line/paragraph gaps and enable trim-silence explicitly (defaults are 0 gap, trim off).
- Loudness presets: off / ACX (audiobook distribution) / podcast.

## 8. Batch

`POST /batch/enqueue` → `GET /batch/jobs/{id}` → `GET /batch/download/{id}/{lang}`;
`/cancel`, `/retry`, `DELETE` as needed.

## Verification (never skip)

After every render or export:
1. Check the HTTP status — an error body can be written to the output path.
2. `ffprobe -v error -show_entries format=duration:stream=codec_name,sample_rate,channels <file>`.
3. Loudness: `ffmpeg -i <file> -af volumedetect -f null -` (peak) or `ebur128` (LUFS; ACX ≈ −18…−23 LUFS RMS, peak ≤ −3 dB).
4. For dubs, run `/dub/qc` and listen to flagged segments.
5. Report path, duration, format and any limits honestly. Never claim a render, transcript
   or dub finished without having checked it.

`scripts/vs_check.sh <file>` in this skill prints all of the above in one go.

## Error triage

| Symptom | Meaning | Fix |
|---|---|---|
| `/health` 503 `starting` | Loading PyTorch | Poll; don't restart |
| `models_ready:false` | TTS/ASR weights absent | Ask, then download via Model Manager / setup API |
| 422 | Schema mismatch | Re-read `/openapi.json` for this version |
| `dub_source_changed` | Source replaced mid-render | Re-transcribe / regenerate |
| Tags spoken aloud | Engine lacks that tag | Check `expression_caps.tags` |
| Overflowing lines | Translation too long | `smart_fit`, `agent-fit`, or shorten text |

## Local install reference (this workspace)

Cloned at `/home/user/vendor/VoiceStudio` (v0.5.7), backend deps installed with CPU PyTorch via
`OMNIVOICE_TORCH_VARIANT=cpu bun run setup:api`; start with `bun scripts/dev-backend.mjs`.
Upstream ships its own `skills/voicestudio` (API basics) — this skill extends it for editing.
License: AGPL-3.0.
