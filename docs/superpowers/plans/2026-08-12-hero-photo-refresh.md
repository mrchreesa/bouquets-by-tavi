# Hero Photo Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the hero section's illustrated bouquet with the real bouquet photo (`images/bouquet.png`), move the displaced illustration into the Our Story section in place of its current line-art placeholder, and add a gold line-art decorative background layer (corner florals, sparkle dust, a drifting petal) behind the hero, per `docs/superpowers/specs/2026-08-12-hero-photo-refresh-design.md`.

**Architecture:** Two new Python generator/processing scripts in `tools/` (following the existing `gen_hero_bouquet.py` / `gen_story_bouquet.py` convention — a script emits a checked-in asset, with a "regenerate with" comment at its point of use), plus HTML/CSS edits in `index.html` and `css/style.css`. No build step, no new dependencies beyond Pillow/numpy/scipy, all three already installed in this environment.

**Tech Stack:** Same as the rest of the site — static HTML/CSS/vanilla JS, no framework. Verified via `python3 -m http.server` + Playwright MCP against `http://localhost:8000`, matching the verification style used in `docs/superpowers/plans/2026-07-30-hero-bouquet-animation-design.md`'s implementation.

## Global Constraints

- No build step, no framework — plain files only.
- `images/bouquet.png` (the source photo) is never modified in place — all processing writes to a new file.
- `images/story.svg`, `images/hero.svg`, and their generators stay in the repo, unused — do not delete them (matches existing precedent for superseded hero assets).
- All new animation (sparkle twinkle, petal drift) must live inside `@media (prefers-reduced-motion: no-preference)`; outside that query, every element must render in a complete, static, fully-visible state — no `opacity: 0` elements left stranded without the query.
- The decorative background layer must never intercept clicks: `pointer-events: none`.
- No horizontal overflow at 375px viewport width, at any point in this plan.
- Reuse the site's existing gold (`#B99668` / the `goldL` gradient pattern from `gen_story_bouquet.py`) for all new line-art — no new colors introduced.

---

### Task 1: Background-removal script for the hero photo

**Files:**
- Create: `tools/cutout_bouquet.py`
- Create (generated, not hand-edited): `images/bouquet-cutout.png`

