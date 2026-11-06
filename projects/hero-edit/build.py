#!/usr/bin/env python3
"""Writes film-15/index.html and film-10/index.html (huashu-motion compositions) from the cut lists below.

Hero edits, no soundtrack (music is added afterwards). Type: Anton caps with the #75FF78 accent (chosen by James for
hero edits, Nov 2026). Times are seconds on a 0.5 s grid.

Structure (James's montage brief, "transformation" formula): hook (~15 %) → connection (~20 %) → build (~30 %)
→ payoff (~20 %) → linger (~15 %). Contrast shot to shot: intimacy vs scale, stillness vs movement, dark vs light.
One hook line per cut (from James's hook-line list), split into two readable blocks; the name closes the linger.
"""
import math
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
SPEAK_BASE = 0.22        # s per word
SPEAK_PER_LETTER = 0.06  # s per letter (longer words take longer to say; letters spell out across this)
SPEAK_MIN, SPEAK_MAX = 0.32, 0.85
PAUSE_COMMA = 0.2        # extra beat after , : ;
PAUSE_STOP = 0.3         # extra beat after . ? !
LETTER_FADE = 0.25    # each letter's fade-in
WRITE_SHARE = 1.0     # letters are spread over the whole of the word's spoken time
READ_BASE = 0.07      # hold after the last letter lands = READ_BASE + READ_PER_WORD (about 0.35 s)
READ_PER_WORD = 0.28  # the 10 s cuts pass a slightly smaller value
CHUNK_GAP = 0.0       # the next chunk starts writing as soon as the last one clears (no dead air)
CAPTION_TOP = 520     # px; single row in the upper third, not too high (James, Nov 2026)
CHERRY = "#FDE68A"    # unused: green words no longer have an outline (kept so old templates still build)

# The closing line over the linger shot (replaces the name card); its last chunk stays until the fade.
OUTRO = "Go on, | look after *yourself*"
OUTRO_DELAY = 0.1     # after the linger shot starts
OUTRO_TOP = 760       # px; first line, centred over the sea
OUTRO_LINE = 140      # px between the two stacked lines
FADE_OUT = 0.6        # s of fade to black at the very end

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
        dur = offsets[-1] + write_time(words[-1]) * WRITE_SHARE + LETTER_FADE + READ_BASE + read_per_word
        out.append((spans, round(at, 2), round(at + dur, 2)))
        at += dur + CHUNK_GAP
    return out


SPIRAL_FRAMES = 3       # each clip flashes for this many frames in the opening spiral (2 felt a touch too quick)
SPIRAL_LAND_FRAMES = 4  # ... the last three slow down as the spiral lands
SPIRAL_ANGLE = 32.0     # degrees of turn on the first flash, easing to 0 on the hook shot


def spiral_flashes(cut, extra=()):
    """Opening spiral: every clip in the edit flashes by, turning and zooming, and lands on the hook shot.
    Returns [(clip, at, dur, media, angle, scale)] and the time the spiral ends."""
    seen, order = set(), []
    for c, _, _, m in list(cut[1:]) + list(extra) + list(cut[:1]):   # the hook clip last, so the spiral lands into it
        if c not in seen:
            seen.add(c); order.append((c, m))
    flashes, at, n = [], 0.0, len(order)
    for i, (c, m) in enumerate(order):
        frames = SPIRAL_LAND_FRAMES if i >= n - 3 else SPIRAL_FRAMES
        dur = round(frames / 30, 4)
        p = i / max(1, n - 1)
        angle = round(-SPIRAL_ANGLE * (1 - p) ** 1.4, 2)
        rad = math.radians(abs(angle))
        scale = round(max(1.0, math.cos(rad) + (1920 / 1080) * math.sin(rad)) * 1.04, 3)   # cover the frame while turned
        flashes.append((c, round(at, 4), dur, m, angle, scale))
        at += dur
    return flashes, round(at, 3)


