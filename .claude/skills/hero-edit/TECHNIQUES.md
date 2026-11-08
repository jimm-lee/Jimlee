# Technique library: when to reach for what

Graphic, layout-driven editing methods in the same vein as the grid framework (James's DaVinci reference, Nov 2026).
**Pull them only when they fit.** An edit gets the house basics (opening spiral, letter-by-letter captions, closing
line) plus **at most one or two signature techniques**, and a signature technique is not repeated in consecutive
edits of a series. Plain hard cuts on the beat are the default; a technique has to earn its place.

Status: **built** = in the engine (`build.py` / `template.html`, plan keys in `build_plans.py`);
**easy** = post-only, buildable from existing clips in a few lines; **shoot** = needs footage filmed for it.

## Choosing quickly

| Caption / mood | Reach for | Avoid |
|---|---|---|
| Lists, abundance ("camera roll", "not on Instagram", "a little look") | fit-to-grid collage, film strip, photo stack | slow fades |
| Memory, time passing ("three years", "memories") | photo stack, film strip, freeze frame | flashes, echo trails |
| Contrast, before/after ("routine", "putting off", "Ireland to NZ", "comfort zone") | split screen, crop to grid + spin, crop flash | mirror |
| Distance, journey ("18,000km", "other side of the world") | zoom-through / nested frame, match cut | blinds |
| Stillness, reflection ("getting lost", "finding yourself") | luma / soft fade, shape-mask iris, mirror (lightly) | grids, flashes, echo |
| Energy, effort, a leap ("took the leap", "comfort zone") | freeze frame on the peak, echo trail, speed ramp (fast to real), crop flash | luma fade |

## The techniques

### Built

1. **Opening spiral** (built, every edit). Every clip flashes by, 3 frames each, turning from 32° to level, landing on
   the hook. *Use*: always; it's the house hook. *Watch*: it pushes captions later, so check the payoff for faces.
2. **Crop to grid, duplicate clips and offset** (built: `kind="grid"`). One clip cut into cells that pop in on
   black, each copy slightly out of sync, then the full shot takes over. Add `spin=True` and the finished grid circles
   and spirals into the full clip. *Use*: the connection, on one strong still or slow shot (a sauna, a landscape)
   that deserves an arrival. *Avoid*: fast motion (the offset reads as a glitch), faces under the caption row.
3. **Resized clips fit to grid, a collage** (built: `kind="collage"`). Several clips pop into a 2×3 or 3×3 grid in a
   stair step. *Use*: the build, when the caption is about variety or abundance. Pick clips with different colours,
   so the cells read as separate. *Avoid*: more than once per edit; captions over busy gutters (keep it to one chunk).
4. **Crop flash** (built: `kind="grid", shot="last", cols=2, rows=2, order="stair"`). The shot arrives quarter by
   quarter. *Use*: into the linger or payoff, as a reveal. *Avoid*: on the hook (the spiral already does this job).
5. **Flash frames** (built: `kind="flash"`). Two frames of 55 % white. *Use*: only on grid transitions. *Avoid*:
   everywhere else (James found filters and flashes distracting).

### Easy to add (post-only, from the existing library)

6. **Split screen** (built, top/bottom: `kind="split", a=(clip, media), into=i, dur=0.8`; B slides up beside A, holds, then fills the frame; masks + transforms only; first used on #7) (2 or 3 vertical or horizontal panels, one clip each, sliding in). *Use*: contrast captions: the
   motorway beside the coast ("routine"), the abandoned car beside the open paddock ("putting it off"), the Irish
   jerseys beside the NZ landscape ("Ireland to New Zealand"). Hold 1–1.5 s, then the winning panel expands to fill.
7. **Echo / stack trail** (duplicates of a moving clip, offset 2–3 frames, fading copies behind). The grid's "duplicate
   & offset" idea applied to motion. *Use*: one movement payoff (dune run, beach run, deck spin, dragon boats) at the
   energy peak. *Avoid*: still shots (nothing to trail), and more than ~0.5 s.
8. **Photo stack / Polaroid drop** (built: `kind="stack", at, dur, clips=[...]`; first used on #6) (frames drop in as white-bordered cards, slightly rotated, piling up, then the top
   card scales to full screen). *Use*: memory captions: "three years", "camera roll full of memories", "not
   everything makes it onto Instagram". Feels personal, like flicking through prints.
9. **Film strip scroll** (a vertical strip of frames scrolls up, slows, and the centre frame expands to full).
   *Use*: "my camera roll" taken literally; a strong build alternative to the collage. *Avoid*: in the same edit as
   the photo stack.
10. **Freeze frame and stutter** (hold the peak frame for 0.3–0.6 s, optionally stepping 2–3 held frames).
    *Use*: the peak of an action: the splash in the ice bath on "LEAP", the wave crashing, the face pop in #10. The
    held frame gives a caption word room to land. *Watch*: blurry peaks look soft frozen, so pick a sharp frame.
11. **Zoom-through / punch-in** (built: `kind="zoom", into=i`, the payoff index; first used on #7) (end of clip A scales up fast into clip B, which settles from slightly large).
    *Use*: between build shots for momentum, or into the payoff. Replaces a hard cut once or twice, not every cut.
12. **Nested frame / infinite zoom** (the next clip appears small, framed inside the current one, then scales to
    fill; can chain 2–3). *Use*: distance and journey: "18,000km from home", "other side of the world". *Avoid*: with
    the spiral right after it (two zooms in a row).
13. **Shape-mask iris** (built: `kind="iris", shot="last", dur=0.8, x=50, y=44`; first used on #5) (a circle or rounded rectangle opens from a point, often the sun or a face, to reveal the
    next clip). *Use*: soft reveals into the linger: an iris opening from the sun in 2636 / 2603 / 9619 sunrises.
    Calmer than the crop flash; suits reflective captions.
14. **Blinds / strip wipe** (5–7 vertical strips slide in, staggered). A calmer cousin of the grid. *Use*: section
    changes in a measured edit (connection to build). *Avoid*: in an edit that already has a grid.
15. **Mirror / kaleidoscope split** (built as a left-right mirror: `kind="mirror", shot=0, at="land", dur=0.9`; first used on #5) (the frame mirrored left-right or into four). *Use*: sparingly, for disorientation:
    "getting lost", the hook of "putting it off". 0.5–1 s, then snap to normal. *Avoid*: with faces (looks odd).
16. **Luma / soft fade** (brightness-led dissolve). *Use*: the slow edits only (stillness, reflection) and time
    passing. *Avoid*: energetic edits, where it kills pace.
17. **Speed ramp, fast to real** (2–3× into real speed as the moment lands). *Use*: entering a payoff with motion.
    **No slow-motion unless James asks** (he didn't want the dune run slowed).
18. **Match cut** (planning, not an effect: cut between shots that share a shape, colour or motion, like sun to sun,
    water to water, or a path to a path). *Use*: anywhere, for free; especially payoff to linger
    (e.g. the sunset on the deck to the sunrise over the sea).
19. **Spin transition** (the motion of a spinning clip, such as 0389 on the deck, carried into the next clip by
    rotating it the same way). *Use*: high-energy edits, once. *Avoid*: right after the opening spiral.

23. **Impact frame** (built: `kind="impact", shot=0, at=0.0, looks=["invert","mono","invert","mono"], shake=0.3`;
    first used on #6, as the intro instead of the spiral). Anime-style hit: four single frames of the shot as stark
    high-contrast mono / inverted, then colour snaps back with a 0.3 s screen shake. *Use*: to open an edit with a
    punch, especially on a bold silhouette (a flag, a skyline, a figure against sky); or on one hard moment (the
    splash, a wave). *Avoid*: with the spiral in the same intro (pick one); on soft, low-contrast shots (mono turns to
    mush); more than once per edit. *Note*: `om qa` reports the single frames as "pops"; that's intended.

### Needs shooting (add to the shot list, not fakeable well)

20. **Whip pan** (fast pan blur hides the cut; film the out-pan and the in-pan in the same direction).
21. **Swipe / mask transition** (a hand or object covers the lens, and the next shot starts uncovered).
22. **Text behind subject** (caption sits behind a person or landmark): needs a clean subject mask; skip unless the
    shot has a simple silhouette against sky.

## Suggested picks for the remaining caption edits

| # | Caption | Signature technique(s) |
|---|---|---|
| 4 | Turns out, there's a lot of life outside your comfort zone | crop to grid + spin, collage, crop flash (built) |
| 5 | Somewhere between getting lost and finding yourself | mirror on the hook (lightly), shape-mask iris into the linger, soft fades. No grid |
| 6 | Three years, one big decision, and a camera roll full of memories | photo stack in the build, freeze frame on the payoff |
| 7 | What happens when you stop putting off the life you've imagined? | split screen (abandoned car beside the open paddock), zoom-through into the payoff |
| 8 | Ireland to New Zealand. A decision I'll never regret | nested-frame zoom (the distance), match cut into the linger |
| 9 | A reminder that there's a whole world waiting outside your routine | split screen (motorway beside the world), crop flash |
| 10 | Not everything makes it onto Instagram. Here's a little of it | freeze frame on the face pop, film strip scroll |

Sources consulted (Nov 2026): vidpros "Best transitions for short-form videos"; Insta360 "How to create film
transitions"; Nikon "10 tricks to add pace and energy"; Motion Array / DaVinci Resolve Club split-screen guides;
Opus Pro "11 editing aesthetics dominating short-form in 2026"; HitFilm stutter docs. Grid techniques: James's
DaVinci timeline reference.

## Used so far

| # | Signature techniques |
|---|---|
| 1–3 | none (spiral + clean cuts) |
| 4 | crop to grid + spin, collage, crop flash, flashes |
| 5 | mirror on the hook, iris into the linger |
| 6 | impact frame intro (no spiral), photo stack in the build |
| 7 | split screen in the connection, zoom-through into the payoff |
