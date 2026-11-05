#!/usr/bin/env python3
"""Writes film-15/index.html and film-10/index.html (huashu-motion compositions) from the cut lists below.

Hero edits, no soundtrack (music is added afterwards). Type: Anton caps with the #75FF78 accent (chosen by James for
hero edits, Nov 2026). Times are seconds on a 0.5 s grid.

Structure (James's montage brief, "transformation" formula): hook (~15 %) → connection (~20 %) → build (~30 %)
→ payoff (~20 %) → linger (~15 %). Contrast shot to shot: intimacy vs scale, stillness vs movement, dark vs light.
One hook line per cut (from James's hook-line list), split into two readable blocks; the name closes the linger.
"""
from pathlib import Path

HERE = Path(__file__).parent

# (clip, start, duration, media_start)
CUT_15 = [
    # 01 hook 0–2.5: emotional interruption, lowering into the ice, the splash
    ("0170", 0.0, 2.5, 1.4),
    # 02 connection 2.5–5.5: the world (wide, light), then the human (walking, moving)
    ("8230", 2.5, 1.0, 3.6),        # the coast from above
    ("2524", 3.5, 2.0, 1.3),        # Movember walk
    # 03 build 5.5–9.5: rhythm, still/dark/loud alternating, cuts getting shorter
    ("0171", 5.5, 1.0, 15.5),       # sauna: stillness, warm and close
    ("7989", 6.5, 1.0, 3.3),        # rodeo: chaos, daylight
    ("9161", 7.5, 0.5, 1.0),        # fight night: dark
    ("9319", 8.0, 0.5, 2.5),        # dragon boats: effort
    ("9170", 8.5, 0.5, 0.6),        # geyser: pressure
    ("9357", 9.0, 0.5, 1.2),        # Split Apple Rock: stillness, scale
    # 04 payoff 9.5–13: strongest images, movement and scale
    ("9661_slow", 9.5, 2.0, 4.4),   # dune run, half speed
    ("2148", 11.5, 1.5, 0.6),       # sun on the sea
    # 05 linger 13–15: quiet expression; turns to camera at golden hour
    ("2153", 13.0, 2.0, 3.3),
]
# (text html, css size class, start, end, top px)
TITLES_15 = [
    ("The ordinary days<br>are quietly building", "h", 0.4, 2.5, 240),
    ('the <span class="acc">extraordinary</span> life<br>you\'ve always imagined.', "h", 2.5, 5.5, 240),
]
END_15 = 13.0
LEN_15 = 15.0

CUT_10 = [
    ("0170", 0.0, 2.0, 1.8),        # hook: into the ice
    ("8230", 2.0, 0.5, 3.6),        # connection: the world
    ("2524", 2.5, 1.0, 1.5),        # connection: the human
    ("0171", 3.5, 0.5, 15.5),       # build
    ("7989", 4.0, 0.5, 3.4),
    ("9161", 4.5, 0.5, 1.2),
    ("9170", 5.0, 0.5, 0.6),
    ("9319", 5.5, 0.5, 2.5),
    ("9661_slow", 6.0, 1.5, 4.6),   # payoff
    ("2148", 7.5, 1.0, 0.9),
    ("2153", 8.5, 1.5, 3.8),        # linger
]
TITLES_10 = [
    ("Your comfort zone<br>can quietly become", "h", 0.3, 2.0, 240),
    ('the most <span class="acc">expensive</span> place<br>you ever live.', "h", 2.0, 3.8, 240),
]
END_10 = 8.5
LEN_10 = 10.0

END_LINE = "James"
END_WORD = "Leahy"

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
