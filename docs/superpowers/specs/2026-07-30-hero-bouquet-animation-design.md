# Animated Hero Bouquet — Design Spec

**Date:** 2026-07-30
**Status:** Approved by user (via live animated previews in the visual companion)

## Overview

The hero's right-hand slot held `images/hero.svg`, a flat placeholder: a blush
background, a few concentric-circle "blossoms" on thin gold stems, and a `T`
monogram. The user asked for a visually impressive animated mark in its place —
"flowery and girly", then, after a first pass, "way more advanced… resemble
closer to a real bouquet, real flowers… more kitsch, chic… give it the wow
factor."

## Decisions (confirmed with user)

| Question | Decision |
|---|---|
| Placement | Replace the placeholder in the existing hero-image slot; layout untouched |
| Monogram | Keep a `T` — the bouquet is a brand mark, not just decoration |
| Palette | Bold jewel tones (crimson, burgundy, magenta, plum) rather than the site's soft pastel |
| Flowers | Roses + peonies, plus two cream roses for tonal contrast |
| Direction | Evolved from the "Floating Bouquet" sketch (composition animated in place), pushed to photographic-illustration fidelity |

## What was built

A generated SVG, `images/hero-bouquet.svg`:

- **15 blooms in three depth layers.** Each is built from cupped, shaded petals
  laid out in rings on a golden-angle spiral, so no flower reads as a symmetric
  rosette. Inner rings furl progressively (`lean`); peony petals are ruffled.
  ~350 petals total.
- **Depth.** A blurred dark mass sits behind the cluster and each bloom has a
  soft occlusion pool beneath it, so gaps between flowers read as shadow rather
  than background. Per-bloom drop shadows separate the layers.
- **Botanicals.** Eucalyptus sprigs fan out past the bloom silhouette, dark
  leaves sit behind for depth, baby's breath fills the gaps.
- **Wrap.** A florist's paper cone with flared shoulders, fold lines and an
  interior shadow where the stems disappear.
- **Ribbon.** Gold band, dimensional teardrop loops with fold shadows, and
  swallowtail streamers.
- **Monogram.** A cream seal on the knot, popping in last with a slow glint.

**Motion:** petals unfurl outward staggered back-to-front over ~2.5s; every
bloom then sways and bobs on its own period (negative animation delays put each
at a different phase, so nothing ever synchronises); ribbon loops breathe,
streamers flutter; petals occasionally detach and drift down; sparkle dust,
drifting bokeh, and a periodic light-sweep across the blooms.

## Implementation Notes

- **The SVG is generated, not hand-written.** `tools/gen_hero_bouquet.py` emits
  it. Petal geometry is arithmetic (ring counts, radii, spiral offsets, jitter)
  and would be unmaintainable as literal path data. Any future change edits the
  generator and regenerates.
- **Loaded via `<img>`, not inlined.** An inline SVG's `<style>` block leaks its
  class names (`.p`, `.sway`, `.bob`…) into the page's global CSS scope; `<img>`
  keeps the SVG a separate document. CSS animations inside the file still run —
  verified in-browser.
- **Reduced motion.** All animation lives inside
  `@media (prefers-reduced-motion: no-preference)`, so the no-animation state is
  the *default* and renders the finished bouquet. Effects that only make sense
  in flight (light sweep, falling petals, monogram glint) are held at
  `opacity: 0` outside the query. Verified: 490 animations drop to 0 and the
  composition still renders complete.
- **Size.** 240 KB raw, ~22 KB gzipped — which is what GitHub Pages serves.

## Verification performed

- Animation timeline scrubbed at 700 / 1100 / 3400 ms via `getAnimations()`.
  This caught a real bug: the per-bloom occlusion pools rendered at full opacity
  from frame 0, showing as dark blobs before their petals arrived. Fixed by
  fading each pool in on its flower's delay.
- `prefers-reduced-motion: reduce` emulated; confirmed 0 animations and a
  complete static bouquet.
- Live site checked at 1280px and 390px: no horizontal overflow, image sized by
  the existing `.hero-image` rules with no CSS changes needed.

## Out of Scope

No layout, copy, or CSS changes — the swap is `src` + `alt` only. `story.svg`
remains a placeholder. The old `images/hero.svg` is left in place, now unused.
