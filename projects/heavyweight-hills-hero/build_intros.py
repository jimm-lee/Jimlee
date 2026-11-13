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

import fx
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

# shots where the faces sit where the caption row would be: captions starting over them move to clear space
# (3276: James's head sits high, so up into the sky; 3220: faces mid-frame under a white ceiling, so down onto
# the dark jersey)
HIGH_FACE = {"3276": 300, "3220": 1300}
# pale backgrounds (concrete footpath, dirt, the white bin): captions over them get a soft dark halo
LIGHT_BG = {"3386"}   # (3307/3353, the summit-bin tap, are not used: James found them distracting)

ENDCARD = 3.0      # s: the ask (QR code to the Movember page) after the closing line; cfg endcard=0 leaves it off
QR = PROJECTS / "heavyweight-hills/film/assets/qr.svg"

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
        chunks=("Just because I | haven't *posted* it, | doesn't mean | I haven't been | *doing* it. | "
                "*30* kilo weight | *vest,* same as | last year. | So walking | *up* the hill, | walking *down* | "
                "the hill, obviously. | *30* kilos | on my back, | at least one | hill *every* day | for the whole | "
                "month of *Movember,* | and calling it | *Heavyweight* *Hills.* | We all carry | our own *weight,* | "
                "but this one | is *visible.*"),
        fix={0: 0.3, 48: 18.62},   # 0: the first caption is up as the video opens   # word index → start (Whisper places a few segment starts early)
    ),
    "intro-b": dict(
        title="Heavyweight Hills — intro B: the why",
        length=31.0,
        # voice: the Nov 9 re-record (Movember_4) + James saying the closing line (New Recording 10)
        cut=[("3220", 0.0, 1.65, 1.2),     # hook: the beard coming off, "So why bother?"
             ("MAP", 1.65, 1.95, 0.0),     # "Why do Movember?": every hill so far, pulling back from Mount Drury
             ("3269", 3.6, 2.4, 0.0),      # "Last year my uncle": the harbour, someone sitting alone
             ("3402", 6.0, 2.5, 0.3),      # "made the irreversible decision": the empty path at night
             ("3320", 8.5, 1.3, 0.0),      # "that ended up": branch over the surf
             ("3286", 9.8, 2.2, 0.5),      # "shattering both sides": the rain
             ("3292", 12.0, 1.3, 1.0),     # "of our family": night street
             ("3373", 13.3, 2.2, 0.6),     # "in the last three months": night road climb
             ("3377", 15.5, 2.4, 0.0),     # "I've lost two grandparents"
             ("3276", 17.9, 1.6, 0.2),     # "So for me, putting on": walking selfie in the vest
             ("3267", 19.5, 1.6, 0.85),    # "this vest": the vest in full view
             ("3246", 21.1, 1.8, 3.8),     # "is a sign of strength": summit selfie
             ("3265", 22.9, 1.4, 1.0),     # "There's always a way out": the steep path up
             ("3290", 24.3, 2.3, 0.95),    # "strong enough to ask": the wave
             ("3428", 26.6, 4.4, 1.3)],    # linger: the Mount at night, James says "Go on, look after yourself"
        map=dict(kind="all", at=1.65),
        chunks=("So why | *bother?* | Why do | *Movember?* | Last year | my *uncle* | made the | *irreversible* | "
                "decision | that ended up | *shattering* | both sides | of our *family,* | and in the | "
                "last three months, | I've lost two | *grandparents.* | So for me, | putting on | this *vest* | "
                "is a sign | of *strength.* | There's always | a way *out,* | and you need | to be *strong* | "
                "enough to *ask.*"),
        spoken_outro=59,   # words from here are James saying "Go on, look after yourself": the closing rows follow them
        fix={0: 0.35, 23: 13.35, 40: 21.1, 45: 23.05, 59: 27.05},
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
MIN_SHOW = 0.7     # s: no caption is up for less than this (0.45 s was too quick to read)
PHRASE_STAGGER = 0.07   # s between words as a phrase writes on
PHRASE_WRITE = 0.18     # s for a word's letters to fade in
WRITE_MAX = 0.3    # s: a word's letters are all in within this, so it reads as it is said


def captions(spec, words, fix):
    """Captions that track the voice: [(html, at, out)]. Phrasing and green words from the hand-made spec,
    timing from Whisper: each phrase arrives (whole) with its first spoken word and stays until the next phrase is
    spoken, never less than MIN_SHOW (James, Nov 9: one-word captions tied to fast speech flashed by too quickly)."""
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
        # the whole phrase writes on at once (a quick ripple across the words), so it can be read for its full time
        spans = [word_span(t, j * PHRASE_STAGGER, PHRASE_WRITE) for j, t in enumerate(part)]
        last_end = ws[-1][2]
        nxt = words[i][1] - 0.05 if i < len(words) else None
        if nxt is None or nxt - last_end > END_HOLD:
            out_t = last_end + END_HOLD      # a pause: hold, then clear
        else:
            out_t = max(nxt, at + MIN_SHOW)   # straight on: replaced as the next word is said
        free = out_t
        out.append((" ".join(spans), at, round(out_t, 2)))
    quick = [(round(o - a, 2), re.sub("<[^>]+>", "", h)) for h, a, o in out if o - a < MIN_SHOW - 0.01]
    assert not quick, f"captions on screen for less than {MIN_SHOW} s: {quick}"   # never again too quick to read
    return out


def build(name, cfg):
    d = HERE / name
    (d / "assets/map").mkdir(parents=True, exist_ok=True)
    (d / "assets/fonts").mkdir(parents=True, exist_ok=True)
    shutil.copytree(VENDOR, d / "vendor", dirs_exist_ok=True)
    for f in ("BebasNeue.woff2", "BebasNeue-OFL.txt", "Outfit-var.woff2", "Outfit-OFL.txt"):
        shutil.copy(FONTS / f, d / "assets/fonts" / f)
    shutil.copy(MAP_SRC / "land.png", d / "assets/map/land.png")
    shutil.copy(QR, d / "assets/qr.svg")
    clips = d / "assets/clips"
    if not clips.exists():
        clips.symlink_to("../../clips")

    words = json.loads((HERE / f"voiceover/words-{name}.json").read_text())
    for i in sorted(cfg.get("drop", []), reverse=True):   # Whisper ghosts (words that are not in the audio)
        del words[i]
    for i, start in cfg["fix"].items():
        words[i][1] = start
    cut_at = cfg.get("spoken_outro", len(words))
    caps = captions(cfg["chunks"], words[:cut_at], {})
    length, cut = cfg["length"], cfg["cut"]
    end_at = cut[-1][1]
    if not cfg.get("outro", True):   # no closing line: the last caption holds into the fade
        o_html = []
    elif "spoken_outro" in cfg:   # the closing line is in James's voice: each word appears as he says it
        spoken = words[cut_at:]
        outro_at = round(spoken[0][1] - 0.05, 2)
        o_html = [(w, s, min(WRITE_MAX, max(0.15, e - s))) for (w, *_), (_, s, e) in zip(OUTRO, spoken)]
    else:
        outro_at = end_at + 0.15
        o_html, t = [], outro_at
        for k, (w, gap, dur) in enumerate(OUTRO):
            t += gap
            o_html.append((w, t, dur))
    if o_html and caps and caps[-1][2] > outro_at:   # the last caption clears as the closing line starts
        caps[-1] = (caps[-1][0], caps[-1][1], outro_at)
        assert outro_at - caps[-1][1] >= MIN_SHOW - 0.01, f"{name}: last caption too quick before the closing line"
    if o_html:
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
    fx_html, fx_js, fx_windows = fx.build(cfg.get("fx", []), cut)
    tops, halo = dict(cfg.get("tops", {})), set()
    for i, (_, a, o) in enumerate(caps):
        clip = next((c for c, s, dd, _ in cut if s <= a + 0.05 < s + dd), None)
        if clip in HIGH_FACE:
            tops.setdefault(i, HIGH_FACE[clip])
        if any(c in LIGHT_BG and s < o and a < s + dd for c, s, dd, _ in cut) or any(s < o and a < e for s, e in fx_windows):
            halo.add(i)   # pale ground, or a busy hook underneath
    types = [f'  <div class="t h cap{" halo" if i in halo else ""}" id="c{i}" data-om-id="caption-{i}" '
             f'style="top:{tops.get(i, CAPTION_TOP)}px">{h}</div>'
             for i, (h, a, o) in enumerate(caps)]
    titles = [(f"c{i}", a, o) for i, (h, a, o) in enumerate(caps)]
    if o_html:
        types.append(f'  <div class="t h cap" id="o1" data-om-id="outro-1" style="top:{OUTRO_TOP}px">{row1}</div>')
        types.append(f'  <div class="t h cap" id="o2" data-om-id="outro-2" '
                     f'style="top:{OUTRO_TOP + OUTRO_LINE}px">{row2}</div>')
        titles += [("o1", outro_at, length), ("o2", row2_at, length)]
    elif titles:   # the last caption stays up to the end
        i, a, _ = titles[-1]
        titles[-1] = (i, a, length)
    titles_js = ", ".join(f"['{i}', {a}, {o}]" for i, a, o in titles)
    mp = cfg.get("map", dict(kind="none", at=-1))
    html = (HERE / "template.html").read_text()
    for k, v in {"TITLE": cfg["title"], "SHOTS": "\n".join(shots), "TYPES": "\n".join(types), "CUT_JS": cut_js,
                 "TITLES_JS": titles_js, "END": str(end_at), "END_DUR": str(round(length - end_at, 2)),
                 "FX_HTML": fx_html, "FX_JS": fx_js,
                 "LENGTH": str(length), "ENDCARD_DUR": str(cfg.get("endcard", ENDCARD)), "FADE_OUT": str(FADE_OUT), "LETTER_FADE": str(LETTER_FADE),
                 "MAP_KIND": mp["kind"], "MAP_AT": str(mp["at"]), "MAP_W": str(MAP["width_m"]),
                 "MAP_H": str(MAP["height_m"]),
                 "MAP_STYLE": ' style="visibility:visible"' if mp["at"] == 0 else "", "MAPJSON": json.dumps(MAP, separators=(",", ":"))}.items():
        html = html.replace("{{" + k + "}}", v)
    (d / "index.html").write_text(html)
    total = round(length + cfg.get("endcard", ENDCARD), 2)
    (d / "LENGTH").write_text(f"{total}\n")
    print(f"{name}: {len(caps)} captions, {len(cut)} shots, {total} s (end card from {length} s)")
    return caps


if __name__ == "__main__":
    for name, cfg in INTROS.items():
        build(name, cfg)
