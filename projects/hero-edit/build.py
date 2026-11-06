#!/usr/bin/env python3
"""Writes film-15/index.html and film-10/index.html (huashu-motion compositions) from the cut lists below.

Hero edits, no soundtrack (music is added afterwards). Type: Anton caps with the #75FF78 accent (chosen by James for
hero edits, Nov 2026). Times are seconds on a 0.5 s grid.

Structure (James's montage brief, "transformation" formula): hook (~15 %) → connection (~20 %) → build (~30 %)
→ payoff (~20 %) → linger (~15 %). Contrast shot to shot: intimacy vs scale, stillness vs movement, dark vs light.
One hook line per cut (from James's hook-line list), split into two readable blocks; the name closes the linger.
"""
import re
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

CUT_20 = [
    # 01 hook 0–3: the unexpected image (glowing jellyfish) under the first caption, then the cold plunge
    ("0989", 0.0, 2.0, 2.4),        # jellyfish, magenta in the dark
    ("0170", 2.0, 1.0, 2.6),        # ice bath, the splash
    # 02 connection 3–7: the world (wide, still), then people (training)
    ("2894", 3.0, 1.5, 1.6),        # Aoraki / Mt Cook and the glacier lake
    ("3048", 4.5, 1.0, 2.0),        # the Wānaka tree
    ("6234", 5.5, 1.5, 4.0),        # pad work at the gym
    # 03 build 7–13: rhythm; food and town between effort and landscape, 1 s cuts to 0.5 s
    ("9681", 7.0, 1.0, 2.0),        # vintage town, red truck
    ("9733", 8.0, 0.5, 0.2),        # oysters
    ("0171", 8.5, 0.5, 15.5),       # sauna
    ("7989", 9.0, 0.5, 3.3),        # rodeo
    ("9651", 9.5, 0.5, 0.3),        # river gorge
    ("9161", 10.0, 0.5, 1.0),       # fight night
    ("9644", 10.5, 0.5, 0.8),       # seafood platter
    ("9170", 11.0, 0.5, 0.6),       # geyser
    ("3148", 11.5, 0.5, 2.6),       # candlelit table
    ("9319", 12.0, 0.5, 2.5),       # dragon boats
    ("2987", 12.5, 0.5, 0.5),       # Clay Cliffs
    # 04 payoff 13–17: movement and scale, then warmth
    ("9661_slow", 13.0, 1.5, 4.4),  # dune run, half speed
    ("3365", 14.5, 1.0, 1.0),       # running the beach
    ("2153", 15.5, 1.5, 3.6),       # golden hour, turns to camera
    # 05 linger 17–20: the sea at dusk, closing line, fade to black
    ("3366", 17.0, 3.0, 1.0),
]
HOOK_20 = "Some places | *stay* with you | long after | you've physically | left them behind."
HOOK_20_START = 0.3
END_20 = 17.0
LEN_20 = 20.0

# "The escape" (15 s): open on the grind, break out into the life
CUT_E = [
    # 01 hook 0–2.5: gridlocked motorway under the hook line, then into the ice
    ("0595", 0.0, 1.5, 1.0),        # motorway traffic at dusk
    ("7815", 1.5, 1.0, 0.5),        # ice bath close-up by the sea
    # 02 connection 2.5–5.5: open land, a path in, people
    ("9070", 2.5, 1.0, 1.0),        # paddock running out to sea stacks
    ("0079", 3.5, 1.0, 0.3),        # bush boardwalk
    ("2207", 4.5, 1.0, 2.0),        # buskers and a crowd
    # 03 build 5.5–9.5: 0.5 s cuts, loud/quiet, in/out
    ("1422", 5.5, 0.5, 2.3),        # rugby test
    ("9500", 6.0, 0.5, 1.0),        # tasting paddle
    ("0811", 6.5, 0.5, 1.0),        # rocky river
    ("6234", 7.0, 0.5, 4.5),        # pad work
    ("2565", 7.5, 0.5, 0.6),        # the odd bar
    ("8092", 8.0, 0.5, 2.0),        # harbour of yachts
    ("9504", 8.5, 0.5, 1.0),        # wall of wine
    ("9545", 9.0, 0.5, 0.5),        # misty jetty
    # 04 payoff 9.5–12: the sunrise wave, then warmth
    ("9065", 9.5, 1.5, 0.6),        # sunrise breaking against the island
    ("2153", 11.0, 1.0, 4.1),       # golden hour, turns to camera
    # 05 linger 12–15: sunrise over the sea (stops before the face at 5.0 s), closing line, fade
    ("2636", 12.0, 3.0, 1.8),
]
HOOK_E = "Being busy | isn't the same | thing as | building a life | you're *proud* of."
HOOK_E_START = 0.3
END_E = 12.0
LEN_E = 15.0

