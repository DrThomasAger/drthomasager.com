"""Ten weavings — one generator per version, grown one at a time.

Each variant returns a full <svg class="planes"> string for a given
height, drawn from PROJECTS in ../build.py. Run:  python weave.py N
to render ribbons/vN.html through the real site page shell.
"""
import math, re, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import build as B

W = 1440


def _mix(c1, c2, t):
    return B._mix(c1, c2, t)


def _ribbon_path(pts_top, pts_bot):
    return ("M" + " L".join(f"{x:.0f},{y:.1f}" for x, y in pts_top)
            + " L" + " L".join(f"{x:.0f},{y:.1f}" for x, y in reversed(pts_bot))
            + " Z")


def _glyphs_along(mid, syms, ink, k, step=0.011, size0=5.5):
    """Small symbols strewn along a midline, rotated to its tangent."""
    n = len(mid) - 1
    texts, j = "", 0
    u = 0.03 + (k % 3) * 0.02
    while u < 0.97:
        i = int(u * n)
        x, y = mid[i]
        x2, y2 = mid[min(i + 2, n)]
        ang = math.degrees(math.atan2(y2 - y, x2 - x))
        size = size0 + ((j * 7 + k * 3) % 4) * 1.1
        texts += (f'<text x="{x:.0f}" y="{y:.1f}" font-size="{size:.1f}" '
                  f'fill="{ink}" text-anchor="middle" '
                  f'transform="rotate({ang:.0f} {x:.0f} {y:.1f})" '
                  f'font-family="Cascadia Mono, Segoe UI Historic, '
                  f'Segoe UI Symbol, Leelawadee UI, Consolas, monospace">'
                  f'{syms[j % len(syms)]}</text>')
        u += step + ((j * 3) % 3) * 0.004
        j += 1
    return texts


# ------------------------------------------------------------------
# v1 — The Mandorla Braid.
# Each stream is a PAIR of ribbons mirroring each other exactly about
# a wandering axis (a local symmetry per stream). Where the pair meets
# the braid crosses over-and-under for real (segments alternate draw
# order), and between crossings the two hues open into mandorla lenses.
# All ribbons half-transparent, so every crossing — within a pair and
# between streams — blooms a third color.
# ------------------------------------------------------------------
def v1(h=320):
    pts = 240
    content = ""
    names = list(B.PROJECTS)
    for k, name in enumerate(names):
        st = B.PROJECTS[name]
        axis0 = h * (0.16 + 0.68 * k / (len(names) - 1))
        drift = h * 0.16
        sd = (sum(map(ord, name)) % 89) / 11.0
        thick = h * 0.055
        # the mirrored pair
        midA, midB, axis_pts = [], [], []
        for i in range(pts + 1):
            u = i / pts
            axis = (axis0 + drift * math.sin(1.1 * math.pi * u + sd)
                    + drift * 0.4 * math.sin(2.3 * math.pi * u + sd * 2.2))
            env = h * 0.085 * (0.55 + 0.45 * math.sin(0.9 * math.pi * u + sd))
            sep = env * math.sin(3.0 * math.pi * u + sd)  # zero = crossing
            x = u * W
            axis_pts.append((x, axis))
            midA.append((x, axis + sep))
            midB.append((x, axis - sep))
        # crossings where sin(3πu + sd) = 0
        zeros = []
        m = math.ceil((0 * 3 + sd / math.pi))
        t = (-sd / (3 * math.pi))
        while t < 1:
            if t > 0:
                zeros.append(t)
            t += 1 / 3
        cuts = [0.0] + zeros + [1.0]
        for c1, c2 in zip(cuts, cuts[1:]):
            i1, i2 = int(c1 * pts), min(int(c2 * pts) + 2, pts)
            seg_order = ([("A", st["hues"][0], midA), ("B", st["hues"][1], midB)]
                         if int(c1 * 6) % 2 == 0 else
                         [("B", st["hues"][1], midB), ("A", st["hues"][0], midA)])
            for _, hue, mid in seg_order:
                seg = mid[i1:i2 + 1]
                tops = [(x, y - thick / 2) for x, y in seg]
                bots = [(x, y + thick / 2) for x, y in seg]
                content += (f'<path d="{_ribbon_path(tops, bots)}" '
                            f'fill="{hue}" fill-opacity="0.55"/>')
        ink = _mix(st["hues"][0], "#000000", 0.62)
        content += _glyphs_along(midA, st["symbols"], ink, k)
        ink2 = _mix(st["hues"][1], "#000000", 0.62)
        content += _glyphs_along(midB, st["symbols"], ink2, k + 1)
    return (f'<svg class="planes" viewBox="0 0 {W} {h}" '
            f'preserveAspectRatio="none" aria-hidden="true">{content}</svg>')


