"""Ground-truth check: render a known font as a fake 'sample' and see if the matcher ranks it first."""
import json, sys, os, numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import match
idx = json.load(open("gf/index.json")); files = {i["family"]: i["file"] for i in idx}
letters = "AEGHKQRSMJ"
for truth in sys.argv[1:]:
    font, _ = match.load_font(files[truth])
    os.makedirs("fake", exist_ok=True)
    from PIL import ImageDraw
    for ch in letters:
        im = Image.new("L", (420, 360), 255); ImageDraw.Draw(im).text((40, 40), ch, font=font, fill=0)
        m = np.asarray(im) < 128; ys, xs = np.where(m)
        crop = im.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1)).resize((max(1,int((xs.max()-xs.min())*74/(ys.max()-ys.min()))), 74))
        crop.save(f"fake/{ch}.png")
    refs = {c: match.ref_glyph(c, "fake") for c in letters}
    import concurrent.futures as cf
    jobs = [(i["file"], letters, refs) for i in idx if i["file"]]
    res = []
    with cf.ProcessPoolExecutor(4) as ex:
        for it, per in zip([i for i in idx if i["file"]], ex.map(match.score_font, jobs, chunksize=8)):
            if per: res.append((np.mean(list(per.values())), it["family"]))
    res.sort(reverse=True); names = [n for _, n in res]
    print(f"truth={truth:18s} rank={names.index(truth)+1:4d} of {len(names)}   top3: {', '.join(names[:3])}")