GRID_GAP = 10            # px black gutter between grid cells
GRID_OFFSET = 0.08       # s media offset between duplicated grid cells ("duplicate clips & offset")


def grid_cells(cols, rows, gap=GRID_GAP):
    """Cell rectangles (left, top, width, height) in px over the 1080×1920 frame, with black gutters."""
    w = (1080 - gap * (cols + 1)) / cols
    h = (1920 - gap * (rows + 1)) / rows
    return [(round(gap + c * (w + gap), 1), round(gap + r * (h + gap), 1), round(w, 1), round(h, 1))
            for r in range(rows) for c in range(cols)]


def build_fx(cut, fx):
    """Grid framework: crop-to-grid builds (duplicate clips, offset), fit-to-grid collages, crop flashes, flashes.
    Returns (html, cell timings for JS, flash times, {shot index: time the full shot takes over})."""
    import random
    html, cells, flashes, takeover, spins = [], [], [], {}, []
    for n, f in enumerate(fx or []):
        kind = f["kind"]
        if kind == "flash":
            flashes.append(f["at"])
            continue
        step = f.get("frames", 2) / 30
        if kind == "grid":                      # one clip cropped into cells that pop in, each slightly out of sync
            i = len(cut) - 1 if f["shot"] == "last" else f["shot"]
            c, at, d, m = cut[i]
            rects = grid_cells(f["cols"], f["rows"], f.get("gap", GRID_GAP))
            order = list(range(len(rects)))
            if f.get("order", "random") == "random":
                random.Random(n).shuffle(order)
            end = round(at + len(rects) * step, 3)
            spin = f.get("spin")                # when every cell is in: the grid spirals into the full clip
            hold, spin_dur = f.get("hold", 0.15), f.get("spin_dur", 0.6)
            gone = round(end + hold + spin_dur, 3) if spin else end
            takeover[i] = round(end + hold, 3) if spin else end
            if spin:
                spins.append((f"fx{n}g", f"s{i}", takeover[i], spin_dur))
                html.append(f'  <div class="spinwrap" id="fx{n}g" style="position:absolute;inset:0">')
            for k, idx in enumerate(order):
                l, t, w, h = rects[idx]
                cid = f"fx{n}c{k}"
                html.append(f'  <div class="shot cell" id="{cid}" style="clip-path:inset({t}px {1080 - l - w}px {1920 - t - h}px {l}px)">'
                            f'<video src="assets/clips/{c}.mp4" class="clip" data-start="{at}" data-duration="{round(gone - at + .1, 3)}" '
                            f'data-media-start="{round(m + (k % 3) * GRID_OFFSET, 2)}" muted playsinline></video></div>')
                cells.append((cid, round(at + k * step, 3), gone))
            if spin:
                html.append('  </div>')
        elif kind == "collage":                 # several clips resized into a grid, popping in one by one
            rects = grid_cells(f["cols"], f["rows"], f.get("gap", GRID_GAP))
            at, dur = f["at"], f["dur"]
            for k, ((c, m), (l, t, w, h)) in enumerate(zip(f["clips"], rects)):
                cid = f"fx{n}c{k}"
                start = round(at + k * step, 3)
                html.append(f'  <div class="shot cell tile" id="{cid}" style="inset:auto;left:{l}px;top:{t}px;width:{w}px;height:{h}px">'
                            f'<video src="assets/clips/{c}.mp4" class="clip" data-start="{start}" data-duration="{round(at + dur - start, 3)}" '
                            f'data-media-start="{m}" muted playsinline></video></div>')
                cells.append((cid, start, round(at + dur, 3)))
    return "\n".join(html), cells, flashes, takeover, spins