# ------------------------------------------------------------------
# v2 — The Gathered Sheaf.
# All ten strands sweep in from both edges and pass through one
# central waist — a sheaf bound in the middle of the sky. The whole
# composition is bilaterally symmetric about the center line (one
# great symmetry made of many local ones), and at the waist every
# stream crosses every other, blooming a dense woven jewel. Learned
# from v1: cores stay crisp (0.85), each ribbon carries a wide
# translucent aura (0.18) so crossings still bloom halos and jewels
# without washing the hues.
# ------------------------------------------------------------------
def v2(h=320):
    pts = 240
    content = ""
    strands = []
    names = list(B.PROJECTS)
    for k, name in enumerate(names):
        st = B.PROJECTS[name]
        for v, hue in enumerate(st["hues"]):
            strands.append((name, st, hue, k * 2 + v))
    n = len(strands)
    for name, st, hue, idx in strands:
        # edge offset: fanned above/below center at the edges,
        # squeezed to a slim waist at u = 0.5
        spread = (idx - (n - 1) / 2) / ((n - 1) / 2)   # -1 .. 1
        edge = h * 0.42 * spread
        waist = h * 0.055 * spread
        sd = (sum(map(ord, name)) % 55) / 8.0 + idx
        thick = h * (0.055 if idx % 2 == 0 else 0.028)
        mid = []
        for i in range(pts + 1):
            u = i / pts
            s = abs(u - 0.5) * 2            # 0 at waist, 1 at edges
            g = s * s * (3 - 2 * s)         # smooth gather
            ripple = h * 0.05 * (1 - g) * math.sin(6.0 * math.pi * u + sd)
            y = h / 2 + waist * (1 - g) + edge * g + ripple
            mid.append((u * W, y))
        aura = thick * 2.6
        for width, op in ((aura, 0.18), (thick, 0.85)):
            tops = [(x, y - width / 2) for x, y in mid]
            bots = [(x, y + width / 2) for x, y in mid]
            content += (f'<path d="{_ribbon_path(tops, bots)}" '
                        f'fill="{hue}" fill-opacity="{op}"/>')
        ink = _mix(hue, "#000000", 0.6)
        content += _glyphs_along(mid, st["symbols"], ink, idx)
    return (f'<svg class="planes" viewBox="0 0 {W} {h}" '
            f'preserveAspectRatio="none" aria-hidden="true">{content}</svg>')


# ------------------------------------------------------------------
# v3 — The Rosette of Rings.
# A new technique: no filled ribbon paths at all — each stream is a
# great stroked circle. All ten rings pass through one shared point
# (the classic flower-pattern construction), so every pair of rings
# opens a petal lens where it overlaps. Local symmetry at every lens,
# rotational symmetry in the whole. Translucent strokes make each
# petal a blended jewel; glyphs walk the circumference of their ring.
# ------------------------------------------------------------------
def v3(h=320):
    content = ""
    cx, cy = W * 0.70, h * 0.50
    R = h * 0.62
    strands = []
    for k, (name, st) in enumerate(B.PROJECTS.items()):
        for v, hue in enumerate(st["hues"]):
            strands.append((name, st, hue, k * 2 + v))
    n = len(strands)
    for name, st, hue, idx in strands:
        th = math.pi * 2 * idx / n
        ox, oy = cx + R * math.cos(th), cy + R * math.sin(th) * 0.55
        thick = h * (0.05 if idx % 2 == 0 else 0.024)
        content += (f'<ellipse cx="{ox:.0f}" cy="{oy:.0f}" '
                    f'rx="{R:.0f}" ry="{R * 0.55:.0f}" fill="none" '
                    f'stroke="{hue}" stroke-width="{thick:.1f}" '
                    f'stroke-opacity="0.6"/>')
        ink = _mix(hue, "#000000", 0.6)
        m = 34
        for j in range(m):
            phi = math.pi * 2 * j / m + idx
            gx = ox + R * math.cos(phi)
            gy = oy + R * 0.55 * math.sin(phi)
            if not (-40 < gx < W + 40 and -20 < gy < h + 20):
                continue
            ang = math.degrees(phi) + 90
            content += (f'<text x="{gx:.0f}" y="{gy:.1f}" font-size="6.2" '
                        f'fill="{ink}" text-anchor="middle" '
                        f'transform="rotate({ang:.0f} {gx:.0f} {gy:.1f})" '
                        f'font-family="Cascadia Mono, Segoe UI Historic, '
                        f'Segoe UI Symbol, Leelawadee UI, Consolas, monospace">'
                        f'{st["symbols"][j % len(st["symbols"])]}</text>')
    return (f'<svg class="planes" viewBox="0 0 {W} {h}" '
            f'preserveAspectRatio="none" aria-hidden="true">{content}</svg>')


