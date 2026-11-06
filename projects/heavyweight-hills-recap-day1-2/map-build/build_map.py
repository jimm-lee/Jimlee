"""Turn the OpenStreetMap extract into an SVG map (vector roads, parks, coastline) plus a raster land layer."""
import json, math, sys
from PIL import Image, ImageDraw
SRC, OUT = sys.argv[1], sys.argv[2]
S, W_, N, E = -37.672, 176.150, -37.612, 176.215
LAT0 = math.radians((S + N) / 2)
MX = 111320 * math.cos(LAT0); MY = 110574
WIDTH_M = (E - W_) * MX; HEIGHT_M = (N - S) * MY
def xy(lat, lon): return ((lon - W_) * MX, (N - lat) * MY)       # metres, y down
d = json.load(open(SRC))
els = d["elements"]
def geom(e):
    if e["type"] == "way": return [e.get("geometry") or []]
    if e["type"] == "relation": return [m.get("geometry") or [] for m in e.get("members", []) if m.get("role") in ("outer", "")]
    return []
def path(pts, close=False):
    if len(pts) < 2: return ""
    s = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (xy(p["lat"], p["lon"]) for p in pts))
    return s + ("Z" if close else "")
# ---- land raster: draw coastlines, flood-fill the sea from known sea points ----
R = 0.6  # px per metre
Wpx, Hpx = int(WIDTH_M * R), int(HEIGHT_M * R)
img = Image.new("L", (Wpx, Hpx), 255); dr = ImageDraw.Draw(img)
for e in els:
    if e.get("tags", {}).get("natural") == "coastline":
        for g in geom(e):
            pts = [tuple(c * R for c in xy(p["lat"], p["lon"])) for p in g]
            if len(pts) > 1: dr.line(pts, fill=0, width=3)
seeds = [(-37.615, 176.212), (-37.640, 176.212), (-37.668, 176.152), (-37.645, 176.152), (-37.615, 176.152), (-37.625, 176.158)]
for la, lo in seeds:
    x, y = (c * R for c in xy(la, lo))
    if img.getpixel((int(x), int(y))) == 255: ImageDraw.floodfill(img, (int(x), int(y)), 128)
land = img.point(lambda v: 255 if v != 128 else 0)
land.save(f"{OUT}/land_mask.png")
# ---- vector layers ----
parks, woods, beaches, roads_major, roads_minor, paths_, coast = [], [], [], [], [], [], []
for e in els:
    t = e.get("tags", {})
    for g in geom(e):
        if not g: continue
        if t.get("leisure") == "park": parks.append(path(g, True))
        elif t.get("natural") in ("wood", "scrub"): woods.append(path(g, True))
        elif t.get("natural") == "beach": beaches.append(path(g, True))
        elif t.get("natural") == "coastline": coast.append(path(g))
        elif "highway" in t:
            h = t["highway"]
            if h in ("motorway", "trunk", "primary", "secondary", "tertiary", "motorway_link", "trunk_link", "primary_link"): roads_major.append(path(g))
            elif h in ("residential", "unclassified", "service", "living_street", "road"): roads_minor.append(path(g))
            elif h in ("footway", "path", "steps", "track", "pedestrian", "cycleway"): paths_.append(path(g))
reserve = next(e for e in els if e.get("tags", {}).get("name") == "Mount Drury Reserve")
peak = next(e for e in els if e["type"] == "node" and e.get("tags", {}).get("name") == "Mount Drury")
mauao = [e for e in els if e["type"] == "node" and e.get("tags", {}).get("natural") == "peak"]
byid = {e["id"]: e for e in els if e["type"] == "way"}
def pts_of(i, rev=False):
    g = [xy(p["lat"], p["lon"]) for p in byid[i]["geometry"]]; return g[::-1] if rev else g
# route: north entrance -> winding gravel track up -> summit -> grass/steps/gravel down to the south end (traced from the workout map)
route = pts_of(574736364, rev=True) + pts_of(574736363) + pts_of(574736368, rev=True) + pts_of(574736366, rev=True) + pts_of(574736367, rev=True)
out = {"width_m": WIDTH_M, "height_m": HEIGHT_M, "raster_px_per_m": R,
       "parks": parks, "woods": woods, "beaches": beaches, "coast": coast,
       "roads_major": roads_major, "roads_minor": roads_minor, "paths": paths_,
       "reserve": path(reserve["geometry"], True), "peak": xy(peak["lat"], peak["lon"]),
       "peaks": [{"name": p["tags"].get("name"), "xy": xy(p["lat"], p["lon"])} for p in mauao],
       "route": "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in route),
       "route_start": route[0], "route_end": route[-1],
       "mauao_label": xy(-37.6318, 176.1693), "mount_label": xy(-37.6440, 176.1890), "drury": xy(-37.63446, 176.18300)}
json.dump(out, open(f"{OUT}/map.json", "w"))
print(f"map {WIDTH_M:.0f} x {HEIGHT_M:.0f} m; land raster {Wpx}x{Hpx}; parks {len(parks)} woods {len(woods)} beaches {len(beaches)} roads {len(roads_major)}+{len(roads_minor)} paths {len(paths_)} coast {len(coast)}; route {len(route)} pts; peaks {[p['tags'].get('name') for p in mauao]}")
