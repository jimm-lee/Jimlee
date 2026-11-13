"""Visual hooks for the Heavyweight Hills edits (overlays on top of the cut; see TECHNIQUES.md in hero-edit).

Each hook sits above the shots for its window and hands back to the cut underneath, so the edit's shot list stays
the plain story. Kinds:

- spiral: every listed clip flashes by for a few frames, turning from `angle` to level and zooming in, landing on
          the shot underneath (the "opening spiral").
- grid:   one clip duplicated into cols × rows cells (each a little out of sync) that pop in on black one by one,
          hold, then the full shot takes over (crop to grid, duplicate and offset).
- zoom:   the outgoing shot punches forward, two frames of white, the incoming shot lands from a zoom.
- split:  two clips slide in as top and bottom halves, hold, then the bottom one opens to fill the frame.
"""
FPS = 30


def _video(clip, start, dur, media):
    return (f'<video src="assets/clips/{clip}.mp4" class="clip" data-start="{start:.3f}" data-duration="{dur:.3f}" '
            f'data-media-start="{media:.3f}" muted playsinline></video>')


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
        else:
            raise ValueError(f"unknown hook {kind}")
    return "\n".join(html), ",\n    ".join(js), windows
