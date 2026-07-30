#!/usr/bin/env python3
"""Generate a realistic animated bouquet SVG for the Flowers by Tavi hero."""
import math, random, sys

R = random.Random(11)
W, H = 560, 640

def n(v):
    return f"{round(v, 1):g}"

# ── petal / leaf geometry ─────────────────────────────────────────

def petal_path(w, h, ruffles=0, tip=1.0, lean=0.0):
    """Cupped petal, base at (0,0), pointing up. `lean` furls it sideways."""
    lx, rx = -w*(1.05 + lean*0.55), w*(1.05 - lean*0.55)
    tx = -w*lean*0.45
    p = ["M0,0",
         f"C{n(lx)},{n(-h*0.28)} {n(-w*0.95 + tx)},{n(-h*0.78)} "
         f"{n(-w*0.32 + tx)},{n(-h*tip)}"]
    if ruffles <= 0:
        p.append(f"C{n(-w*0.13 + tx)},{n(-h*(tip+0.08))} {n(w*0.13 + tx)},"
                 f"{n(-h*(tip+0.08))} {n(w*0.32 + tx)},{n(-h*tip)}")
    else:
        cnt = ruffles*2
        xs = [-w*0.32 + tx + (w*0.64)*(i/cnt) for i in range(cnt+1)]
        for i in range(1, cnt+1):
            x0, x1 = xs[i-1], xs[i]
            cy = -h*(tip + (0.15 if i % 2 else -0.03))
            p.append(f"Q{n((x0+x1)/2)},{n(cy)} {n(x1)},{n(-h*tip)}")
    p.append(f"C{n(w*0.95 + tx)},{n(-h*0.78)} {n(rx)},{n(-h*0.28)} 0,0Z")
    return "".join(p)

def leaf_path(w, h):
    return (f"M0,0C{n(-w)},{n(-h*0.34)} {n(-w*0.72)},{n(-h*0.86)} 0,{n(-h)}"
            f"C{n(w*0.72)},{n(-h*0.86)} {n(w)},{n(-h*0.34)} 0,0Z")

# ── colour families: (deep base, mid, lit tip) per ring, outer→inner ──
TONES = {
    "rose": [("#7A1024", "#B32B42", "#DC6274"), ("#5E0A1C", "#8F1E33", "#B93A4E"),
             ("#420513", "#6B1224", "#93213A"), ("#2A0209", "#480A16", "#6B1526")],
    "peony": [("#8E1A55", "#C43D7E", "#F0A0C6"), ("#711244", "#A32C68", "#CE5B94"),
              ("#570C33", "#821F50", "#A93C72"), ("#3A0620", "#5C1237", "#7F2352")],
    "wine": [("#5A0E33", "#8A2454", "#B4527E"), ("#460925", "#6E1940", "#933160"),
             ("#320617", "#521030", "#762348"), ("#1E030D", "#3A091E", "#581432")],
    "cream": [("#C9A075", "#EBD6BA", "#FFFAF2"), ("#B58C63", "#DCC4A4", "#F8EEDF"),
              ("#9C7350", "#C4A784", "#E6D6C0"), ("#7E5A3C", "#A88B66", "#CDB795")],
}

