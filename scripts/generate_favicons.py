# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "Pillow>=10.4",
# ]
# ///
"""Generate favicon assets deterministically — no AI, no external asset.

Renders a monogram (a dark charcoal rounded square with an off-white
capital "F") into every raster icon PaperMod's <head> references
(favicon.ico, favicon-16x16.png, favicon-32x32.png, apple-touch-icon.png)
and writes them into static/.

static/safari-pinned-tab.svg is not produced by this script: it is a
hand-written, single-colour (black-on-transparent) silhouette, since
Safari recolours a mask icon itself and ignores any colour baked into it.

Usage:
    uv run scripts/generate_favicons.py            # write missing sizes
    uv run scripts/generate_favicons.py --force    # overwrite existing files
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = REPO_ROOT / "static"

BACKGROUND = (30, 30, 32)  # dark charcoal
FOREGROUND = (245, 245, 240)  # off-white
CORNER_RADIUS_RATIO = 0.22
LETTER = "F"

# Bold system fonts to try, in order of preference. All of these ship with
# a stock macOS install; if none is found (e.g. a different OS), Pillow's
# built-in bitmap font is used as a graceful fallback.
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Black.ttf",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
]

RASTER_SIZES: dict[str, int] = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "apple-touch-icon.png": 180,
}
ICO_SIZES = (16, 32, 48)


def load_font(size: int) -> ImageFont.ImageFont | ImageFont.FreeTypeFont:
    """Load the first available bold system font at `size`, else Pillow's default."""
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    print("[warn] no system font found, falling back to Pillow's default bitmap font")
    return ImageFont.load_default()


def render_monogram(size: int) -> Image.Image:
    """Render one size of the dark rounded-square 'F' monogram."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    radius = round(size * CORNER_RADIUS_RATIO)
    draw.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=BACKGROUND)

    font = load_font(round(size * 0.62))
    bbox = draw.textbbox((0, 0), LETTER, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - w) / 2 - bbox[0]
    y = (size - h) / 2 - bbox[1]
    draw.text((x, y), LETTER, font=font, fill=FOREGROUND)
    return img


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing files"
    )
    args = parser.parse_args()

    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    written = 0

    for name, size in RASTER_SIZES.items():
        target = STATIC_DIR / name
        if target.exists() and not args.force:
            print(f"[skip] {name}: exists")
            continue
        render_monogram(size).save(target, format="PNG")
        print(f"[ok  ] wrote {target.relative_to(REPO_ROOT)} ({size}x{size})")
        written += 1

    ico_target = STATIC_DIR / "favicon.ico"
    if ico_target.exists() and not args.force:
        print("[skip] favicon.ico: exists")
    else:
        base = render_monogram(max(ICO_SIZES))
        base.save(ico_target, format="ICO", sizes=[(s, s) for s in ICO_SIZES])
        sizes_str = ", ".join(f"{s}x{s}" for s in ICO_SIZES)
        print(f"[ok  ] wrote {ico_target.relative_to(REPO_ROOT)} ({sizes_str})")
        written += 1

    print(f"\nDone. Wrote {written} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