# ------------------------------------------------------------------
# v4 — The Plaited Lattice.
# Two diagonal families of ribbons — a warp rising left-to-right and
# a weft falling — crossing like basketwork. Every intersection is a
# translucent jewel (v1's discovery), and the jewels form a rippling
# checkerboard: local symmetry at each crossing, a woven-cloth
# symmetry over the whole. Ribbons stay full-hue at 0.65 so the
# lattice reads crisp, not misty.
# ------------------------------------------------------------------
def v4(h=320):
    pts = 160
    content = ""
    strands = []
    for k, (name, st) in enumerate(B.PROJECTS.items()):
        for v, hue in enumerate(st["hues"]):
            strands.append((name, st, hue, k * 2 + v))
    for name, st, hue, idx in strands:
        rising = idx % 2 == 0            # family by parity: warp / weft
        lane = idx // 2                  # 0..4 within its family
        sd = (sum(map(ord, name)) % 34) / 5.0
        thick = h * 0.052
        y0 = h * (-0.25 + 0.38 * lane)   # entry height, spread across
        slope = h * 0.9 * (1 if rising else -1)
        mid = []
        for i in range(pts + 1):
            u = i / pts
            y = (y0 + slope * u
                 + h * 0.06 * math.sin(4.2 * math.pi * u + sd)
                 + h * 0.03 * math.sin(9.1 * math.pi * u + sd * 2))
            # fold back into band so ribbons keep re-entering the sky
            yy = y % (h * 1.5) - h * 0.25
            mid.append((u * W, yy))
        # split at fold seams so the wrap never draws a vertical scar
        runs, run = [], [mid[0]]
        for (x1, y1), (x2, y2) in zip(mid, mid[1:]):
            if abs(y2 - y1) > h * 0.5:
                runs.append(run); run = []
            run.append((x2, y2))
        runs.append(run)
        ink = _mix(hue, "#000000", 0.6)
        for seg in runs:
            if len(seg) < 3:
                continue
            tops = [(x, y - thick / 2) for x, y in seg]
            bots = [(x, y + thick / 2) for x, y in seg]
            content += (f'<path d="{_ribbon_path(tops, bots)}" '
                        f'fill="{hue}" fill-opacity="0.65"/>')
            content += _glyphs_along(seg, st["symbols"], ink, idx, step=0.05)
    return (f'<svg class="planes" viewBox="0 0 {W} {h}" '
            f'preserveAspectRatio="none" aria-hidden="true">{content}</svg>')


# ------------------------------------------------------------------
# v5 — The Braided Rainbow Arch.
# The rainbow itself, at last: ten concentric bands rising as one
# great arch over the black — a single strong center. But the bands
# are alive: neighboring bands trade places in slow braided
# exchanges along the arc, so the strict spectrum order melts and
# reforms — local braid symmetries strung along one whole-page
# symmetry. Full hue, high opacity, the ink look kept.
# ------------------------------------------------------------------
def v5(h=320):
    content = ""
    cx, cy = W * 0.62, h * 1.28
    strands = []
    for k, (name, st) in enumerate(B.PROJECTS.items()):
        for v, hue in enumerate(st["hues"]):
            strands.append((name, st, hue, k * 2 + v))
    n = len(strands)
    pts = 220
    for name, st, hue, idx in strands:
        base = h * 0.58 + h * 0.052 * idx
        thick = h * (0.045 if idx % 2 == 0 else 0.024)
        phase = math.pi * (idx % 2)          # neighbors oppose -> braids
        mid = []
        for i in range(pts + 1):
            t = math.pi * (0.02 + 0.96 * i / pts)      # sweep the arch
            r = base + h * 0.055 * math.sin(4.0 * t + phase + idx * 0.35)
            x = cx + r * 1.9 * math.cos(t)
            y = cy - r * math.sin(t)
            mid.append((x, y))
        tops, bots = [], []
        for i, (x, y) in enumerate(mid):
            t = math.pi * (0.02 + 0.96 * i / pts)
            nx, ny = math.cos(t), -math.sin(t)          # outward normal
            tops.append((x + nx * thick, y + ny * thick))
            bots.append((x - nx * thick, y - ny * thick))
        content += (f'<path d="{_ribbon_path(tops, bots)}" '
                    f'fill="{hue}" fill-opacity="0.8"/>')
        ink = _mix(hue, "#000000", 0.6)
        content += _glyphs_along(mid, st["symbols"], ink, idx, step=0.014)
    return (f'<svg class="planes" viewBox="0 0 {W} {h}" '
            f'preserveAspectRatio="none" aria-hidden="true">{content}</svg>')


