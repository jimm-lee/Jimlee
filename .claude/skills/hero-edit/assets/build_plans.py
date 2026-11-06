#!/usr/bin/env python3
"""Ten caption-led hero edits (10 or 15 s) from James's caption list, staged for approval.

Each plan uses the five-part shape (hook → connection → build → payoff → linger), the house caption style from
build.py (Bebas Neue, word by word, one green word with the dark-cherry outline) and closes on "Go on, look after
yourself". Writes plans/pNN/index.html; the clips, fonts and runtime are shared through links.
"""
import importlib.util
import os
import re
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("build", HERE / "build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

# 15 s: hook 0–2.5 · connection 2.5–5.5 · build 5.5–9.5 · payoff 9.5–12 · linger 12–15
# 10 s: hook 0–2 · connection 2–3.5 · build 3.5–6 · payoff 6–7.5 · linger 7.5–10
QUICK = 0.24  # reading time per word for the 10 s cuts


def seq(start, step, clips):
    """Consecutive shots of equal length: [(clip, media_start), ...] → [(clip, at, dur, media)]."""
    return [(c, round(start + i * step, 2), step, m) for i, (c, m) in enumerate(clips)]


PLANS = [
    # Second pass (Nov 6): new sequences from the full library. Each edit has its own hook, payoff and linger;
    # a clip appears in at most two edits and never next to the same shot twice (see variety_report()).
    dict(slug="p01-camera-roll", length=15,
         hook="My camera roll | since moving | to the other | side of | the *world*.",
         cut=[("9170", 0.0, 2.5, 0.2),                      # hook: the geyser going up
              ("9619", 2.5, 1.0, 0.2), ("9491", 3.5, 2.0, 1.0),   # wharf at sunrise, lakeside farm track
              *seq(5.5, 0.5, [("7185", 0.5), ("1422", 2.3), ("2815", 0.5), ("2565", 0.5),
                              ("9733", 0.2), ("0989", 3.0), ("7909", 0.5), ("2207", 3.0)]),   # buskers after the caption clears
              ("races", 9.5, 2.0, 1.2),                     # payoff: at the races with friends
              ("9355", 11.5, 3.5, 1.5)]),                   # linger: Split Apple Rock on glittering water
    dict(slug="p02-took-the-leap", length=10, read=QUICK,
         hook="POV: | You actually | took the *leap*.",
         cut=[("0170", 0.0, 2.0, 1.8),                      # hook: into the ice, the splash
              ("2894", 2.0, 1.0, 1.6),                      # Aoraki / Mt Cook
              *seq(3.0, 0.5, [("9651", 0.3), ("9361", 1.0), ("9319", 2.5), ("2987", 0.5)]),
              ("0389", 5.0, 1.5, 0.8),                      # payoff: spinning on deck at sunset
              ("2636", 6.5, 3.5, 1.3)],                     # linger: sunrise over the sea
         outro_top=420),
    dict(slug="p03-18000km", length=15,
         hook="A little look | at what life | looks like | *18,000km* from home.",
         cut=[("8342", 0.0, 2.5, 1.0),                      # hook: Auckland from the ferry
              ("2842", 2.5, 1.0, 1.0), ("9681", 3.5, 2.0, 2.0),   # lake through the pines, vintage town
              *seq(5.5, 0.5, [("9522", 1.5), ("0811", 1.0), ("0793", 0.5), ("5222", 1.0),
                              ("2772", 1.0), ("9504", 1.0), ("9357", 1.2), ("7185", 1.8)]),
              ("3365", 9.5, 2.0, 1.0),                      # payoff: running the beach
              ("3048", 11.5, 3.5, 1.2)]),                   # linger: the Wānaka tree
    dict(slug="p04-comfort-zone", length=15,
         hook="Turns out, | there's a lot | of life | outside your | *comfort* zone.",
         cut=[("7815", 0.0, 2.5, 0.5),                      # hook: ice-filled tub, close
              ("9545", 2.5, 1.0, 0.2), ("0171", 3.5, 2.0, 15.0),  # misty jetty, the sauna
              *seq(5.5, 0.5, [("0160", 2.0), ("9525", 1.0), ("6169", 1.0), ("8701", 5.0),
                              ("9065", 0.6), ("3148", 2.6), ("9371", 1.0), ("9644", 0.8)]),
              ("6234", 9.5, 2.0, 3.5),                      # payoff: pad work
              ("2603", 11.5, 3.5, 0.5)]),                   # linger: sunrise through the trees
    dict(slug="p05-getting-lost", length=15,
         hook="Somewhere between | getting *lost* | and finding | yourself.",
         cut=[("2005", 0.0, 2.5, 0.2),                      # hook: at the waterfall's edge
              ("0079", 2.5, 1.0, 0.3), ("0836", 3.5, 2.0, 0.3),   # boardwalk, the car the bush took
              ("9491", 5.5, 0.5, 1.0), ("2841", 6.0, 1.0, 0.8), ("8383", 7.0, 1.0, 10.0),
              ("2148", 8.0, 1.0, 0.5), ("8233", 9.0, 0.5, 2.0),
              ("3266", 9.5, 2.0, 1.4),                      # payoff: walking up the path
              ("1949", 11.5, 3.5, 0.3)]),                   # linger: dusk beach into the night path
    dict(slug="p06-three-years", length=15,
         hook="Three years, | one big decision, | and a | camera roll | full of *memories*.",
         cut=[("8078", 0.0, 2.5, 0.1),                      # hook: the ensign over the city
              ("8230", 2.5, 1.0, 0.5), ("2524", 3.5, 2.0, 1.3),   # coast from above, the Movember walk
              *seq(5.5, 0.5, [("1609", 2.0), ("9733", 0.5), ("9161", 1.0), ("9500", 1.0),
                              ("0989", 5.0), ("7989", 4.5), ("7157", 1.0), ("8092", 2.0)]),
              ("7278", 9.5, 2.0, 2.0),                      # payoff: dinner with friends
              ("5963", 11.5, 3.5, 1.2)]),                   # linger: sunset over the ranges
    dict(slug="p07-putting-it-off", length=15,
         hook="What happens | when you stop | putting off | the life you've | *imagined*?",
         cut=[("0842", 0.0, 2.5, 0.0),                      # hook: the car the bush swallowed
              ("9070", 2.5, 1.0, 1.5), ("9361", 3.5, 2.0, 2.5),   # paddock to the sea, river over rocks
              *seq(5.5, 0.5, [("5222", 2.5), ("9651", 0.8), ("2987", 1.0), ("9170", 2.8),
                              ("9319", 4.0), ("0811", 2.0), ("9619", 0.8), ("8297", 4.5)]),
              ("3276", 9.5, 2.0, 0.35),                     # payoff: the selfie, smiling
              ("9023", 11.5, 3.5, 1.2)]),                   # linger: palm at sunrise
    dict(slug="p08-ireland-to-nz", length=10, read=QUICK,
         hook="Ireland | to *New* *Zealand*. | A decision | I'll never regret.",
         cut=[("1422", 0.0, 2.0, 1.0),                      # hook: Ireland's green jerseys in NZ
              ("9525", 2.0, 1.0, 1.5),                      # the valley
              *seq(3.0, 0.5, [("3148", 2.5), ("9681", 4.0), ("7909", 2.0), ("2772", 2.0)]),
              ("3225", 5.0, 1.5, 0.2),                      # payoff: smiling into the low sun
              ("8092", 6.5, 3.5, 1.2)]),                    # linger: harbour of yachts
    dict(slug="p09-outside-your-routine", length=15,
         hook="A reminder | that there's | a whole *world* | waiting outside | your routine.",
         cut=[("0595", 0.0, 2.5, 2.4),                      # hook: the motorway
              ("0079", 2.5, 1.0, 1.0), ("8233", 3.5, 2.0, 6.0),   # boardwalk, the deck view
              *seq(5.5, 0.5, [("7157", 3.0), ("7278", 1.0), ("0793", 1.2), ("6169", 2.5),
                              ("2148", 1.5), ("9500", 2.5), ("8383", 2.0), ("9504", 2.5)]),
              ("9661", 9.5, 2.0, 0.3),                      # payoff: down the dune
              ("2894", 11.5, 3.5, 0.3)]),                   # linger: Aoraki / Mt Cook
    dict(slug="p10-not-on-instagram", length=15,
         hook="Not everything | makes it | onto Instagram. | Here's a | *little* of it.",
         cut=[("2636", 0.0, 1.0, 4.95), ("2565", 1.0, 1.5, 0.3),   # hook: the face, the odd bar
              ("1609", 2.5, 1.0, 3.0), ("9522", 3.5, 1.0, 0.5), ("2207", 4.5, 1.0, 3.5),
              *seq(5.5, 0.5, [("0171", 10.0), ("9644", 1.8), ("0160", 3.5), ("0836", 1.5),
                              ("9065", 2.0), ("races", 0.3), ("8701", 2.0), ("2815", 1.0)]),
              ("7815", 9.5, 2.0, 4.0),                      # payoff: in the ice tub
              ("3366", 11.5, 3.5, 0.8)]),                   # linger: dusk sea
]


LINGER = 4.0  # s; the closing line needs time to spell out and still hold before the fade


def clip_length(clip: str) -> float:
    import subprocess
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(HERE / "clips" / f"{clip}.mp4")], capture_output=True, text=True).stdout
    return float(out.strip())


