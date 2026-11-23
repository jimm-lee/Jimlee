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
        chunks=("One hill. | 30 kilos. | One *promise.* | Show up again | tomorrow. | One missed day | "
                "would be easy | to explain, | and that's exactly | why I made | this commitment | *public.*"),
        outro=False,
        fix={0: 0.35, 10: 6.88, 18: 10.2},
    ),
    "hk-weight": dict(
        title="Heavyweight Hills — hooks: not the weight",
        length=13.0,
        # Nov 23 rebuild: one colour grade (g = graded copy), dissolves for flow, two clean hooks
        fx=[dict(kind="letterbox", at=0.1, dur=1.3),
            dict(kind="dissolve", at=1.8, dur=0.35),
            dict(kind="dissolve", at=3.9, dur=0.4),
            dict(kind="iris", at=6.2, dur=1.0),
            dict(kind="dissolve", at=8.2, dur=0.35),
            dict(kind="dissolve", at=9.6, dur=0.4),
            dict(kind="dissolve", at=11.0, dur=0.45)],
        cut=[("g3542", 0.0, 1.8, 4.4),     # (the letterbox opens on you) "30 kilos on my back": vest selfie, golden light
             ("g3386", 1.8, 2.1, 0.2),     # "but it's not": feet on the footpath
             ("g3552", 3.9, 2.3, 0.0),     # "the weight I'm doing this for.": the sun low through the haze
             ("g3440", 6.2, 2.0, 0.3),     # (the sun's light swells into night) "I didn't start this challenge": the stairs
             ("g3449", 8.2, 1.4, 0.5),     # "because I thought it'd be easy.": feet climbing them
             ("g3576", 9.6, 1.4, 0.1),     # "I started because someone": the sun back through the trees
             ("g3549", 11.0, 2.0, 2.0)],   # "mattered enough to make me show up.": the sun going down over the sea
        endcard_bg=("g3549", 2.6),      # the QR card sits over the same graded sunset (blurred), so the ending flows
        chunks=("30 kilos | on my back, | but it's not | the weight | I'm doing this | for. | I didn't start | "
                "this challenge | because I thought | it'd be easy. | I started | because *someone* | "
                "mattered enough | to make me | show up."),
        outro=False,
        fix={0: 0.35, 14: 6.5},
    ),
    "hk-grand": dict(
        title="Heavyweight Hills — hooks: I'm grand",
        length=12.4,
        fx=[dict(kind="freeze", at=1.15, dur=0.85, clip="3542", media=5.55),
            dict(kind="nest", at=5.65, dur=0.9)],
        cut=[("3542", 0.0, 2.3, 4.4),      # "If you've ever said I'm grand": the smile freezes into a photo
             ("3389", 2.3, 1.55, 0.6),     # "when you weren't,": your shadow at night
             ("3624", 3.85, 1.8, 0.3),     # "this one's for you.": feet in the dark
             ("3632", 5.65, 2.6, 0.4),     # (feet to feet: grows out of a window) "You can look completely fine"
             ("3524", 8.25, 1.9, 0.2),     # "turn up every day": the beach
             ("3535", 10.15, 2.25, 1.4)],  # "and still be carrying more than people realise.": sun through the trees
        chunks=("If you've | ever said, | I'm *grand,* | when you weren't, | this one's | for you. | You can look | "
                "completely fine, | turn up | every day | and still be | *carrying* | more than people | realise."),
        outro=False,
        tops={0: 300, 1: 300, 2: 300},   # over the split, the selfie's face sits at the caption row
        fix={0: 0.35, 13: 5.68},
    ),
    "hk-nobody": dict(
        title="Heavyweight Hills — hooks: nobody watching",
        length=12.1,
        fx=[dict(kind="blinds", at=5.35, dur=0.85, strips=7)],
        cut=[("3542", 0.0, 1.9, 4.2),      # "A heavier vest isn't the point": vest selfie
             ("3624", 1.9, 0.7, 0.2),      # match cuts, feet to feet: "showing up"
             ("3449", 2.6, 0.6, 1.2),      #   feet on the night stairs
             ("3632", 3.2, 0.75, 0.0),     #   feet and shadow on the footpath "when nobody"
             ("3605", 3.95, 1.4, 0.5),     # "is watching is.": the bridge railings (strips carry the verticals into...)
             ("3440", 5.35, 2.4, 0.3),     # (...blinds) "The hardest part of this challenge": the night stairs
             ("3621", 7.75, 2.0, 2.0),     # "isn't the hill. It's making": the orange sunset
             ("3470", 9.75, 2.35, 1.0)],   # "the decision to show up again tomorrow.": the summit at sunset
        chunks=("A heavier vest | isn't the point. | Showing up | when *nobody* | is watching is. | "
                "The hardest part | of this challenge | isn't the hill. | It's making | the decision | to show up | "
                "again *tomorrow.*"),
        outro=False,
        fix={0: 0.35, 13: 5.38},
    ),
    "hk-reminder": dict(
        title="Heavyweight Hills — hooks: your reminder",
        length=16.4,
        fx=[dict(kind="bloom", at=1.3, dur=0.9),
            dict(kind="iris", at=9.4, dur=1.0)],
        cut=[("3621", 0.0, 1.3, 0.5),      # "There have been mornings": the orange sky...
             ("3604", 1.3, 2.0, 0.2),      # (...blooms into) "and evenings,": the bridge at night
             ("3535", 3.3, 1.4, 0.5),      # "that I've questioned,": sun through the trees
             ("3637", 4.7, 1.6, 0.3),      # "why am I even doing this?": the wet night road
             ("3549", 6.3, 3.1, 1.0),      # "And then I remember who I started it for.": the sun going down over the sea
             ("3632", 9.4, 2.6, 0.3),      # (opens out of the sun) "If you're waiting until you feel": your shadow
             ("3545", 12.0, 2.2, 0.5),     # "motivated to make a change,": the sun over the hill
             ("3470", 14.2, 2.2, 0.5)],    # "let this be your reminder.": the summit at sunset
        chunks=("There have been | mornings and evenings, | that I've questioned, | why am I | even doing this? | "
                "And then | I *remember* | who I started | it for. | If you're waiting | until you feel | "
                "motivated | to make a | change, | let this be | your *reminder.*"),
        outro=False,
        fix={0: 0.35, 15: 6.4, 24: 9.53},
    ),
    "hk-checkin": dict(
        title="Heavyweight Hills — hooks: checking in",
        length=13.3,
        fx=[dict(kind="nest", at=1.2, dur=0.9),
            dict(kind="bloom", at=5.3, dur=0.9)],
        cut=[("3440", 0.0, 1.2, 0.3),      # "We talk a lot about": the night stairs...
             ("3449", 1.2, 2.4, 0.3),      # (...your feet climbing them, out of a window) "getting stronger, but we don't"
             ("3576", 3.6, 1.7, 0.1),      # "talk enough about checking in on each other.": sun through the trees...
             ("3390", 5.3, 2.1, 0.0),      # (...blooms into) "If you've ever said": your shadow at night
             ("3579", 7.4, 1.2, 3.0),      # "I'm fine,": the wide-eyed selfie
             ("3392", 8.6, 2.5, 1.2),      # "when you weren't,": the night footpath, your hand
             ("3549", 11.1, 2.2, 1.0)],    # "this one's for you.": the sun going down over the sea
        chunks=("We talk | a lot about | getting stronger, | but we don't | talk enough | about *checking* | in on | "
                "each other. | If you've | ever said, | I'm *fine,* | when you weren't, | this one's | for you."),
        outro=False,
        fix={0: 0.35},
    ),
}

if __name__ == "__main__":
    for name, cfg in HOOKS.items():
        build(name, cfg)
