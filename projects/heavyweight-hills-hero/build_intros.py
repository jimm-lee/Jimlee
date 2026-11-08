#!/usr/bin/env python3
"""Two 30 s voice-led intros for Heavyweight Hills (Movember 2026), in the hero-edit house style.

Writes intro-a/index.html and intro-b/index.html (huashu-motion compositions). Captions follow James's voice-over
word by word (timings in voiceover/words-<intro>.json), letters spelling out across each spoken word. The map is the
Day 3 & 4 recap map (OpenStreetMap), with a pin for every hill so far, from the clips' GPS.

    python3 build_intros.py && om render intro-a --silent    # then mux the voice (see README)
"""
import json
import math
import re
import shutil
from pathlib import Path

HERE = Path(__file__).parent
PROJECTS = HERE.parent
MAP_SRC = PROJECTS / "heavyweight-hills-recap-day3-4/film/assets/map"
FONTS = PROJECTS / "hero-edit/film-15/assets/fonts"
VENDOR = PROJECTS / "hero-edit/film-15/vendor"

CAPTION_TOP = 520     # px; the house caption row (upper third)
OUTRO_TOP = 760       # px; "Go on," then "look after yourself" 140 px below
OUTRO_LINE = 140
FADE_OUT = 0.6
LETTER_FADE = 0.15
WORD_MIN, WORD_MAX = 0.28, 0.85   # a word's letters spread over its spoken time, within these bounds
HOLD_MAX = 0.9                    # a chunk stays up at most this long after its last word, if nothing follows

# ---- map: same projection as heavyweight-hills-recap-day3-4/map-build/build_map34.py ----
S, W_, N, E = -37.705, 176.150, -37.612, 176.215
MX = 111320 * math.cos(math.radians((S + N) / 2))
MY = 110574


def xy(lat, lon):
    return [round((lon - W_) * MX, 1), round((N - lat) * MY, 1)]


MAP = json.loads((MAP_SRC / "map.json").read_text())
HILLS = {   # from the clips' GPS (IMG_3373/3377/3389, IMG_3401/3402/3404) and the earlier recaps
    "drury": dict(name="Mount Drury", at=MAP["drury"], dx=0, dy=-60),
    "ave": dict(name="3rd Avenue", at=MAP["ave_mid"], dx=-170, dy=0),
    "cliff": dict(name="Cliff Road", at=xy(-37.6799, 176.1698), dx=170, dy=0),
    "17th": dict(name="17th Avenue", at=xy(-37.7052, 176.1500), dx=60, dy=60),
}
DAYS = ["drury", "drury", "ave", "drury", "drury", "17th", "cliff", "drury"]   # 1–8 Nov (NZ time)
MAP["hills"] = HILLS
MAP["days"] = DAYS

# shots where James's head sits high in frame: captions starting over them move up into the sky
HIGH_FACE = {"3276": 300}

OUTRO = [("Go on,", 0.0, 0.32), ("look", 0.38, 0.30), ("after", 0.36, 0.40), ("*yourself*", 0.40, 0.70)]

