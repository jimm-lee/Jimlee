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
    dict(slug="p01-camera-roll", length=15,
         hook="My camera roll | since moving | to the other | side of | the *world*.",
         cut=[("0989", 0.0, 2.5, 2.4),
              ("8230", 2.5, 1.0, 3.6), ("2207", 3.5, 1.0, 2.0), ("9733", 4.5, 1.0, 0.2),
              *seq(5.5, 0.5, [("7989", 3.3), ("2565", 0.6), ("9170", 0.6), ("1422", 2.3),
                              ("9500", 1.0), ("9161", 1.0), ("3048", 2.0), ("6234", 4.5)]),
              ("9661", 9.5, 1.0, 2.2), ("2153", 10.5, 1.0, 4.1),
              ("3366", 11.5, 3.5, 0.8)]),
    dict(slug="p02-took-the-leap", length=10, read=QUICK,
         hook="POV: | You actually | took the *leap*.",
         cut=[("0170", 0.0, 2.0, 1.8),
              ("2894", 2.0, 1.0, 1.6), ("3048", 3.0, 0.5, 2.0),
              *seq(3.5, 0.5, [("6234", 4.5), ("7989", 3.4), ("9161", 1.2), ("9170", 0.6), ("9319", 2.5)]),
              ("9661", 6.0, 1.0, 2.3), ("2153", 7.0, 0.5, 4.5),
              ("2148", 7.5, 2.5, 0.1)]),
    dict(slug="p03-18000km", length=15,
         hook="A little look | at what life | looks like | *18,000km* from home.",
         cut=[("9065", 0.0, 2.5, 0.3),
              ("9070", 2.5, 1.0, 1.0), ("8092", 3.5, 1.0, 2.0), ("2207", 4.5, 1.0, 2.0),
              *seq(5.5, 0.5, [("9681", 2.0), ("9733", 0.2), ("1422", 2.3), ("0811", 1.0),
                              ("9644", 0.8), ("3148", 2.6), ("9504", 1.0), ("2987", 0.5)]),
              ("3048", 9.5, 1.5, 1.5), ("2153", 11.0, 1.0, 4.1),
              ("2636", 12.0, 3.0, 1.8)]),
    dict(slug="p04-comfort-zone", length=10, read=QUICK,
         hook="Turns out, | there's a lot | of life | outside your | *comfort* zone.",
         cut=[("7815", 0.0, 2.0, 0.5),
              ("9070", 2.0, 1.0, 1.0), ("2207", 3.0, 0.5, 2.0),
              *seq(3.5, 0.5, [("1422", 2.3), ("9500", 1.0), ("0811", 1.0), ("6234", 4.5), ("9545", 0.5)]),
              ("9065", 6.0, 1.0, 0.6), ("2153", 7.0, 0.5, 4.5),
              ("2636", 7.5, 2.5, 2.2)]),
    dict(slug="p05-getting-lost", length=15,
         hook="Somewhere between | getting *lost* | and finding | yourself.",
         cut=[("2005", 0.0, 2.5, 0.2),
              ("0079", 2.5, 1.5, 0.2), ("9545", 4.0, 1.5, 0.0),
              ("0811", 5.5, 1.0, 1.0), ("3048", 6.5, 1.0, 2.0), ("9651", 7.5, 0.5, 0.3),
              ("2987", 8.0, 0.5, 0.5), ("3365", 8.5, 1.0, 1.0),
              ("2894", 9.5, 1.5, 1.6), ("2153", 11.0, 1.0, 4.1),
              ("3366", 12.0, 3.0, 1.0)]),
    dict(slug="p06-three-years", length=15,
         hook="Three years, | one big decision, | and a | camera roll | full of *memories*.",
         cut=[("0389", 0.0, 2.5, 0.8),
              ("8230", 2.5, 1.0, 3.6), ("2524", 3.5, 2.0, 1.3),
              *seq(5.5, 0.5, [("9319", 2.5), ("7989", 3.3), ("9161", 1.0), ("0170", 2.6),
                              ("9733", 0.2), ("2207", 2.0), ("1422", 2.3), ("9681", 2.0)]),
              ("9661", 9.5, 1.5, 2.2), ("2153", 11.0, 1.0, 4.1),
              ("2636", 12.0, 3.0, 1.8)]),
    dict(slug="p07-putting-it-off", length=15,
         hook="What happens | when you stop | putting off | the life you've | *imagined*?",
         cut=[("0595", 0.0, 1.5, 1.0), ("0170", 1.5, 1.0, 2.6),
              ("2894", 2.5, 1.0, 1.6), ("3048", 3.5, 1.0, 2.0), ("6234", 4.5, 1.0, 4.0),
              *seq(5.5, 0.5, [("9681", 2.0), ("2987", 0.5), ("9161", 1.0), ("9170", 0.6),
                              ("9651", 0.3), ("7989", 3.3), ("9065", 0.6), ("9319", 2.5)]),
              ("9661", 9.5, 1.5, 2.2), ("2153", 11.0, 1.0, 4.1),
              ("3366", 12.0, 3.0, 1.0)]),
    dict(slug="p08-ireland-to-nz", length=10, read=QUICK,
         hook="Ireland | to *New* *Zealand*. | A decision | I'll never regret.",
         cut=[("1422", 0.0, 2.0, 1.0),
              ("2894", 2.0, 1.0, 1.6), ("8230", 3.0, 0.5, 3.6),
              *seq(3.5, 0.5, [("0170", 2.6), ("9161", 1.0), ("7989", 3.3), ("9065", 0.6), ("2207", 2.0)]),
              ("9661", 6.0, 1.0, 2.3), ("2153", 7.0, 0.5, 4.5),
              ("2148", 7.5, 2.5, 0.1)]),
    dict(slug="p09-outside-your-routine", length=10, read=QUICK,
         hook="A reminder | that there's | a whole *world* | waiting outside | your routine.",
         cut=[("0595", 0.0, 2.0, 0.8),
              ("9070", 2.0, 1.0, 1.0), ("0079", 3.0, 0.5, 0.3),
              *seq(3.5, 0.5, [("2894", 1.6), ("9170", 0.6), ("7989", 3.3), ("0989", 2.4), ("9319", 2.5)]),
              ("9661", 6.0, 1.0, 2.3), ("2153", 7.0, 0.5, 4.5),
              ("9065", 7.5, 2.5, 0.2)]),
    dict(slug="p10-not-on-instagram", length=15,
         hook="Not everything | makes it | onto Instagram. | Here's a | *little* of it.",
         cut=[("2636", 0.0, 1.0, 4.95), ("2565", 1.0, 1.5, 0.3),
              ("0793", 2.5, 1.0, 0.5), ("2207", 3.5, 1.0, 2.0), ("3148", 4.5, 1.0, 2.4),
              *seq(5.5, 0.5, [("9500", 1.0), ("9504", 1.0), ("9733", 0.2), ("9644", 0.8),
                              ("0171", 15.5), ("6234", 4.5), ("1422", 2.3), ("9681", 2.0)]),
              ("9065", 9.5, 1.5, 0.6), ("2153", 11.0, 1.0, 4.1),
              ("3366", 12.0, 3.0, 1.0)]),
]


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


for plan in PLANS:
    d = HERE / "plans" / plan["slug"]
    link(HERE / "clips", d / "assets" / "clips")
    link(HERE / "film-15" / "assets" / "fonts", d / "assets" / "fonts")
    link(HERE / "film-15" / "vendor", d / "vendor")
    length = plan["length"]
    end_at = plan["cut"][-1][1]  # the linger shot carries the closing line
    start = 0.3 if length == 15 else 0.2
    html = build.render(plan["cut"], plan["hook"], start, end_at, float(length), plan["slug"],
                        read_per_word=plan.get("read", build.READ_PER_WORD))
    (d / "index.html").write_text(html)
    print(plan["slug"], length, "s; caption stills at", caption_times(plan))