**Interfaces:**
- Produces: `images/bouquet-cutout.png`, an RGBA PNG, 1000px wide (height proportional to the source's 1368×1150 aspect ratio, i.e. 841px), consumed by Task 2.

`images/bouquet.png` is a flat RGB PNG (1368×1150) with a solid black backing baked in — no alpha channel. Pixel sampling on this exact file (corners and a histogram of per-pixel max-channel luminance) showed a single dominant spike of ~557,000 pixels at luminance 0–4 (the background) and a separate, roughly uniform continuous tail from ~5–250 (the bouquet's own natural shadow-to-highlight range) — i.e. there's no ambiguous secondary dark cluster to worry about, but a naive global threshold would still risk punching transparent holes into legitimately dark shadow pixels *inside* the bouquet (e.g. gaps between petals). The fix verified below: flood-fill from the image border to isolate only the border-connected near-black region as "background," which leaves internal dark pixels alone.

- [ ] **Step 1: Write `tools/cutout_bouquet.py`**

```python
#!/usr/bin/env python3
"""Remove the solid black backing from a bouquet photo exported without an
alpha channel, producing a transparent cutout for use as the hero image.

Approach: flood-fill from the image border to find the border-connected
near-black region (the true background), rather than a naive global
threshold — this leaves legitimately dark pixels *inside* the bouquet
(shadow gaps between petals) untouched. The background mask is grown by a
couple of pixels before feathering to strip the anti-aliased dark fringe
that sits between the original black backing and the flowers, which is
what prevents a black halo when the cutout is composited onto a light
background."""
from PIL import Image
from scipy import ndimage
import numpy as np
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "images/bouquet.png"
OUT = sys.argv[2] if len(sys.argv) > 2 else "images/bouquet-cutout.png"
OUT_WIDTH = 1000

NEAR_BLACK = 12   # per-pixel max(R,G,B) at or below this is background-candidate
GROW_PX = 2        # dilate the background mask inward by this many pixels
FEATHER_SIGMA = 1.0  # gaussian blur applied to the alpha channel

def main():
    img = Image.open(SRC).convert("RGB")
    arr = np.asarray(img).astype(np.uint8)

    near_black = arr.max(axis=2) <= NEAR_BLACK
    labels, _ = ndimage.label(near_black, structure=np.ones((3, 3)))
    border_labels = (set(labels[0, :]) | set(labels[-1, :])
                      | set(labels[:, 0]) | set(labels[:, -1]))
    border_labels.discard(0)
    bg = np.isin(labels, list(border_labels))

    bg_grown = ndimage.binary_dilation(bg, iterations=GROW_PX)
    alpha = np.where(bg_grown, 0, 255).astype(np.float32)
    alpha = ndimage.gaussian_filter(alpha, sigma=FEATHER_SIGMA)
    alpha = np.clip(alpha, 0, 255).astype(np.uint8)

    rgba = Image.fromarray(np.dstack([arr, alpha]), mode="RGBA")

    w, h = rgba.size
    new_h = round(h * OUT_WIDTH / w)
    rgba = rgba.resize((OUT_WIDTH, new_h), Image.LANCZOS)
    rgba.save(OUT, optimize=True)

    a = np.asarray(rgba)[:, :, 3]
    print(f"{OUT}: {rgba.size[0]}x{rgba.size[1]}, "
          f"{(a == 0).sum()} fully transparent px, {(a == 255).sum()} fully opaque px, "
          f"{a.size} total")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it and check the summary output**

Run: `python3 tools/cutout_bouquet.py`
Expected: prints a line like `images/bouquet-cutout.png: 1000x841, <N1> fully transparent px, <N2> fully opaque px, 841000 total` with `<N1>` in the low-hundred-thousands (background) and `<N2>` making up most of the rest. No traceback.

- [ ] **Step 3: Visually confirm no black fringe**

Run this composite check (mirrors how the cutout will actually sit on the page — over the site's `--blush` color):

```bash
python3 -c "
from PIL import Image
cutout = Image.open('images/bouquet-cutout.png').convert('RGBA')
bg = Image.new('RGBA', cutout.size, '#F7E4DF')
Image.alpha_composite(bg, cutout).convert('RGB').save('/tmp/cutout-check.png')
"
```

Then view `/tmp/cutout-check.png` (e.g. with the Read tool, since it's an image file). Expected: the bouquet reads cleanly against the blush background with no dark/black rim around the petals or wrap paper edges. If a fringe is visible, increase `GROW_PX` to 3 in `tools/cutout_bouquet.py` and re-run Steps 2–3.

- [ ] **Step 4: Commit**

```bash
git add tools/cutout_bouquet.py images/bouquet-cutout.png images/bouquet.png
git commit -m "feat: add background-removal script and cutout for the hero bouquet photo"
```

(`images/bouquet.png` is included here since it's currently untracked and is the source asset the script depends on.)

---

### Task 2: Swap the hero image to the bouquet photo

**Files:**
- Modify: `index.html:59-62` (the `.hero-image` block)
- Modify: `css/style.css:378-387` (`.hero-image` and `.hero-image img` rules)

**Interfaces:**
- Consumes: `images/bouquet-cutout.png` from Task 1.

- [ ] **Step 1: Swap the hero `<img>`**

Change:
```html
        <div class="hero-image">
          <!-- Animated bouquet mark. Regenerate with: python3 tools/gen_hero_bouquet.py images/hero-bouquet.svg -->
          <img src="images/hero-bouquet.svg" alt="An illustrated bouquet of roses and peonies wrapped in paper, tied with a gold ribbon bearing the Tavi monogram" width="560" height="640">
        </div>
```
to:
```html
        <div class="hero-image">
          <!-- Real bouquet photo, background removed. Regenerate with: python3 tools/cutout_bouquet.py -->
          <img src="images/bouquet-cutout.png" alt="A handcrafted bouquet of blush and white roses and peonies wrapped in blush paper, tied with a satin ribbon" width="1000" height="841">
        </div>
```

- [ ] **Step 2: Restyle `.hero-image` for a photo instead of a full-bleed illustration**

Change:
```css
.hero-image {
  max-width: 420px;
  margin: 0 auto;
  width: 100%;
}

.hero-image img {
  border-radius: 260px 260px 6px 6px;
  box-shadow: 0 24px 48px -24px rgba(169, 106, 116, 0.45);
}
```
to:
```css
.hero-image {
  max-width: 480px;
  margin: 0 auto;
  width: 100%;
}

.hero-image img {
  filter: drop-shadow(0 22px 30px rgba(169, 106, 116, 0.4));
}
```

(`border-radius` + `box-shadow` were an arch-frame treatment for the old full-bleed SVG; `drop-shadow` follows the photo's actual transparent silhouette instead of boxing it, so the bouquet appears to float free like it does in the reference image.)

- [ ] **Step 3: Verify in the browser**

Run `python3 -m http.server 8000` (background). Playwright `browser_navigate` to `http://localhost:8000`.
- `browser_take_screenshot` at 1280px width: confirm the bouquet photo appears in the hero, floating on the blush background with no visible box/frame and no black fringe.
- `browser_evaluate`: `document.querySelector('.hero-image img').naturalWidth > 0` — expect `true` (image loaded, not broken).
- Check sizing: `browser_evaluate` `document.querySelector('.hero-image img').getBoundingClientRect().width` at 1280px viewport. If it renders under 380px wide (looks cramped relative to the text column), increase `.hero-image` `max-width` to `520px` and re-check.
- `browser_resize` to 375×800: `browser_evaluate` `document.documentElement.scrollWidth <= 375` — expect `true` (no overflow).

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: swap the hero illustration for the real bouquet photo"
```

---

### Task 3: Move the animated illustration into Our Story

**Files:**
- Modify: `index.html:251-254` (the `.story-image` block)

**Interfaces:**
- Consumes: `images/hero-bouquet.svg` (already exists, unchanged from before Task 2).

- [ ] **Step 1: Swap the Our Story `<img>`**

Change:
```html
        <div class="story-image">
          <!-- Generated illustration. Regenerate with: python3 tools/gen_story_bouquet.py images/story.svg -->
          <img src="images/story.svg" alt="A delicate gold line-art bouquet resting in front of a softly glowing heart, in blush pink and gold tones" width="480" height="560">
        </div>
```
to:
```html
        <div class="story-image">
          <!-- Animated bouquet mark, moved here from the hero. Regenerate with: python3 tools/gen_hero_bouquet.py images/hero-bouquet.svg -->
          <img src="images/hero-bouquet.svg" alt="An animated illustrated bouquet of roses and peonies wrapped in paper, tied with a gold ribbon bearing the Tavi monogram" width="560" height="640">
        </div>
```

No CSS changes needed — `.story-image` (`css/style.css:631-638`) wraps the image in a fixed-padding white frame and doesn't force an aspect ratio; the new width/height attributes (560×640 vs. the old 480×560) keep the intrinsic ratio correct so the browser doesn't stretch it before/while it loads.

- [ ] **Step 2: Verify in the browser**

With the dev server still running, Playwright `browser_navigate` to `http://localhost:8000#story` (or scroll to `#story`).
- `browser_take_screenshot`: confirm the animated jewel-tone bouquet illustration now appears in the Our Story section's white frame, not the old gold line-art placeholder.
- `browser_evaluate`: `document.querySelector('.story-image img').getAnimations === undefined` is expected (animations live inside the SVG document, not the host page) — instead confirm the image loaded: `document.querySelector('.story-image img').naturalWidth > 0` — expect `true`.
- Visually confirm (via the screenshot) the image isn't stretched or squashed inside the white frame.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: move the animated bouquet illustration into Our Story"
```

---

### Task 4: Decorative background layer for the hero

**Files:**
- Create: `tools/gen_hero_decor.py`
- Create (generated, not hand-edited): `images/hero-decor.svg`
- Modify: `index.html:45-46` (top of the `.hero` section)
- Modify: `css/style.css` (add a `.hero-decor` rule near the existing `.hero` rule, `css/style.css:288-292`)

**Interfaces:**
- Produces: `images/hero-decor.svg`, viewBox `0 0 1100 640`, consumed by the HTML/CSS changes in this same task.

This generator reuses the fine gold-line-art `bloom()` / `stem()` / `leaf()` drawing style already established in `tools/gen_story_bouquet.py` (rather than the hero bouquet's filled-petal style) for two corner floral clusters, adds a scatter of sparkle marks near each, and one petal that drifts down and across the hero on a loop. Static (no-motion) state: corner florals and sparkles fully drawn, sparkles at a settled lower opacity, petal at its resting position — nothing renders as invisible/incomplete without the animation.

- [ ] **Step 1: Write `tools/gen_hero_decor.py`**

```python
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
```

- [ ] **Step 2: Generate the SVG**

Run: `python3 tools/gen_hero_decor.py images/hero-decor.svg`
Expected: prints `images/hero-decor.svg: <N> KB` with no traceback.

- [ ] **Step 3: Wire it into the hero section**

Change:
```html
    <section class="hero">
      <div class="hero-inner">
```
to:
```html
    <section class="hero">
      <img class="hero-decor" src="images/hero-decor.svg" alt="" aria-hidden="true">
      <div class="hero-inner">
```

- [ ] **Step 4: Add the `.hero-decor` CSS rule**

Directly after the existing `.hero` rule in `css/style.css`:
```css
.hero {
  position: relative;
  background: linear-gradient(180deg, var(--blush-light), var(--blush));
  padding: 3.5rem 1.25rem 4rem;
}
```
add:
```css

.hero-decor {
  position: absolute;
  inset: 0;
  z-index: -1;
  width: 100%;
  height: 100%;
  object-fit: cover;
  pointer-events: none;
}
```

(`.hero` already has `position: relative`, making it the containing block/stacking context. `z-index: -1` on the decor image paints it above `.hero`'s own gradient background but below `.hero-inner`'s in-flow static content — see the design spec's stacking-order note — so it never covers the text or bouquet photo.)

- [ ] **Step 5: Add the reduced-motion note to the existing media query (no code change needed — confirm only)**

Open `css/style.css` and find the `@media (prefers-reduced-motion: reduce)` block near the end of the file. No edit is required here: every animation this task adds lives inside `@media (prefers-reduced-motion: no-preference)` in the generated SVG itself (same pattern as `hero-bouquet.svg`), so the page-level reduced-motion query doesn't need to know about it. Just confirm the block still exists and is unchanged.

- [ ] **Step 6: Verify in the browser**

With the dev server running, Playwright `browser_navigate` to `http://localhost:8000`.
- `browser_take_screenshot` at 1280px: confirm a small gold line-art floral appears in the hero's top-left corner and a larger one bottom-right, with sparkle marks near each, sitting behind the headline/CTA and the bouquet photo (not on top of them).
- `browser_evaluate`: `getComputedStyle(document.querySelector('.hero-decor')).zIndex` — expect `"-1"`.
- `browser_evaluate`: click-through check — `document.elementFromPoint(x, y)` at a point over the CTA button should return the CTA button element, not `.hero-decor` (confirms `pointer-events: none` is working and the button is still clickable).
- `browser_resize` to 375×800: `browser_evaluate` `document.documentElement.scrollWidth <= 375` — expect `true`.

- [ ] **Step 7: Commit**

```bash
git add tools/gen_hero_decor.py images/hero-decor.svg index.html css/style.css
git commit -m "feat: add gold line-art decorative background layer to the hero"
```

---

### Task 5: Full verification pass

**Files:** none (verification only).

- [ ] **Step 1: Full-page visual check at desktop width**

With the dev server running, Playwright `browser_navigate` to `http://localhost:8000`, `browser_resize` to 1280×900, `browser_take_screenshot` (full page). Confirm:
- Hero: bouquet photo floating free on the blush background, no black fringe, corner line-art + sparkles + petal visible behind the text, CTA dropdown still clickable.
- Our Story section: animated jewel-tone bouquet illustration in the white frame, not stretched.

- [ ] **Step 2: Mobile width check**

`browser_resize` to 390×844. `browser_evaluate` `document.documentElement.scrollWidth <= 390` — expect `true`. `browser_take_screenshot` (full page) — confirm the hero photo, decorative corners, and Our Story illustration all still look intentional (nothing cropped mid-flower, nothing overlapping the CTA).

- [ ] **Step 3: Reduced-motion check**

Use `browser_run_code_unsafe` to call the Playwright page API directly: `await page.emulateMedia({ reducedMotion: 'reduce' })`, then reload. `browser_take_screenshot` on the hero: confirm the corner florals, sparkles, and petal all still render complete and visible (just static) — nothing missing or at zero opacity. Repeat for the Our Story section's illustration (should already have been covered when `hero-bouquet.svg` was originally built, but confirm it still holds in its new location).

- [ ] **Step 4: Console check**

`browser_console_messages` — confirm no 404s for `images/bouquet-cutout.png`, `images/hero-decor.svg`, or `images/hero-bouquet.svg`, and no JS errors.

- [ ] **Step 5: Final commit (only if Task 5 surfaced fixes)**

If any check above required a code change, stage and commit it with a message describing the specific fix (e.g. `fix: prevent hero decor overlap on mobile widths`). If nothing needed changing, no commit is needed for this task.
