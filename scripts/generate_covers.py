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
from io import BytesIO
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

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
}

COST_PER_IMAGE_USD = 0.04


def build_prompt(slug: str) -> str:
    """Combine style prefix with slug-specific topic. Raises KeyError on unknown slug."""
    return f"{STYLE_PREFIX} Topic: {SLUG_PROMPTS[slug]}"


def png_bytes_to_webp(png_bytes: bytes, target: Path) -> None:
    """Convert PNG bytes to WebP file at target path."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(BytesIO(png_bytes)) as img:
        img.save(target, format="WEBP", quality=85, method=6)


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


def cover_path(slug: str) -> Path:
    return POSTS_DIR / slug / "cover.webp"


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
        target = cover_path(slug)
        if target.exists() and not args.force:
            print(f"[skip] {slug}: {target.relative_to(REPO_ROOT)} exists")
            continue
        print(f"[gen ] {slug}: calling gpt-image-1 ...")
        png = generate_image(client, slug)
        png_bytes_to_webp(png, target)
        generated += 1
        print(f"[ok  ] {slug}: wrote {target.relative_to(REPO_ROOT)}")

    cost = generated * COST_PER_IMAGE_USD
    print(f"\nDone. Generated {generated} image(s). Estimated cost: ${cost:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
