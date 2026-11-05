# Brand font reference database

The display face James chose (Nov 2026) came from a Canva sample, `sample-source.jpg`. Its name is not yet known.
This folder holds a scan of every capital so any candidate font can be checked against it objectively.

| File | What it is |
|---|---|
| `glyphs/A.png` … `Z.png` | Each capital, scanned and cropped from the sample (25 letters; the sample has no **W**) |
| `glyph-sheet.png` | All scanned capitals on one sheet |
| `glyphs.json` | Per-letter measurements: width, height, aspect ratio, ink coverage, descent below baseline |
| `match-results.json` | Top 20 matches from all of Google Fonts, with a score for every letter |
| `match-sheet.png` | The sample above the six closest Google Fonts, letter by letter |
| `tools/` | Scripts to rescan, rematch and check new fonts (below) |

## The font's fingerprint

Use these traits to recognise it, or as search terms on font sites:

- **Floating crossbars.** The middle bars of **E**, **F** and **H** are separate wedge-shaped strokes that don't touch
  the left stem. This is the most distinctive trait.
- **A has a curved, sweeping crossbar** and a flared left leg.
- **Flared, tapering stems.** Strokes swell toward the ends and finish in pointed, wedge-like feet (no bracketed serifs).
- **Calligraphic diagonals.** The legs of **K** and **R** kick out and curl at the foot.
- **Q's tail** sweeps underneath and drops about 15% below the baseline. It is the only letter with a descender.
- **G** has a horizontal bar; **J** sits on the baseline with a hooked foot.
- **Heavy weight:** ink fills about 45–55% of each letter's bounding box. Caps-only in the sample; Canva fell back
  to a plain sans for the lowercase line, which suggests the display face is caps-only or its lowercase wasn't used.
- **Proportions:** generous, slightly wide caps; letter-spaced in the sample.

Good search terms: *"flared display font floating crossbar"*, *"tapered serif display caps"*, *"glyphic display
typeface"*. On Canva, open the sample text and read the font name in the font picker; that's the quickest route.

## What the search found

- All **1,529** Google Fonts families (every category except Handwriting and Monospace) were scored, heaviest weight.
- **No exact match.** A true match scores about **0.94**; the best Google font scored **0.71**. The font is almost
  certainly Canva-exclusive or commercial.
- Closest free relatives: **Averia Libre** 0.71, **Arima** 0.65, **Averia Sans Libre** 0.65, **Salsa** 0.64.
  They share the soft, flared feel but none have the floating crossbars.

How sure is the matcher? Four known fonts (Philosopher, Arima, Cinzel, Fraunces) were each rendered as a fake
"sample", and the matcher picked the right one as #1 of 1,529 every time.

## Checking a font you find

```sh
# one-time: a Python 3.10+ environment with the tools' dependencies
python -m venv .venv && .venv/bin/pip install pillow numpy scipy fonttools brotli
.venv/bin/python brand/fonts/reference/tools/check_font.py path/to/CandidateFont.otf
```

Accepts `.ttf`, `.otf`, `.woff` and `.woff2`. Variable fonts are tried at every weight and the best is reported.

| Score | Meaning |
|---|---|
| **≥ 0.88** | Very likely the brand font |
| 0.70 – 0.88 | Close relative |
| < 0.70 | Different design |

It also lists the five least-similar letters, a quick way to see *why* a near-miss isn't it.

## Rebuilding

- `tools/scan.py SAMPLE.jpg OUTDIR`: re-scan a new sample. It expects two rows, `A–N` then `O–Z` without W.
- `tools/fetch.py GF_METADATA.json OUTDIR`: download the Google Fonts catalogue
  (metadata from `https://fonts.google.com/metadata/fonts`).
- `tools/match.py INDEX.json GLYPHDIR LETTERS TOPN OUT.json [PREV.json]`: rank fonts.
- `tools/selftest.py FAMILY…`: confirm the matcher still identifies known fonts. Run it from a folder holding
  `gf/` from `fetch.py`.
