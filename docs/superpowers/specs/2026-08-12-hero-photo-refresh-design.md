# Hero Photo Refresh — Design Spec

**Date:** 2026-08-12
**Status:** Approved by user

## Overview

The user shared a reference hero image (a competitor/inspiration screenshot): a
soft blush-and-white photographic bouquet on a blush background, decorated with
fine gold line-art florals in the corners, small sparkle marks, and a single
falling petal. They'd already dropped a matching real bouquet photo into the
repo at `images/bouquet.png`.

The current hero uses `images/hero-bouquet.svg`, a generated animated
illustration deliberately drawn in **bold jewel tones** (crimson/burgundy/plum)
as a contrast to the site's soft pastel palette — see
[[2026-07-30-hero-bouquet-animation-design]]. That illustration is well-built
and shouldn't be discarded; the user wants it moved to the Our Story section
instead of deleted, and the real photo to take its place in the hero.

## Decisions (confirmed with user)

| Question | Decision |
|---|---|
| Hero bouquet source | Use the real photo `images/bouquet.png`, not another illustration |
| Fate of the current hero animation | Move `hero-bouquet.svg` down into the Our Story section, replacing `images/story.svg` there (left in place, unused — matching how `hero.svg` was left after the last hero-image swap) |
| Background decorative elements | Recreate the reference closely: gold line-art corner florals + sparkle marks + a drifting petal, redrawn in the site's own gold (`#B99668`), not copied from the reference image |
| Motion for the new decorative elements | Subtle animation (petal drift, sparkle twinkle), consistent with the site's existing animated details (announcement bar, hero bouquet sway) — not static |

## Problem: `bouquet.png` has a baked-in black backing

`images/bouquet.png` (1368×1150) is a flat RGB PNG with a solid black
background — no alpha channel. The reference image shows the bouquet floating
free on the blush background with no visible box, so the black has to be
removed, not covered.

**Approach:** a one-off Python script, `tools/cutout_bouquet.py` (Pillow +
numpy, both already available in this environment), thresholds near-black
pixels to transparent and feathers the edge over a few pixels to avoid a hard
cutout line or a black fringe/halo around light petal edges. Output goes to a
new file, `images/bouquet-cutout.png`; the original `bouquet.png` is left
untouched as the source asset, and the script is kept (regenerate comment in
the HTML, matching the convention used for the generated SVGs) in case the
cutout needs retuning.

## Implementation Notes

### 1. Hero bouquet photo

- `.hero-image img` swaps `src` to `images/bouquet-cutout.png`; `alt` updated
  to describe the real bouquet (roses, peonies, blush wrap, ribbon).
- Width/height attributes updated to the photo's real aspect ratio (roughly
  1368×1150, landscape) rather than the old portrait SVG's 560×640 — the grid
  column / max-width for `.hero-image` gets rebalanced so a landscape photo
  doesn't look cramped or oversized against the text column.
- `.hero-image img`'s current `border-radius: 260px 260px 6px 6px` +
  `box-shadow` (an arch-frame treatment designed for a full-bleed illustration)
  is replaced with `filter: drop-shadow(...)`, which follows the photo's actual
  alpha silhouette instead of its rectangular box — this is what makes the
  bouquet look like it's floating free, matching the reference, instead of
  sitting in a cropped frame.

### 2. Our Story section swap

- `#story .story-image img` swaps `src` from `images/story.svg` to
  `images/hero-bouquet.svg` (the existing animated jewel-tone illustration,
  unchanged); `alt` updated to describe the animated bouquet instead of the
  line-art placeholder.
- Width/height attributes updated to the SVG's real 560×640 ratio so it isn't
  stretched inside the white polaroid-style `.story-image` frame.
- `images/story.svg` and `tools/gen_story_bouquet.py` stay in the repo,
  unused — not deleted, matching precedent.

### 3. Decorative background layer

- New generator `tools/gen_hero_decor.py`, a companion to
  `gen_hero_bouquet.py` / `gen_story_bouquet.py`, reuses the fine gold-line-art
  bloom/stem/leaf drawing style already established in `gen_story_bouquet.py`
  (`stroke="url(#goldL)"` line art) rather than inventing a new visual
  language. Emits `images/hero-decor.svg`, sized to the `.hero` section:
  - A small line-art floral sketch in the top-left corner.
  - A larger line-art spray (peony-style) in the bottom-right corner.
  - A handful of small sparkle/star marks scattered near each corner cluster.
  - One petal shape that drifts slowly across the hero on a loop (translate +
    rotate, staggered so it doesn't feel mechanical).
- Loaded via `<img>` (not inlined — same reasoning as the hero bouquet: avoids
  leaking `<style>` class names into the page's global CSS scope), absolutely
  positioned to cover the full `.hero`, placed behind `.hero-inner` in stacking
  order, `pointer-events: none` so it never intercepts clicks on the text/CTA.
- Sparkle twinkle and petal drift animations live inside
  `@media (prefers-reduced-motion: no-preference)`; outside that query the
  layer renders as a complete static composition (corner florals + sparkles at
  a settled opacity + petal at its resting position) — same pattern as
  `hero-bouquet.svg`'s existing reduced-motion handling.

### 4. Verification

- Regenerate both SVGs from their generators and load the live site.
- Check the hero at mobile (~390px) and desktop (~1280px) widths: no
  horizontal overflow, cutout photo reads cleanly against the blush gradient
  (no black fringe at the edges), decorative layer doesn't overlap/crowd the
  text or CTA dropdown.
- Check the Our Story section: swapped-in animation isn't stretched, still
  animates, still respects `prefers-reduced-motion`.
- Emulate `prefers-reduced-motion: reduce` and confirm the hero decorative
  layer and both bouquet illustrations settle into complete static states.

## Out of Scope

- No changes to hero copy, CTA, or announcement bar.
- No re-shoot or re-generation of `bouquet.png` itself — only background
  removal on the existing file.
- `hero.svg` (already unused since the previous hero-animation change) and
  `story.svg` stay in the repo, both now unused, per existing precedent of not
  deleting superseded assets.