# ------------------------------------------------------------------
# v6 — The Falling Helix Banners.
# The unexplored axis: verticality. Each stream falls from the top
# edge as a banner of its two hues twisting around one another — five
# double-helix columns swaying like hanging silks. The twist crossing
# repeats down each fall (a ladder of local symmetries), and the
# column row across the page is itself a rhythm. Glyphs ride the
# falls, reading downward like brushwork.
# ------------------------------------------------------------------
def v6(h=320):
    content = ""
    names = list(B.PROJECTS)
    pts = 120
    for k, name in enumerate(names):
        st = B.PROJECTS[name]
        xk = W * (0.34 + 0.155 * k)
        sd = (sum(map(ord, name)) % 21) / 3.0
        sway = 26 + 10 * math.sin(sd)
        turns = 2.2 + (k % 3) * 0.5
        for v, hue in enumerate(st["hues"]):
            thick = 16 if v == 0 else 9
            phase = math.pi * v
            mid = []
            for i in range(pts + 1):
                t = i / pts
                x = (xk + sway * math.sin(2 * math.pi * turns * t + phase)
                     + 34 * math.sin(1.3 * math.pi * t + sd) * t)
                y = t * h * 1.04 - h * 0.02
                mid.append((x, y))
            tops = [(x - thick / 2, y) for x, y in mid]
            bots = [(x + thick / 2, y) for x, y in mid]
            content += (f'<path d="{_ribbon_path(tops, bots)}" '
                        f'fill="{hue}" fill-opacity="0.72"/>')
            ink = _mix(hue, "#000000", 0.6)
            content += _glyphs_along(mid, st["symbols"], ink, k * 2 + v,
                                     step=0.06)
    return (f'<svg class="planes" viewBox="0 0 {W} {h}" '
            f'preserveAspectRatio="none" aria-hidden="true">{content}</svg>')


# ------------------------------------------------------------------
# v7 — The Rivers of Symbols.
# The inversion: no ribbon fills at all. Each stream's body IS its
# symbols — a dense current of glowing full-hue glyphs flowing along
# a wandering course, swelling and thinning like a calligrapher's
# stroke. Where two rivers cross, their alphabets mingle. The page
# is written, literally, by what it carries.
# ------------------------------------------------------------------
def v7(h=320):
    content = ""
    pts = 200
    strands = []
    for k, (name, st) in enumerate(B.PROJECTS.items()):
        for v, hue in enumerate(st["hues"]):
            strands.append((name, st, hue, k * 2 + v))
    for name, st, hue, idx in strands:
        sd = ((sum(map(ord, name)) * 7 + idx * 31) % 89) / 6.0
        yL = h * (0.10 + 0.80 * ((sd * 13.7) % 1))
        yR = h * (0.10 + 0.80 * ((sd * 7.3 + 0.47) % 1))
        amp = h * 0.16
        mid = []
        for i in range(pts + 1):
            u = i / pts
            wob = amp * (0.8 * math.sin(1.4 * math.pi * u + sd * 1.7)
                         + 0.45 * math.sin(3.1 * math.pi * u + sd * 3.1))
            mid.append((u * W, yL + (yR - yL) * B._sm(u) + wob))
        j = 0
        u = 0.015 + (idx % 4) * 0.008
        while u < 0.985:
            i = int(u * pts)
            x, y = mid[i]
            swell = 0.55 + 0.45 * math.sin(math.pi * u + sd)   # stroke width
            row = ((j * 11 + idx * 7) % 5 - 2)
            y += row * 7.5 * swell
            x2, y2 = mid[min(i + 2, pts)]
            ang = math.degrees(math.atan2(y2 - y, x2 - x))
            size = 6.0 + 8.5 * swell * (((j * 7 + idx) % 4) / 3.0)
            content += (f'<text x="{x:.0f}" y="{y:.1f}" '
                        f'font-size="{size:.1f}" fill="{hue}" '
                        f'fill-opacity="0.9" text-anchor="middle" '
                        f'transform="rotate({ang:.0f} {x:.0f} {y:.1f})" '
                        f'font-family="Cascadia Mono, Segoe UI Historic, '
                        f'Segoe UI Symbol, Leelawadee UI, Consolas, monospace">'
                        f'{st["symbols"][j % len(st["symbols"])]}</text>')
            u += 0.0065 + ((j * 3) % 3) * 0.003
            j += 1
    return (f'<svg class="planes" viewBox="0 0 {W} {h}" '
            f'preserveAspectRatio="none" aria-hidden="true">{content}</svg>')


