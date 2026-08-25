"""The consensus system as its own website — the real engine, with the
review's changes laid over it, rendered into review-site/site/."""
import math, sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import build as B

# ---- 1. Co-radiant lights: one luminance band for the four directions
B.PROJECTS["Smile"]["color"] = "#f5c542"          # gold, quieted a step
B.PROJECTS["Videogames"]["color"] = "#62d194"     # jade, held
B.PROJECTS["Sacred Travel"]["color"] = "#ff7f8d"  # ruby, lifted
B.PROJECTS["Machine Learning"]["color"] = "#6f9ce4"  # sapphire, lifted

# ---- 2. Secondaries by one uniform rule: the opposite's hue, quieted
OPPOSITE = {"Machine Learning": "Sacred Travel",
            "Sacred Travel": "Machine Learning",
            "Smile": "Videogames",
            "Videogames": "Smile"}
for name, opp in OPPOSITE.items():
    quiet = B._mix(B.PROJECTS[opp]["color"], "#000000", 0.22)
    B.PROJECTS[name]["hues"] = [B.PROJECTS[name]["color"], quiet]
B.PROJECTS["Buddhism"]["hues"] = ["#ffffff", "url(#dta-thread)"]
B.RESERVE_COLORS = []   # no sixth seat

THREAD = [B.PROJECTS[n]["color"] for n in
          ["Machine Learning", "Smile", "Sacred Travel", "Videogames"]]

def stream_svg(h=320):
    """The Great Rope with the consensus: crop-proof thread (the
    sunwise cycle repeated) and phase-coupled strand pairs (each
    stream's two strands travel as a couple)."""
    w = 1440
    strands = []
    for k, (name, st) in enumerate(B.PROJECTS.items()):
        for v, hue in enumerate(st["hues"]):
            strands.append((name, st, hue, k, v))
    n = len(strands)
    pts = 240
    coils = 3.3
    stops = ""
    cycle = THREAD + THREAD          # repeat: any crop shows all four
    for i, c in enumerate(cycle):
        stops += (f'<stop offset="{i / (len(cycle) - 1):.3f}" '
                  f'stop-color="{c}"/>')
    content = (f'<defs><linearGradient id="dta-thread" '
               f'x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient></defs>')
    for name, st, hue, k, v in strands:
        # couples: streams sit 2pi/5 apart; partners sit pi/n inside
        phase = 2 * math.pi * k / 5 + v * (math.pi / n)
        thick = 11 if v == 0 else 6.5
        mid = []
        for i in range(pts + 1):
            u = i / pts
            cyu = (h * 0.5
                   + h * 0.24 * math.sin(1.15 * math.pi * u + 0.6)
                   + h * 0.10 * math.sin(2.6 * math.pi * u + 2.2))
            breathe = h * (0.10 + 0.085 * math.sin(2.0 * math.pi * u + 1.1))
            y = cyu + breathe * math.sin(2 * math.pi * coils * u + phase)
            mid.append((u * w, y))
        tops = [(x, y - thick / 2) for x, y in mid]
        bots = [(x, y + thick / 2) for x, y in mid]
        d = ("M" + " L".join(f"{x:.0f},{y:.1f}" for x, y in tops)
             + " L" + " L".join(f"{x:.0f},{y:.1f}" for x, y in reversed(bots))
             + " Z")
        content += f'<path d="{d}" fill="{hue}" fill-opacity="0.75"/>'
        ink = ("#8a8a8a" if hue.startswith("url")
               else B._mix(hue, "#000000", 0.6))
        j = 0
        u = 0.03 + ((k * 2 + v) % 3) * 0.02
        while u < 0.97:
            i = int(u * pts)
            x, y = mid[i]
            x2, y2 = mid[min(i + 2, pts)]
            ang = math.degrees(math.atan2(y2 - y, x2 - x))
            size = 5.5 + ((j * 7 + (k * 2 + v) * 3) % 4) * 1.1
            glyph = st["symbols"][j % len(st["symbols"])]
            content += (f'<text x="{x:.0f}" y="{y:.1f}" '
                        f'font-size="{size:.1f}" fill="{ink}" '
                        f'text-anchor="middle" '
                        f'transform="rotate({ang:.0f} {x:.0f} {y:.1f})" '
                        f'font-family="Cascadia Mono, Segoe UI Historic, '
                        f'Segoe UI Symbol, Leelawadee UI, Consolas, '
                        f'monospace">{glyph}</text>')
            u += 0.02 + ((j * 3) % 3) * 0.004
            j += 1
    return (f'<svg class="planes" viewBox="0 0 {w} {h}" '
            f'preserveAspectRatio="none" aria-hidden="true">{content}</svg>')

B.stream_svg = stream_svg
B.SITE = HERE / "site"

SIGNATURE_CSS = f"""
/* ---- Consensus signature: the thread of four worn as rules ---- */
.band-head {{
  border-bottom: 3px solid;
  border-image: linear-gradient(90deg,
    {THREAD[0]}, {THREAD[1]}, {THREAD[2]}, {THREAD[3]}, {THREAD[0]}) 1;
  padding-bottom: .5rem;
}}
.see-all:hover, .post-body a:hover {{
  text-decoration-color: {THREAD[2]};
}}
.foot-cta {{
  border-bottom: 3px solid;
  border-image: linear-gradient(90deg,
    {THREAD[0]}, {THREAD[1]}, {THREAD[2]}, {THREAD[3]}, {THREAD[0]}) 1;
}}
/* white lives in a bordered chip wherever it must stand as a swatch */
.stream-dot {{ border: 1px solid rgba(0,0,0,.35); }}
.foot-grid .stream-dot, .midband .stream-dot {{
  border-color: rgba(255,255,255,.45);
}}
"""

B.main()
base = B.SITE / "assets" / "base.css"
base.write_text(base.read_text(encoding="utf-8") + SIGNATURE_CSS,
                encoding="utf-8")
print(f"Consensus site built into {B.SITE}")
