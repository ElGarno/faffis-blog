# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "openai>=1.55",
#     "python-dotenv>=1.0",
#     "Pillow>=10.4",
# ]
# ///
"""Generate cover images for blog posts via OpenAI gpt-image-1.

Usage:
    uv run scripts/generate_covers.py                 # all slugs, skip existing
    uv run scripts/generate_covers.py --slug Tapo     # single slug
    uv run scripts/generate_covers.py --force         # overwrite existing
"""

from __future__ import annotations

import argparse
import base64
import os
import sys
import tempfile
from io import BytesIO
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

from shot_to_cover import crop_to_cover

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "content" / "posts"

STYLE_PREFIX = (
    "Minimalist tech illustration, flat design, soft gradients, "
    "muted color palette (deep blue, warm orange, soft white), "
    "no text, no logos, no people, abstract geometric shapes "
    "representing the topic, suitable as blog post cover."
)

SLUG_PROMPTS: dict[str, str] = {
    "Tapo": (
        "smart plug device with energy waveforms and time-series chart elements"
    ),
    "wippestoolen": (
        "neighborhood houses connected by tool icons (hammer, drill, ladder), "
        "trust-network feel"
    ),
    "tcbw-website": (
        "tennis court silhouette merging into a clean static-site grid, "
        "blue and white"
    ),
    "tcbw-getraenkebuchung": (
        "iPad on a tennis-club bar counter with abstract drink list and NFC waves; "
        "subtle tennis racket and tennis ball motifs in the background"
    ),
    "mai-tasting": (
        "whisky and wine bottle silhouettes with AI/vision overlay, "
        "abstract neural patterns"
    ),
    "solar-prediction": (
        "solar panels under a forecast sky, a rising prediction curve overlaid, "
        "hourly bars beneath it"
    ),
    "doko-stats": (
        "abstract playing cards fanned out, turning into a bar chart, "
        "no faces, no text, no suits that resemble a real brand"
    ),
}

COST_PER_IMAGE_USD = 0.04


def build_prompt(slug: str) -> str:
    """Combine style prefix with slug-specific topic. Raises KeyError on unknown slug."""
    return f"{STYLE_PREFIX} Topic: {SLUG_PROMPTS[slug]}"


def png_bytes_to_webp(
    png_bytes: bytes, target: Path, *, crop_for_cover: bool = False
) -> None:
    """Convert PNG bytes to WebP file at target path.

    gpt-image-1 only produces square images. Plain posts historically kept
    that native square as-is, but a "projekte" cover must be a 1200x675
    16:9 image (see layouts/projekte/*.html and project-card CSS), so
    crop_for_cover=True center-crops it via shot_to_cover.crop_to_cover
    instead of saving the untouched square. Center, not top: the square
    source has its subject in the middle, and a top crop cuts it off.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    if not crop_for_cover:
        with Image.open(BytesIO(png_bytes)) as img:
            img.save(target, format="WEBP", quality=85, method=6)
        return

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(png_bytes)
        tmp_path = Path(tmp.name)
    try:
        crop_to_cover(tmp_path, target, anchor="center")
    finally:
        tmp_path.unlink(missing_ok=True)


def generate_image(client: OpenAI, slug: str) -> bytes:
    """Call gpt-image-1 with prompt for slug; return PNG bytes."""
    prompt = build_prompt(slug)
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        n=1,
    )
    b64 = response.data[0].b64_json
    if b64 is None:
        raise RuntimeError(
            f"OpenAI returned no b64_json for slug {slug!r}; got {response.data[0]!r}"
        )
    return base64.b64decode(b64)


def cover_path(slug: str, section: str = "posts") -> Path:
    return REPO_ROOT / "content" / section / slug / "cover.webp"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--slug",
        choices=sorted(SLUG_PROMPTS.keys()),
        help="Generate only this slug (default: all)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing cover.webp",
    )
    parser.add_argument(
        "--section", default="posts", choices=["posts", "projekte"],
        help="Content section to write covers into",
    )
    args = parser.parse_args()

    load_dotenv(REPO_ROOT / ".env")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set (.env or env var)", file=sys.stderr)
        return 1

    client = OpenAI(api_key=api_key)
    slugs = [args.slug] if args.slug else list(SLUG_PROMPTS.keys())
    generated = 0

    for slug in slugs:
        target = cover_path(slug, args.section)
        if target.exists() and not args.force:
            print(f"[skip] {slug}: {target.relative_to(REPO_ROOT)} exists")
            continue
        print(f"[gen ] {slug}: calling gpt-image-1 ...")
        png = generate_image(client, slug)
        png_bytes_to_webp(png, target, crop_for_cover=(args.section == "projekte"))
        generated += 1
        print(f"[ok  ] {slug}: wrote {target.relative_to(REPO_ROOT)}")

    cost = generated * COST_PER_IMAGE_USD
    print(f"\nDone. Generated {generated} image(s). Estimated cost: ${cost:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