def with_long_linger(cut):
    """Give the last shot LINGER seconds by taking the difference from the payoff shot before it."""
    *rest, (pc, pa, pd, pm), (lc, la, ld, lm) = cut
    extra = round(LINGER - ld, 2)
    if extra <= 0:
        return cut
    limit = {"2636": 4.95}.get(lc, clip_length(lc)) - 0.05   # 2636: stop before the face enters
    media = round(max(0.0, min(lm, limit - LINGER)), 2)
    return [*rest, (pc, pa, round(pd - extra, 2), pm), (lc, round(la - extra, 2), LINGER, media)]


def link(target: Path, link_path: Path) -> None:
    if link_path.is_symlink() or link_path.exists():
        return
    link_path.parent.mkdir(parents=True, exist_ok=True)
    os.symlink(os.path.relpath(target, link_path.parent), link_path)


def caption_times(plan):
    """When each hook chunk is fully on screen (for the storyboard stills)."""
    read = plan.get("read", build.READ_PER_WORD)
    out = []
    for spans, start, end in build.chunks(plan["hook"], 0.3 if plan["length"] == 15 else 0.2, read):
        last = max(float(t) for t in re.findall(r'data-t="([\d.]+)"', spans))
        out.append(round(min(start + last + 0.3, end - 0.2), 2))
    return out


