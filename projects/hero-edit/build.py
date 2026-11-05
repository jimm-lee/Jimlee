#!/usr/bin/env python3
"""Writes film-15/index.html and film-10/index.html (huashu-motion compositions) from the cut lists below.

Hero edits, no soundtrack (music is added afterwards). House style: brand/README.md. Captions are written in the
spirit of James's stoic/strategy quotes (stillness, response over circumstance, discipline over motivation,
consistency over applause, building quietly). Times are seconds on a 0.5 s grid.
"""
from pathlib import Path

HERE = Path(__file__).parent

# (clip, start, duration, media_start)
CUT_15 = [
    ("0171", 0.0, 2.0, 15.5),       # sauna: stillness
    ("8230", 2.0, 0.5, 3.8),        # the coast from above
    ("9170", 2.5, 1.0, 0.4),        # geyser: pressure
    ("7989", 3.5, 1.0, 3.3),        # rodeo: the chaos
    ("9161", 4.5, 1.0, 1.0),        # fight night
    ("0170", 5.5, 2.0, 1.6),        # ice bath
    ("9661_slow", 7.5, 1.5, 4.6),   # dune run, half speed
    ("9319", 9.0, 0.5, 2.5),        # dragon boats
    ("9357", 9.5, 0.5, 1.2),        # Split Apple Rock
    ("2153", 10.0, 2.0, 2.4),       # vest selfie, golden hour
    ("0389", 12.0, 3.0, 1.0),       # end: sunset on deck
]
# (text html, css size class, start, end, top px)
TITLES_15 = [
    ('Be<br><span class="acc">still.</span>', "l", 0.0, 2.5, 230),
    ("You can't control<br>the <span class=\"acc\">chaos.</span>", "m", 2.5, 4.5, 250),
    ('Only your<br><span class="acc">response.</span>', "m", 4.5, 5.5, 250),
    ('Discipline<br>over <span class="acc">comfort.</span>', "m", 5.5, 7.5, 230),
    ('Hard moments<br>reveal <span class="acc">strength.</span>', "m", 7.5, 9.0, 1130),
    ('Build it<br><span class="acc">quietly.</span>', "l", 10.0, 12.0, 230),
]
END_15 = 12.0
LEN_15 = 15.0

CUT_10 = [
    ("0170", 0.0, 1.5, 1.6),
    ("9170", 1.5, 1.0, 0.4),
    ("7989", 2.5, 0.5, 3.4),
    ("9161", 3.0, 0.5, 1.2),
    ("9661_slow", 3.5, 1.5, 4.6),
    ("2153", 5.0, 2.0, 2.4),
    ("0389", 7.0, 3.0, 1.0),
]
TITLES_10 = [
    ('Discipline<br>over <span class="acc">comfort.</span>', "m", 0.0, 1.5, 230),
    ('Control the<br><span class="acc">response.</span>', "m", 1.5, 3.5, 250),
    ('Hard moments<br>reveal <span class="acc">strength.</span>', "m", 3.5, 5.0, 1130),
    ('Build it<br><span class="acc">quietly.</span>', "l", 5.0, 7.0, 230),
]
END_10 = 7.0
LEN_10 = 10.0

END_LINE = "Do the"
END_WORD = "WORK."

TEMPLATE = (HERE / "template.html").read_text()


def render(cut, titles, end_at, length, title):
    last = len(cut) - 1
    shots = "\n".join(
        f'  <div class="shot{" endshot" if i == last else ""}" id="s{i}"'
        f'{" style=\"visibility:visible\"" if i == 0 else ""} data-om-id="shot-{c}">'
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
            .replace("{{END_LINE}}", END_LINE)
            .replace("{{END_WORD}}", END_WORD)
            .replace("{{END}}", str(end_at))
            .replace("{{END_DUR}}", str(length - end_at)))


(HERE / "film-15/index.html").write_text(render(CUT_15, TITLES_15, END_15, LEN_15, "Hero edit — 15 s"))
(HERE / "film-10/index.html").write_text(render(CUT_10, TITLES_10, END_10, LEN_10, "Hero edit — 10 s"))
print("wrote film-15/index.html, film-10/index.html")
