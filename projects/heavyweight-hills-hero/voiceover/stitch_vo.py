#!/usr/bin/env python3
"""Stitch the Heavyweight Hills intro voice-overs from James's three Movember voice memos.

Usage: python3 stitch_vo.py <plan> take=file ... [out.wav]
  Prefer cleaned takes (clean_take.py → <take>.clean.wav): less breathing and hiss, clearer voice.
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
],
    # 10 s promos from the unused Movember_4 lines (takes: m4=Movember_4.m4a o=New_Recording_10.m4a)
    "promo-invisible": [
    ("m4", 121.18, 123.82, 0.45, "Because we all carry weight."),
    ("m4", 132.30, 135.95, 0.35, "Sometimes, most of the time even, it's invisible."),
    ("m4", 136.20, 137.10, 0.55, "You don't see it."),
    ("o", 5.10, 6.95, 0.00, "Go on, look after yourself."),
],
    "promo-lifetime": [
    ("m4", 182.40, 186.72, 0.50, "Some people hold that weight on their shoulders for a lifetime and don't tell anyone."),
    ("m4", 275.60, 279.55, 0.00, "There's always someone who can relate to your story."),
],
    "promo-stare": [
    ("m4", 150.40, 153.62, 0.10, "Most of the times I stare at that vest for two minutes"),
    ("m4", 154.95, 156.95, 0.50, "before even trying to pick it up."),
    ("m4", 158.70, 160.20, 0.25, "Preparing myself"),
    ("m4", 161.45, 164.12, 0.00, "for a little bit of suffering."),
],
    "promo-change": [
    ("m4", 216.12, 217.98, 0.15, "So many men"),
    ("m4", 219.20, 221.12, 0.10, "hold this weight on their shoulders and"),
    ("m4", 222.05, 223.22, 0.50, "don't tell anyone."),
    ("m4", 230.15, 231.36, 0.60, "And that needs to change."),
    ("o", 29.40, 31.15, 0.00, "Go on, look after yourself."),
],
    "promo-mind": [
    ("m4", 253.20, 256.30, 0.30, "No one ever knows how bad it really is"),
    ("m4", 258.38, 259.56, 0.60, "inside your mind."),
    ("m4", 282.28, 283.40, 0.60, "You just need to say it."),
    ("o", 9.25, 11.42, 0.00, "Go on, look after yourself."),
],
    # 20 s clips with a pause at ~10 s for the second visual hook (takes: m4=Movember_4 o=New_Recording_10)
    "clip-weight": [
    ("m4", 121.18, 123.82, 0.45, "Because we all carry weight."),
    ("m4", 132.30, 135.95, 0.35, "Sometimes, most of the time even, it's invisible."),
    ("m4", 136.20, 137.10, 1.60, "You don't see it."),          # the pause carries the 10 s hook
    ("m4", 216.12, 217.98, 0.15, "So many men"),
    ("m4", 219.20, 221.12, 0.10, "hold this weight on their shoulders and"),
    ("m4", 222.05, 223.22, 0.50, "don't tell anyone."),
    ("m4", 230.15, 231.36, 0.00, "And that needs to change."),
],
    "clip-stare": [
    ("m4", 150.40, 153.62, 0.10, "Most of the times I stare at that vest for two minutes"),
    ("m4", 154.95, 156.95, 0.50, "before even trying to pick it up."),
    ("m4", 158.70, 160.20, 0.25, "Preparing myself"),
    ("m4", 161.45, 164.12, 0.90, "for a little bit of suffering."),   # the pause carries the 10 s hook
    ("m4", 200.35, 203.10, 0.60, "I can hold that weight on my shoulders"),
    ("o", 5.10, 6.95, 0.00, "Go on, look after yourself."),
],
    "clip-say": [
    ("m4", 253.20, 256.30, 0.30, "No one ever knows how bad it really is"),
    ("m4", 258.38, 259.56, 0.50, "inside your mind."),
    ("m4", 182.40, 186.72, 0.90, "Some people hold that weight on their shoulders for a lifetime and don't tell anyone."),
    ("m4", 275.60, 279.55, 0.40, "There's always someone who can relate to your story."),
    ("m4", 282.28, 283.40, 0.00, "You just need to say it."),
],
    # Hooks (Movember_hooks voice note, Nov 19; take h=Movember_hooks.clean.wav): best take of each, long pauses tightened
    "hook-01": [("h", 6.20, 12.00, 0.0, "I didn't start this challenge because I thought it would be easy. I started because someone mattered enough to make me show up.")],
    "hook-02": [("h", 30.75, 34.90, 0.0, "A heavier vest isn't the point, showing up when nobody is watching is.")],
    "hook-03": [("h", 57.45, 63.50, 0.0, "You can look completely fine, turn up every day and still be carrying more than people realise.")],
    "hook-04": [("h", 83.35, 89.35, 0.0, "The hardest part of this challenge isn't the hill, it's making the decision to show up again tomorrow.")],
    "hook-05": [("h", 98.30, 103.58, 0.0, "30 kilos on my back, but it's not the weight I'm doing this for.")],
    "hook-06": [("h", 126.45, 132.05, 0.45, "There have been mornings and evenings that I've questioned, why am I even doing this?"),
                ("h", 133.25, 135.50, 0.0, "Then I remember who I started it for.")],
    "hook-07": [("h", 138.82, 141.92, 0.45, "If you've ever said, I'm grand, when you weren't,"),
                ("h", 142.75, 143.66, 0.0, "this one's for you.")],
    "hook-07b": [("h", 146.30, 151.10, 0.40, "If you've ever said, I'm fine, when you weren't,"),
                 ("h", 151.45, 152.88, 0.0, "this one's for you.")],
    "hook-08": [("h", 169.80, 175.45, 0.0, "One hill, 30 kilos, one promise, show up again tomorrow.")],
    "hook-09": [("h", 190.88, 197.05, 0.0, "If you're waiting until you feel motivated to make a change, let this be your reminder.")],
    "hook-10": [("h", 200.38, 205.12, 0.0, "We talk a lot about getting stronger, but we don't talk enough about checking in on each other.")],
    "hook-11": [("h", 214.95, 217.88, 0.40, "One missed day would be easy to explain,"),
                ("h", 218.70, 222.12, 0.0, "and that's exactly why I made this commitment public.")],
    "promo-hold": [
    ("m4", 194.40, 197.10, 0.15, "I can put myself under"),
    ("m4", 197.85, 199.40, 0.40, "stressful situations."),
    ("m4", 200.35, 203.10, 0.60, "I can hold that weight on my shoulders"),
    ("o", 17.62, 19.28, 0.00, "Go on, look after yourself."),
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
    # takes already run through clean_take.py carry their own EQ/de-ess/compression: only set the level here
    cleaned = all(takes[t].endswith(".clean.wav") for t in order)
    voice = "loudnorm=I=-16:TP=-1.5:LRA=7" if cleaned else VOICE
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
        f"concat=n={len(plan)}:v=0:a=1,adelay={int(LEAD * 1000)},apad=pad_dur={TAIL},{voice}[vo]"
    inputs = [x for f in levelled for x in ("-i", f)]
    ffmpeg(*inputs, "-filter_complex", graph, "-map", "[vo]", "-ar", "48000", out)
    for f in levelled:
        Path(f).unlink()
    (HERE / f"vo_cues-{name}.json").write_text(json.dumps(cues, indent=1))
    print(f"{out}: {t + LEAD + TAIL:.2f} s")


if __name__ == "__main__":
    main()