# ------------------------------------------------------------------
# v8 — The Woven Smile.
# Representational weaving: the streams converge to draw the brand
# mark itself — a giant (-: across the sky. The opening paren is an
# arc-bundle of braided bands, the dash a straight sheaf, the colon
# two woven rosettes. Every element is built from all five streams
# running parallel with gentle braids, so the mark IS the rainbow.
# ------------------------------------------------------------------
def v8(h=320):
    content = ""
    strands = []
    for k, (name, st) in enumerate(B.PROJECTS.items()):
        for v, hue in enumerate(st["hues"]):
            strands.append((name, st, hue, k * 2 + v))
    n = len(strands)
    pts = 150

    def bundle(path_fn, t0, t1, gap, thick_scale=1.0, glyph_step=0.05):
        out = ""
        for name, st, hue, idx in strands:
            off = (idx - (n - 1) / 2) * gap
            braid = gap * 0.55
            mid = []
            for i in range(pts + 1):
                t = t0 + (t1 - t0) * i / pts
                x, y, nx, ny = path_fn(t)
                o = off + braid * math.sin(5.0 * t + idx)
                mid.append((x + nx * o, y + ny * o))
            thick = (7.5 if idx % 2 == 0 else 4.5) * thick_scale
            tops = [(x, y - thick / 2) for x, y in mid]
            bots = [(x, y + thick / 2) for x, y in mid]
            out += (f'<path d="{_ribbon_path(tops, bots)}" '
                    f'fill="{hue}" fill-opacity="0.8"/>')
            ink = _mix(hue, "#000000", 0.55)
            out += _glyphs_along(mid, st["symbols"], ink, idx,
                                 step=glyph_step, size0=4.5)
        return out

    cx, cy = W * 0.68, h * 0.5
    R = h * 0.40

    def paren(t):  # big opening paren: arc from top to bottom, bowing left
        a = math.pi * (0.65 + 0.7 * t)
        x = cx + R * 1.15 * math.cos(a)
        y = cy + R * math.sin(a)
        return x, y, math.cos(a), math.sin(a)

    def dash(t):   # the nose-dash, level sheaf
        x = W * 0.715 + (W * 0.085) * t
        y = cy - h * 0.02
        return x, y, 0.0, 1.0

    content += bundle(paren, 0.0, 1.0, 5.2)
    content += bundle(dash, 0.0, 1.0, 4.6, thick_scale=0.85)
    for dy in (-h * 0.17, h * 0.17):     # the colon: two woven rosettes
        ox, oy = W * 0.865, cy + dy
        r = h * 0.075

        def ring(t, ox=ox, oy=oy, r=r):
            a = 2 * math.pi * t
            return (ox + r * 1.6 * math.cos(a), oy + r * math.sin(a),
                    math.cos(a), math.sin(a))

        content += bundle(ring, 0.0, 1.0, 2.6, thick_scale=0.6,
                          glyph_step=0.09)
    return (f'<svg class="planes" viewBox="0 0 {W} {h}" '
            f'preserveAspectRatio="none" aria-hidden="true">{content}</svg>')