INTROS = {
    "intro-a": dict(
        title="Heavyweight Hills — intro A: the challenge",
        length=28.75,
        # (clip, start, duration, media start); "MAP" is the map scene
        cut=[("3373", 0.0, 1.7, 0.0),      # hook: night road climb, nobody saw it
             ("3286", 1.7, 1.65, 1.4),     # "haven't been doing it": in the rain
             ("3352", 3.35, 1.85, 0.9),    # "30 kilo weight vest": the vest, at night, with a mate
             ("3290", 5.2, 1.3, 1.8),      # "same as last year": night selfie in the vest
             ("3260", 6.5, 0.8, 0.0),      # "walking up the hill": feet on the track
             ("3327", 7.3, 1.1, 0.0),      # up the dirt track
             ("3313", 8.4, 1.0, 0.0),      # "walking down the hill": the grass slope
             ("3265", 9.4, 1.2, 1.0),      # the steep path
             ("3276", 10.6, 1.6, 0.2),     # "30 kilos on my back": walking selfie in the vest
             ("MAP", 12.2, 6.3, 0.0),      # "one hill every day": a pin per day
             ("3244", 18.5, 2.6, 2.0),     # "Heavyweight Hills": the terraces
             ("3246", 21.1, 2.5, 3.8),     # "we all carry our own weight": summit selfie
             ("3267", 23.6, 1.6, 0.85),     # "this one is visible": the vest in full view (before the camera drops)
             ("3319", 25.2, 3.55, 0.0)],   # linger: the harbour from the top (the whole clip)
        map=dict(kind="days", at=12.2),
        chunks=("Just because I | haven't *posted* it, | doesn't mean I | haven't been | *doing* it. | "
                "*30* kilo weight | *vest,* | same as | last year. | "
                "So walking | *up* the hill, | walking *down* | the hill, | obviously. | "
                "*30* kilos | on my back, | at least | one hill | *every* day | for the whole | month of | *Movember,* | "
                "and calling it | *Heavyweight* *Hills.* | "
                "We all carry | our own *weight,* | but this one | is *visible.*"),
        fix={0: 0.62, 48: 18.62},   # word index → start (Whisper places a few segment starts early)
    ),
    "intro-b": dict(
        title="Heavyweight Hills — intro B: the why",
        length=29.0,
        cut=[("MAP", 0.0, 3.3, 0.0),       # hook: every hill so far, pulling back from Mount Drury
             ("3322", 3.3, 2.05, 0.2),     # "a bigger reason": Main Beach through the trees
             ("3269", 5.35, 2.35, 0.0),    # "a memory of someone special": the harbour, someone sitting alone
             ("3402", 7.7, 2.5, 0.3),      # "my uncle": the empty path at night
             ("3292", 10.2, 2.2, 1.0),     # "the last three months": night street
             ("3286", 12.4, 2.2, 0.5),     # "two grandparents": the rain
             ("3276", 14.6, 2.4, 0.0),     # "we all carry weight": walking selfie in the vest
             ("3389", 17.0, 2.6, 0.6),     # "some of it is invisible": the shadow
             ("3315", 19.6, 2.4, 0.0),     # "this month": Running for Movember
             ("3290", 22.0, 2.6, 0.95),    # "no one has to carry that weight alone": the wave
             ("3428", 24.6, 4.4, 1.3)],    # linger: the Mount at night
        map=dict(kind="all", at=0.0),
        chunks=("It's a physical | *challenge,* | but as always, | there's a | *bigger* reason | behind it. | "
                "It's a memory | of someone | *special.* | I lost my | *uncle* last year, | and in | the last | "
                "three months, | I've lost two | *grandparents.* | Because we all | carry *weight.* | "
                "Just some of | it is *invisible.* | So this month, | let's make sure | no one has | to carry | "
                "that weight *alone.*"),
        fix={0: 0.66, 46: 20.1, 47: 20.62},
    ),
}


def letters(text):
    return "".join(f'<span class="l">{ch}</span>' for ch in text)


def word_span(word, t, d):
    m = re.fullmatch(r"(.*?)\*(.+)\*([.,?!:;]*)", word)
    if m:
        body = f'{letters(m.group(1))}<span class="acc">{letters(m.group(2))}</span>{letters(m.group(3))}'
    else:
        body = letters(word)
    return f'<span class="w" data-t="{t:.2f}" data-d="{d:.2f}">{body}</span>'


MAX_WORDS = 3      # never more than three words on screen (most captions are one or two)
END_HOLD = 1.1     # s: at a pause, the last caption stays this long after its last word
MIN_SHOW = 0.45    # s: no caption flashes by faster than this (the next one waits a moment if it has to)
WRITE_MAX = 0.3    # s: a word's letters are all in within this, so it reads as it is said


def captions(spec, words, fix):
    """Captions that track the voice: [(html, at, out)]. Phrasing and green words from the hand-made spec,
    timing from Whisper: each caption arrives with its first word and stays until the next one is spoken."""
    parts = [p.split() for p in spec.split("|")]
    assert all(len(p) <= MAX_WORDS for p in parts), [p for p in parts if len(p) > MAX_WORDS]
    n = sum(map(len, parts))
    assert n == len(words), f"spec has {n} words, the voice has {len(words)}"
    words = [list(w) for w in words]
    for i, start in fix.items():
        words[i][1] = start
    out, i, free = [], 0, 0.0
    for part in parts:
        ws = words[i:i + len(part)]
        i += len(part)
        at = round(max(ws[0][1] - 0.05, free), 2)   # after a quick caption, this one may land a moment late
        spans = [word_span(t, max(0.0, w[1] - at), min(WRITE_MAX, max(0.15, w[2] - w[1]))) for t, w in zip(part, ws)]
        last_end = ws[-1][2]
        nxt = words[i][1] - 0.05 if i < len(words) else None
        if nxt is None or nxt - last_end > END_HOLD:
            out_t = last_end + END_HOLD      # a pause: hold, then clear
        else:
            out_t = max(nxt, at + MIN_SHOW)   # straight on: replaced as the next word is said
        free = out_t
        out.append((" ".join(spans), at, round(out_t, 2)))
    return out


