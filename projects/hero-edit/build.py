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
    # 04 payoff 9.5–13: strongest images, movement, then warmth
    ("9661_slow", 9.5, 1.5, 4.4),   # dune run, half speed
    ("2153", 11.0, 1.0, 4.1),       # golden hour, turns to camera
    # 05 linger 13–15: the open sea at sunset, slow push, fade to black. No name, no text
    ("2148", 12.0, 3.0, 0.1),
]
# Captions: one hook line per cut, shown as chunks of 2–3 words on a single row ("|" splits chunks, *word* = green
# accent with the cherry outline). Words pop in one at a time; each chunk clears once it has had time to be read.
HOOK_15 = "The ordinary days | are quietly building | the *extraordinary* life | you've always imagined."
HOOK_15_START = 0.4
END_15 = 12.0
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
    ("9661_slow", 6.0, 1.0, 4.6),   # payoff
    ("2153", 7.0, 0.5, 4.5),        # golden hour, turns to camera
    ("2148", 7.5, 2.5, 0.1),        # linger: open sea, closing line, fade to black
]
HOOK_10 = "Your comfort zone | can quietly become | the most | *expensive* place | you ever live."
HOOK_10_START = 0.2
HOOK_10_READ = 0.24  # slightly quicker reads so the hook clears before the payoff
END_10 = 7.5
LEN_10 = 10.0

WORD_GAP = 0.14       # seconds between words popping in
READ_BASE = 0.35      # minimum hold once the chunk is complete
READ_PER_WORD = 0.28  # extra reading time per word
CHUNK_GAP = 0.1       # empty beat between chunks
CAPTION_TOP = 250     # px; single row in the upper third
CHERRY = "#990F3D"    # James picked B (dark cherry) over #8C172E, Nov 2026

# The closing line over the linger shot (replaces the name card); its last chunk stays until the fade.
OUTRO = "Go on, | look after *yourself*"
OUTRO_DELAY = 0.3     # after the linger shot starts
OUTRO_TOP = 800       # px; centred over the sea

END_LINE = "James"
END_WORD = "Leahy"

TEMPLATE = (HERE / "template.html").read_text()


def chunks(hook: str, start: float, read_per_word: float = READ_PER_WORD) -> list[tuple[str, float, float]]:
    """Split a hook line into timed chunks: (html of word spans, start, end)."""
    out, at = [], start
    for part in (p.strip() for p in hook.split("|")):
        words = part.split()
        spans = " ".join(
            f'<span class="w acc">{w[1:-1]}</span>' if w.startswith("*") and w.endswith("*")
            else f'<span class="w">{w}</span>' for w in words)
        dur = WORD_GAP * (len(words) - 1) + READ_BASE + read_per_word * len(words)
        out.append((spans, round(at, 2), round(at + dur, 2)))
        at += dur + CHUNK_GAP
    return out


def render(cut, hook, hook_start, end_at, length, title, tops=None, read_per_word=READ_PER_WORD):
    titles = chunks(hook, hook_start, read_per_word)
    outro = chunks(OUTRO, end_at + OUTRO_DELAY)
    outro[-1] = (outro[-1][0], outro[-1][1], length)  # the last words stay through the fade
    tops = dict(tops or {})
    tops.update({len(titles) + i: OUTRO_TOP for i in range(len(outro))})
    titles = titles + outro
    last = len(cut) - 1
    shots = "\n".join(
        f'  <div class="shot{" endshot" if i == last else ""}" id="s{i}"'
        f'{" style=\"visibility:visible\"" if i == 0 else ""} data-om-id="shot-{c}">'
        f'<video src="assets/clips/{c}.mp4" class="clip" data-start="{s}" data-duration="{d}" '
        f'data-media-start="{m}" muted playsinline></video></div>'
        for i, (c, s, d, m) in enumerate(cut)
    )
    types = "\n".join(
        f'  <div class="t h cap" id="t{i}" style="top:{(tops or {}).get(i, CAPTION_TOP)}px" data-om-id="caption-{i}">{html}</div>'
        for i, (html, s, e) in enumerate(titles)
    )
    cut_js = ",\n    ".join(f"['s{i}', {s}, {d}]" for i, (_, s, d, _) in enumerate(cut))
    titles_js = ",\n    ".join(f"['t{i}', {s}, {e}]" for i, (_, s, e) in enumerate(titles))
    return (TEMPLATE.replace("{{TITLE}}", title)
            .replace("{{SHOTS}}", shots)
            .replace("{{TYPES}}", types)
            .replace("{{CUT_JS}}", cut_js)
            .replace("{{TITLES_JS}}", titles_js)
            .replace("{{CHERRY}}", CHERRY)
            .replace("{{WORD_GAP}}", str(WORD_GAP))
            .replace("{{END_LINE}}", END_LINE)
            .replace("{{END_WORD}}", END_WORD)
            .replace("{{END}}", str(end_at))
            .replace("{{END_DUR}}", str(length - end_at)))


(HERE / "film-15/index.html").write_text(render(CUT_15, HOOK_15, HOOK_15_START, END_15, LEN_15, "Hero edit — 15 s"))
(HERE / "film-10/index.html").write_text(render(CUT_10, HOOK_10, HOOK_10_START, END_10, LEN_10, "Hero edit — 10 s",
                                                tops={4: 1130}, read_per_word=HOOK_10_READ))  # last chunk sits in the sand, clear of James on the dune)
print("wrote film-15/index.html, film-10/index.html")
