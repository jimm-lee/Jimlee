# House style (videos)

Use this for every video from now on, so they look designed rather than template-made.

| Element | Spec |
|---|---|
| Title typeface | **Merienda** Black (900), a cursive, calligraphic display face. SIL OFL 1.1: `fonts/Merienda-var.woff2`, licence `fonts/Merienda-OFL.txt` |
| Case | **CAPS** for big title words ("30 KG", "HEAVYWEIGHT HILLS", "UP."); **sentence case** for spoken lines ("Every hill around here"), where the cursive shows |
| Accent words | **#75FF78** green |
| Body / white | #FFFFFF; small credits #FFFFFF at 85% |
| Small labels | **Outfit** Medium (500), 36px, tracking 13px, caps (`fonts/Outfit-var.woff2`) |
| Shadow on all type | subtle, **down and to the right**: `4px 6px 0 rgba(0,0,0,.28), 6px 8px 12px rgba(0,0,0,.35)` |
| Legibility shade | top and bottom gradient behind type (see `--shade`) |
| Rule | 6px × 420px green bar with a soft offset shadow |
| Position | upper two-thirds; **nothing below y 1440**, and keep lower-half text left of x 960 |

> **Hero edits (Nov 2026):** James chose **Anton** caps for hero edits (white, #75FF78 on one word, same shadow),
> from a side-by-side of six faces (`projects/hero-edit/font-options.jpg`), and no colour grade on the footage.
> Merienda remains the face for other videos unless he says otherwise.

Sizes for 1080×1920: XL 180 (one word), L 130, M 96, S 68. Keep lines under ~880 px wide.
For 16:9, multiply by ~0.56.

`house-style.css` has all of it as CSS for huashu-motion compositions. In Concat, use the same values in a title's
style (font Merienda 900, colour #75FF78, a down-right drop shadow).

How it was chosen: James liked a Canva font called "Para" (scanned in `fonts/reference/`) and asked for something
a little more cursive in the same vein; Merienda won the side-by-side on footage. Also compared and declined:
Montserrat Bold/ExtraBold (cleaner and faster to read, but generic; James kept Merienda for its personal,
hand-drawn feel). Previous house style (until v13):
Outfit Light titles with an all-round shadow.

Use green on one or two key words per screen, not whole sentences.
Verified readable over grass, bright overcast sky and night street footage (Heavyweight Hills, Nov 2026).

> **Brand font reference:** the chosen display face (from a Canva sample, name not yet known) is scanned letter by
> letter in [`fonts/reference/`](fonts/reference/README.md), with its distinguishing traits and a checker that scores
> any font file against it. No exact match exists in Google Fonts; the closest free relatives are Averia Libre
> and Arima.

## Reels / Shorts / TikTok rules (1080×1920)

Distilled from a 2026 Instagram Reels captioning guide (from a captioning-tool vendor). The safe-zone figures are
Instagram's current UI, not ours. Re-check them on a real phone; the UI changes.

### Safe zone, the hard rule

| Area | Keep text out of |
|---|---|
| Bottom | **y > 1440** (bottom 480 px: like/comment buttons, caption, audio bar). Never below y 1520 |
| Right edge | **x > 960** (right 90–120 px: the action button column) |
| Default home for text | the **upper two-thirds** of the frame (y 200–1300) |

The QR code and anything to be read or scanned must sit fully inside the safe zone.

### Type

- **Weight:** Instagram's upload compression degrades thin strokes. Use Regular/Medium or heavier for anything
  that must be read; keep Light only for very large display words. (Hence Merienda Black for titles.)
- **Contrast treatment:** every line gets either a shadow/outline (about a 2 px dark stroke or a firm offset shadow)
  or a semi-transparent box. Plain text with no treatment fails on bright scenes and in Instagram's dark mode.
- **Typeface:** clean sans-serif with a high x-height. No script or decorative faces for anything read at speed.
- **Size:** about 60–75 px for caption-style lines (bold weights can sit at 60). Headlines go bigger, as in the
  scale above. Karaoke or word-by-word captions need a size step up and stronger contrast.
- **Alignment:** centre by default. It survives feed, grid, Explore and Stories crops.

### Copy and pacing

- **10 words or fewer** per on-screen block, **2 lines max**, and line height about 1.3× the font size for
  stacked caption lines.
- Split longer thoughts across sequential blocks; don't squeeze them into one line.
- End on a deliberate **2–3 s end screen**, never a hard cut on the last caption.
- On-screen text and the post's written caption are separate jobs. On-screen text carries the message for the
  many viewers who never unmute. The written caption carries the hook, context and searchable keywords. Don't
  duplicate one into the other.

### Captions workflow (what we already do)

1. Transcribe the voice-over (Whisper via VoiceStudio), checked against the script for names and numbers,
   e.g. "Movember", not "November".
2. Burn in only what the titles don't already say; export an `.srt` for upload as well.
3. Before publishing, **preview on a real phone** and confirm nothing important sits below y 1440 or right of x 960.

### Status of Heavyweight Hills v14 against these rules

| Rule | Status |
|---|---|
| Safe zone | ✅ All text above y 1440 (checked frame by frame with the zone overlaid); end card rearranged to finish at about y 1330 |
| Weight | ✅ Merienda Black titles |
| Contrast | ✅ Down-right shadow plus top/bottom shade |
| ≤ 10 words, ≤ 2 lines | ✅ |
| Centred | ✅ |
| End screen | ✅ About 6 s |

### Claims treated with caution

The guide also asserts that the 2026 algorithm "weighs" on-screen text and that Instagram runs OCR on it for search.
These are plausible but unverified vendor claims, so they don't drive any rule here; the practical rules above
stand on readability alone.
