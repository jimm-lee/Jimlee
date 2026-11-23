#!/usr/bin/env python3
"""Clean a voice memo before it is cut: less breathing, less background hiss, clearer voice.

Usage: python3 clean_take.py take.m4a take.words.json out.wav [--report]

1. Noise reduction (noisereduce spectral gating, 80 %, hiss profile from the gaps): the phone/room hiss.
2. Breaths: frames outside the spoken words (Whisper word timings, padded so word edges are never touched), and
   breathy frames inside long word spans (noisy, quiet, at least BREATH_MIN long), are turned down by BREATH_DB
   with short ramps, so the gaps fall to near-silence instead of an audible in-breath.
3. Clarity (ffmpeg): high-pass, less boxiness at 250 Hz, presence at 3–5 kHz, de-esser, gentle compression.
Writes 48 kHz mono WAV. stitch_vo.py then cuts the selects from the cleaned takes.
"""
import json
import subprocess
import sys

import numpy as np
import noisereduce as nr
import soundfile as sf

SR = 48000
FRAME = 0.02            # s analysis frame
PAD_BEFORE = 0.06       # s kept before each word's start (Whisper starts can be late on plosives)
PAD_AFTER = 0.10        # s kept after each word's end (word tails, decays)
BREATH_DB = -24.0       # gain on breaths and gaps
BREATH_MIN = 0.15       # s: a breathy stretch inside a word span must last this long to count (spares s/f/sh)
RAMP = 0.025            # s fade in/out of the attenuation
CLARITY = ("highpass=f=85,equalizer=f=250:t=q:w=1.2:g=-2.5,equalizer=f=3800:t=q:w=1.4:g=3,"
           "equalizer=f=9000:t=h:w=2000:g=1,deesser=i=0.35:m=0.5:f=0.5,"
           "acompressor=threshold=0.1:ratio=2.5:attack=6:release=180:makeup=1.5")


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def frame_features(x):
    n = int(FRAME * SR)
    frames = x[: len(x) // n * n].reshape(-1, n)
    rms_db = 20 * np.log10(np.sqrt((frames ** 2).mean(axis=1)) + 1e-9)
    spec = np.abs(np.fft.rfft(frames * np.hanning(n), axis=1)) ** 2 + 1e-12
    freqs = np.fft.rfftfreq(n, 1 / SR)
    band = spec[:, (freqs > 300) & (freqs < 8000)]
    flatness = np.exp(np.log(band).mean(axis=1)) / band.mean(axis=1)
    return rms_db, flatness, n


def breath_mask(x, words):
    """True where the frame is breath or gap (to be turned down)."""
    rms_db, flat, n = frame_features(x)
    t = (np.arange(len(rms_db)) + 0.5) * FRAME
    in_word = np.zeros(len(t), bool)
    for _, s, e in words:
        in_word |= (t >= s - PAD_BEFORE) & (t <= e + PAD_AFTER)
    speech_level = np.median(rms_db[in_word]) if in_word.any() else rms_db.max() - 20
    breathy = (flat > 0.28) & (rms_db < speech_level - 9)
    # inside word spans, only long breathy runs (an in-breath), never short fricatives
    run = np.zeros(len(t), bool)
    i = 0
    while i < len(t):
        if breathy[i] and in_word[i]:
            j = i
            while j < len(t) and breathy[j] and in_word[j]:
                j += 1
            if (j - i) * FRAME >= BREATH_MIN:
                run[i:j] = True
            i = j
        else:
            i += 1
    return (~in_word) | run, n, speech_level


def apply_gain(x, mask, n):
    g = np.where(mask, 10 ** (BREATH_DB / 20), 1.0)
    g = np.repeat(g, n)
    g = np.concatenate([g, np.full(len(x) - len(g), g[-1] if len(g) else 1.0)])
    k = int(RAMP * SR)
    g = np.convolve(g, np.ones(k) / k, mode="same")   # smooth ramps, no clicks
    return x * g


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    src, words_path, out = sys.argv[1:4]
    words = json.load(open(words_path))
    x = decode(src)
    # hiss profile learned from the gaps between words only, so quiet consonants (the "v" in "vest") are kept;
    # the adaptive (non-stationary) mode took them for noise
    gap = np.ones(len(x), bool)
    for _, s, e in words:
        gap[max(0, int((s - 0.15) * SR)):int((e + 0.2) * SR)] = False
    noise = x[gap] if gap.sum() > SR else None
    clean = nr.reduce_noise(y=x, sr=SR, y_noise=noise, stationary=True, prop_decrease=0.8)
    mask, n, level = breath_mask(clean, words)
    y = apply_gain(clean, mask, n)
    tmp = out + ".tmp.wav"
    sf.write(tmp, y.astype(np.float32), SR, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", CLARITY, "-ar", str(SR), "-c:a", "pcm_s24le", out],
                   check=True)
    subprocess.run(["rm", "-f", tmp], check=True)
    if "--report" in sys.argv:
        gaps = mask.mean() * 100
        print(f"{out}: speech level {level:.1f} dBFS, {gaps:.0f} % of frames turned down by {-BREATH_DB:.0f} dB")


if __name__ == "__main__":
    main()
