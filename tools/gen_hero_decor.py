#!/usr/bin/env python3
"""Generate the hero section's ambient decorative layer: sparkle dust and a
single drifting petal. The gold line-art corner florals are separate
generated-image assets (images/hero-corner-tl.webp / hero-corner-br.webp,
produced by tools/cutout_lineart.py) — this script only draws the small
ambient touches that float across the whole hero: sparkles and one petal."""
import sys

W, H = 1100, 640

def build():
    L = []
    A = L.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
      f'height="{H}" role="img" focusable="false">'
      f'<defs><linearGradient id="goldL" x1="0" y1="0" x2="1" y2="1">'
      f'<stop offset="0" stop-color="#8A6A35"/><stop offset=".5" stop-color="#E7C88C"/>'
      f'<stop offset="1" stop-color="#8A6A35"/></linearGradient></defs>')

    spark = "M0,-1 L.22,-.22 L1,0 L.22,.22 L0,1 L-.22,.22 L-1,0 L-.22,-.22Z"
    for sx, sy, sc, d in [(40, 60, 6, 0.2), (176, 44, 5, 1.4), (216, 168, 5.5, 2.5),
                          (988, 402, 6, 0.6), (1074, 560, 5, 1.8), (858, 590, 5.5, 3.0),
                          (150, 260, 4.5, 3.4), (960, 610, 4.5, 2.0), (560, 40, 5, 1.0),
                          (700, 580, 5, 2.8)]:
        A(f'<g transform="translate({sx},{sy}) scale({sc})">'
          f'<g class="spark" style="animation-delay:{d:.2f}s">'
          f'<path d="{spark}" fill="#E7C88C"/></g></g>')

    petal_d = "M0,0 C-9,-14 -9,-32 0,-46 C9,-32 9,-14 0,0 Z"
    A(f'<g class="fall" transform="translate(230,560)">'
      f'<path d="{petal_d}" fill="#EFCFC8" fill-opacity=".85" '
      f'stroke="url(#goldL)" stroke-width=".8"/></g>')

    A("""<style>
.spark{opacity:.5}
@media (prefers-reduced-motion:no-preference){
 .spark{transform-box:fill-box;transform-origin:center;
   animation:spark 3.6s ease-in-out infinite both}
 @keyframes spark{0%,100%{opacity:.5;transform:scale(.6) rotate(0)}
   50%{opacity:1;transform:scale(1) rotate(90deg)}}
 .fall{animation:fall 15s ease-in-out infinite}
 @keyframes fall{0%{transform:translate(230px,20px) rotate(-10deg);opacity:0}
   8%{opacity:.85}
   82%{opacity:.85}
   100%{transform:translate(230px,560px) rotate(300deg);opacity:0}}
}
</style></svg>""")
    return "".join(L)

if __name__ == "__main__":
    svg = build()
    out = sys.argv[1] if len(sys.argv) > 1 else "hero-decor.svg"
    with open(out, "w") as fh:
        fh.write(svg)
    print(f"{out}: {len(svg)/1024:.1f} KB")
