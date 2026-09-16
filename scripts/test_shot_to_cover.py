"""Tests for shot_to_cover — pure image functions, no network."""

from pathlib import Path

from PIL import Image
from shot_to_cover import compose_phone_cover, crop_to_cover, to_gallery_shot


def _make(path: Path, size: tuple[int, int], color: tuple[int, int, int]) -> Path:
    Image.new("RGB", size, color).save(path, format="PNG")
    return path


def close(a: tuple[int, ...], b: tuple[int, ...], tol: int = 10) -> bool:
    """True if every channel of a and b differs by at most tol (lossy-WebP tolerant)."""
    return all(abs(x - y) <= tol for x, y in zip(a, b))


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
        for x in range(1440):
            img.putpixel((x, y), (255, 0, 0))
    img.save(src, format="PNG")
    target = tmp_path / "cover.webp"

    crop_to_cover(src, target)

    with Image.open(target) as out:
        assert out.size == (1200, 675)
        r, g, b = out.getpixel((600, 5))
        assert r > 150 and g < 100 and b < 100


def test_compose_phone_cover_lays_out_three_frames(tmp_path: Path) -> None:
    sources = [
        _make(tmp_path / f"p{i}.png", (1290, 2796), (200, 100, 50)) for i in range(3)
    ]
    target = tmp_path / "cover.webp"
    background = (245, 240, 232)

    compose_phone_cover(sources, target, background=background)

    with Image.open(target) as out:
        assert out.size == (1200, 675)
        # The corners stay background; the middle carries a frame.
        assert close(out.getpixel((2, 2)), background)
        assert not close(out.getpixel((600, 337)), background)


def test_to_gallery_shot_scales_by_height(tmp_path: Path) -> None:
    src = _make(tmp_path / "p.png", (1290, 2796), (0, 0, 0))
    target = tmp_path / "shot-1.webp"

    to_gallery_shot(src, target, height=1400)

    with Image.open(target) as out:
        assert out.height == 1400
        assert abs(out.width - 646) <= 1
