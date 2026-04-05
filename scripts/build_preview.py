"""Build the 1200x630 OpenGraph preview card for tosca-irina.

Composition:
  - Left column: Hohenstein 1899 Tosca poster, full height, subtle inset frame
  - Right column: typographic block on cream background matching the site palette
  - Gold hairline separator between columns

Run from the repo root: python scripts/build_preview.py
Output: preview.jpg (written to repo root)
"""
from __future__ import annotations

import io
import pathlib
import urllib.request

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "preview.jpg"

WIDTH, HEIGHT = 1200, 630

# Palette (mirrors :root in index.html)
CREAM = (253, 246, 236)
CREAM_DARK = (245, 235, 216)
BURGUNDY = (122, 35, 50)
GOLD = (200, 165, 92)
GOLD_LIGHT = (212, 184, 122)
TEXT = (58, 48, 40)
TEXT_LIGHT = (107, 94, 82)
ROSE = (196, 114, 127)

POSTER_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/"
    "4/40/Tosca_%281899%29.jpg/1200px-Tosca_%281899%29.jpg"
)

FONT_REG = "C:/Windows/Fonts/georgia.ttf"
FONT_BOLD = "C:/Windows/Fonts/georgiab.ttf"
FONT_ITALIC = "C:/Windows/Fonts/georgiai.ttf"
FONT_BOLDITALIC = "C:/Windows/Fonts/georgiaz.ttf"


def load_poster() -> Image.Image:
    req = urllib.request.Request(POSTER_URL, headers={"User-Agent": "tosca-irina-build/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return Image.open(io.BytesIO(resp.read())).convert("RGB")


def vertical_gradient(size: tuple[int, int], top: tuple[int, int, int], bot: tuple[int, int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size, top)
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        r = round(top[0] * (1 - t) + bot[0] * t)
        g = round(top[1] * (1 - t) + bot[1] * t)
        b = round(top[2] * (1 - t) + bot[2] * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img


def draw_centered(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.FreeTypeFont, fill):
    """Draw text centered horizontally around xy[0] at vertical position xy[1]."""
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((xy[0] - w // 2, xy[1]), text, font=font, fill=fill)


def main() -> None:
    # 1. Background with subtle vertical gradient (cream -> cream_dark)
    canvas = vertical_gradient((WIDTH, HEIGHT), CREAM, CREAM_DARK)

    # 2. Poster on the left
    poster = load_poster()
    # Fit to full height minus a small margin
    margin = 24
    target_h = HEIGHT - 2 * margin
    ratio = poster.width / poster.height
    target_w = round(target_h * ratio)
    poster = poster.resize((target_w, target_h), Image.LANCZOS)

    # Soft shadow for the poster
    shadow = Image.new("RGBA", (target_w + 40, target_h + 40), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(shadow)
    sh_draw.rectangle((20, 20, 20 + target_w, 20 + target_h), fill=(60, 30, 20, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=14))
    canvas.paste(shadow, (margin - 20, margin - 12), shadow)
    canvas.paste(poster, (margin, margin))

    # Thin gold border around poster
    border = ImageDraw.Draw(canvas)
    border.rectangle(
        (margin - 1, margin - 1, margin + target_w, margin + target_h),
        outline=GOLD,
        width=2,
    )

    # 3. Right panel: typography
    right_x0 = margin + target_w + 48
    right_x1 = WIDTH - 40
    center_x = (right_x0 + right_x1) // 2

    draw = ImageDraw.Draw(canvas)

    # Gold ornamental rule (top)
    rule_y = 110
    draw.line((right_x0 + 30, rule_y, right_x1 - 30, rule_y), fill=GOLD, width=2)
    # Center diamond
    cx = (right_x0 + right_x1) // 2
    draw.polygon(
        [(cx, rule_y - 6), (cx + 6, rule_y), (cx, rule_y + 6), (cx - 6, rule_y)],
        fill=GOLD,
    )
    # Cover the rule where the diamond sits so it looks segmented
    draw.rectangle((cx - 10, rule_y - 1, cx + 10, rule_y + 1), fill=CREAM)
    draw.polygon(
        [(cx, rule_y - 6), (cx + 6, rule_y), (cx, rule_y + 6), (cx - 6, rule_y)],
        fill=GOLD,
    )

    # "PENTRU IRINA" — letterspaced small caps feel
    f_eyebrow = ImageFont.truetype(FONT_BOLD, 22)
    eyebrow = "P E N T R U   I R I N A"
    draw_centered(draw, (center_x, 132), eyebrow, f_eyebrow, GOLD)

    # "Tosca" — huge title
    f_title = ImageFont.truetype(FONT_BOLDITALIC, 148)
    draw_centered(draw, (center_x, 170), "Tosca", f_title, BURGUNDY)

    # Composer
    f_sub = ImageFont.truetype(FONT_ITALIC, 30)
    draw_centered(draw, (center_x, 340), "Giacomo Puccini", f_sub, TEXT)

    # Small gold ornament
    orn_y = 392
    draw.line((cx - 70, orn_y, cx - 14, orn_y), fill=GOLD_LIGHT, width=1)
    draw.line((cx + 14, orn_y, cx + 70, orn_y), fill=GOLD_LIGHT, width=1)
    f_orn = ImageFont.truetype(FONT_REG, 20)
    draw_centered(draw, (center_x, orn_y - 14), "♥", f_orn, ROSE)

    # Venue + date
    f_detail = ImageFont.truetype(FONT_REG, 26)
    draw_centered(draw, (center_x, 420), "Bayerische Staatsoper · München", f_detail, TEXT)
    f_date = ImageFont.truetype(FONT_BOLD, 26)
    draw_centered(draw, (center_x, 458), "Luni, 6 aprilie 2026 · ora 18:00", f_date, BURGUNDY)

    # Sign-off
    f_sign = ImageFont.truetype(FONT_ITALIC, 24)
    draw_centered(draw, (center_x, 540), "Cu dragoste, Matthias", f_sign, TEXT_LIGHT)

    # 4. Save as JPEG
    canvas.save(OUT, "JPEG", quality=88, optimize=True, progressive=True)
    size_kb = OUT.stat().st_size / 1024
    print(f"Wrote {OUT}  ({WIDTH}x{HEIGHT}, {size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