def gradients():
    o = []
    for fam, tones in TONES.items():
        for i, (b, m, t) in enumerate(tones):
            o.append(f'<linearGradient id="{fam}{i}" x1=".15" y1="1" x2="0" y2="0">'
                     f'<stop offset="0" stop-color="{b}"/>'
                     f'<stop offset=".42" stop-color="{m}"/>'
                     f'<stop offset="1" stop-color="{t}"/></linearGradient>')
    o += [
        '<linearGradient id="sheen" x1=".1" y1="1" x2=".35" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".7" stop-color="#fff" stop-opacity=".26"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity=".02"/></linearGradient>',

        '<linearGradient id="cup" x1="0" y1="1" x2="0" y2="0">'
        '<stop offset="0" stop-color="#1C0208" stop-opacity=".5"/>'
        '<stop offset="1" stop-color="#1C0208" stop-opacity="0"/></linearGradient>',

        '<linearGradient id="leafG" x1="0" y1="1" x2=".35" y2="0">'
        '<stop offset="0" stop-color="#12301E"/><stop offset=".55" stop-color="#2F6845"/>'
        '<stop offset="1" stop-color="#79A382"/></linearGradient>',
        '<linearGradient id="leafD" x1="0" y1="1" x2=".35" y2="0">'
        '<stop offset="0" stop-color="#0A1F13"/><stop offset="1" stop-color="#26543A"/>'
        '</linearGradient>',
        '<linearGradient id="eucG" x1="0" y1="1" x2=".4" y2="0">'
        '<stop offset="0" stop-color="#4A6B54"/><stop offset=".6" stop-color="#7B9C82"/>'
        '<stop offset="1" stop-color="#B4C9B4"/></linearGradient>',
        '<linearGradient id="eucD" x1="0" y1="1" x2=".4" y2="0">'
        '<stop offset="0" stop-color="#2A4433"/><stop offset="1" stop-color="#5E7F68"/>'
        '</linearGradient>',

        '<linearGradient id="goldG" x1=".1" y1="1" x2=".7" y2="0">'
        '<stop offset="0" stop-color="#6E5228"/><stop offset=".3" stop-color="#B4914F"/>'
        '<stop offset=".55" stop-color="#F7E9C2"/><stop offset=".78" stop-color="#C7A45E"/>'
        '<stop offset="1" stop-color="#8A6A35"/></linearGradient>',
        '<linearGradient id="goldE" x1="0" y1="0" x2=".9" y2="1">'
        '<stop offset="0" stop-color="#A8853F"/><stop offset=".42" stop-color="#F7EAC6"/>'
        '<stop offset="1" stop-color="#856A34"/></linearGradient>',

        '<linearGradient id="wrapA" x1=".1" y1="0" x2=".9" y2="1">'
        '<stop offset="0" stop-color="#FFFCF6"/><stop offset=".38" stop-color="#F3E3D2"/>'
        '<stop offset=".74" stop-color="#DCC0A8"/>'
        '<stop offset="1" stop-color="#BE9C82"/></linearGradient>',
        '<linearGradient id="wrapB" x1=".2" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#E4D0BA"/><stop offset=".55" stop-color="#C2A488"/>'
        '<stop offset="1" stop-color="#95795F"/></linearGradient>',
        '<linearGradient id="wrapIn" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#7A3F3A" stop-opacity=".55"/>'
        '<stop offset="1" stop-color="#7A3F3A" stop-opacity="0"/></linearGradient>',

        '<linearGradient id="stemG" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#1B3A25"/><stop offset=".45" stop-color="#4A7A52"/>'
        '<stop offset="1" stop-color="#1B3A25"/></linearGradient>',

        '<radialGradient id="bgG" cx="44%" cy="32%" r="80%">'
        '<stop offset="0" stop-color="#FEF4EE"/><stop offset=".48" stop-color="#F6DAD3"/>'
        '<stop offset="1" stop-color="#E4B6AF"/></radialGradient>',
        '<radialGradient id="warmG" cx="50%" cy="50%" r="50%">'
        '<stop offset="0" stop-color="#FFEAD6" stop-opacity=".9"/>'
        '<stop offset="1" stop-color="#FFEAD6" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="maskG" cx="50%" cy="50%" r="50%">'
        '<stop offset="0" stop-color="#3A0616" stop-opacity=".85"/>'
        '<stop offset=".65" stop-color="#3A0616" stop-opacity=".45"/>'
        '<stop offset="1" stop-color="#3A0616" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="bokehG" cx="50%" cy="50%" r="50%">'
        '<stop offset="0" stop-color="#FFF7E4" stop-opacity=".85"/>'
        '<stop offset=".7" stop-color="#FBE3C9" stop-opacity=".3"/>'
        '<stop offset="1" stop-color="#FBE3C9" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="vigG" cx="50%" cy="42%" r="64%">'
        '<stop offset=".55" stop-color="#7A3540" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#7A3540" stop-opacity=".3"/></radialGradient>',
        '<linearGradient id="shimG" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".5"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',

        '<filter id="blur8" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="10"/></filter>',
        '<filter id="blur20" x="-40%" y="-40%" width="180%" height="180%">'
        '<feGaussianBlur stdDeviation="22"/></filter>',
        '<filter id="softd" x="-40%" y="-40%" width="180%" height="185%">'
        '<feDropShadow dx="1" dy="5" stdDeviation="5" flood-color="#33040F" '
        'flood-opacity=".4"/></filter>',
        f'<clipPath id="bqClip"><rect width="{W}" height="{H}"/></clipPath>',
    ]
    return "".join(o)

