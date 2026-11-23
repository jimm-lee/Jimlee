#!/usr/bin/env python3
"""One colour grade for an edit (James, Nov 23: "colour graded and flow"): graded copies of clips, used as "g<clip>".

Filmic teal-and-amber: soft S-curve with lifted blacks and rolled-off highlights, cool shadows, warm highlights,
slightly calmer saturation. Night clips get a touch more exposure so day and night sit together in one film.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
CLIPS = HERE / "clips"
NIGHT = {"3440", "3449", "3635", "3637", "3624", "3390", "3392", "3389", "3604", "3605", "3643"}
LOOK = ("curves=master='0/0.04 0.2/0.15 0.5/0.5 0.8/0.84 1/0.96',"
        "colorbalance=rs=-0.10:gs=-0.02:bs=0.12:rm=-0.02:gm=0.0:bm=0.03:rh=0.10:gh=0.03:bh=-0.10,"
        "huesaturation=hue=-18:saturation=-0.35:colors=g,"          # bright greens pulled towards olive
        "eq=saturation=0.92:contrast=1.04,"
        "vignette=angle=PI/5:mode=forward")
NIGHT_LIFT = "eq=gamma=1.12:brightness=0.015,"


def graded(clip):
    """clips/g<clip>.mp4, made once."""
    out = CLIPS / f"g{clip}.mp4"
    if not out.exists():
        vf = (NIGHT_LIFT if clip in NIGHT else "") + LOOK + ",format=yuv420p"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(CLIPS / f"{clip}.mp4"), "-vf", vf,
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-g", "15", "-an",
                        "-movflags", "+faststart", str(out)], check=True)
    return out


if __name__ == "__main__":
    for c in sys.argv[1:]:
        print(graded(c))
