"""Tests for generate_covers — pure functions only (no network calls)."""

from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image

from generate_covers import (
    SLUG_PROMPTS,
    STYLE_PREFIX,
    build_prompt,
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
