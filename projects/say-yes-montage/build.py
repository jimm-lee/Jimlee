#!/usr/bin/env python3
"""Writes film-30/index.html and film-10/index.html (huashu-motion compositions) from the cut lists below.

House style: brand/README.md (Merienda Black titles, #75FF78 accent on one word, Outfit labels,
down-right shadow, nothing below y 1440). Times are seconds on a 120 BPM grid (beat = 0.5 s).
"""
from pathlib import Path

HERE = Path(__file__).parent

# (clip, start, duration, media_start)
CUT_30 = [
    ("9661", 0.0, 2.0, 0.3),    # dune run: the hook
    ("9023", 2.0, 1.5, 1.4),    # sunrise, palm
    ("2148", 3.5, 1.5, 0.6),    # sunset over the sea
    ("9357", 5.0, 1.0, 1.0),    # Split Apple Rock
    ("8078", 6.0, 0.5, 0.4),    # flags and the city
    ("8342", 6.5, 1.0, 1.5),    # ferry, skyline
    ("7909", 7.5, 1.5, 0.4),    # splash off the bow
    ("0389", 9.0, 1.5, 1.6),    # sunset selfie on deck
    ("7989", 10.5, 2.5, 3.3),   # rodeo
    ("9161", 13.0, 1.5, 1.2),   # fight night
    ("races", 14.5, 1.5, 1.2),  # at the races with friends
    ("5222", 16.0, 1.0, 1.0),   # purple light on the water
    ("6169", 17.0, 1.0, 0.8),   # wood-fired oven
    ("5963", 18.0, 1.0, 1.5),   # sunset over the ranges
    ("2524", 19.0, 2.5, 1.3),   # Movember walk
    ("2153", 21.5, 3.5, 2.2),   # vest selfie, golden hour
]
# (text html, css size class, start, end, top px)
TITLES_30 = [
    ('Say<br><span class="acc big">YES.</span>', "l", 0.0, 2.0, 170),
    ('To early<br>starts.', "l", 2.0, 3.5, 250),
    ('And late<br><span class="acc">sunsets.</span>', "l", 3.5, 5.0, 250),
    ('New<br><span class="acc">places.</span>', "l", 5.0, 7.5, 250),
    ('Front-row<br><span class="acc">seats.</span>', "l", 10.5, 13.0, 250),
    ('Big<br><span class="acc">nights.</span>', "l", 13.0, 14.5, 250),
    ('Good<br><span class="acc">people.</span>', "l", 14.5, 16.0, 250),
    ('Good<br><span class="acc">food.</span>', "l", 17.0, 18.0, 250),
    ('And good<br><span class="acc">causes.</span>', "l", 19.0, 21.5, 230),
    ('Still saying<br><span class="acc">yes.</span>', "l", 22.0, 25.0, 230),
]
END_30 = 25.0
LEN_30 = 30.0

CUT_10 = [
    ("9661", 0.0, 1.5, 0.3),
    ("9023", 1.5, 1.0, 1.6),
    ("9357", 2.5, 0.5, 1.0),
    ("8342", 3.0, 0.5, 1.5),
    ("7989", 3.5, 1.0, 3.5),
    ("9161", 4.5, 0.5, 1.2),
    ("races", 5.0, 0.5, 1.6),
    ("6169", 5.5, 0.5, 0.8),
    ("2524", 6.0, 1.0, 1.5),
    ("2153", 7.0, 0.5, 2.6),
]
TITLES_10 = [
    ('Say<br><span class="acc big">YES.</span>', "l", 0.0, 1.5, 170),
]
END_10 = 7.5
LEN_10 = 10.0

TEMPLATE = (HERE / "template.html").read_text()


def render(cut, titles, end_at, length, title):
    shots = "\n".join(
        f'  <div class="shot" id="s{i}"{" style=\"visibility:visible\"" if i == 0 else ""} data-om-id="shot-{c}">'
        f'<video src="assets/clips/{c}.mp4" class="clip" data-start="{s}" data-duration="{d}" '
        f'data-media-start="{m}" muted playsinline></video></div>'
        for i, (c, s, d, m) in enumerate(cut)
    )
    types = "\n".join(
        f'  <div class="t {cls}" id="t{i}" style="top:{top}px{";opacity:1" if s == 0 else ""}" data-om-id="title-{i}">{html}</div>'
        for i, (html, cls, s, e, top) in enumerate(titles)
    )
    cut_js = ",\n    ".join(f"['s{i}', {s}, {d}]" for i, (_, s, d, _) in enumerate(cut))
    titles_js = ",\n    ".join(f"['t{i}', {s}, {e}]" for i, (_, _, s, e, _) in enumerate(titles))
    return (TEMPLATE.replace("{{TITLE}}", title)
            .replace("{{SHOTS}}", shots)
            .replace("{{TYPES}}", types)
            .replace("{{CUT_JS}}", cut_js)
            .replace("{{TITLES_JS}}", titles_js)
            .replace("{{END}}", str(end_at))
            .replace("{{END_DUR}}", str(length - end_at))
            .replace("{{LEN}}", str(length)))


(HERE / "film-30/index.html").write_text(render(CUT_30, TITLES_30, END_30, LEN_30, "Say Yes — 30 s"))
(HERE / "film-10/index.html").write_text(render(CUT_10, TITLES_10, END_10, LEN_10, "Say Yes — 10 s"))
print("wrote film-30/index.html, film-10/index.html")
