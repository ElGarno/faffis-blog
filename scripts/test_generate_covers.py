"""Tests for generate_covers — pure functions only (no network calls)."""

from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image

from generate_covers import (
    SLUG_PROMPTS,
    STYLE_PREFIX,
    build_prompt,
    cover_path,
    png_bytes_to_webp,
)


def test_build_prompt_combines_prefix_and_topic() -> None:
    prompt = build_prompt("Tapo")
    assert STYLE_PREFIX in prompt
    assert SLUG_PROMPTS["Tapo"] in prompt


def test_build_prompt_unknown_slug_raises() -> None:
    with pytest.raises(KeyError):
        build_prompt("unknown-slug")


def test_png_bytes_to_webp_writes_valid_webp(tmp_path: Path) -> None:
    img = Image.new("RGB", (1024, 1024), color=(0, 0, 255))
    buf = BytesIO()
    img.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    target = tmp_path / "cover.webp"
    png_bytes_to_webp(png_bytes, target)

    assert target.exists()
    with Image.open(target) as out:
        assert out.format == "WEBP"
        assert out.size == (1024, 1024)


def test_png_bytes_to_webp_crops_square_source_for_cover(tmp_path: Path) -> None:
    # gpt-image-1 only ever returns a square image; a "projekte" cover must
    # be cropped to the portfolio's 1200x675 ratio instead of staying square.
    img = Image.new("RGB", (1024, 1024), color=(0, 0, 255))
    buf = BytesIO()
    img.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    target = tmp_path / "cover.webp"
    png_bytes_to_webp(png_bytes, target, crop_for_cover=True)

    assert target.exists()
    with Image.open(target) as out:
        assert out.format == "WEBP"
        assert out.size == (1200, 675)


def test_cover_path_targets_the_requested_section() -> None:
    assert cover_path("doko-stats", "projekte").parts[-3:] == (
        "projekte",
        "doko-stats",
        "cover.webp",
    )
    assert cover_path("Tapo").parts[-3:] == ("posts", "Tapo", "cover.webp")
