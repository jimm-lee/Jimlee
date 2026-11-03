#!/usr/bin/env bash
# Verify a VoiceStudio output: format, duration, peak and integrated loudness.
set -euo pipefail
f="${1:?usage: vs_check.sh <audio-or-video-file>}"
[ -s "$f" ] || { echo "ERROR: $f missing or empty" >&2; exit 1; }
if head -c 1 "$f" | grep -q '[{<]'; then echo "ERROR: $f looks like a text/JSON error body:" >&2; head -c 300 "$f" >&2; exit 1; fi
ffprobe -v error -show_entries format=format_name,duration:stream=codec_type,codec_name,sample_rate,channels -of default=nw=1 "$f"
ffmpeg -hide_banner -nostats -i "$f" -af volumedetect -f null - 2>&1 | grep -E 'mean_volume|max_volume' | sed 's/.*\] //'
ffmpeg -hide_banner -nostats -i "$f" -af ebur128 -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | sed 's/^ *//' || true
