# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "Pillow>=10.4",
# ]
# ///
"""Turn raw screenshots into portfolio cover images.

Usage:
    uv run scripts/shot_to_cover.py crop    shot.png content/projekte/basar/cover.webp
    uv run scripts/shot_to_cover.py phones  content/projekte/mai-tasting/cover.webp \
        --background "#F5F0E8" a.png b.png c.png
    uv run scripts/shot_to_cover.py gallery a.png content/projekte/mai-tasting/shot-1.webp
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

COVER_SIZE = (1200, 675)
# Lossless: covers get re-processed in place by later steps (normalising an
# existing cover with itself as src and target), so re-encoding must not
# introduce generation loss. WEBP_QUALITY then controls compression effort,
# not visual fidelity (see Pillow's WebP plugin docs).
WEBP_QUALITY = 82


def _save(img: Image.Image, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    img.save(target, format="WEBP", lossless=True, quality=WEBP_QUALITY, method=6)


def crop_to_cover(
    src: Path, target: Path, size: tuple[int, int] = COVER_SIZE
) -> None:
    """Scale a landscape capture to the target width, then crop from the top."""
    with Image.open(src) as img:
        rgb = img.convert("RGB")
        scale = size[0] / rgb.width
        # BOX avoids LANCZOS ringing/blurring thin high-contrast details away
        # when shrinking (e.g. hairline borders in UI screenshots).
        scaled = rgb.resize(
            (size[0], max(size[1], round(rgb.height * scale))), Image.BOX
        )
        cover = scaled.crop((0, 0, size[0], size[1]))
    # Saved outside the with-block so src may be the same path as target.
    _save(cover, target)


def compose_phone_cover(
    sources: list[Path],
    target: Path,
    background: tuple[int, int, int],
    size: tuple[int, int] = COVER_SIZE,
) -> None:
    """Lay portrait frames side by side, centred, on a solid background."""
    if not sources:
        raise ValueError("compose_phone_cover needs at least one source")

    margin = round(size[1] * 0.08)
    gap = round(size[0] * 0.02)
    frame_height = size[1] - 2 * margin

    frames = []
    for src in sources:
        with Image.open(src) as img:
            img = img.convert("RGB")
            width = round(img.width * frame_height / img.height)
            frames.append(img.resize((width, frame_height), Image.LANCZOS))

    total = sum(f.width for f in frames) + gap * (len(frames) - 1)
    if total > size[0] - 2 * margin:
        shrink = (size[0] - 2 * margin - gap * (len(frames) - 1)) / sum(
            f.width for f in frames
        )
        frames = [
            f.resize((round(f.width * shrink), round(f.height * shrink)), Image.LANCZOS)
            for f in frames
        ]
        total = sum(f.width for f in frames) + gap * (len(frames) - 1)

    canvas = Image.new("RGB", size, background)
    x = (size[0] - total) // 2
    for frame in frames:
        canvas.paste(frame, (x, (size[1] - frame.height) // 2))
        x += frame.width + gap

    _save(canvas, target)


def to_gallery_shot(src: Path, target: Path, height: int = 1400) -> None:
    """Scale a portrait frame to a fixed height for the detail-page gallery."""
    with Image.open(src) as img:
        img = img.convert("RGB")
        width = int(img.width * height / img.height)
        _save(img.resize((width, height), Image.LANCZOS), target)


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)

    p_crop = sub.add_parser("crop", help="landscape capture -> 16:9 cover")
    p_crop.add_argument("src", type=Path)
    p_crop.add_argument("target", type=Path)

    p_phones = sub.add_parser("phones", help="portrait frames -> 16:9 cover")
    p_phones.add_argument("target", type=Path)
    p_phones.add_argument("sources", type=Path, nargs="+")
    p_phones.add_argument("--background", default="#F5F0E8")

    p_gallery = sub.add_parser("gallery", help="portrait frame -> gallery image")
    p_gallery.add_argument("src", type=Path)
    p_gallery.add_argument("target", type=Path)
    p_gallery.add_argument("--height", type=int, default=1400)

    args = parser.parse_args()

    if args.mode == "crop":
        crop_to_cover(args.src, args.target)
    elif args.mode == "phones":
        compose_phone_cover(
            args.sources, args.target, background=_hex_to_rgb(args.background)
        )
    else:
        to_gallery_shot(args.src, args.target, height=args.height)

    print(f"wrote {args.target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
