---
name: hero-edit
description: James's approved style and process for short vertical hero edits (10–15 s, 1080×1920) of his New Zealand life — caption-led montages with Bebas Neue captions that spell out letter by letter at speaking pace, a green accent word, no name card, and the closing line "Go on, look after yourself". Use whenever James asks for a hero edit, montage, reel or caption edit from his clips, or adds clips to the library.
---

# Hero edits (James's approved style, Nov 2026)

Working project: `projects/hero-edit/` (`build.py` = engine, `build_plans.py` = the ten caption edits, `clips/` =
edit copies, `COMPOSITIONS.md` = clip library and structures). Copies of the engine, template and plan file as
approved are in `assets/` here; start a new project from them if `projects/hero-edit/` is gone.
Renders with huashu-motion (`.claude/skills/huashu-motion/bin/om`). Brand file: `brand/README.md`.

## The look (locked: "use that going forward")

| Element | Spec |
|---|---|
| Frame | 1080×1920, 30 fps, **10 or 15 s max**, silent (James adds music) |
| Footage | **No grade.** iPhone HLG → SDR only: `zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv`; SDR clips untouched. **Real speed** (no slow-mo unless asked). No vignette, flashes or filters |
| Type | **Bebas Neue** caps, letter-spacing .035em, thickened with a 3 px same-colour `-webkit-text-stroke`, white |
| Accent | **One green word** (#75FF78) per caption line, **just the green + the shadow, no outline** (cherry and pastel-yellow outlines were tried and dropped) |
| Shadow | `4px 6px 0 rgba(0,0,0,.28), 6px 8px 12px rgba(0,0,0,.35)` on all type |
| Caption position | single row, `top: 520px` (upper third, not too high); no text below y 1440 |
| Ending | **No name card** (reads as forced promotion). Close on an open landscape with **"GO ON, / LOOK AFTER YOURSELF"** (*yourself* green), two stacked rows, fade to black |

## Captions (the part James cares most about)

- One hook line per edit, split with `|` into chunks of **2–3 words**, shown one chunk at a time on a single row.
- Each word **arrives as if read aloud** and **spells out letter by letter** across its whole spoken time:
  word time = 0.22 s + 0.06 s per letter (0.32–0.85 s), plus 0.2 s after `, : ;` and 0.3 s after `. ? !`;
  each letter fades in over 0.25 s. (Popping whole words in, and fast spelling, both read badly.)
- A chunk holds ~0.35 s after its last letter, then the **next chunk starts straight away — no gap** (a half-second
  pause loses attention).
- Closing line: row 2 starts writing as soon as row 1's last word is written; final shot is **4 s** so the full line
  holds about a second before a 0.6 s fade (anything shorter "fades too quickly to read").
- **Weighted-vest clips** (2524, 2153, 3225, 3266, 3276) only where training fits the caption; never in reflective
  or lifestyle edits ("it takes from the overall experience"). Prefer the sauna, beach, deck, races or ice for a vest-free you.
- Never put a caption over a face. If a clip with people sits under a caption, move the clip after the caption clears.
- Check every caption is readable on its background (white on white sky fails).

## Voice-led edits (James, Nov 2026)

When an edit carries James's voice-over (e.g. `projects/heavyweight-hills-hero/`), captions **track the voice**
instead of the hook-line pacing above:
- **1–2 words on screen at a time, 3 at most**, phrased by hand as natural groups ("Just because I | haven't *posted* it,").
- Each caption arrives with its first spoken word (Whisper word timings) and stays until the next one is said;
  never shorter than 0.45 s (the next waits a moment), and it holds 1.1 s at a pause. "They were jumping off the
  screen too quickly" when they cleared early.
- Letters still spell in, but fast: a word is complete within 0.3 s of being said.
- **Impact words green** (Movember, vest, Heavyweight Hills, uncle, grandparents, invisible, visible, alone…), at
  most one per caption; 124 px Bebas.

## Structure (five parts) and variety

15 s: hook 0–2.5 · connection 2.5–5.5 · build 5.5–9.5 (0.5 s cuts) · payoff 9.5–11 · linger 11–15.
10 s: hook 0–2 · connection 2–3 · build 3–5 · payoff 5–6 · linger 6–10.
- **Hook**: an unexpected image under the first caption chunk (geyser, ice plunge, jellyfish, motorway…).
- **Opening spiral** (James, Nov 2026): before the hook lands, every clip in the edit flashes by for **3 frames**
  (the last three for 4: "slowed by the smallest margin so you get the essence of it"), turning from 32° to level
  and zooming to cover the frame, landing on the hook shot (~0.9 s for 8 clips, ~1.4 s for 13). The first caption
  starts as it lands, which pushes captions later: re-check that the last chunk doesn't land on the payoff's faces.
  `render(..., spiral=True)`.
- Alternate close/wide, still/moving, dark/light, alone/with people.
- **Don't repeat clips in a similar order across a series**: each edit has its own hook, payoff and linger shot;
  a clip appears in at most two edits and never next to the same shot twice. `build_plans.py` prints a variety
  report on every build — keep it at "none / none / none".

## Grid framework (from James's DaVinci reference, Nov 2026; built; use on some edits only, see TECHNIQUES.md)

Plan key `fx=[...]` in `build_plans.py` (engine: `build.build_fx`):
- `dict(kind="grid", shot=i | "last", cols, rows, frames=2, order="random"|"stair")`: **crop to grid,
  duplicate clips & offset**. The shot's clip is duplicated into cells (each 0.08 s out of sync) that pop in on black,
  one every `frames`, then the full shot takes over. `shot="last", cols=2, rows=2, order="stair"` = **crop flash**
  into the linger.
  Add `spin=True` (James, Nov 2026): once every cell is in, the grid holds 0.15 s, then **circles and spirals into
  the centre** (turns 300°, shrinks) while the full clip spirals out of it (from -240°, tiny, to full) over 0.6 s.
- `dict(kind="collage", at, dur, cols, rows, frames=3, clips=[(clip, media)...])`: **resized clips fit to grid**.
  Different clips pop into a collage one by one (stair step); leave that time empty in `cut`.
- `dict(kind="flash", at)`: two frames of white (55 %) on a grid transition. Keep to grid moments only.
- Captions stay letter by letter (no text flicker); edits stay silent (sound design is James's).
- Grid builds push nothing later, but re-check captions against the payoff: move a shot rather than cover a face.

## Technique library: pull only when it fits

`TECHNIQUES.md` lists 22 graphic editing methods in the same vein (grid, collage, crop flash, split screen, echo
trail, photo stack, film strip, freeze frame, zoom-through, nested frame, iris, blinds, mirror, match cut…), each with
**when to use it, when not to, and whether it's built**, plus a caption-to-technique table and picks for the
remaining edits. James's rule: **only some edits get a signature technique**. Give an edit at most one or two, never
the same one in consecutive edits, and default to clean beat cuts. Read `TECHNIQUES.md` when planning each edit; build
an "easy" technique into the engine only when an edit calls for it, then mark it built there.

## Process (one at a time, properly)

1. New clips: contact sheet (4–6 frames each), note content, convert to `clips/NNNN.mp4` (HLG → SDR as above,
   `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920`), add to `COMPOSITIONS.md`.
2. Plan in `build_plans.py`; run it; variety report clean; `om check` 0 errors.
3. `om still` at each caption chunk, mid-word, the build, payoff and the closing line; **look** for faces under
   captions, unreadable backgrounds, captions running into the payoff or the closing line.
4. Render one edit (`om render <dir> --silent`), re-encode to exact length (`-t 10|15`, x264 crf 16), `om qa`
   (no pops, no dead stretch), frame strip every 0.5 s.
5. Commit to the branch (never the `.om/` cache or `out/`; clear `.om/cache` after rendering — it is huge),
   send the video, wait for James before the next one.

Show stills before rendering when planning something new. Ask James for shots the library lacks (a real leap,
Ireland footage, close human details) rather than faking them.