def render(cut, hook, hook_start, end_at, length, title, tops=None, read_per_word=READ_PER_WORD, outro_top=None,
           spiral=False, fx=None):
    collage_clips = [(c, 0, 0, m) for f in (fx or []) if f["kind"] == "collage" for c, m in f["clips"]]
    flashes, spiral_end = spiral_flashes(cut, collage_clips) if spiral else ([], 0.0)
    if spiral:
        hook_start = max(hook_start, spiral_end + 0.1)   # the first caption starts as the spiral lands
    titles = chunks(hook, hook_start, read_per_word)
    # closing line: two stacked rows that both stay up; the second starts writing as soon as the first is said
    outro = chunks(OUTRO, end_at + OUTRO_DELAY)
    first = OUTRO.split("|")[0].split()
    first_said = sum(speak(w) for w in first[:-1]) + write_time(first[-1])  # line 2 follows straight on
    outro = [(outro[0][0], outro[0][1], length),
             (outro[1][0], round(outro[0][1] + first_said, 2), length)]
    tops = dict(tops or {})
    tops.update({len(titles) + i: (outro_top or OUTRO_TOP) + i * OUTRO_LINE for i in range(len(outro))})
    titles = titles + outro
    last = len(cut) - 1
    shots = "\n".join(
        f'  <div class="shot{" endshot" if i == last else ""}" id="s{i}"'
        f'{" style=\"visibility:visible\"" if i == 0 else ""} data-om-id="shot-{c}">'
        f'<video src="assets/clips/{c}.mp4" class="clip" data-start="{s}" data-duration="{d}" '
        f'data-media-start="{m}" muted playsinline></video></div>'
        for i, (c, s, d, m) in enumerate(cut)
    )
    shots += "".join(
        f'\n  <div class="shot spiral" id="sp{i}" data-om-id="spiral-{c}">'
        f'<video src="assets/clips/{c}.mp4" class="clip" data-start="{a}" data-duration="{d}" '
        f'data-media-start="{m}" muted playsinline></video></div>'
        for i, (c, a, d, m, _, _) in enumerate(flashes)
    )
    fx_html, fx_cells, fx_flashes, takeover, fx_spins = build_fx(cut, fx)
    spin_js = ",\n    ".join(f"['{w}', '{sid}', {a}, {d}]" for w, sid, a, d in fx_spins)
    shots += ("\n" + fx_html) if fx_html else ""
    cut_js = ",\n    ".join(f"['s{i}', {takeover.get(i, s)}, {round(s + d - takeover.get(i, s), 3)}]"
                             for i, (_, s, d, _) in enumerate(cut))
    fx_js = ",\n    ".join(f"['{cid}', {a}, {e}]" for cid, a, e in fx_cells)
    flash_js = ", ".join(str(t) for t in fx_flashes)
    spiral_js = ",\n    ".join(f"['sp{i}', {a}, {d}, {ang}, {sc}]" for i, (_, a, d, _, ang, sc) in enumerate(flashes))
    types = "\n".join(
        f'  <div class="t h cap" id="t{i}" style="top:{(tops or {}).get(i, CAPTION_TOP)}px" data-om-id="caption-{i}">{html}</div>'
        for i, (html, s, e) in enumerate(titles)
    )
    titles_js = ",\n    ".join(f"['t{i}', {s}, {e}]" for i, (_, s, e) in enumerate(titles))
    return (TEMPLATE.replace("{{TITLE}}", title)
            .replace("{{SHOTS}}", shots)
            .replace("{{TYPES}}", types)
            .replace("{{CUT_JS}}", cut_js)
            .replace("{{SPIRAL_JS}}", spiral_js)
            .replace("{{FX_JS}}", fx_js)
            .replace("{{FLASH_JS}}", flash_js)
            .replace("{{SPIN_JS}}", spin_js)
            .replace("{{SPIRAL_END}}", str(spiral_end))
            .replace("{{TITLES_JS}}", titles_js)
            .replace("{{CHERRY}}", CHERRY)
            .replace("{{LETTER_FADE}}", str(LETTER_FADE))
            .replace("{{WRITE_SHARE}}", str(WRITE_SHARE))
            .replace("{{FADE_OUT}}", str(FADE_OUT))
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