def build(name, cfg):
    d = HERE / name
    (d / "assets/map").mkdir(parents=True, exist_ok=True)
    (d / "assets/fonts").mkdir(parents=True, exist_ok=True)
    shutil.copytree(VENDOR, d / "vendor", dirs_exist_ok=True)
    for f in ("BebasNeue.woff2", "BebasNeue-OFL.txt", "Outfit-var.woff2", "Outfit-OFL.txt"):
        shutil.copy(FONTS / f, d / "assets/fonts" / f)
    shutil.copy(MAP_SRC / "land.png", d / "assets/map/land.png")
    clips = d / "assets/clips"
    if not clips.exists():
        clips.symlink_to("../../clips")

    words = json.loads((HERE / f"voiceover/words-{name}.json").read_text())
    caps = captions(cfg["chunks"], words, cfg["fix"])
    length, cut = cfg["length"], cfg["cut"]
    end_at = cut[-1][1]
    outro_at = end_at + 0.15
    o_html, t = [], outro_at
    for k, (w, gap, dur) in enumerate(OUTRO):
        t += gap
        o_html.append((w, t, dur))
    row1 = " ".join(word_span(w, t - outro_at, dd) for w, t, dd in o_html[:1])
    row2_at = o_html[1][1]
    row2 = " ".join(word_span(w, t - row2_at, dd) for w, t, dd in o_html[1:])

    shots = []
    for i, (c, s, dur, m) in enumerate(cut):
        if c == "MAP":
            continue
        first = ' style="visibility:visible"' if s == 0 else ""   # frame 0 is the poster: never blank
        shots.append(f'  <div class="shot" id="s{i}"{first} data-om-id="shot-{i}-{c}"><video src="assets/clips/{c}.mp4" '
                     f'class="clip" data-start="{s}" data-duration="{dur}" data-media-start="{m}" muted playsinline>'
                     f'</video></div>')
    cut_js = ", ".join(f"['{'map' if c == 'MAP' else f's{i}'}', {s}, {dur}]" for i, (c, s, dur, m) in enumerate(cut))
    tops = dict(cfg.get("tops", {}))
    for i, (_, a, _) in enumerate(caps):
        clip = next((c for c, s, dd, _ in cut if s <= a + 0.05 < s + dd), None)
        if clip in HIGH_FACE:
            tops.setdefault(i, HIGH_FACE[clip])
    types = [f'  <div class="t h cap" id="c{i}" data-om-id="caption-{i}" style="top:{tops.get(i, CAPTION_TOP)}px">{h}</div>'
             for i, (h, a, o) in enumerate(caps)]
    types.append(f'  <div class="t h cap" id="o1" data-om-id="outro-1" style="top:{OUTRO_TOP}px">{row1}</div>')
    types.append(f'  <div class="t h cap" id="o2" data-om-id="outro-2" style="top:{OUTRO_TOP + OUTRO_LINE}px">{row2}</div>')
    titles = [(f"c{i}", a, o) for i, (h, a, o) in enumerate(caps)] + [("o1", outro_at, length), ("o2", row2_at, length)]
    titles_js = ", ".join(f"['{i}', {a}, {o}]" for i, a, o in titles)
    mp = cfg["map"]
    html = (HERE / "template.html").read_text()
    for k, v in {"TITLE": cfg["title"], "SHOTS": "\n".join(shots), "TYPES": "\n".join(types), "CUT_JS": cut_js,
                 "TITLES_JS": titles_js, "END": str(end_at), "END_DUR": str(round(length - end_at, 2)),
                 "LENGTH": str(length), "FADE_OUT": str(FADE_OUT), "LETTER_FADE": str(LETTER_FADE),
                 "MAP_KIND": mp["kind"], "MAP_AT": str(mp["at"]), "MAP_W": str(MAP["width_m"]),
                 "MAP_H": str(MAP["height_m"]),
                 "MAP_STYLE": ' style="visibility:visible"' if mp["at"] == 0 else "", "MAPJSON": json.dumps(MAP, separators=(",", ":"))}.items():
        html = html.replace("{{" + k + "}}", v)
    (d / "index.html").write_text(html)
    print(f"{name}: {len(caps)} captions, {len(cut)} shots, {length} s")


if __name__ == "__main__":
    for name, cfg in INTROS.items():
        build(name, cfg)