# ── flower construction ───────────────────────────────────────────
# rings: (petal count, size ratio, ruffles, lean, spiral offset ratio)
SPECS = {
    "rose": {"rings": [(7, 1.00, 0, 0.00, 0.00), (6, 0.78, 0, 0.12, 0.05),
                       (5, 0.56, 0, 0.26, 0.09), (4, 0.38, 0, 0.42, 0.12)],
             "core": 3, "coreh": 0.24, "wr": 0.74},
    "peony": {"rings": [(10, 1.00, 3, 0.00, 0.00), (9, 0.80, 3, 0.08, 0.03),
                        (7, 0.60, 2, 0.18, 0.06), (6, 0.42, 2, 0.30, 0.08)],
              "core": 5, "coreh": 0.22, "wr": 0.68},
    "bud": {"rings": [(5, 1.00, 0, 0.10, 0.00), (4, 0.66, 0, 0.28, 0.06)],
            "core": 3, "coreh": 0.34, "wr": 0.80},
}

def petal(w, h, fill, ruffles, lean, delay, rot, dx, dy, scale):
    d = petal_path(w, h, ruffles, 1.0, lean)
    parts = [f'<path d="{d}" fill="url(#{fill})" stroke="#2A0410" '
             f'stroke-opacity=".38" stroke-width=".8"/>']
    if h >= 20:
        parts.append(f'<path d="{petal_path(w*0.70, h*0.34, 0, 1.0, lean)}" '
                     f'fill="url(#cup)"/>')
        parts.append(f'<path d="{petal_path(w*0.44, h*0.62, 0, 1.0, lean)}" '
                     f'fill="url(#sheen)"/>')
    return (f'<g transform="translate({n(dx)},{n(dy)}) rotate({n(rot)}) scale({n(scale)})">'
            f'<g class="p" style="animation-delay:{delay:.2f}s">' + "".join(parts) +
            '</g></g>')

def flower(cx, cy, radius, kind, fam, dbase, rot=0.0, swd=5.0, swp=0.0,
           bod=3.6, bop=0.0, yscale=1.0):
    spec, tones = SPECS[kind], TONES[fam]
    nr = len(spec["rings"])
    body = []
    # soft occlusion pool under the bloom so gaps read as depth
    body.append(f'<ellipse class="pool" style="animation-delay:{dbase:.2f}s" '
                f'rx="{n(radius*0.98)}" ry="{n(radius*0.88)}" fill="url(#maskG)"/>')
    spiral = rot
    for ri, (count, rs, ruf, lean, soff) in enumerate(spec["rings"]):
        h, w = radius*rs, radius*rs*spec["wr"]
        fill = f"{fam}{min(ri, len(tones)-1)}"
        delay = dbase + (nr - ri)*0.08
        step = 360.0/count
        spiral += 137.5*0.28          # golden-angle drift → spiral, not rosette
        sr = math.radians(spiral*1.6)
        ox, oy = math.sin(sr)*radius*soff, -math.cos(sr)*radius*soff
        br = radius*rs*0.19
        for i in range(count):
            a = spiral + i*step + R.uniform(-7, 7)
            rad = math.radians(a)
            body.append(petal(w, h, fill, ruf, lean, delay + i*0.012, a,
                              ox + math.sin(rad)*br, oy - math.cos(rad)*br,
                              R.uniform(0.92, 1.08)))
    ch = radius*spec["coreh"]
    cf = f"{fam}{len(tones)-1}"
    for i in range(spec["core"]):
        a = rot + i*(360.0/spec["core"]) + 24
        body.append(petal(ch*0.66, ch, cf, 0, 0.55, dbase, a, 0, 0, 1.0))
    body.append(f'<circle r="{n(radius*0.045)}" fill="#180207" opacity=".7"/>')
    ys = f" scale(1,{n(yscale)})" if yscale != 1.0 else ""
    return (f'<g transform="translate({n(cx)},{n(cy)}){ys}" filter="url(#softd)">'
            f'<g class="sway" style="animation-duration:{swd}s;animation-delay:-{swp}s">'
            f'<g class="bob" style="animation-duration:{bod}s;animation-delay:-{bop}s">'
            + "".join(body) + '</g></g></g>')

# ── greenery ──────────────────────────────────────────────────────

