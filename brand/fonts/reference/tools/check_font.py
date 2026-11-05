"""Score any font file (.ttf/.otf/.woff/.woff2) against the brand reference glyphs.

    python check_font.py path/to/Font.otf [more fonts...]

A true match scores about 0.94 (verified by self-tests). The best Google Fonts candidate scored 0.71.
"""
import os, sys, string, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import match
HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "glyphs")
LETTERS = "".join(c for c in string.ascii_uppercase if c != "W")
refs = {c: match.ref_glyph(c, REF) for c in LETTERS}
for path in sys.argv[1:]:
    rng = match.weight_range(path)
    weights = [None] if not rng else sorted({w for w in (100,200,300,400,500,600,700,800,900) if rng[0] <= w <= rng[1]} | {rng[1]})
    best = None
    for w in weights:
        p = match.score_font((path, LETTERS, refs, w))
        if p and (best is None or np.mean(list(p.values())) > np.mean(list(best[1].values()))): best = (w, p)
    per = best[1] if best else None
    if rng: print(f"{os.path.basename(path)}: variable font, weights {rng[0]:g}-{rng[1]:g}; best at {best[0] if best else '?'}")
    if not per:
        print(f"{os.path.basename(path)}: could not score (missing capitals or unreadable file)"); continue
    s = float(np.mean(list(per.values())))
    verdict = "very likely THE brand font" if s >= 0.88 else "close relative" if s >= 0.70 else "different design"
    worst = sorted(per.items(), key=lambda kv: kv[1])[:5]
    print(f"{os.path.basename(path)}: {s:.3f}  -> {verdict}")
    print("   least similar letters:", ", ".join(f"{c} {v:.2f}" for c, v in worst))
