#!/usr/bin/env python3
"""Hook videos for Heavyweight Hills (Nov 19): two of James's spoken hooks each (Movember_hooks voice note), the
first with a visual hook at 0 s and the second landing with another visual hook, then the QR card.

Same engine and house style as the intros, promos and 20 s clips (build_intros.py, hooks in fx.py).
Voice: voiceover/stitch_vo.py hk-<name> h=Movember_hooks.clean.wav.
"""
from build_intros import build

HOOKS = {
    "hk-promise": dict(
        title="Heavyweight Hills — hooks: one promise",
        length=14.3,
        fx=[dict(kind="spiral", at=0.0, clips=[("3637", 0.5), ("3604", 0.5), ("3545", 0.5), ("3605", 1.0),
                                               ("3535", 1.0), ("3470", 1.0), ("3524", 0.3), ("3632", 0.3)]),
            dict(kind="grid", at=6.7, dur=0.8, clip="3604", media=0.5, cols=2, rows=2, frames=3, order="stair")],
        cut=[("3621", 0.0, 1.5, 0.0),      # (spiral lands) "One hill.": the orange sunset
             ("3542", 1.5, 1.3, 4.8),      # "30 kilos.": vest selfie
             ("3470", 2.8, 1.4, 0.8),      # "One promise.": the summit at sunset
             ("3637", 4.2, 2.5, 0.5),      # "Show up again tomorrow.": the wet night road
             ("3604", 6.7, 2.3, 0.4),      # (bridge bursts into a grid) "One missed day would be easy to explain"
             ("3605", 9.0, 2.2, 0.5),      # "and that's exactly why": the bridge walkway at night
             ("3542", 11.2, 3.1, 0.5)],    # "I made this commitment public.": the sun going down over the hill
        chunks=("One *hill.* | *30* kilos. | One *promise.* | Show up again | *tomorrow.* | One missed day | "
                "would be easy | to *explain,* | and that's exactly | why I made | this commitment | *public.*"),
        outro=False,
        fix={0: 0.35, 10: 6.88, 18: 10.2},
    ),
    "hk-weight": dict(
        title="Heavyweight Hills — hooks: not the weight",
        length=13.0,
        fx=[dict(kind="grid", at=0.0, dur=0.9, clip="3542", media=4.8, cols=3, rows=3, frames=2, order="stair"),
            dict(kind="split", at=6.2, dur=1.4, top=("3621", 2.0), bottom=("3635", 1.0))],
        cut=[("3542", 0.0, 1.8, 4.4),      # (vest selfie bursts into a 3 x 3 grid) "30 kilos"
             ("3624", 1.8, 1.8, 0.0),      # "on my back, but": feet in the dark
             ("3637", 3.6, 2.0, 0.5),      # "it's not the weight I'm doing this for.": the wet night road
             ("3635", 5.6, 3.0, 0.4),      # (sunset over the night road, then the road opens up) "I didn't start this challenge"
             ("3535", 8.6, 2.0, 0.5),      # "I started because someone mattered": sun through the trees
             ("3470", 10.6, 2.4, 1.5)],    # "enough to make me show up.": the summit at sunset
        chunks=("*30* kilos | on my back, | but it's not | the *weight* | I'm doing this | *for.* | I didn't start | "
                "this *challenge* | because I thought | it'd be *easy.* | I started | because *someone* | "
                "mattered enough | to make me | show *up.*"),
        outro=False,
        fix={0: 0.35, 14: 6.5},
    ),
    "hk-grand": dict(
        title="Heavyweight Hills — hooks: I'm grand",
        length=12.4,
        fx=[dict(kind="split", at=0.0, dur=1.4, top=("3542", 4.8), bottom=("3389", 0.6)),
            dict(kind="spiral", at=5.65, clips=[("3621", 3.0), ("3545", 1.0), ("3604", 1.0), ("3632", 1.0),
                                                ("3572", 0.5), ("3605", 1.5)])],
        cut=[("3389", 0.0, 3.85, 0.6),     # (smiling selfie over the night shadow; the shadow opens up) "If you've ever said I'm grand"
             ("3624", 3.85, 1.8, 0.3),     # "this one's for you.": feet in the dark
             ("3632", 5.65, 2.6, 0.4),     # (spiral lands) "You can look completely fine": your shadow on the footpath, the wave
             ("3524", 8.25, 1.9, 0.2),     # "turn up every day": the beach
             ("3535", 10.15, 2.25, 1.4)],  # "and still be carrying more than people realise.": sun through the trees
        chunks=("If you've | ever said, | I'm *grand,* | when you *weren't,* | this one's | for *you.* | You can look | "
                "completely *fine,* | turn up | every day | and still be | *carrying* more | than people | *realise.*"),
        outro=False,
        tops={0: 300, 1: 300, 2: 300},   # over the split, the selfie's face sits at the caption row
        fix={0: 0.35, 13: 5.68},
    ),
    "hk-nobody": dict(
        title="Heavyweight Hills — hooks: nobody watching",
        length=12.1,
        fx=[dict(kind="spiral", at=0.0, clips=[("3605", 0.5), ("3621", 2.0), ("3604", 0.3), ("3545", 1.5),
                                               ("3635", 0.3), ("3637", 1.0), ("3470", 2.0), ("3624", 0.0)]),
            dict(kind="zoom", at=5.35)],
        cut=[("3542", 0.0, 1.9, 3.9),      # (spiral lands) "A heavier vest isn't the point": vest selfie
             ("3624", 1.9, 1.6, 0.0),      # "showing up when nobody": feet in the dark
             ("3605", 3.5, 1.85, 0.5),     # "is watching is.": the bridge at night (punches forward at 5.35)
             ("3635", 5.35, 2.4, 0.3),     # (lands from the zoom) "The hardest part of this challenge": night road
             ("3621", 7.75, 2.0, 2.0),     # "isn't the hill. It's making": the orange sunset
             ("3470", 9.75, 2.35, 1.0)],   # "the decision to show up again tomorrow.": the summit at sunset
        chunks=("A heavier *vest* | isn't the point. | Showing up | when *nobody* | is watching is. | The *hardest* part | "
                "of this challenge | isn't the *hill.* | It's making | the *decision* | to show up | again *tomorrow.*"),
        outro=False,
        fix={0: 0.35, 13: 5.38},
    ),
    "hk-reminder": dict(
        title="Heavyweight Hills — hooks: your reminder",
        length=16.4,
        fx=[dict(kind="split", at=0.0, dur=1.5, top=("3621", 0.5), bottom=("3604", 0.2)),
            dict(kind="grid", at=8.8, dur=0.8, clip="3572", media=0.2, cols=2, rows=2, frames=3, order="stair")],
        cut=[("3604", 0.0, 2.6, 0.2),      # (morning sky over the night bridge; the bridge opens up) "There have been mornings and evenings"
             ("3535", 2.6, 1.8, 0.5),      # "that I've questioned,": sun through the trees
             ("3637", 4.4, 1.9, 0.3),      # "why am I even doing this?": the wet night road
             ("3621", 6.3, 2.3, 4.5),      # "And then I remember who I started it for.": the orange sunset
             ("3572", 8.6, 1.9, 0.0),      # (the sun bursts into a grid) "If you're waiting"
             ("3632", 10.5, 1.9, 0.3),     # "until you feel": your shadow on the footpath
             ("3545", 12.4, 1.8, 0.5),     # "motivated to make a change,": the sun over the hill
             ("3470", 14.2, 2.2, 0.5)],    # "let this be your reminder.": the summit at sunset
        chunks=("There have been | mornings and *evenings,* | that I've *questioned,* | why am I | even *doing* this? | "
                "And then | I *remember* | who I started | it *for.* | If you're waiting | until you feel | *motivated* | "
                "to make a | *change,* | let this be | your *reminder.*"),
        outro=False,
        fix={0: 0.35, 15: 6.4, 24: 9.53},
    ),
    "hk-checkin": dict(
        title="Heavyweight Hills — hooks: checking in",
        length=13.3,
        fx=[dict(kind="grid", at=0.0, dur=0.9, clip="3440", media=0.5, cols=3, rows=3, frames=2, order="stair"),
            dict(kind="spiral", at=5.3, clips=[("3549", 1.0), ("3552", 1.0), ("3439", 1.0), ("3570", 1.0),
                                               ("3537", 0.5), ("3392", 0.8)])],
        cut=[("3440", 0.0, 2.2, 0.3),      # (night stairs burst into a 3 x 3 grid) "We talk a lot about getting stronger,"
             ("3449", 2.2, 1.4, 0.5),      # "but we don't talk enough": feet on the stairs
             ("3576", 3.6, 1.7, 0.3),      # "about checking in on each other.": sun through the trees
             ("3390", 5.3, 2.15, 0.0),     # (spiral lands) "If you've ever said": your shadow on the night footpath
             ("3579", 7.45, 1.15, 3.0),    # "I'm fine,": the wide-eyed selfie
             ("3392", 8.6, 2.5, 1.2),      # "when you weren't,": the night footpath, your hand
             ("3549", 11.1, 2.2, 1.0)],    # "this one's for you.": the sun going down over the sea
        chunks=("We talk | a lot about | getting *stronger,* | but we don't | talk enough | about *checking* in | "
                "on each other. | If you've | ever said, | I'm *fine,* | when you *weren't,* | this one's | for *you.*"),
        outro=False,
        fix={0: 0.35},
    ),
}

if __name__ == "__main__":
    for name, cfg in HOOKS.items():
        build(name, cfg)