def sprig(cx, cy, ang, length, delay, pairs=6, size=9.0, grad="eucG",
          swd=6.0, swp=0.0):
    rad = math.radians(ang)
    tx, ty = cx + math.sin(rad)*length, cy - math.cos(rad)*length
    perp = math.radians(ang + 90)
    bow = length*0.17
    c1x, c1y = (cx + math.sin(rad)*length*0.35 + math.sin(perp)*bow,
                cy - math.cos(rad)*length*0.35 - math.cos(perp)*bow)
    c2x, c2y = (cx + math.sin(rad)*length*0.72 + math.sin(perp)*bow*0.7,
                cy - math.cos(rad)*length*0.72 - math.cos(perp)*bow*0.7)
    parts = [f'<path d="M{n(cx)},{n(cy)}C{n(c1x)},{n(c1y)} {n(c2x)},{n(c2y)} '
             f'{n(tx)},{n(ty)}" fill="none" stroke="#4A6B54" stroke-width="1.8" '
             f'stroke-linecap="round"/>']

    def bez(t):
        m = 1-t
        return (m**3*cx + 3*m*m*t*c1x + 3*m*t*t*c2x + t**3*tx,
                m**3*cy + 3*m*m*t*c1y + 3*m*t*t*c2y + t**3*ty)

    for i in range(pairs):
        t = 0.20 + 0.78*(i/max(1, pairs-1))
        px, py = bez(t)
        s = size*(1.0 - 0.42*t)
        for sgn in (-1, 1):
            lx, ly = px + math.sin(perp)*s*0.92*sgn, py - math.cos(perp)*s*0.92*sgn
            parts.append(
                f'<ellipse cx="{n(lx)}" cy="{n(ly)}" rx="{n(s)}" ry="{n(s*1.22)}" '
                f'fill="url(#{grad})" stroke="#2A4433" stroke-opacity=".45" '
                f'stroke-width=".6" transform="rotate({n(ang*0.55)} {n(lx)} {n(ly)})"/>')
    return (f'<g class="sway" style="animation-duration:{swd}s;animation-delay:-{swp}s;'
            f'transform-origin:{n(cx)}px {n(cy)}px">'
            f'<g class="grow" style="animation-delay:{delay:.2f}s;'
            f'transform-origin:{n(cx)}px {n(cy)}px">' + "".join(parts) + '</g></g>')

def big_leaf(cx, cy, ang, w, h, delay, grad="leafG", swd=5.5, swp=0.0):
    return (f'<g transform="translate({n(cx)},{n(cy)}) rotate({n(ang)})">'
            f'<g class="sway" style="animation-duration:{swd}s;animation-delay:-{swp}s">'
            f'<g class="grow" style="animation-delay:{delay:.2f}s">'
            f'<path d="{leaf_path(w, h)}" fill="url(#{grad})" stroke="#0A1F13" '
            f'stroke-opacity=".5" stroke-width=".7"/>'
            f'<path d="M0,{n(-h*0.06)}L0,{n(-h*0.9)}" stroke="#D8E6D2" '
            f'stroke-width=".8" opacity=".3" fill="none"/></g></g></g>')

def breath(cx, cy, spread, count, delay, swd=4.4, swp=0.0):
    parts = []
    for _ in range(count):
        a, r = R.uniform(0, 360), R.uniform(spread*0.3, spread)
        x = cx + math.cos(math.radians(a))*r
        y = cy + math.sin(math.radians(a))*r*0.85
        parts.append(f'<path d="M{n(cx)},{n(cy)}Q{n((cx+x)/2)},{n((cy+y)/2-5)} '
                     f'{n(x)},{n(y)}" fill="none" stroke="#6E8C72" stroke-width=".9" '
                     f'opacity=".75"/>')
        rr = R.uniform(2.6, 4.2)
        parts.append(f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(rr)}" fill="#FFFCF6" '
                     f'stroke="#C9A282" stroke-opacity=".6" stroke-width=".5"/>')
        parts.append(f'<circle cx="{n(x-rr*0.2)}" cy="{n(y-rr*0.2)}" r="{n(rr*0.3)}" '
                     f'fill="#E0B968"/>')
    return (f'<g class="sway" style="animation-duration:{swd}s;animation-delay:-{swp}s;'
            f'transform-origin:{n(cx)}px {n(cy)}px">'
            f'<g class="grow" style="animation-delay:{delay:.2f}s;'
            f'transform-origin:{n(cx)}px {n(cy)}px">' + "".join(parts) + '</g></g>')

# ── build ─────────────────────────────────────────────────────────

