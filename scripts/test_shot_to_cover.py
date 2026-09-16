"""Tests for shot_to_cover — pure image functions, no network."""

from pathlib import Path

from PIL import Image
from shot_to_cover import compose_phone_cover, crop_to_cover, to_gallery_shot


def _make(path: Path, size: tuple[int, int], color: tuple[int, int, int]) -> Path:
    Image.new("RGB", size, color).save(path, format="PNG")
    return path


def test_crop_to_cover_produces_exact_size(tmp_path: Path) -> None:
    src = _make(tmp_path / "shot.png", (1440, 900), (10, 20, 30))
    target = tmp_path / "cover.webp"

    crop_to_cover(src, target)

    with Image.open(target) as out:
        assert out.format == "WEBP"
        assert out.size == (1200, 675)


def test_crop_to_cover_keeps_top_of_tall_capture(tmp_path: Path) -> None:
    # A full-page capture is much taller than 16:9; the interesting part is the top.
    src = tmp_path / "tall.png"
    img = Image.new("RGB", (1440, 3000), (255, 255, 255))
    for y in range(300):
        for x in range(0, 1440, 40):
            img.putpixel((x, y), (255, 0, 0))
    img.save(src, format="PNG")
    target = tmp_path / "cover.webp"

    crop_to_cover(src, target)

    with Image.open(target) as out:
        assert out.size == (1200, 675)
        assert (255, 0, 0) in {out.getpixel((x, 5)) for x in range(0, 1200, 10)}


def test_compose_phone_cover_lays_out_three_frames(tmp_path: Path) -> None:
    sources = [
        _make(tmp_path / f"p{i}.png", (1290, 2796), (200, 100, 50)) for i in range(3)
    ]
    target = tmp_path / "cover.webp"

    compose_phone_cover(sources, target, background=(245, 240, 232))

    with Image.open(target) as out:
        assert out.size == (1200, 675)
        # The corners stay background; the middle carries a frame.
        assert out.getpixel((2, 2)) == (245, 240, 232)
        assert out.getpixel((600, 337)) != (245, 240, 232)


def test_to_gallery_shot_scales_by_height(tmp_path: Path) -> None:
    src = _make(tmp_path / "p.png", (1290, 2796), (0, 0, 0))
    target = tmp_path / "shot-1.webp"

    to_gallery_shot(src, target, height=1400)

    with Image.open(target) as out:
        assert out.height == 1400
        assert out.width == 645
