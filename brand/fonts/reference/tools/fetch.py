"""Download the heaviest latin weight of every candidate Google Fonts family (woff2)."""
import json, re, sys, urllib.parse, urllib.request, concurrent.futures as cf, os
meta, out = sys.argv[1], sys.argv[2]
t = open(meta).read(); d = json.loads(t[t.index("{"):])
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
fams = [f for f in d["familyMetadataList"]
        if f.get("category") not in ("Handwriting", "Monospace")
        and "latin" in f.get("subsets", []) and any(k.isdigit() for k in f.get("fonts", {}))]
def get(f):
    name = f["family"]; fn = os.path.join(out, re.sub(r"\W", "", name) + ".woff2")
    if os.path.exists(fn): return name, fn, None
    w = max(int(k) for k in f["fonts"] if k.isdigit())
    url = "https://fonts.googleapis.com/css2?family=" + urllib.parse.quote(name) + f":wght@{w}&display=swap"
    try:
        css = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode()
        src = None
        for sub, body in re.findall(r"/\*\s*([\w-]+)\s*\*/\s*@font-face\s*\{([^}]*)\}", css):
            if sub == "latin": src = re.search(r"url\(([^)]+)\)", body).group(1)
        src = src or re.search(r"url\(([^)]+)\)", css).group(1)
        open(fn, "wb").write(urllib.request.urlopen(urllib.request.Request(src, headers=UA), timeout=30).read())
        return name, fn, w
    except Exception as e:
        return name, None, str(e)[:60]
res = []
with cf.ThreadPoolExecutor(16) as ex:
    for name, fn, info in ex.map(get, fams):
        res.append({"family": name, "file": fn, "info": info, "category": next(f["category"] for f in fams if f["family"] == name)})
json.dump(res, open(os.path.join(out, "index.json"), "w"))
ok = [r for r in res if r["file"]]
print(len(fams), "families,", len(ok), "downloaded,", len(res) - len(ok), "failed")
