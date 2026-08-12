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

    # Known small background pockets fully enclosed by leaf/foliage silhouettes,
    # identified by pixel-level review of this specific photo. The border
    # flood-fill above can't reach these (no path to the image border through
    # the gaps). Listed explicitly rather than inferred by a generic size
    # heuristic — a generic "absorb any small enclosed near-black blob" rule
    # also erodes legitimate deep shadow elsewhere (paper-wrap fold crease,
    # petal shadow, leaf-in-shadow) that happens to be small and near-black too.
    # Coordinates scaled from output (1000x841) space to original (1368x1150).
    KNOWN_ENCLOSED_POCKETS = [
        (186, 209, 436, 465), (182, 191, 447, 473), (187, 211, 405, 414),
        (312, 326, 1245, 1261), (309, 315, 1309, 1331), (297, 305, 1322, 1333),
        (311, 319, 1261, 1279), (346, 360, 1213, 1226),
    ]
    for y0, y1, x0, x1 in KNOWN_ENCLOSED_POCKETS:
        bg[y0:y1, x0:x1] |= near_black[y0:y1, x0:x1]

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
