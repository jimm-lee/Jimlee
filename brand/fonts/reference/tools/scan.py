"""Scan the reference sample: split the two capital rows into one glyph image per letter."""
import sys, json, numpy as np
from PIL import Image
from scipy import ndimage
src, out = sys.argv[1], sys.argv[2]
im = np.asarray(Image.open(src).convert("L"), dtype=np.float32)
ink = im < 128
rows = ink.sum(1) > 3
# find horizontal bands of ink (text rows)
bands, y = [], 0
while y < len(rows):
    if rows[y]:
        y0 = y
        while y < len(rows) and rows[y]: y += 1
        if y - y0 > 40: bands.append((y0, y))
    y += 1
letters = ["ABCDEFGHIJKLMN", "OPQRSTUVXYZ"]
meta = {}
for (y0, y1), labels in zip(bands[:2], letters):
    band = ink[y0:y1]
    cols = band.sum(0) > 0
    segs, x = [], 0
    while x < len(cols):
        if cols[x]:
            x0 = x
            while x < len(cols) and cols[x]: x += 1
            segs.append([x0, x])
        x += 1
    # merge tiny gaps (pieces of one letter)
    merged = []
    for s in segs:
        if merged and s[0] - merged[-1][1] < 4: merged[-1][1] = s[1]
        else: merged.append(s)
    print(f"row y{y0}-{y1}: {len(merged)} glyphs for {len(labels)} letters")
    for (x0, x1), ch in zip(merged, labels):
        g = band[:, x0:x1]
        ys = np.where(g.any(1))[0]
        g = g[ys.min():ys.max()+1]
        Image.fromarray((~g * 255).astype(np.uint8)).save(f"{out}/{ch}.png")
        h, w = g.shape
        meta[ch] = {"width": int(w), "height": int(h), "ink_ratio": round(float(g.mean()), 4),
                    "aspect_w_over_h": round(w / h, 4), "baseline_drop_px": int(y0 + ys.max() - (y1 - 1))}
json.dump({"source": "Canva sample supplied by James, Nov 2026", "rows": [list(b) for b in bands[:2]], "glyphs": meta}, open(f"{out}/glyphs.json", "w"), indent=1)
print("cap heights:", sorted(set(v["height"] for v in meta.values())))
