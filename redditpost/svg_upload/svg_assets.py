from pathlib import Path
import base64
import mimetypes
import sys


def image_to_data_uri(path: Path) -> str:
    """
    Convert an image file into a base64 data URI
    suitable for embedding directly into SVG.

    This makes the SVG fully self-contained and portable.
    """
    mime, _ = mimetypes.guess_type(path)
    if not mime:
        raise ValueError(f"Cannot determine MIME type for {path}")

    data = path.read_bytes()
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def add_logo(
    dwg,
    logo_path: Path,
    x: int,
    y: int,
    size: int,
    fallback_color: str = "#e5e7eb",
):
    """
    Add a primary logo image to an svgwrite Drawing.

    Behavior:
    - Embeds logo as base64 (portable SVG)
    - Falls back to a skeleton circle if logo is missing or fails
    """
    if logo_path.exists():
        try:
            href = image_to_data_uri(logo_path)
            dwg.add(dwg.image(
                href=href,
                insert=(x, y),
                size=(size, size)
            ))
            return True
        except Exception as e:
            print(f"[WARN] Failed to embed logo: {e}", file=sys.stderr)

    # Fallback skeleton
    dwg.add(dwg.circle(
        center=(x + size // 2, y + size // 2),
        r=size // 2,
        fill=fallback_color
    ))
    return False


def add_inline_image(
    dwg,
    image_path: Path,
    x: int,
    y: int,
    width: int,
    height: int,
):
    """
    Add a small inline image (e.g. badges, awards, flairs).

    Intended for:
    - Reddit awards
    - Verification badges
    - Small UI decorations

    Behavior:
    - Base64-embedded for portability
    - Silent no-op if image is missing (badges are optional)
    """
    if not image_path.exists():
        return False

    try:
        href = image_to_data_uri(image_path)
        dwg.add(dwg.image(
            href=href,
            insert=(x, y),
            size=(width, height)
        ))
        return True
    except Exception as e:
        print(f"[WARN] Failed to embed inline image: {e}", file=sys.stderr)
        return False
