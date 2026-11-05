# House style (videos)

Use this for every video from now on, so they look designed rather than template-made.

| Element | Spec |
|---|---|
| Typeface | **Outfit** (variable, 100–900), SIL OFL 1.1 — `fonts/Outfit-var.woff2`, licence in `fonts/Outfit-OFL.txt` |
| Headlines | Outfit **Light (300)**, uppercase, letter-spacing −2px, line-height 0.98 |
| Accent words | **#75FF78** green, Outfit **Regular (400)** (one step heavier than white so it holds over grass) |
| Body / white | #FFFFFF; small credits #FFFFFF at 85% |
| Kicker | Outfit Medium (500), 36px, tracking 13px, uppercase |
| Shadow on all type | `0 1px 1px rgba(0,0,0,.45), 0 3px 6px rgba(0,0,0,.45), 0 10px 30px rgba(0,0,0,.45)` |
| Legibility shade | top and bottom gradient behind type (see `--shade`) |
| Rule | 6px × 420px green bar with a soft shadow |

Sizes for 1080×1920: XL 210 (one word), L 140, M 104, S 72. Keep any headline line inside ~90% of the frame width.
For 16:9, multiply by ~0.56.

`house-style.css` has all of it as CSS for huashu-motion compositions. In Concat, use the same values in a title's
style (font Outfit, weight 300/400, colour #75FF78, drop shadow).

Use green on one or two key words per screen, not whole sentences.
Verified readable over grass, bright overcast sky and night street footage (Heavyweight Hills, Nov 2026).

> **Pending:** James is choosing a new, slightly heavier typeface, with a subtle shadow offset down and to the
> right. The Outfit Light spec above stays until it's swapped in.

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
  that must be read; keep Light only for very large display words. This is why the house face is moving heavier.
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

### Status of Heavyweight Hills v13 against these rules

| Rule | Status |
|---|---|
| Safe zone | ❌ Six moments sit low in the frame, inside the bottom 480 px: "THIS MOVEMBER…" (y 1380–1654), "UP." / "DOWN." / "REPEAT." (1350–1555), "EVERY HILL AROUND HERE" (1420–1623), "ALL MOVEMBER LONG." (1420–1624). Also the end card's "SCAN TO DONATE", link and name (y 1430–1680). The QR code (y 820–1400) is clear. |
| Weight | ⚠️ Outfit Light is thinner than recommended; being replaced. |
| Contrast | ✅ Layered shadow plus top/bottom shade on every line. |
| ≤ 10 words, ≤ 2 lines | ✅ Every block. |
| Centred | ✅ |
| End screen | ✅ About 6 s, longer than the minimum. Good for scanning the QR. |

Fix with the font change: lift low titles to about y 1150–1300 and move the end-card text block up so it ends
above y 1440.

### Claims treated with caution

The guide also asserts that the 2026 algorithm "weighs" on-screen text and that Instagram runs OCR on it for search.
These are plausible but unverified vendor claims, so they don't drive any rule here; the practical rules above
stand on readability alone.