def build():
    L = []
    A = L.append
    A(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" '
      f'height="{H}" role="img" shape-rendering="geometricPrecision" '
      f'aria-label="An animated luxury bouquet of roses and peonies wrapped in paper '
      f'with a gold ribbon and the Tavi monogram">'
      f'<title>Flowers by Tavi</title><defs>{gradients()}</defs>'
      f'<g clip-path="url(#bqClip)"><rect width="{W}" height="{H}" fill="url(#bgG)"/>'
      f'<ellipse cx="276" cy="248" rx="252" ry="242" fill="url(#warmG)"/>')

    for bx, by, br, dur, ph in [(70, 120, 34, 26, 0), (486, 96, 26, 31, 7),
                                (44, 424, 30, 29, 14), (508, 392, 22, 24, 4),
                                (300, 58, 20, 33, 19), (150, 556, 26, 28, 11)]:
        A(f'<circle class="drift" cx="{bx}" cy="{by}" r="{br}" fill="url(#bokehG)" '
          f'filter="url(#blur8)" style="animation-duration:{dur}s;animation-delay:-{ph}s"/>')

    # deep shadow mass behind the flower cluster → gaps read as depth
    A('<g filter="url(#blur20)" opacity=".55">'
      '<ellipse cx="278" cy="256" rx="196" ry="168" fill="#4A0A1E"/>'
      '<ellipse cx="170" cy="300" rx="96" ry="88" fill="#3A0716"/>'
      '<ellipse cx="392" cy="290" rx="92" ry="84" fill="#3A0716"/></g>')

    # ── greenery, fanning out past the blooms ────────────────────
    for sx, sy, ang, ln, ps, sz, d, g, sw, ph in [
            (268, 404, -74, 268, 8, 11.0, 0.28, "eucD", 6.6, 0.0),
            (282, 404,  72, 262, 8, 11.0, 0.32, "eucD", 7.1, 2.2),
            (270, 402, -42, 316, 9, 10.5, 0.24, "eucG", 6.2, 4.0),
            (288, 402,  40, 310, 9, 10.5, 0.26, "eucG", 6.9, 1.1),
            (276, 400, -14, 342, 9,  9.8, 0.20, "eucG", 6.4, 3.3),
            (286, 400,  16, 336, 9,  9.8, 0.22, "eucD", 7.3, 5.0),
            (262, 406, -96, 214, 6, 10.5, 0.36, "eucD", 6.0, 2.7),
            (296, 406,  96, 208, 6, 10.5, 0.38, "eucD", 6.7, 4.4),
            (266, 404, -58, 292, 8, 10.0, 0.30, "eucG", 5.8, 5.6),
            (292, 404,  56, 286, 8, 10.0, 0.34, "eucG", 6.5, 1.9)]:
        A(sprig(sx, sy, ang, ln, d, ps, sz, g, sw, ph))

    for cx, cy, ang, w, h, d, g, sw, ph in [
            (188, 378, -56, 22, 112, 0.42, "leafD", 5.8, 0.6),
            (372, 372,  56, 22, 110, 0.44, "leafD", 6.1, 2.9),
            (234, 362, -22, 20, 128, 0.46, "leafG", 5.4, 1.7),
            (330, 358,  22, 20, 124, 0.48, "leafG", 5.9, 3.8),
            (140, 344, -78, 19, 96, 0.50, "leafD", 5.6, 4.6),
            (420, 336,  78, 19, 94, 0.52, "leafD", 6.3, 0.9),
            (206, 348, -38, 18, 104, 0.54, "leafG", 5.2, 2.4),
            (356, 344,  38, 18, 102, 0.56, "leafG", 6.0, 4.1)]:
        A(big_leaf(cx, cy, ang, w, h, d, g, sw, ph))

    # ── stems + paper wrap ───────────────────────────────────────
    A('<g class="grow" style="animation-delay:.08s;transform-origin:280px 610px">'
      '<g fill="none" stroke="url(#stemG)" stroke-width="4.5" stroke-linecap="round">')
    for d in ["M282,312C280,388 284,446 281,502", "M204,330C228,398 260,452 274,504",
              "M364,324C342,396 304,452 288,504", "M166,360C200,420 250,466 270,506",
              "M404,352C372,418 318,466 292,506", "M242,346C254,406 268,458 277,506"]:
        A(f'<path d="{d}"/>')
    A('</g>')
    # back panel — paper flares up and out at the shoulders, tapers to the stems
    A('<path d="M104,350C132,472 206,562 236,614L324,614C354,562 428,470 456,344'
      'C420,392 372,408 336,400C308,394 294,382 280,384C266,382 252,394 224,400'
      'C188,408 140,394 104,350Z" fill="url(#wrapB)" stroke="#8E7358" '
      'stroke-width="1"/>')
    # front panel
    A('<path d="M148,378C170,482 224,570 248,614L312,614C336,570 390,480 412,372'
      'C384,412 344,424 316,418C298,414 290,404 280,406C270,404 262,414 244,418'
      'C216,424 176,414 148,378Z" fill="url(#wrapA)" stroke="#B4967C" '
      'stroke-width="1"/>')
    # interior shadow where the stems disappear into the paper
    A('<path d="M148,378C176,414 216,424 244,418C262,414 270,404 280,406'
      'C290,404 298,414 316,418C344,424 384,412 412,372C392,428 344,452 280,452'
      'C216,452 168,428 148,378Z" fill="url(#wrapIn)"/>')
    A('<g fill="none" stroke="#A8886C" stroke-width="1.1" opacity=".55">')
    for d in ["M196,410C212,486 244,566 254,612", "M280,412C280,490 280,560 280,612",
              "M366,404C350,482 316,566 306,612", "M162,388C176,470 214,566 234,614",
              "M400,382C386,466 346,566 326,614"]:
        A(f'<path d="{d}"/>')
    A('</g></g>')

    # ── blooms, back → front ─────────────────────────────────────
    blooms = [
        # cx,  cy,  r, kind,   fam,     dly,  rot, swd, swp, bod, bop, ysc
        (256, 106, 32, "bud",   "wine",  0.60,  14, 5.2, 0.4, 3.4, 1.1, 1.00),
        (356,  98, 30, "bud",   "wine",  0.62, 200, 5.7, 2.6, 3.8, 0.3, 1.00),
        (108, 244, 32, "bud",   "wine",  0.64, 120, 4.9, 1.5, 3.2, 2.5, 1.00),
        (456, 228, 30, "bud",   "rose",  0.66, 300, 5.4, 3.8, 3.6, 0.7, 1.00),
        (176, 156, 46, "rose",  "rose",  0.84,  25, 5.0, 1.3, 3.6, 2.4, 0.95),
        (398, 148, 44, "rose",  "wine",  0.86,  70, 5.9, 0.7, 3.3, 3.0, 0.95),
        (300, 154, 42, "peony", "cream", 0.88, 130, 5.5, 3.1, 4.0, 0.8, 0.94),
        (100, 322, 42, "rose",  "wine",  0.90, 190, 6.2, 2.1, 4.2, 1.6, 0.97),
        (466, 306, 40, "rose",  "peony", 0.92,  40, 5.3, 4.2, 3.7, 2.8, 0.97),
        (140, 386, 46, "rose",  "rose",  1.02, 100, 4.8, 1.8, 3.1, 0.5, 0.98),
        (430, 372, 44, "peony", "peony", 1.04, 250, 5.1, 3.7, 3.5, 2.1, 0.98),
        (196, 268, 60, "rose",  "cream", 1.12, 155, 6.0, 1.0, 4.4, 3.4, 0.96),
        (388, 254, 56, "rose",  "rose",  1.16,  95, 5.6, 3.4, 4.6, 1.2, 0.96),
        (286, 380, 44, "rose",  "wine",  1.20,  60, 5.0, 2.7, 3.9, 4.0, 0.98),
        (284, 262, 74, "peony", "peony", 1.34,  10, 6.4, 2.4, 4.8, 3.6, 0.95),
    ]
    breaths = [(84, 176, 32, 8, 0.68, 4.6, 0.5), (478, 168, 30, 8, 0.70, 4.2, 2.3),
               (218, 74, 28, 7, 0.64, 4.9, 1.4), (348, 62, 26, 7, 0.66, 4.4, 3.1),
               (60, 384, 26, 6, 0.74, 4.1, 0.9), (500, 366, 24, 6, 0.76, 4.7, 2.8),
               (348, 316, 22, 5, 0.80, 4.3, 1.8), (216, 330, 22, 5, 0.82, 4.5, 3.6)]
    bi = 0
    for i, b in enumerate(blooms):
        A(flower(*b))
        if i in (3, 6, 9, 11) and bi < len(breaths):
            A(breath(*breaths[bi])); bi += 1
            if bi < len(breaths):
                A(breath(*breaths[bi])); bi += 1
    while bi < len(breaths):
        A(breath(*breaths[bi])); bi += 1

    # ── ribbon + bow ─────────────────────────────────────────────
    A('<g class="grow" style="animation-delay:1.55s;transform-origin:280px 500px">'
      # ribbon band cinching the paper
      '<path d="M216,486C244,496 316,496 344,486C346,500 346,510 344,522'
      'C316,532 244,532 216,522C214,510 214,500 216,486Z" '
      'fill="url(#goldG)" stroke="#6E5228" stroke-width=".9"/>'
      # swallowtail streamers
      '<g class="tail" style="animation-delay:-0.4s;transform-origin:266px 520px">'
      '<path d="M258,518C246,556 238,584 214,610L236,598L240,616'
      'C260,586 272,556 278,522Z" fill="url(#goldE)" stroke="#6E5228" '
      'stroke-width=".8"/>'
      '<path d="M266,524C256,558 248,582 232,602" fill="none" stroke="#8A6A35" '
      'stroke-width=".7" opacity=".5"/></g>'
      '<g class="tail" style="animation-delay:-2.1s;transform-origin:296px 520px">'
      '<path d="M302,518C314,556 322,584 346,610L324,598L320,616'
      'C300,586 288,556 282,522Z" fill="url(#goldE)" stroke="#6E5228" '
      'stroke-width=".8"/>'
      '<path d="M294,524C304,558 312,582 328,602" fill="none" stroke="#8A6A35" '
      'stroke-width=".7" opacity=".5"/></g>'
      # left loop — teardrop, fuller at the outer end, with a fold shadow
      '<g class="loop" style="animation-delay:-0.9s;transform-origin:280px 500px">'
      '<path d="M278,498C250,470 196,466 176,488C160,506 178,528 208,524'
      'C238,520 264,510 278,498Z" fill="url(#goldG)" stroke="#6E5228" '
      'stroke-width=".9"/>'
      '<path d="M278,498C252,494 212,494 186,504C176,508 174,516 182,520" '
      'fill="none" stroke="#6E5228" stroke-width=".9" opacity=".45"/></g>'
      # right loop
      '<g class="loop" style="animation-delay:-2.6s;transform-origin:280px 500px">'
      '<path d="M282,498C310,470 364,466 384,488C400,506 382,528 352,524'
      'C322,520 296,510 282,498Z" fill="url(#goldG)" stroke="#6E5228" '
      'stroke-width=".9"/>'
      '<path d="M282,498C308,494 348,494 374,504C384,508 386,516 378,520" '
      'fill="none" stroke="#6E5228" stroke-width=".9" opacity=".45"/></g>'
      # knot gathering the loops
      '<path d="M266,486C276,482 284,482 294,486C298,494 298,506 294,514'
      'C284,518 276,518 266,514C262,506 262,494 266,486Z" '
      'fill="url(#goldE)" stroke="#6E5228" stroke-width=".9"/></g>')

    # ── monogram medallion ───────────────────────────────────────
    A('<g class="pop" style="animation-delay:2s;transform-origin:280px 500px">'
      '<circle cx="280" cy="500" r="27" fill="#FFFDFB" stroke="url(#goldE)" '
      'stroke-width="2.8"/>'
      '<circle cx="280" cy="500" r="21.5" fill="none" stroke="#C9A96E" '
      'stroke-width=".9" opacity=".75"/>'
      '<text x="280" y="511" text-anchor="middle" font-size="28" fill="#A96A74" '
      'font-family="Georgia,\'Times New Roman\',serif">T</text>'
      '<g class="glint"><circle cx="280" cy="500" r="27" fill="url(#shimG)" '
      'opacity=".55"/></g></g>')

    # ── sparkle dust ─────────────────────────────────────────────
    spark = "M0,-1 L.22,-.22 L1,0 L.22,.22 L0,1 L-.22,.22 L-1,0 L-.22,-.22Z"
    for sx, sy, s, d in [(66, 148, 9, 0.0), (494, 124, 7, 0.7), (48, 300, 7, 1.5),
                         (512, 268, 8, 0.3), (280, 46, 6, 1.9), (416, 500, 7, 1.1),
                         (146, 508, 6, 2.3), (368, 74, 5, 0.5), (198, 68, 5, 1.7),
                         (492, 546, 6, 2.6), (66, 548, 5, 0.9), (280, 616, 6, 2.0),
                         (128, 424, 5, 1.3), (438, 434, 5, 2.4)]:
        A(f'<g transform="translate({sx},{sy}) scale({s})">'
          f'<g class="spark" style="animation-delay:{d+2.15:.2f}s">'
          f'<path d="{spark}" fill="#E7C88C"/>'
          f'<path d="{spark}" fill="#FFF8E6" transform="scale(.5)"/></g></g>')

    # ── drifting petals ──────────────────────────────────────────
    for px, py, rot, fam, sc, dur, dl in [
            (150, 150, 24, "peony0", 1.0, 13, 3.0), (424, 196, -30, "rose0", 0.85, 16, 8.0),
            (256, 118, 12, "wine0", 0.75, 14, 12.5), (368, 306, -18, "peony1", 0.9, 18, 5.5),
            (196, 232, 34, "cream0", 0.8, 15, 17.0)]:
        A(f'<g class="fall" style="animation-duration:{dur}s;animation-delay:{dl}s">'
          f'<g transform="translate({px},{py}) rotate({rot}) scale({sc})">'
          f'<path d="{petal_path(14, 24)}" fill="url(#{fam})" stroke="#2A0410" '
          f'stroke-opacity=".3" stroke-width=".6"/></g></g>')

    A(f'<g class="shim"><rect x="-190" y="-60" width="150" height="{H+140}" '
      f'fill="url(#shimG)" transform="rotate(16 280 300)"/></g>'
      f'<rect width="{W}" height="{H}" fill="url(#vigG)"/></g>')

    A("""<style>
/* static fallback: the composition is complete without motion, but the
   effects that only make sense in flight are hidden */
.shim,.fall,.glint{opacity:0}
.spark{opacity:.5}
@media (prefers-reduced-motion:no-preference){
 .p{transform-box:fill-box;transform-origin:50% 100%;
    animation:bloom .95s cubic-bezier(.28,1.5,.5,1) both}
 @keyframes bloom{0%{transform:scale(.06) rotate(-18deg);opacity:0}
   55%{opacity:1}100%{transform:scale(1) rotate(0);opacity:1}}
 .grow{animation:grow 1.1s cubic-bezier(.22,1.2,.4,1) both}
 @keyframes grow{0%{transform:scale(.22);opacity:0}100%{transform:scale(1);opacity:1}}
 .pool{animation:pool .9s ease-out both}
 @keyframes pool{0%{opacity:0}100%{opacity:1}}
 .pop{animation:pop .85s cubic-bezier(.24,1.7,.5,1) both}
 @keyframes pop{0%{transform:scale(0) rotate(-45deg);opacity:0}
   100%{transform:scale(1) rotate(0);opacity:1}}
 .sway{transform-box:fill-box;transform-origin:50% 100%;animation-name:sway;
   animation-timing-function:ease-in-out;animation-iteration-count:infinite}
 @keyframes sway{0%,100%{transform:rotate(-1.6deg)}50%{transform:rotate(1.6deg)}}
 .bob{transform-box:fill-box;transform-origin:50% 100%;animation-name:bob;
   animation-timing-function:ease-in-out;animation-iteration-count:infinite}
 @keyframes bob{0%,100%{transform:translateY(3px) scale(.99)}
   50%{transform:translateY(-4px) scale(1.01)}}
 .tail{animation:tail 5.5s ease-in-out infinite}
 @keyframes tail{0%,100%{transform:rotate(-3.5deg) skewX(2deg)}
   50%{transform:rotate(3.5deg) skewX(-2deg)}}
 .loop{animation:loop 6s ease-in-out infinite}
 @keyframes loop{0%,100%{transform:scaleY(.96) rotate(-1deg)}
   50%{transform:scaleY(1.04) rotate(1deg)}}
 .drift{animation-name:drift;animation-timing-function:ease-in-out;
   animation-iteration-count:infinite}
 @keyframes drift{0%,100%{transform:translate(0,0) scale(1)}
   33%{transform:translate(16px,-22px) scale(1.16)}
   66%{transform:translate(-14px,14px) scale(.88)}}
 .spark{transform-box:fill-box;transform-origin:center;
   animation:spark 3.2s ease-in-out infinite both}
 @keyframes spark{0%,100%{opacity:0;transform:scale(.2) rotate(0)}
   50%{opacity:1;transform:scale(1) rotate(90deg)}}
 .fall{animation-name:fall;animation-timing-function:linear;
   animation-iteration-count:infinite}
 @keyframes fall{0%{transform:translate(0,0) rotate(0);opacity:0}
   6%{opacity:.9}80%{opacity:.9}
   100%{transform:translate(-80px,480px) rotate(320deg);opacity:0}}
 .shim{animation:shim 8s cubic-bezier(.5,0,.5,1) infinite}
 @keyframes shim{0%{transform:translateX(0);opacity:0}4%{opacity:.8}
   26%{transform:translateX(780px);opacity:0}100%{transform:translateX(780px);opacity:0}}
 .glint{transform-box:fill-box;transform-origin:center;
   animation:glint 7s ease-in-out infinite}
 @keyframes glint{0%,88%,100%{opacity:0}94%{opacity:.75}}
}
</style></svg>""")
    return "".join(L)

if __name__ == "__main__":
    svg = build()
    out = sys.argv[1] if len(sys.argv) > 1 else "bouquet.svg"
    with open(out, "w") as fh:
        fh.write(svg)
    print(f"{out}: {len(svg)/1024:.1f} KB, {svg.count('<path')} paths, "
          f"{svg.count('<ellipse')} ellipses, {svg.count('<circle')} circles")
