"""Merge an Overpass extract and OSM API tiles into one SVG-ready map with three routes."""
import json, math, sys, glob
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw
D = sys.argv[1]
S, W_, N, E = -37.705, 176.150, -37.612, 176.215
LAT0 = math.radians((S + N) / 2); MX = 111320 * math.cos(LAT0); MY = 110574
WIDTH_M = (E - W_) * MX; HEIGHT_M = (N - S) * MY
def xy(lat, lon): return ((lon - W_) * MX, (N - lat) * MY)
ways = {}
for e in json.load(open(f"{D}/mount.json"))["elements"]:
    if e["type"] == "way" and e.get("geometry"): ways[e["id"]] = {"tags": e.get("tags", {}), "g": [(p["lat"], p["lon"]) for p in e["geometry"]]}
    if e["type"] == "relation":
        for m in e.get("members", []):
            if m.get("geometry") and m.get("role") in ("outer", ""):
                ways[f"r{e['id']}_{len(ways)}"] = {"tags": e.get("tags", {}), "g": [(p["lat"], p["lon"]) for p in m["geometry"]]}
for f in sorted(glob.glob(f"{D}/tile_*.osm")) + [f"{D}/ave_area.osm"]:
    root = ET.parse(f).getroot()
    nodes = {n.get("id"): (float(n.get("lat")), float(n.get("lon"))) for n in root.iter("node")}
    for w in root.iter("way"):
        i = int(w.get("id"))
        if i in ways: continue
        g = [nodes[nd.get("ref")] for nd in w.iter("nd") if nd.get("ref") in nodes]
        if len(g) > 1: ways[i] = {"tags": {t.get("k"): t.get("v") for t in w.iter("tag")}, "g": g}
def path(g, close=False):
    s = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (xy(*p) for p in g)); return s + ("Z" if close else "")
# land raster by flood-filling the sea from known sea points
R = 0.5; Wpx, Hpx = int(WIDTH_M * R), int(HEIGHT_M * R)
img = Image.new("L", (Wpx, Hpx), 255); dr = ImageDraw.Draw(img)
for w in ways.values():
    if w["tags"].get("natural") == "coastline": dr.line([tuple(c * R for c in xy(*p)) for p in w["g"]], fill=0, width=3)
for la, lo in [(-37.615, 176.212), (-37.640, 176.212), (-37.645, 176.152), (-37.668, 176.152), (-37.615, 176.152), (-37.625, 176.158), (-37.690, 176.178), (-37.680, 176.172)]:
    x, y = (int(c * R) for c in xy(la, lo))
    if 0 <= x < Wpx and 0 <= y < Hpx and img.getpixel((x, y)) == 255: ImageDraw.floodfill(img, (x, y), 128)
land = img.point(lambda v: 255 if v != 128 else 0); land.save(f"{D}/land_mask.png")
L = {k: [] for k in ("parks", "woods", "beaches", "coast", "roads_major", "roads_minor", "paths")}
for w in ways.values():
    t, g = w["tags"], w["g"]
    if t.get("leisure") == "park" and g[0] == g[-1]: L["parks"].append(path(g, True))
    elif t.get("natural") in ("wood", "scrub") and g[0] == g[-1]: L["woods"].append(path(g, True))
    elif t.get("natural") == "beach" and g[0] == g[-1]: L["beaches"].append(path(g, True))
    elif t.get("natural") == "coastline": L["coast"].append(path(g))
    elif "highway" in t:
        h = t["highway"]
        if h in ("motorway", "trunk", "primary", "secondary", "tertiary", "motorway_link", "trunk_link", "primary_link", "secondary_link"): L["roads_major"].append(path(g))
        elif h in ("residential", "unclassified", "service", "living_street", "road"): L["roads_minor"].append(path(g))
        elif h in ("footway", "path", "steps", "track", "pedestrian", "cycleway"): L["paths"].append(path(g))
def P(i, rev=False): g = ways[i]["g"]; return g[::-1] if rev else g
# Day 3: Third Avenue from the harbour end up to the crest (~16.7 m, NZ 8 m DEM)
ave = P(28502068, rev=True); crest = min(range(len(ave)), key=lambda k: (ave[k][0] + 37.68930) ** 2 + (ave[k][1] - 176.16255) ** 2)
ave = ave[:crest + 1]
# Day 4: usual track (north entrance -> summit) and the steeper north-east face
drury = P(574736364, rev=True)
steep = [(-37.63410, 176.18395)] + P(574736365) + [drury[-1]]
reserve = next(w for w in ways.values() if w["tags"].get("name") == "Mount Drury Reserve")
rt = lambda g: "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (xy(*p) for p in g))
out = dict(width_m=WIDTH_M, height_m=HEIGHT_M, **L, reserve=path(reserve["g"], True),
           route_ave=rt(ave), route_drury=rt(drury), route_steep=rt(steep),
           ave_mid=xy(*ave[len(ave) // 2]), ave_end=xy(*ave[0]), ave_crest=xy(*ave[-1]),
           drury=xy(-37.63446, 176.18300), lbl_tauranga=xy(-37.6995, 176.1585), lbl_mount=xy(-37.6470, 176.1900),
           lbl_mauao=xy(-37.6318, 176.1693))
json.dump(out, open(f"{D}/map.json", "w"))
print(f"{WIDTH_M:.0f}x{HEIGHT_M:.0f} m; ways {len(ways)}; " + ", ".join(f"{k} {len(v)}" for k, v in L.items()) + f"; ave route {len(ave)} pts, drury {len(drury)}, steep {len(steep)}")