def variety_report():
    """Every clip's uses, plus any pair of shots that sits side by side in more than one edit."""
    from collections import Counter, defaultdict
    uses, pairs = Counter(), defaultdict(list)
    for plan in PLANS:
        clips = [c for c, *_ in plan["cut"]]
        uses.update(clips)
        for a, b in zip(clips, clips[1:]):
            pairs[tuple(sorted((a, b)))].append(plan["slug"][:3])
    repeats = {k: v for k, v in pairs.items() if len(v) > 1}
    ends = Counter((p["cut"][-2][0], p["cut"][-1][0]) for p in PLANS)
    print("clips used 3+ times:", {c: n for c, n in uses.items() if n >= 3} or "none")
    print("shot pairs repeated across edits:", repeats or "none")
    print("payoff+linger repeated:", {k: n for k, n in ends.items() if n > 1} or "none")


variety_report()
for plan in PLANS:
    d = HERE / "plans" / plan["slug"]
    link(HERE / "clips", d / "assets" / "clips")
    link(HERE / "film-15" / "assets" / "fonts", d / "assets" / "fonts")
    link(HERE / "film-15" / "vendor", d / "vendor")
    plan["cut"] = with_long_linger(plan["cut"])
    length = plan["length"]
    end_at = plan["cut"][-1][1]  # the linger shot carries the closing line
    start = 0.3 if length == 15 else 0.2
    html = build.render(plan["cut"], plan["hook"], start, end_at, float(length), plan["slug"],
                        read_per_word=plan.get("read", build.READ_PER_WORD), outro_top=plan.get("outro_top"))
    (d / "index.html").write_text(html)
    print(plan["slug"], length, "s; caption stills at", caption_times(plan))
