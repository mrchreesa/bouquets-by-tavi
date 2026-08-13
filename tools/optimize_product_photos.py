#!/usr/bin/env python3
"""Resize product photos for the collection grid and save as WebP.

Cards display at up to ~350px wide (3-column grid at 1100px); 800px on the
longest side gives comfortable 2x retina coverage at quality 80."""
from PIL import Image
import sys

MAX_SIDE = 800
QUALITY = 80

SOURCES = [
    "images/1.PNG",
    "images/2.PNG",
    "images/3.PNG",
    "images/4.PNG",
    "images/4.1.PNG",
    "images/4.2.PNG",
    "images/5.jpg.jpeg",
    "images/5.1.jpg.jpeg",
    "images/6.PNG",
]


def out_path(src: str) -> str:
    name = src.rsplit("/", 1)[-1]
    if name.endswith(".jpg.jpeg"):
        stem = name.removesuffix(".jpg.jpeg")
    else:
        stem = name.rsplit(".", 1)[0]
    return f"images/{stem}.webp"


def optimize(src: str) -> tuple[str, int, int, int]:
    out = out_path(src)
    img = Image.open(src)
    img = img.convert("RGB")
    w, h = img.size
    if max(w, h) > MAX_SIDE:
        scale = MAX_SIDE / max(w, h)
        img = img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    w, h = img.size
    img.save(out, format="WEBP", quality=QUALITY)
    size_kb = out and __import__("os").path.getsize(out) // 1024
    return out, w, h, size_kb


def main() -> None:
    for src in SOURCES:
        out, w, h, kb = optimize(src)
        print(f"{src} -> {out}  {w}x{h}  {kb} KB")


if __name__ == "__main__":
    main()
