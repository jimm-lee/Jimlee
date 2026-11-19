"""Visual hooks for the Heavyweight Hills edits (overlays on top of the cut; see TECHNIQUES.md in hero-edit).

Each hook sits above the shots for its window and hands back to the cut underneath, so the edit's shot list stays
the plain story. Kinds:

- spiral: every listed clip flashes by for a few frames, turning from `angle` to level and zooming in, landing on
          the shot underneath (the "opening spiral").
- grid:   one clip duplicated into cols × rows cells (each a little out of sync) that pop in on black one by one,
          hold, then the full shot takes over (crop to grid, duplicate and offset).
- zoom:   the outgoing shot punches forward, two frames of white, the incoming shot lands from a zoom.
- split:  two clips slide in as top and bottom halves, hold, then the bottom one opens to fill the frame.

Calmer, more cinematic set (James, Nov 19: "something new, something fresh"):
- iris:   the sun's glow swells out from where the sun is until it fills the frame, and the next shot comes up
          out of the light (a hard-edged circle read as a dark hole when going from sunset into night).
- nest:   the next shot appears as a small rounded window inside the current one and grows to fill the frame.
- blinds: the next shot arrives as vertical strips sliding up, staggered.
- bloom:  a bright, soft dissolve (the incoming shot fades in from over-exposed).
- freeze: the moment freezes into a white-bordered print, tilts, holds, and snaps back.
- strip:  a film strip of frames from different days scrolls up, slows, and the last frame opens into the shot.
"""
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
TRANSITIONS = ("iris", "nest", "blinds", "bloom")   # the incoming shot plays over the outgoing one
FPS = 30


def _video(clip, start, dur, media):
    return (f'<video src="assets/clips/{clip}.mp4" class="clip" data-start="{start:.3f}" data-duration="{dur:.3f}" '
            f'data-media-start="{media:.3f}" muted playsinline></video>')


def still(clip, media):
    """A frame of a clip as a JPEG (clips/stills/, not committed); -> path as the page sees it."""
    d = HERE / "clips" / "stills"
    d.mkdir(exist_ok=True)
    name = f"{clip}_{int(media * 1000)}.jpg"
    if not (d / name).exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{media}", "-i", str(HERE / "clips" / f"{clip}.mp4"),
                        "-frames:v", "1", "-q:v", "3", str(d / name)], check=True)
    return f"assets/clips/stills/{name}"


def brightest(clip, media):
    """Where the sun is: the brightest spot of a frame (blurred), as x %, y %."""
    import cv2
    p = HERE / still(clip, media).replace("assets/clips/", "clips/")
    g = cv2.GaussianBlur(cv2.cvtColor(cv2.imread(str(p)), cv2.COLOR_BGR2GRAY), (0, 0), 25)
    y, x = divmod(int(g.argmax()), g.shape[1])
    return round(100 * x / g.shape[1], 1), round(100 * y / g.shape[0], 1)


def adjust_cut(fx_list, cut):
    """Transitions keep the outgoing shot on screen under the incoming one: stretch it, start the next one later."""
    cut = list(cut)
    for f in fx_list:
        if f["kind"] not in TRANSITIONS:
            continue
        at, dur = f["at"], f["dur"]
        k = next(i for i, (c, s, d, m) in enumerate(cut) if abs(s - at) < 1e-3)
        pc, ps, pd, pm = cut[k - 1]
        c, s, d, m = cut[k]
        f["_incoming"] = (c, m)
        if f["kind"] == "iris" and "x" not in f:   # open from the sun in the outgoing frame
            f["x"], f["y"] = brightest(pc, pm + (at - ps))
        cut[k - 1] = (pc, ps, round(pd + dur, 3), pm)
        cut[k] = (c, round(s + dur, 3), round(d - dur, 3), round(m + dur, 3))
    return cut


