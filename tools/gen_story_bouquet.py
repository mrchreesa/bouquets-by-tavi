#!/usr/bin/env python3
"""Generate the animated Our Story illustration: a delicate gold line-art
bouquet resting in front of a softly pulsing blush heart. Companion to
gen_hero_bouquet.py, but drawn in the site's existing fine-line style (see
the occasion icons and the original story.svg placeholder) rather than the
hero's filled-petal style — small and line-based reads far better than
filled shapes do at this size."""
import sys

W, H = 480, 560

def n(v):
    return f"{round(v, 1):g}"

def gradients():
    return "".join([
        '<radialGradient id="bgS" cx="42%" cy="30%" r="85%">'
        '<stop offset="0" stop-color="#FDF8F2"/>'
        '<stop offset=".55" stop-color="#FBEDE8"/>'
        '<stop offset="1" stop-color="#EFCFC8"/></radialGradient>',

        '<linearGradient id="goldL" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#8A6A35"/><stop offset=".5" stop-color="#E7C88C"/>'
        '<stop offset="1" stop-color="#8A6A35"/></linearGradient>',

        '<filter id="heartBlur" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="4.5"/></filter>',
    ])

def bloom(cx, cy, r, delay, fringe=True):
    """Concentric-ring open flower, drawn in gold line art."""
    g = [f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="none" '
         f'stroke="url(#goldL)" stroke-width="1.4"/>',
         f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r*0.46)}" fill="#EFCFC8" '
         f'fill-opacity=".6" stroke="url(#goldL)" stroke-width="1.2"/>']
    if fringe:
        for i in range(6):
            import math
            a = math.radians(i*60 + 18)
            fx, fy = cx + r*1.22*math.cos(a), cy + r*1.22*math.sin(a)
            mx, my = cx + r*0.86*math.cos(a), cy + r*0.86*math.sin(a)
            g.append(f'<path d="M{n(mx)},{n(my)} Q{n(fx)},{n(fy-6)} {n(fx-3)},{n(fy+6)}" '
                     f'fill="none" stroke="url(#goldL)" stroke-width="1" opacity=".7"/>')
    return (f'<g class="p" style="animation-delay:{delay:.2f}s;'
            f'transform-origin:{n(cx)}px {n(cy)}px">' + "".join(g) + '</g>')

def stem(d, delay, swp=0.0):
    return (f'<path class="draw" style="animation-delay:{delay:.2f}s" d="{d}" '
            f'fill="none" stroke="url(#goldL)" stroke-width="1.6" '
            f'stroke-linecap="round" pathLength="1"/>')

def leaf(cx, cy, ang, size, delay):
    import math
    a = math.radians(ang)
    tx, ty = cx + size*1.7*math.sin(a), cy - size*1.7*math.cos(a)
    perp = math.radians(ang + 90)
    bow = size*0.9
    c1x, c1y = cx + size*0.5*math.sin(a) + bow*math.sin(perp), cy - size*0.5*math.cos(a) - bow*math.cos(perp)
    c2x, c2y = cx + size*0.5*math.sin(a) - bow*math.sin(perp), cy - size*0.5*math.cos(a) + bow*math.cos(perp)
    d = (f"M{n(cx)},{n(cy)} Q{n(c1x)},{n(c1y)} {n(tx)},{n(ty)} "
         f"Q{n(c2x)},{n(c2y)} {n(cx)},{n(cy)}")
    return (f'<path class="p" style="animation-delay:{delay:.2f}s;'
            f'transform-origin:{n(cx)}px {n(cy)}px" d="{d}" fill="#EFCFC8" '
            f'fill-opacity=".55" stroke="url(#goldL)" stroke-width="1"/>')