WORD_GAP = 0.14       # fallback spacing if a word has no spoken timing
# Words arrive as if read aloud: each word takes about as long as it does to say, plus a pause after punctuation.
SPEAK_BASE = 0.2         # s per word
SPEAK_PER_LETTER = 0.045 # s per letter (longer words take longer to say)
SPEAK_MIN, SPEAK_MAX = 0.3, 0.7
PAUSE_COMMA = 0.2        # extra beat after , : ;
PAUSE_STOP = 0.3         # extra beat after . ? !
READ_BASE = 0.35      # hold once the chunk's last word has landed (with READ_PER_WORD below)
READ_PER_WORD = 0.28  # added to READ_BASE for the hold; the 10 s cuts pass a smaller value
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


def write_time(word: str) -> float:
    """How long a word takes to say, without the pause after punctuation (its letters fade in over this)."""
    letters_ = sum(ch.isalnum() for ch in word)
    return round(min(SPEAK_MAX, max(SPEAK_MIN, SPEAK_BASE + SPEAK_PER_LETTER * letters_)), 2)


def speak(word: str) -> float:
    """Roughly how long a word takes to say aloud, including a pause after punctuation."""
    letters = sum(ch.isalnum() for ch in word)
    t = min(SPEAK_MAX, max(SPEAK_MIN, SPEAK_BASE + SPEAK_PER_LETTER * letters))
    if word.rstrip("*")[-1:] in ",:;":
        t += PAUSE_COMMA
    elif word.rstrip("*")[-1:] in ".?!":
        t += PAUSE_STOP
    return round(t, 2)


def letters(text: str) -> str:
    """Each character in its own span so a word can fade in letter by letter."""
    return "".join(f'<span class="l">{ch}</span>' for ch in text)


def word_span(word: str, t: float = 0.0, d: float = 0.4) -> str:
    """One word starting t s into its chunk and writing itself out over d s, letter by letter.
    *word* (with any trailing punctuation) is the green accent."""
    m = re.fullmatch(r"\*(.+)\*([.,?!:;]*)", word)
    if m:
        return (f'<span class="w" data-t="{t}" data-d="{d}"><span class="acc">{letters(m.group(1))}</span>'
                f'{letters(m.group(2))}</span>')
    return f'<span class="w" data-t="{t}" data-d="{d}">{letters(word)}</span>'


def chunks(hook: str, start: float, read_per_word: float = READ_PER_WORD) -> list[tuple[str, float, float]]:
    """Split a hook line into timed chunks: (html of word spans, start, end)."""
    out, at = [], start
    for part in (p.strip() for p in hook.split("|")):
        words = part.split()
        offsets, t = [], 0.0
        for w in words:
            offsets.append(round(t, 2))
            t += speak(w)
        spans = " ".join(word_span(w, o, write_time(w)) for w, o in zip(words, offsets))
        dur = offsets[-1] + 0.25 + READ_BASE + read_per_word
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
(HERE / "film-20/index.html").write_text(render(CUT_20, HOOK_20, HOOK_20_START, END_20, LEN_20, "Hero edit — 20 s"))
(HERE / "film-escape/index.html").write_text(render(CUT_E, HOOK_E, HOOK_E_START, END_E, LEN_E, "Hero edit — The escape"))
print("wrote film-15, film-10, film-20 and film-escape index.html")