def build(fx_list, cut):
    """-> (html, js_entries, windows): overlay markup, JS FX entries, and [(start, end)] hook windows."""
    html, js, windows = [], [], []
    for n, f in enumerate(fx_list):
        kind, at = f["kind"], f["at"]
        if kind == "spiral":
            frames, land = f.get("frames", 3), f.get("land_frames", 4)
            t, items = at, []
            clips = f["clips"]
            for k, (clip, media) in enumerate(clips):
                fr = land if k >= len(clips) - 3 else frames          # the last three slow down as it lands
                d = fr / FPS
                ang = f.get("angle", 32) * (1 - k / len(clips))
                sc = 1.35 - 0.3 * k / len(clips)
                fid = f"fx{n}s{k}"
                html.append(f'  <div class="fxshot" id="{fid}">{_video(clip, t, d, media)}</div>')
                items.append(f"['{fid}', {t:.3f}, {d:.3f}, {ang:.1f}, {sc:.3f}]")
                t += d
            js.append(f"['spiral', [{', '.join(items)}]]")
            windows.append((at, t))
        elif kind == "grid":
            cols, rows, frames, dur = f["cols"], f["rows"], f.get("frames", 2), f["dur"]
            clip, media = f["clip"], f["media"]
            gap = 10
            w, h = (1080 - gap * (cols + 1)) / cols, (1920 - gap * (rows + 1)) / rows
            order = [(r, c) for r in range(rows) for c in range(cols)]
            if f.get("order") == "stair":
                order = sorted(order, key=lambda rc: (rc[0] + rc[1], rc[0]))
            cells = []
            html.append(f'  <div class="fxgrid" id="fx{n}">')
            for k, (r, c) in enumerate(order):
                appear = at + k * frames / FPS
                cid = f"fx{n}c{k}"
                html.append(f'    <div class="cell" id="{cid}" style="left:{gap + c * (w + gap):.1f}px;top:{gap + r * (h + gap):.1f}px;'
                            f'width:{w:.1f}px;height:{h:.1f}px">{_video(clip, appear, at + dur - appear, media + 0.08 * k)}</div>')
                cells.append(f"['{cid}', {appear:.3f}]")
            html.append("  </div>")
            js.append(f"['grid', 'fx{n}', {at:.3f}, {at + dur:.3f}, [{', '.join(cells)}]]")
            windows.append((at, at + dur))
        elif kind == "zoom":
            out_i = next(i for i, (c, s, d, m) in enumerate(cut) if s < at <= s + d + 1e-6 and abs(s + d - at) < 1e-3)
            in_i = next(i for i, (c, s, d, m) in enumerate(cut) if abs(s - at) < 1e-3)
            js.append(f"['zoom', 's{out_i}', 's{in_i}', {at:.3f}]")
            windows.append((at - 0.25, at + 0.4))
        elif kind == "split":
            dur = f["dur"]
            (tc, tm), (bc, bm) = f["top"], f["bottom"]
            html.append(f'  <div class="fxshot" id="fx{n}t">{_video(tc, at, dur, tm)}</div>')
            html.append(f'  <div class="fxshot" id="fx{n}b">{_video(bc, at, dur, bm)}</div>')
            js.append(f"['split', 'fx{n}t', 'fx{n}b', {at:.3f}, {dur:.3f}]")
            windows.append((at, at + dur))
        elif kind in TRANSITIONS:
            dur = f["dur"]
            clip, media = f["_incoming"]
            fid = f"fx{n}"
            if kind == "blinds":
                strips, ids = f.get("strips", 7), []
                w = 1080 / strips
                for k in range(strips):
                    sid = f"{fid}b{k}"
                    html.append(f'  <div class="fxshot" id="{sid}" style="clip-path:inset(0 {1080 - (k + 1) * w - 0.5:.1f}px 0 '
                                f'{k * w - 0.5:.1f}px)">{_video(clip, at, dur, media)}</div>')
                    ids.append(f"'{sid}'")
                js.append(f"['blinds', [{', '.join(ids)}], {at:.3f}, {dur:.3f}]")
            else:
                cls = "fxshot fxnest" if kind == "nest" else "fxshot"
                html.append(f'  <div class="{cls}" id="{fid}">{_video(clip, at, dur, media)}</div>')
                if kind == "iris":   # the sunlight that swells out over both shots
                    html.append(f'  <div class="fxglow" id="{fid}g"></div>')
                extra = f", {f.get('x', 50)}, {f.get('y', 40)}" if kind == "iris" else ""
                js.append(f"['{kind}', '{fid}', {at:.3f}, {dur:.3f}{extra}]")
            windows.append((at, at + dur))
        elif kind == "freeze":
            dur, clip, media = f["dur"], f["clip"], f["media"]
            fid = f"fx{n}"
            html.append(f'  <div class="fxfreeze" id="{fid}"><div class="dim"></div>'
                        f'<img class="card" src="{still(clip, media)}" alt=""></div>')
            js.append(f"['freeze', '{fid}', {at:.3f}, {dur:.3f}]")
            windows.append((at, at + dur))
        elif kind == "strip":
            dur, frames = f["dur"], f["frames"]          # frames: [(clip, media)...]; the last opens into the cut
            fid = f"fx{n}"
            imgs = "".join(f'<img src="{still(c, m)}" alt="" style="top:{k * 540}px">' for k, (c, m) in enumerate(frames))
            last_c, last_m = frames[-1]
            open_at = at + dur * 0.68
            html.append(f'  <div class="fxstrip" id="{fid}"><div class="col" id="{fid}c">{imgs}</div></div>')
            html.append(f'  <div class="fxshot fxopen" id="{fid}o">{_video(last_c, open_at, at + dur - open_at, last_m)}</div>')
            js.append(f"['strip', '{fid}', {at:.3f}, {dur:.3f}, {len(frames)}]")
            windows.append((at, at + dur))
        else:
            raise ValueError(f"unknown hook {kind}")
    return "\n".join(html), ",\n    ".join(js), windows
