"""Optimize slide background images to WebP.

Reads PNG / JPG files from img/, resizes each to fit within 1080×1920 while
preserving aspect ratio, and writes an optimized .webp file alongside the
source. The HTML references the .webp files; the source PNGs can remain in
the repo (or be git-ignored) as editing masters.

Run from the repo root:
    python scripts/optimize_images.py
"""
from __future__ import annotations

import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "img"

MAX_W, MAX_H = 1080, 1920
QUALITY = 82  # WebP quality — 82 is visually near-lossless for photos
METHOD = 6    # WebP encoder effort (0 fastest, 6 slowest / best compression)


def optimize(src: pathlib.Path) -> pathlib.Path:
    dst = src.with_suffix(".webp")
    with Image.open(src) as img:
        img = img.convert("RGB")
        img.thumbnail((MAX_W, MAX_H), Image.LANCZOS)
        img.save(dst, "WEBP", quality=QUALITY, method=METHOD)
    return dst


def build_social_preview(src: pathlib.Path) -> pathlib.Path:
    """Special-case for the WhatsApp / Open Graph preview image.

    WhatsApp's link-preview crawler has known issues decoding WebP and also
    prefers larger images (~1200+ on the long side) before it will render a
    big portrait card. So for `preview.png` we:
      - upscale 2x via Lanczos (Nano Banana native is ~896x1200)
      - export as high-quality JPEG (fully crawler-compatible)
    """
    dst = src.with_suffix(".jpg")
    with Image.open(src) as img:
        img = img.convert("RGB")
        w, h = img.size
        img = img.resize((w * 2, h * 2), Image.LANCZOS)
        img.save(dst, "JPEG", quality=92, optimize=True, progressive=True)
    return dst


def main() -> None:
    if not IMG_DIR.exists():
        print(f"No img/ directory at {IMG_DIR}")
        return

    sources = sorted(
        p for p in IMG_DIR.iterdir()
        if p.suffix.lower() in {".png", ".jpg", ".jpeg"}
    )
    if not sources:
        print("No PNG/JPG files in img/ to optimize")
        return

    total_in = 0
    total_out = 0
    for src in sources:
        # Slide backgrounds -> WebP
        dst = optimize(src)
        src_kb = src.stat().st_size / 1024
        dst_kb = dst.stat().st_size / 1024
        total_in += src_kb
        total_out += dst_kb
        with Image.open(dst) as im:
            w, h = im.size
        print(f"{src.name:28s} -> {dst.name:28s} {w}x{h}  {src_kb:8.1f} KB -> {dst_kb:7.1f} KB")

        # Social preview -> also produce a crawler-friendly JPG
        if src.stem == "preview":
            jpg = build_social_preview(src)
            jpg_kb = jpg.stat().st_size / 1024
            total_out += jpg_kb
            with Image.open(jpg) as im:
                jw, jh = im.size
            print(f"{'':28s}    {jpg.name:28s} {jw}x{jh}  {'':8s}    {jpg_kb:7.1f} KB")

    print("-" * 90)
    print(f"{'total':60s} {total_in:8.1f} KB -> {total_out:7.1f} KB  "
          f"({100 * total_out / total_in:.1f}%)")


if __name__ == "__main__":
    main()
