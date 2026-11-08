#!/usr/bin/env python3
"""Stitch the Heavyweight Hills intro voice-over from James's three Movember voice memos.

Usage: python3 stitch_vo.py Movember_1.m4a Movember_2.m4a Movember_3.m4a [out.wav]

Each memo is level-matched to -20 LUFS, the selects below are cut at the silences between phrases (20 ms fade in,
40 ms fade out), joined with short breaths, then voice-processed and normalised to -16 LUFS / -1.5 dBTP.
Writes vo_cues.json next to this script (where each select sits on the timeline).
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
LEAD = 0.30   # s of silence before the first word
TAIL = 0.60   # s after the last word

# (take, in, out, gap after, words). Takes: m1 = Movember_1, m2 = Movember_2, m3 = Movember_3.
PLAN = [
    ("m2", 0.61, 10.55, 0.45, "I'm a little late to the whole Movember conversation, but this year we're still "
                              "taking on a challenge. Just because I haven't posted it doesn't mean I haven't been doing it."),
    ("m1", 9.70, 12.36, 0.20, "30 kilo weight vest, same as last year,"),
    ("m2", 21.86, 33.42, 0.55, "so walking up the hill, walking down the hill obviously, 30 kilos on my back, at least "
                               "one hill every day for the whole month of Movember, and calling it Heavyweight Hills."),
    ("m3", 27.35, 32.05, 0.35, "It's a physical challenge, but as always, there's a bigger reason behind it."),
    ("m3", 32.22, 41.45, 0.30, "It's a memory of someone special. I lost my uncle last year, and in the last three "
                               "months, I've lost two grandparents."),
    ("m2", 47.10, 52.84, 0.45, "And it's there to help raise awareness for men's health, men's mental health specifically,"),
    ("m1", 41.45, 45.45, 0.55, "because we all carry weight, just some of it is invisible."),
    ("m1", 46.30, 54.60, 0.60, "So the weight vest is there to help symbolize the weight that men hold on their "
                               "shoulders, except this time it's visible."),
    ("m3", 71.95, 76.55, 0.00, "So this month, let's make sure no one has to carry that weight alone."),
]
VOICE = ("highpass=f=90,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1:g=3,"
         "acompressor=threshold=0.08:ratio=3:attack=8:release=200:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=7")


def ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def main() -> None:
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    memos, out = sys.argv[1:4], sys.argv[4] if len(sys.argv) > 4 else "Heavyweight-Hills-Intro-VO.wav"
    levelled = []
    for i, memo in enumerate(memos, 1):
        dst = f"_m{i}.wav"
        ffmpeg("-i", memo, "-ac", "1", "-af", "loudnorm=I=-20:TP=-3:LRA=11", "-ar", "48000", dst)
        levelled.append(dst)
    chains, labels, cues, t = [], [], [], LEAD
    for i, (take, a, b, gap, words) in enumerate(PLAN):
        d = b - a
        src = int(take[1]) - 1
        chains.append(f"[{src}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,"
                      f"afade=t=out:st={d - 0.04:.3f}:d=0.04,apad=pad_dur={gap}[s{i}]")
        labels.append(f"[s{i}]")
        cues.append({"take": take, "src": [a, b], "at": round(t, 2), "end": round(t + d, 2), "text": words})
        t += d + gap
    graph = ";".join(chains) + ";" + "".join(labels) + \
        f"concat=n={len(PLAN)}:v=0:a=1,adelay={int(LEAD * 1000)},apad=pad_dur={TAIL},{VOICE}[vo]"
    inputs = [x for f in levelled for x in ("-i", f)]
    ffmpeg(*inputs, "-filter_complex", graph, "-map", "[vo]", "-ar", "48000", out)
    for f in levelled:
        Path(f).unlink()
    (HERE / "vo_cues.json").write_text(json.dumps(cues, indent=1))
    print(f"{out}: {t + LEAD + TAIL:.2f} s")


if __name__ == "__main__":
    main()
