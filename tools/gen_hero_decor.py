#!/usr/bin/env python3
"""Generate the hero section's decorative background layer: two gold
line-art corner florals, scattered sparkle dust, and a single drifting
petal. Companion to gen_hero_bouquet.py / gen_story_bouquet.py, reusing the
fine line-art bloom style from gen_story_bouquet.py — delicate line art
reads better than filled shapes for small corner ornaments."""
import math, sys

W, H = 1100, 640

def n(v):
    return f"{round(v, 1):g}"

def gradients():
    return (
        '<linearGradient id="goldL" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#8A6A35"/><stop offset=".5" stop-color="#E7C88C"/>'
        '<stop offset="1" stop-color="#8A6A35"/></linearGradient>'
    )

def bloom(cx, cy, r, delay, fringe=True):
    g = [f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="none" '
         f'stroke="url(#goldL)" stroke-width="1.4"/>',
         f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r*0.46)}" fill="#EFCFC8" '
         f'fill-opacity=".6" stroke="url(#goldL)" stroke-width="1.2"/>']
    if fringe:
        for i in range(6):
            a = math.radians(i * 60 + 18)
            fx, fy = cx + r * 1.22 * math.cos(a), cy + r * 1.22 * math.sin(a)
            mx, my = cx + r * 0.86 * math.cos(a), cy + r * 0.86 * math.sin(a)
            g.append(f'<path d="M{n(mx)},{n(my)} Q{n(fx)},{n(fy-6)} {n(fx-3)},{n(fy+6)}" '
                     f'fill="none" stroke="url(#goldL)" stroke-width="1" opacity=".7"/>')
    return (f'<g class="p" style="animation-delay:{delay:.2f}s;'
            f'transform-origin:{n(cx)}px {n(cy)}px">' + "".join(g) + '</g>')

def stem(d, delay):
    return (f'<path class="draw" style="animation-delay:{delay:.2f}s" d="{d}" '
            f'fill="none" stroke="url(#goldL)" stroke-width="1.6" '
            f'stroke-linecap="round" pathLength="1"/>')

def leaf(cx, cy, ang, size, delay):
    a = math.radians(ang)
    tx, ty = cx + size * 1.7 * math.sin(a), cy - size * 1.7 * math.cos(a)
    perp = math.radians(ang + 90)
    bow = size * 0.9
    c1x = cx + size * 0.5 * math.sin(a) + bow * math.sin(perp)
    c1y = cy - size * 0.5 * math.cos(a) - bow * math.cos(perp)
    c2x = cx + size * 0.5 * math.sin(a) - bow * math.sin(perp)
    c2y = cy - size * 0.5 * math.cos(a) + bow * math.cos(perp)
    d = (f"M{n(cx)},{n(cy)} Q{n(c1x)},{n(c1y)} {n(tx)},{n(ty)} "
         f"Q{n(c2x)},{n(c2y)} {n(cx)},{n(cy)}")
    return (f'<path class="p" style="animation-delay:{delay:.2f}s;'
            f'transform-origin:{n(cx)}px {n(cy)}px" d="{d}" fill="#EFCFC8" '
            f'fill-opacity=".55" stroke="url(#goldL)" stroke-width="1"/>')

def build():
    L = []
    A = L.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
      f'height="{H}" role="img" aria-hidden="true" focusable="false">'
      f'<defs>{gradients()}</defs>')

    # top-left corner floral
    A(stem("M70,230 C74,180 90,130 128,92", 0.1))
    A(stem("M70,230 C60,186 56,140 72,96", 0.2))
    A(leaf(96, 160, -34, 20, 0.6))
    A(leaf(84, 118, 26, 16, 0.7))
    A(bloom(128, 92, 22, 0.9))
    A(bloom(74, 96, 15, 1.0, fringe=False))

    # bottom-right corner spray (larger)
    A(stem("M1034,610 C1020,556 986,500 928,462", 0.1))
    A(stem("M1034,610 C1048,564 1064,514 1050,462", 0.2))
    A(stem("M1034,610 C1000,572 958,542 900,528", 0.3))
    A(leaf(966, 512, -30, 24, 0.65))
    A(leaf(1000, 488, 32, 22, 0.75))
    A(leaf(944, 552, -18, 18, 0.85))
    A(bloom(928, 462, 28, 0.95))
    A(bloom(1050, 462, 20, 1.05))
    A(bloom(900, 528, 16, 1.15, fringe=False))

    # sparkle dust near both clusters
    spark = "M0,-1 L.22,-.22 L1,0 L.22,.22 L0,1 L-.22,.22 L-1,0 L-.22,-.22Z"
    for sx, sy, sc, d in [(40, 60, 6, 0.2), (176, 44, 5, 1.4), (216, 168, 5.5, 2.5),
                          (988, 402, 6, 0.6), (1074, 560, 5, 1.8), (858, 590, 5.5, 3.0),
                          (150, 260, 4.5, 3.4), (960, 610, 4.5, 2.0)]:
        A(f'<g transform="translate({sx},{sy}) scale({sc})">'
          f'<g class="spark" style="animation-delay:{d:.2f}s">'
          f'<path d="{spark}" fill="#E7C88C"/></g></g>')

    # single drifting petal, resting near the lower-left by default
    petal_d = "M0,0 C-9,-14 -9,-32 0,-46 C9,-32 9,-14 0,0 Z"
    A(f'<g class="fall" transform="translate(230,560)">'
      f'<path d="{petal_d}" fill="#EFCFC8" fill-opacity=".85" '
      f'stroke="url(#goldL)" stroke-width=".8"/></g>')

    A("""<style>
.spark{opacity:.5}
@media (prefers-reduced-motion:no-preference){
 .draw{stroke-dasharray:1;stroke-dashoffset:1;
   animation:draw 1.2s cubic-bezier(.22,.8,.3,1) both}
 @keyframes draw{to{stroke-dashoffset:0}}
 .p{transform-box:fill-box;
    animation:bloom .8s cubic-bezier(.28,1.5,.5,1) both}
 @keyframes bloom{0%{transform:scale(.2);opacity:0}
   60%{opacity:1}100%{transform:scale(1);opacity:1}}
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
