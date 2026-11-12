# Carousels (Nov 2026)

Turns photos into Instagram carousel slides (1080×1350, 4:5) in the house style from `brand/`: Merienda titles,
#75FF78 green on key words, Outfit labels, the subtle down-right shadow, and a slide counter.

```sh
node render.mjs specs/demo-heavyweight-hills.json     # -> out/demo-heavyweight-hills/01.png … + preview-strip.png
npm test                                              # 9 tests, no browser needed
```

Needs Node ≥ 18 and Playwright (`npm install` here, or a global install).

## Writing a carousel

A spec is a JSON file listing slides. Image paths are relative to the spec. Words between `*asterisks*` go green, a
new line (`\n`) breaks the line, and `"position": "top" | "centre" | "bottom"` moves the text off a face.
`"focus": "50% 30%"` chooses which part of the photo stays in the crop.

| Layout | Use it for | Fields |
|---|---|---|
| `cover` | Slide 1: the hook. Adds "Swipe →" | `image`, `title`, `kicker`, `line` |
| `photo` | A strong photo with one short line | `image`, `line`, `kicker` |
| `stat` | One big number over a darkened photo | `image`, `value`, `line`, `kicker` |
| `pair` | Two photos stacked: before/after, day/night, then/now | `images` (two), `line`, `kicker` |
| `pano` | One wide photo spread across 2–5 slides so the swipe pans across it | `image`, `span`, `line` (first slice only), `focusY` |
| `words` | A thought or a quote over a blurred photo (or plain dark) | `line`, `small`, `image`, `kicker` |
| `ask` | The call to action: sponsor, follow, come to the fight | `title`, `line`, `link`, `image` (blurred) |

Instagram allows up to 20 slides; 6–10 is the sweet spot. Put the caption you'll post in the spec's `caption`
so it lives with the slides.

## DSLR photos

Export JPEGs (RAW files are refused with a message). Full-size JPEGs are fine. Keep the best ~20 per
carousel idea in a folder next to its spec, e.g. `photos/fight-camp/`. Raw photos are not committed (`.gitignore`), so
copy them into `photos/` locally.

The demo uses stills cropped from the Heavyweight Hills videos (`demo-photos/`), so it's softer than DSLR photos will be.

## Carousel ideas for these photos

**Heavyweight Hills (Movember)**
1. **Halfway up** (the demo): cover → the steep face → a summit number → day/night pair → why → sponsor ask.
2. **What 30 kg looks like**: the vest on a scale, then everyday things that weigh 30 kg (a 6-year-old, three
   bags of dog food, a full suitcase), ending on "now carry it up a hill" and the ask.
3. **One hill, every hour**: a `pano` of the hill or the view across 3 slides, then the same spot at dawn, midday,
   rain and night with `pair` slides.
4. **The mo, week by week**: four close-ups from clean shaven to now, a stat ("days to go"), and the ask.

**Fight camp**
1. **Three weeks out**: cover (hands wrapped) → what a training day looks like (`photo` × 3) → the hills as
   conditioning → "[date] · [venue]" on an `ask` slide.
2. **The details**: wraps, gloves, mouthguard, the scale, the corner: close-ups that DSLR depth of field is made
   for, each with one line on why it matters.
3. **Why I fight**: one `words` slide per honest answer, over blurred training shots, ending on a portrait.
4. **Fight week countdown**: one `stat` per day (7, 6, 5 … 1) with what happens that day.
