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
