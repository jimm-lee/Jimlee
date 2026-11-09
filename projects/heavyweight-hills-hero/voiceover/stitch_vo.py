#!/usr/bin/env python3
"""Stitch the Heavyweight Hills intro voice-overs from James's three Movember voice memos.

Usage: python3 stitch_vo.py <plan> take=file ... [out.wav]
  full / intro-a:  m1=Movember_1.m4a m2=Movember_2.m4a m3=Movember_3.m4a
  intro-b:         m4=Movember_4.m4a o=New_Recording_10.m4a   (the longer second take + the closing-line reads)

Each take is level-matched to -20 LUFS, the selects below are cut at the silences between phrases (20 ms fade in,
40 ms fade out), joined with short breaths, then voice-processed and normalised to -16 LUFS / -1.5 dBTP.
Writes vo_cues-<plan>.json next to this script (where each select sits on the timeline).
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
LEAD = 0.30   # s of silence before the first word
TAIL = 0.60   # s after the last word

# (take, in, out, gap after, words). Takes: m1 = Movember_1, m2 = Movember_2, m3 = Movember_3.
PLANS = {"full": [
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
],
    # 30 s intro A, "the challenge": what it is, the map, and the visible weight
    "intro-a": [
    ("m2", 7.50, 10.55, 0.35, "Just because I haven't posted it doesn't mean I haven't been doing it."),
    ("m1", 9.70, 12.36, 0.20, "30 kilo weight vest, same as last year,"),
    ("m2", 21.86, 31.30, 2.50, "so walking up the hill, walking down the hill obviously, 30 kilos on my back, at least "
                               "one hill every day for the whole month of Movember,"),   # the gap is the map
    ("m2", 31.30, 33.42, 0.60, "and calling it Heavyweight Hills."),
    ("m3", 57.40, 60.92, 0.00, "We all carry our own weight, but this one is visible."),
],
    # 30 s intro B, "the why" (Nov 9 re-record: Movember_4 + New Recording 10 for the spoken closing line)
    "intro-b": [
    ("m4", 1.00, 3.80, 0.35, "So why bother? Why do Movember?"),
    ("m4", 22.30, 31.85, 0.30, "Last year my uncle made the irreversible decision that ended up shattering both sides "
                               "of our family,"),
    ("m4", 70.30, 74.65, 0.50, "and in the last three months I've lost two grandparents."),
    ("m4", 188.05, 190.60, 0.35, "So for me, putting on this vest"),
    ("m4", 191.45, 192.92, 0.50, "is a sign of strength."),
    ("m4", 298.00, 299.10, 0.30, "There's always a way out,"),
    ("m4", 299.90, 301.95, 0.60, "and you need to be strong enough to ask."),
    ("o", 0.80, 3.05, 0.00, "Go on, look after yourself."),
]}
VOICE = ("highpass=f=90,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1:g=3,"
         "acompressor=threshold=0.08:ratio=3:attack=8:release=200:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=7")


def ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] not in PLANS:
        sys.exit(__doc__)
    name, plan = args[0], PLANS[args[0]]
    takes = dict(a.split("=", 1) for a in args[1:] if "=" in a)
    rest = [a for a in args[1:] if "=" not in a]
    out = rest[0] if rest else f"Heavyweight-Hills-{name}-VO.wav"
    order = sorted({t for t, *_ in plan})
    missing = [t for t in order if t not in takes]
    if missing:
        sys.exit(f"missing takes for {name}: {', '.join(missing)}\n{__doc__}")
    levelled = []
    for i, t in enumerate(order):
        dst = f"_{t}.wav"
        ffmpeg("-i", takes[t], "-ac", "1", "-af", "loudnorm=I=-20:TP=-3:LRA=11", "-ar", "48000", dst)
        levelled.append(dst)
    chains, labels, cues, t = [], [], [], LEAD
    for i, (take, a, b, gap, words) in enumerate(plan):
        d = b - a
        src = order.index(take)
        chains.append(f"[{src}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,"
                      f"afade=t=out:st={d - 0.04:.3f}:d=0.04,apad=pad_dur={gap}[s{i}]")
        labels.append(f"[s{i}]")
        cues.append({"take": take, "src": [a, b], "at": round(t, 2), "end": round(t + d, 2), "text": words})
        t += d + gap
    graph = ";".join(chains) + ";" + "".join(labels) + \
        f"concat=n={len(plan)}:v=0:a=1,adelay={int(LEAD * 1000)},apad=pad_dur={TAIL},{VOICE}[vo]"
    inputs = [x for f in levelled for x in ("-i", f)]
    ffmpeg(*inputs, "-filter_complex", graph, "-map", "[vo]", "-ar", "48000", out)
    for f in levelled:
        Path(f).unlink()
    (HERE / f"vo_cues-{name}.json").write_text(json.dumps(cues, indent=1))
    print(f"{out}: {t + LEAD + TAIL:.2f} s")


if __name__ == "__main__":
    main()
