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
LETTER_FADE = 0.25
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

OUTRO = [("Go on,", 0.0, 0.32), ("look", 0.38, 0.30), ("after", 0.36, 0.40), ("*yourself*", 0.40, 0.70)]

INTROS = {
    "intro-a": dict(
        title="Heavyweight Hills — intro A: the challenge",
        length=29.5,
        # (clip, start, duration, media start); "MAP" is the map scene
        cut=[("3373", 0.0, 3.35, 0.0),     # hook: night road climb, nobody saw it
             ("3352", 3.35, 3.15, 0.9),    # the vest, at night, with a mate
             ("3327", 6.5, 2.0, 0.0),      # "up the hill": the dirt track
             ("3313", 8.5, 1.0, 0.0),      # "down the hill": the grass slope
             ("3377", 9.5, 1.1, 0.6),      # night road down
             ("3315", 10.6, 1.6, 0.0),     # "30 kilos on my back": Running for Movember sign
             ("MAP", 12.2, 6.3, 0.0),      # "one hill every day": a pin per day
             ("3430", 18.5, 2.6, 1.1),     # "Heavyweight Hills": the Mount Drury Reserve sign
             ("3401", 21.1, 2.0, 0.6),     # "we all carry our own weight"
             ("3389", 23.1, 2.4, 0.8),     # "this one is visible": the vest's shadow
             ("3319", 25.5, 4.0, 0.0)],    # linger: the harbour from the top
        map=dict(kind="days", at=12.2),
        tops={18: 300, 19: 300},   # "and calling it Heavyweight Hills" sits above the Mount Drury sign
        chunks=("Just because | I haven't *posted* it | doesn't mean I | haven't been *doing* it. | *30* kilo | "
                "weight vest, | same as last year. | So walking | *up* the hill, | walking *down* | the hill, obviously. | "
                "*30* kilos | on my back, | at least | one hill | *every* day | for the whole | month of *Movember,* | "
                "and calling it | *Heavyweight* Hills. | We all carry | our own *weight,* | but this one | is *visible.*"),
        fix={0: 0.62, 48: 18.62},   # word index → start (Whisper places a few segment starts early)
    ),
    "intro-b": dict(
        title="Heavyweight Hills — intro B: the why",
        length=29.0,
        cut=[("MAP", 0.0, 3.3, 0.0),       # hook: every hill so far, pulling back from Mount Drury
             ("3322", 3.3, 2.05, 0.2),     # "a bigger reason": Main Beach through the trees
             ("3402", 5.35, 3.55, 0.0),    # "a memory of someone special": the empty path at night
             ("3320", 8.9, 1.3, 0.0),      # "my uncle": branch over the surf
             ("3373", 10.2, 2.4, 0.6),     # "the last three months"
             ("3377", 12.6, 2.0, 0.0),     # "two grandparents"
             ("3352", 14.6, 3.0, 0.9),     # "we all carry weight": the vest
             ("3389", 17.6, 2.0, 1.2),     # "some of it is invisible": the shadow
             ("3315", 19.6, 2.4, 0.0),     # "this month": Running for Movember
             ("3327", 22.0, 2.6, 1.4),     # "no one has to carry that weight alone"
             ("3428", 24.6, 4.4, 1.3)],    # linger: the Mount at night
        map=dict(kind="all", at=0.0),
        chunks=("It's a | physical challenge, | but as always, | there's a *bigger* | reason behind it. | It's a memory | "
                "of someone *special.* | I lost my *uncle* | last year, | and in the | last three months, | I've lost two | "
                "*grandparents.* | Because we all | carry *weight.* | Just some | of it | is *invisible.* | So this month, | "
                "let's make sure | no one has | to carry | that weight *alone.*"),
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


def captions(spec, words, fix):
    """Map the hand-made chunk spec onto Whisper's word timings: [(html, at, out)]."""
    words = [list(w) for w in words]
    for i, start in fix.items():
        words[i][1] = start
    parts = [p.strip().split() for p in spec.split("|")]
    n = sum(map(len, parts))
    assert n == len(words), f"chunk spec has {n} words, the voice has {len(words)}"
    starts = [w[1] for w in words]
    out, i = [], 0
    for k, part in enumerate(parts):
        ws = words[i:i + len(part)]
        at = ws[0][1] - 0.05
        spans = []
        for j, (shown, w) in enumerate(zip(part, ws)):
            nxt = starts[i + j + 1] if i + j + 1 < len(starts) else w[2] + 0.4
            d = min(WORD_MAX, max(WORD_MIN, min(nxt, w[2] + 0.25) - w[1]))
            spans.append(word_span(shown, w[1] - at, d))
        i += len(part)
        written = ws[-1][1] - at + min(WORD_MAX, max(WORD_MIN, ws[-1][2] - ws[-1][1])) + LETTER_FADE
        nxt_at = words[i][1] - 0.05 if i < len(words) else None
        out_t = at + max(written + 0.35, ws[-1][2] - at + 0.2)
        out_t = max(out_t, min(nxt_at if nxt_at else 1e9, ws[-1][2] + HOLD_MAX))
        if nxt_at is not None:
            out_t = min(out_t, nxt_at)
        out.append((" ".join(spans), round(at, 2), round(out_t, 2)))
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
    tops = cfg.get("tops", {})
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
