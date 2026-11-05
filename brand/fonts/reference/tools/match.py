"""Score fonts against scanned reference glyphs (shape overlap + proportions + weight)."""
import io, json, sys, string, numpy as np, concurrent.futures as cf
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from scipy import ndimage
N = 64
def norm(mask):
    ys, xs = np.where(mask)
    m = mask[ys.min():ys.max()+1, xs.min():xs.max()+1]
    h, w = m.shape; s = N / max(h, w)
    im = Image.fromarray((m * 255).astype(np.uint8)).resize((max(1, round(w*s)), max(1, round(h*s))), Image.LANCZOS)
    c = np.zeros((N, N), np.float32); a = np.asarray(im, np.float32) / 255
    y0, x0 = (N - a.shape[0]) // 2, (N - a.shape[1]) // 2
    c[y0:y0+a.shape[0], x0:x0+a.shape[1]] = a
    return c, w / h, float(m.mean())
def ref_glyph(ch, refdir):
    m = np.asarray(Image.open(f"{refdir}/{ch}.png").convert("L")) < 128
    return norm(m)
def weight_range(path):
    """(min, max) of the wght axis for a variable font, else None."""
    tt = TTFont(path)
    for a in (tt["fvar"].axes if "fvar" in tt else []):
        if a.axisTag == "wght": return (a.minValue, a.maxValue)
    return None
def load_font(path, wght=None):
    tt = TTFont(path); tt.flavor = None
    if wght is not None and "fvar" in tt:
        from fontTools.varLib import instancer
        tt = instancer.instantiateVariableFont(tt, {"wght": wght})
    buf = io.BytesIO(); tt.save(buf); buf.seek(0)
    cmap = tt.getBestCmap() or {}
    return ImageFont.truetype(buf, 200), cmap
def render(font, ch):
    im = Image.new("L", (420, 360), 0); ImageDraw.Draw(im).text((40, 40), ch, font=font, fill=255)
    m = np.asarray(im) > 127
    return norm(m) if m.any() else None
def stroke(a):
    m = a > 0.5
    if not m.any(): return 1e-3
    dt = ndimage.distance_transform_edt(m)
    return float(np.percentile(dt[m], 90))
def score(r, g):
    (ra, rasp, rink), (ga, gasp, gink) = r, g
    rm, gm = ra > 0.5, ga > 0.5
    iou = (rm & gm).sum() / ((rm | gm).sum() + 1e-9)
    # chamfer-style outline agreement: mean distance between the two shapes' edges
    re_, ge_ = rm ^ ndimage.binary_erosion(rm), gm ^ ndimage.binary_erosion(gm)
    if not re_.any() or not ge_.any(): return -1
    d1 = ndimage.distance_transform_edt(~ge_)[re_].mean(); d2 = ndimage.distance_transform_edt(~re_)[ge_].mean()
    edge = 1 - min(1, (d1 + d2) / 2 / 6)
    asp = abs(np.log(gasp / rasp)); wt = abs(np.log((gink + 1e-3) / (rink + 1e-3))); st = abs(np.log(stroke(ga) / stroke(ra)))
    return 0.45 * iou + 0.55 * edge - 0.6 * asp - 0.6 * wt - 0.4 * st
def score_font(args):
    path, letters, refs = args[:3]
    wght = args[3] if len(args) > 3 else None
    try:
        font, cmap = load_font(path, wght)
        per = {}
        for ch in letters:
            if ord(ch) not in cmap: return None
            g = render(font, ch)
            if g is None: return None
            per[ch] = round(float(score(refs[ch], g)), 4)
        return per
    except Exception:
        return None
if __name__ == "__main__":
    index, refdir, letters, top, out = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
    items = json.load(open(index))
    if len(sys.argv) > 6:  # restrict to families from a previous round
        keep = set(json.load(open(sys.argv[6]))["ranking_families"]); items = [i for i in items if i["family"] in keep]
    refs = {c: ref_glyph(c, refdir) for c in letters}
    jobs = [(i["file"], letters, refs) for i in items if i["file"]]
    res = []
    with cf.ProcessPoolExecutor(4) as ex:
        for it, per in zip([i for i in items if i["file"]], ex.map(score_font, jobs, chunksize=8)):
            if per: res.append({"family": it["family"], "category": it["category"], "score": round(float(np.mean(list(per.values()))), 4), "per_letter": per})
    res.sort(key=lambda r: -r["score"])
    json.dump({"letters": letters, "scored": len(res), "ranking": res[:top], "ranking_families": [r["family"] for r in res[:top]]}, open(out, "w"), indent=1)
    print(f"scored {len(res)} fonts on {len(letters)} letters; top {min(10,top)}:")
    for r in res[:10]: print(f"  {r['score']:.3f}  {r['family']}  ({r['category']})")
