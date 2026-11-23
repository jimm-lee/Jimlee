#!/usr/bin/env python3
"""A silent, labelled reel of the fresh visual hooks so James can pick (Nov 19): iris from the sun, nested frame,
blinds, freeze card, film strip, bloom dissolve and sun-to-sun match cuts. -> showcase/index.html"""
from build_intros import build

SHOWCASE = dict(
    title="Heavyweight Hills — fresh hook showcase",
    length=22.0,
    endcard=0,
    outro=False,
    chunks="",
    fix={},
    fx=[dict(kind="iris", at=2.2, dur=0.9, x=60, y=27),
        dict(kind="nest", at=5.2, dur=0.9),
        dict(kind="blinds", at=9.0, dur=0.8, strips=7),
        dict(kind="freeze", at=11.3, dur=1.0, clip="3542", media=5.2),
        dict(kind="strip", at=12.9, dur=2.0, frames=[("3460", 0.4), ("3537", 0.6), ("3604", 1.5), ("3440", 0.6),
                                                      ("3621", 1.0), ("3549", 1.0), ("3632", 0.6)]),
        dict(kind="bloom", at=17.0, dur=0.9)],
    cut=[("3549", 0.0, 2.2, 0.2),       # 1 iris from the sun: sunset over the sea...
         ("3440", 2.2, 1.8, 0.4),       # ...opens into the night stairs
         ("3621", 4.0, 1.2, 0.5),       # 2 nested frame: orange sunset...
         ("3604", 5.2, 2.6, 0.2),       # ...the bridge grows out of a window in it
         ("3635", 7.8, 1.2, 0.4),       # 3 blinds: night road...
         ("3470", 9.0, 1.6, 0.6),       # ...the summit at sunset slides up in strips
         ("3542", 10.6, 2.3, 4.5),      # 4 freeze card: the vest selfie freezes into a print
         ("3632", 12.9, 2.6, 0.4),      # 5 film strip: the days scroll up and the last opens into the shot
         ("3576", 15.5, 1.5, 0.2),      # 6 bloom dissolve: sun through the trees...
         ("3390", 17.0, 2.1, 0.0),      # ...into your shadow at night
         ("3572", 19.1, 0.95, 0.3),     # 7 match cuts, sun to sun to sun
         ("3545", 20.05, 0.95, 1.0),
         ("3552", 21.0, 1.0, 1.2)],
    labels=[("1 · Iris from the sun", 0.3, 3.9), ("2 · Nested frame", 4.1, 7.7), ("3 · Blinds", 7.9, 10.5),
            ("4 · Freeze card", 10.7, 12.8), ("5 · Film strip", 13.0, 15.4), ("6 · Bloom dissolve", 15.6, 19.0),
            ("7 · Match cuts", 19.2, 22.0)],
)

if __name__ == "__main__":
    build("showcase", SHOWCASE)
