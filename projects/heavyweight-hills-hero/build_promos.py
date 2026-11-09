#!/usr/bin/env python3
"""10 s promos for Heavyweight Hills from the unused lines in James's Nov 9 voice-over (Movember_4).

Same engine and house style as the intros (build_intros.py): captions 1–3 words tracking the voice, impact words
green. Writes promo-<name>/index.html; voice from voiceover/stitch_vo.py promo-<name> m4=… o=…
"""
from build_intros import build

PROMOS = {
    "promo-invisible": dict(
        title="Heavyweight Hills — promo: invisible",
        length=11.5,
        cut=[("3276", 0.0, 2.0, 0.2),      # "Because we all": walking selfie in the vest
             ("3267", 2.0, 1.4, 0.85),     # "carry weight": the vest in full view
             ("3402", 3.4, 1.6, 0.3),      # "sometimes, most of the time": the empty path at night
             ("3292", 5.0, 1.0, 1.0),      # "even": night street
             ("3389", 6.0, 2.8, 0.6),      # "it's invisible. You don't see it.": the vest's shadow
             ("3319", 8.8, 2.7, 0.0)],     # James: "Go on, look after yourself", over the harbour
        chunks=("Because | we all | carry *weight,* | sometimes, | most of | the time even, | it's *invisible.* | "
                "You don't | *see* it."),
        spoken_outro=17,
        fix={0: 0.35},
    ),
    "promo-lifetime": dict(
        title="Heavyweight Hills — promo: a lifetime",
        length=10.4,
        cut=[("3352", 0.0, 2.4, 0.9),      # "Some people hold that weight": the vest at night
             ("3373", 2.4, 2.3, 0.6),      # "for a lifetime and don't tell anyone": night road climb
             ("3265", 4.7, 2.7, 1.0),      # "There's always someone": people on the steep path
             ("3428", 7.4, 3.0, 1.3)],     # "who can relate to your story": the Mount at night
        chunks=("Some people | hold that *weight* | on their | shoulders | for a | *lifetime* | and don't | "
                "tell *anyone.* | There's always | *someone* | who can | relate to | your *story.*"),
        drop=[15, 16],                     # Whisper heard "a story" twice; the audio ends cleanly on "anyone"
        outro=False,
        fix={0: 0.35, 15: 5.46},
    ),
    "promo-stare": dict(
        title="Heavyweight Hills — promo: the stare",
        length=11.4,
        cut=[("3276", 0.0, 1.9, 0.2),      # "Most of the times I stare": walking selfie
             ("3267", 1.9, 1.7, 0.85),     # "at that vest for two minutes"
             ("3327", 3.6, 1.4, 0.0),      # "before even trying": the dirt track
             ("3260", 5.0, 0.8, 0.0),      # "to pick it up": feet on the track
             ("3313", 5.8, 1.0, 0.0),      # "preparing": the grass slope
             ("3265", 6.8, 1.8, 1.0),      # "myself, for a little bit": the steep path
             ("3246", 8.6, 2.8, 3.8)],     # "of suffering.": summit selfie, grinning
        chunks=("Most of | the times | I stare | at that *vest* | for *two* minutes | before even | trying to | "
                "pick it up, | *preparing* | myself | for a | little bit | of *suffering.*"),
        outro=False,
        fix={0: 0.35, 12: 3.65, 19: 6.15, 21: 7.92},
    ),
    "promo-change": dict(
        title="Heavyweight Hills — promo: needs to change",
        length=10.6,
        cut=[("3286", 0.0, 2.3, 0.5),      # "So many men": the rain
             ("3352", 2.3, 2.0, 0.9),      # "hold this weight on their shoulders": the vest at night
             ("3401", 4.3, 1.7, 0.5),      # "and don't tell anyone": night flax
             ("3315", 6.0, 1.7, 0.0),      # "And that needs to change": Running for Movember
             ("3319", 7.7, 2.9, 0.0)],     # James: "Go on, look after yourself", over the harbour
        chunks=("So many | *men* | hold this | *weight* | on their | shoulders and | don't tell | *anyone.* | "
                "And that | needs to | *change.*"),
        spoken_outro=18,
        fix={0: 0.36, 3: 2.35},
    ),
}

if __name__ == "__main__":
    for name, cfg in PROMOS.items():
        caps = build(name, cfg)
        print("   " + " | ".join(f"{a:.2f}" for _, a, _ in caps))
