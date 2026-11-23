#!/usr/bin/env python3
"""Three 20 s Heavyweight Hills clips, each with a visual hook at the start and a second one about 10 s in
(James, Nov 13: "a visual hook at the start and a second one 10 sec in to hold attention").

Same engine and house style as the intros and promos (build_intros.py; hooks in fx.py). Voice: the cleaned takes,
voiceover/stitch_vo.py clip-<name> m4=Movember_4.clean.wav o=New_Recording_10.clean.wav. Each ends on the QR card.
"""
from build_intros import build

CLIPS = {
    "clip-weight": dict(
        title="Heavyweight Hills — 20 s: invisible weight",
        length=17.2,
        fx=[dict(kind="spiral", at=0.0, clips=[("3428", 1.5), ("3286", 1.0), ("3244", 2.0), ("3352", 1.0),
                                               ("3310", 0.5), ("3290", 1.6), ("3304", 1.0), ("3389", 1.0)]),
            dict(kind="grid", at=9.5, dur=0.9, clip="3286", media=0.5, cols=2, rows=2, frames=3, order="stair")],
        cut=[("3276", 0.0, 2.95, 0.0),     # (the spiral lands here) "Because we all carry weight": walking selfie
             ("3402", 2.95, 1.6, 0.3),     # "sometimes, most of the": the empty path at night
             ("3292", 4.55, 1.2, 1.0),     # "time even": night street
             ("3389", 5.75, 3.75, 0.6),    # "it's invisible. You don't see it.": the vest's shadow
             ("3286", 9.5, 2.3, 0.5),      # (the rain bursts into a grid at 9.5) "So many men"
             ("3352", 11.8, 2.1, 0.9),     # "hold this weight on their shoulders": the vest at night
             ("3401", 13.9, 1.7, 0.5),     # "and don't tell anyone": night flax
             ("3315", 15.6, 1.6, 0.0)],    # "And that needs to change": Running for Movember
        chunks=("Because we all | carry *weight,* | sometimes, | most of the | time even, | it's *invisible.* | "
                "You don't | *see* it. | So many *men* | hold this *weight* | on their shoulders | and don't tell | "
                "*anyone.* | And that needs | to *change.*"),
        outro=False,
        fix={0: 0.35, 20: 11.94, 30: 15.68},
    ),
    "clip-stare": dict(
        title="Heavyweight Hills — 20 s: the stare",
        length=17.2,
        fx=[dict(kind="grid", at=0.0, dur=1.0, clip="3267", media=0.6, cols=3, rows=3, frames=2, order="stair"),
            dict(kind="zoom", at=11.0)],
        cut=[("3267", 0.0, 2.4, 0.0),      # (the vest selfie bursts into a 3 x 3 grid) "Most of the times I stare"
             ("3276", 2.4, 1.2, 0.3),      # "for two minutes": walking selfie
             ("3327", 3.6, 1.4, 0.0),      # "before even trying": the dirt track
             ("3260", 5.0, 0.8, 0.0),      # "to pick it up": feet on the track
             ("3313", 5.8, 1.0, 0.0),      # "preparing": the grass slope
             ("3265", 6.8, 1.8, 1.0),      # "myself, for a little": the steep path
             ("3246", 8.6, 2.4, 3.8),      # "bit of suffering.": the grin (punches forward at 11.0)
             ("3352", 11.0, 2.0, 1.0),     # (lands from the zoom) "I can hold that weight": the vest at night
             ("3310", 13.0, 1.8, 0.0),     # "on my shoulders.": the golden view from the top
             ("3305", 14.8, 2.4, 0.0)],    # James: "Go on, look after yourself", the old tree over the town
        chunks=("Most of the | times I stare | at that *vest* | for *two* minutes | before even | trying to | "
                "pick it up, | *preparing* myself | for a little | bit of *suffering.* | I can *hold* | that weight | "
                "on my *shoulders.*"),
        spoken_outro=35,
        fix={0: 0.35, 12: 3.65, 19: 6.15, 21: 7.92, 27: 11.46},
    ),
    "clip-say": dict(
        title="Heavyweight Hills — 20 s: say it",
        length=16.9,
        fx=[dict(kind="split", at=0.0, dur=1.5, top=("3310", 0.6), bottom=("3389", 0.6)),
            dict(kind="spiral", at=10.0, clips=[("3290", 1.5), ("3304", 1.0), ("3246", 4.0),
                                                ("3386", 0.5), ("3310", 0.3), ("3265", 0.5)])],
        cut=[("3389", 0.0, 3.6, 0.6),      # (golden day view over the night shadow, then the shadow opens up) "how bad it really is"
             ("3402", 3.6, 1.8, 0.3),      # "inside your mind.": the empty path at night
             ("3352", 5.4, 2.2, 0.9),      # "Some people hold that weight": the vest at night
             ("3373", 7.6, 2.4, 0.6),      # "for a lifetime and don't tell anyone": night road climb
             ("3265", 10.0, 3.0, 0.3),     # (the spiral lands here) "There's always someone": people on the hill
             ("3304", 13.0, 1.9, 1.0),     # "to your story": the terraces in golden light
             ("3290", 14.9, 2.0, 1.5)],    # "You just need to say it.": straight to camera
        chunks=("No one | ever *knows* | how bad it | really is | inside | your *mind.* | Some people | "
                "hold that *weight* | on their shoulders | for a *lifetime* | and don't tell | *anyone.* | "
                "There's always | *someone* who | can relate | to your *story.* | You just need | to *say* it."),
        drop=[27],                          # Whisper heard a stray "Story." in the pause
        outro=False,
        fix={0: 0.38, 9: 3.72, 12: 5.44, 27: 10.94, 36: 14.97},
    ),
}

if __name__ == "__main__":
    for name, cfg in CLIPS.items():
        build(name, cfg)