# ------------------------------------------------------------------
# v9 — The Great Rope.
# Levels of scale, cabled: one wandering course crosses the whole
# sky, and all ten strands twist around it as a single rope — evenly
# phased, so the cable's braid is a true rotational rhythm. Large
# scale: the course. Middle: the coiling strands. Small: the glyphs.
# Where the rope tightens the hues stack into jewels; where it
# loosens the strands breathe apart and show the black between.
# ------------------------------------------------------------------
def v9(h=320):
    content = ""
    strands = []
    for k, (name, st) in enumerate(B.PROJECTS.items()):
        for v, hue in enumerate(st["hues"]):
            strands.append((name, st, hue, k * 2 + v))
    n = len(strands)
    pts = 240
    coils = 3.3
    for name, st, hue, idx in strands:
        phase = 2 * math.pi * idx / n
        thick = 11 if idx % 2 == 0 else 6.5
        mid = []
        for i in range(pts + 1):
            u = i / pts
            cyu = (h * 0.5
                   + h * 0.24 * math.sin(1.15 * math.pi * u + 0.6)
                   + h * 0.10 * math.sin(2.6 * math.pi * u + 2.2))
            breathe = h * (0.10 + 0.085 * math.sin(2.0 * math.pi * u + 1.1))
            y = cyu + breathe * math.sin(2 * math.pi * coils * u + phase)
            mid.append((u * W, y))
        tops = [(x, y - thick / 2) for x, y in mid]
        bots = [(x, y + thick / 2) for x, y in mid]
        content += (f'<path d="{_ribbon_path(tops, bots)}" '
                    f'fill="{hue}" fill-opacity="0.75"/>')
        ink = _mix(hue, "#000000", 0.6)
        content += _glyphs_along(mid, st["symbols"], ink, idx, step=0.02)
    return (f'<svg class="planes" viewBox="0 0 {W} {h}" '
            f'preserveAspectRatio="none" aria-hidden="true">{content}</svg>')


# ------------------------------------------------------------------
# v10 — The Fountain.
# The synthesis: one source point (v2's anchor), a monumental single
# form (v5's arch), strands in mirrored pairs (v1's local symmetry),
# jewel crossings in the falling spray (v9's exchanges). All ten
# strands rise from one wellspring, arc apart, and fall — a rainbow
# fountain, bilaterally symmetric about its rising column.
# ------------------------------------------------------------------
def v10(h=320):
    content = ""
    strands = []
    for k, (name, st) in enumerate(B.PROJECTS.items()):
        for v, hue in enumerate(st["hues"]):
            strands.append((name, st, hue, k * 2 + v))
    n = len(strands)
    x0, y0 = W * 0.70, h * 1.08
    pts = 150
    for name, st, hue, idx in strands:
        spread = (idx - (n - 1) / 2) / ((n - 1) / 2)   # -1 .. 1 mirrored
        vx = W * 0.26 * spread
        vy = h * (2.5 - 0.55 * abs(spread))            # inner rise higher
        grav = h * 2.1
        thick = 11 if idx % 2 == 0 else 6.5
        wob = 2 * math.pi * idx / n
        mid = []
        for i in range(pts + 1):
            t = i / pts * 1.35
            x = x0 + vx * t + W * 0.012 * math.sin(5.5 * t + wob)
            y = y0 - vy * t + grav * t * t / 2
            if y > h * 1.15:
                continue
            mid.append((x, y))
        if len(mid) < 3:
            continue
        tops = [(x - thick / 2, y) for x, y in mid]
        bots = [(x + thick / 2, y) for x, y in mid]
        content += (f'<path d="{_ribbon_path(tops, bots)}" '
                    f'fill="{hue}" fill-opacity="0.78"/>')
        ink = _mix(hue, "#000000", 0.6)
        content += _glyphs_along(mid, st["symbols"], ink, idx, step=0.03)
    return (f'<svg class="planes" viewBox="0 0 {W} {h}" '
            f'preserveAspectRatio="none" aria-hidden="true">{content}</svg>')


VARIANTS = {1: v1, 2: v2, 3: v3, 4: v4, 5: v5,
            6: v6, 7: v7, 8: v8, 9: v9, 10: v10}


def render(n):
    fn = VARIANTS[n]
    B.FOOT_SVG[0] = fn(h=280)
    body = B.index_body(B.load_posts(), svg_fn=fn)
    html = B.page(f"Weaving v{n} — {B.SITE_NAME}", body)
    html = re.sub(r'(href|src)="assets/', r'\1="../site/assets/', html)
    out = HERE / f"v{n}.html"
    out.write_text(html, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    render(int(sys.argv[1]))