def build():
    L = []
    A = L.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
      f'height="{H}" role="img" aria-label="A delicate gold line-art bouquet resting '
      f'in front of a softly glowing heart, in blush pink and gold tones">'
      f'<defs>{gradients()}</defs>'
      f'<rect width="{W}" height="{H}" fill="url(#bgS)"/>')

    # soft heart glow behind the bouquet — sized to peek out around the cluster
    hx, hy, s = 240, 290, 3.6
    heart_d = ("M0,-10 C-14,-26 -40,-22 -40,0 C-40,20 -18,34 0,52 "
               "C18,34 40,20 40,0 C40,-22 14,-26 0,-10 Z")
    A(f'<g transform="translate({n(hx)},{n(hy)}) scale({s})">'
      f'<g class="heartpulse">'
      f'<path d="{heart_d}" fill="#E3839A" opacity=".6" filter="url(#heartBlur)"/>'
      f'<path d="{heart_d}" fill="none" stroke="#B99668" stroke-width=".65" '
      f'opacity=".95"/></g></g>')

    # stems, fanning up from a low knot to each bloom
    stems = [
        ("M240,486 C238,430 224,360 190,300", 0.15),
        ("M240,486 C240,420 240,340 240,240", 0.25),
        ("M240,486 C244,430 262,362 296,304", 0.15),
        ("M240,486 C232,440 210,392 188,352", 0.35),
        ("M240,486 C248,440 270,392 292,352", 0.35),
    ]
    for d, dl in stems:
        A(stem(d, dl))

    # leaves along the stems
    for cx, cy, ang, sz, dl in [(214, 400, -46, 26, 0.9), (266, 400, 46, 26, 0.95),
                                 (232, 350, -20, 22, 1.0), (250, 348, 20, 22, 1.05)]:
        A(leaf(cx, cy, ang, sz, dl))

    # blooms, back → front
    A(bloom(190, 300, 26, 1.15))
    A(bloom(296, 304, 26, 1.2))
    A(bloom(188, 352, 17, 1.3, fringe=False))
    A(bloom(292, 352, 17, 1.32, fringe=False))
    A(bloom(240, 240, 34, 1.4))

    # ribbon knot gathering the stems
    A('<g class="draw" style="animation-delay:1.75s">'
      '<path d="M212,478C226,484 254,484 268,478C270,486 270,492 268,498'
      'C254,504 226,504 212,498C210,492 210,486 212,478Z" '
      'fill="none" stroke="url(#goldL)" stroke-width="1.3" pathLength="1"/>'
      '<path d="M216,486C202,504 196,516 202,532L214,524 218,536'
      'C222,518 224,502 226,490Z" fill="none" stroke="url(#goldL)" '
      'stroke-width="1.1" pathLength="1"/>'
      '<path d="M264,486C278,504 284,516 278,532L266,524 262,536'
      'C258,518 256,502 254,490Z" fill="none" stroke="url(#goldL)" '
      'stroke-width="1.1" pathLength="1"/></g>')

    # sparkle dust for a touch of luxury
    spark = "M0,-1 L.22,-.22 L1,0 L.22,.22 L0,1 L-.22,.22 L-1,0 L-.22,-.22Z"
    for sx, sy, sc, d in [(148, 214, 6, 0.3), (338, 224, 5.5, 1.6), (240, 158, 5, 2.6)]:
        A(f'<g transform="translate({sx},{sy}) scale({sc})">'
          f'<g class="spark" style="animation-delay:{d+1.9:.2f}s">'
          f'<path d="{spark}" fill="#E7C88C"/></g></g>')

    A("""<style>
.spark{opacity:0}
@media (prefers-reduced-motion:no-preference){
 .draw{stroke-dasharray:1;stroke-dashoffset:1;
   animation:draw 1.1s cubic-bezier(.22,.8,.3,1) both}
 @keyframes draw{to{stroke-dashoffset:0}}
 .p{transform-box:fill-box;
    animation:bloom .7s cubic-bezier(.28,1.5,.5,1) both}
 @keyframes bloom{0%{transform:scale(.2);opacity:0}
   60%{opacity:1}100%{transform:scale(1);opacity:1}}
 .heartpulse{transform-box:fill-box;transform-origin:50% 50%;
   animation:pulse 4.4s ease-in-out infinite}
 @keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
 .spark{transform-box:fill-box;transform-origin:center;
   animation:spark 3.6s ease-in-out infinite both}
 @keyframes spark{0%,100%{opacity:0;transform:scale(.2) rotate(0)}
   50%{opacity:.9;transform:scale(1) rotate(90deg)}}
}
</style></svg>""")
    return "".join(L)

if __name__ == "__main__":
    svg = build()
    out = sys.argv[1] if len(sys.argv) > 1 else "story-bouquet.svg"
    with open(out, "w") as fh:
        fh.write(svg)
    print(f"{out}: {len(svg)/1024:.1f} KB")
