#!/usr/bin/env python3
"""Remove the solid black backing from a generated gold line-art image,
producing a transparent cutout for use as a hero decorative corner ornament.
Unlike cutout_bouquet.py (which protects real photographic shadow detail via
border-connectivity), these source images are pure black background + gold
line art with no legitimate dark content to protect — every near-black pixel,
connected or not, is background. A simple global threshold is correct and
sufficient here."""
from PIL import Image
from scipy import ndimage
import numpy as np
import sys

SRC = sys.argv[1]
OUT = sys.argv[2]
OUT_WIDTH = int(sys.argv[3]) if len(sys.argv) > 3 else 600

NEAR_BLACK = 20
FEATHER_SIGMA = 1.0

def main():
    img = Image.open(SRC).convert("RGB")
    arr = np.asarray(img).astype(np.uint8)

    near_black = arr.max(axis=2) <= NEAR_BLACK
    alpha = np.where(near_black, 0, 255).astype(np.float32)
    alpha = ndimage.gaussian_filter(alpha, sigma=FEATHER_SIGMA)
    alpha = np.clip(alpha, 0, 255).astype(np.uint8)

    rgba = Image.fromarray(np.dstack([arr, alpha]), mode="RGBA")
    w, h = rgba.size
    new_h = round(h * OUT_WIDTH / w)
    rgba = rgba.resize((OUT_WIDTH, new_h), Image.LANCZOS)
    rgba.save(OUT, format="WEBP", quality=80)

    a = np.asarray(rgba)[:, :, 3]
    print(f"{OUT}: {rgba.size[0]}x{rgba.size[1]}, "
          f"{(a == 0).sum()} transparent px, {(a > 200).sum()} opaque px")

if __name__ == "__main__":
    main()
