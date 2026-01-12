from pathlib import Path
import svgwrite
import textwrap

from svg_assets import add_logo, add_inline_image


# ============================================================
# Constants (UNCHANGED)
# ============================================================

ICON_OPTICAL_SHIFT = -1
FOOTER_LIFT = 5

CARD_WIDTH = 400
PADDING = 9
RADIUS = 16

LOGO = 34
LOGO_BOTTOM_PAD = 3
HEADER_GAP = 7
HEADER_BOTTOM_PAD = 7

STORY_SIZE = 11
STORY_LINE = 13
CONTENT_GAP = 10

ICON = 14
META_SIZE = 11
META_GAP = 1
FOOTER_BLOCK_GAP = 16
RIGHT_PADDING = 17

TEXT_CENTER_OFFSET = int(META_SIZE * 0.35)

CARD_WIDTH_CHAR_PER_LINE = 0.60

BADGE_HEIGHT = 11
BADGE_WIDTH = 137
BADGE_TOP_PAD = 4

VERIFIED_SIZE = 13
VERIFIED_GAP = 2

USERNAME_FONT = "DejaVu Sans"
STORY_FONT = "DejaVu Sans Condensed"

FG = "#11151A"
MUTED = "#5C6C74"
BG = "#ffffff"
SKELETON = "#e5e7eb"

BADGE_PATH = Path("assets/badges/reddit-awards.png")
OUT_DEFAULT = Path("reddit_post.svg")


# ============================================================
# SVG Paths (UNCHANGED)
# ============================================================

VERIFIED_BADGE_PATHS = [
    {
        "d": (
            "M12 1 L14.59 3.41 L18 4 L19 7.41 "
            "L21.41 10 L19 12.59 L18 16 "
            "L14.59 16.59 L12 19 L9.41 16.59 "
            "L6 16 L5 12.59 L2.59 10 "
            "L5 7.41 L6 4 L9.41 3.41 Z"
        ),
        "fill": "#42A5F5",
    },
    {
        "d": (
            "M9.5 12.5 L7.5 10.5 L6.5 11.5 "
            "L9.5 14.5 L17.5 6.5 L16.5 5.5 Z"
        ),
        "fill": "#FFFFFF",
    },
]

UPVOTE_PATH = (
    "M12 0.33 L20.56 13.2 H16.8 V17.85 "
    "C16.8 19.63 15.34 21.07 13.58 21.07 "
    "H10.42 C8.66 21.07 7.19 19.63 7.19 17.78 "
    "V13.2 H3.43 Z"
)

COMMENT_PATH = (
    "M10 19 H1.87 A0.88 0.88 0 0 1 1.07 18.48 "
    "L3.1 15.77 A9 9 0 1 1 10 19 Z"
)

SHARE_PATH = (
    "M2.68675 22.4675 "
    "C2.49173 22.4682 2.2985 22.4303 2.11814 22.3561 "
    "C1.93778 22.2819 1.77384 22.1729 1.63571 22.0352 "
    "C1.49759 21.8975 1.388 21.7339 1.31322 21.5538 "
    "C1.23844 21.3737 1.19995 21.1806 1.19995 20.9855 "
    "C1.19995 13.7999 5.78515 8.29194 12 7.80594 "
    "V4.33914 "
    "C12.0004 3.94836 12.1167 3.56649 12.3342 3.24185 "
    "C12.5517 2.9172 12.8607 2.66437 13.2219 2.51535 "
    "C13.5832 2.36633 13.9805 2.32781 14.3636 2.40467 "
    "C14.7468 2.48153 15.0985 2.67032 15.3744 2.94714 "
    "L23.6544 11.2895 "
    "C23.8424 11.4786 23.9479 11.7345 23.9479 12.0011 "
    "C23.9479 12.2678 23.8424 12.5236 23.6544 12.7127 "
    "L15.3744 20.9351 "
    "C15.0986 21.2127 14.7466 21.4021 14.363 21.4792 "
    "C13.9795 21.5563 13.5817 21.5177 13.2201 21.3683 "
    "C12.8585 21.2189 12.5494 20.9654 12.3322 20.64 "
    "C12.115 20.3146 11.9993 19.932 12 19.5407 "
    "V16.2287 "
    "C8.91235 16.5203 7.24675 18.3143 5.34355 20.3627 "
    "C4.81915 20.9267 4.28635 21.5015 3.71635 22.0511 "
    "C3.44035 22.3187 3.07075 22.4687 2.68675 22.4675 "
    "Z"
)



# ============================================================
# Helpers
# ============================================================

def wrap_text(text: str, size: int, max_width: int):
    chars_per_line = int(max_width / (size * CARD_WIDTH_CHAR_PER_LINE))
    wrapper = textwrap.TextWrapper(
        width=max(10, chars_per_line),
        break_long_words=False,
        break_on_hyphens=False,
    )
    return wrapper.wrap(text)


# ============================================================
# Public API
# ============================================================

def generate_reddit_svg(
    *,
    logo_path: Path,
    username: str,
    story_text: str,
    upvotes: str = "999.9K+",
    comments: str = "99.9K+",
    share_text: str = "Share",
    output_path: Path | None = None,
):
    try:
        if not logo_path.exists():
            raise FileNotFoundError(f"Logo not found: {logo_path}")

        for name, val in {
            "username": username,
            "story_text": story_text,
            "upvotes": upvotes,
            "comments": comments,
            "share_text": share_text,
        }.items():
            if not isinstance(val, str) or not val.strip():
                raise ValueError(f"Invalid {name}")

        out = output_path or OUT_DEFAULT

        TEXT_START_X = PADDING + LOGO // 2
        MAX_TEXT_WIDTH = CARD_WIDTH - TEXT_START_X - PADDING
        story_lines = len(wrap_text(story_text, STORY_SIZE, MAX_TEXT_WIDTH))

        CARD_HEIGHT = (
            PADDING + LOGO + LOGO_BOTTOM_PAD + HEADER_BOTTOM_PAD +
            story_lines * STORY_LINE + CONTENT_GAP + ICON + 5
        )
# Can skip this error 
        dwg = svgwrite.Drawing(out, size=(CARD_WIDTH, CARD_HEIGHT))

        dwg.add(dwg.rect(
            (0, 0), (CARD_WIDTH, CARD_HEIGHT),
            rx=RADIUS, ry=RADIUS,
            fill=BG, stroke=SKELETON
        ))

        y = PADDING

        # Logo
        add_logo(
            dwg=dwg,
            logo_path=logo_path,
            x=PADDING,
            y=y,
            size=LOGO,
            fallback_color=SKELETON,
        )

        username_x = PADDING + LOGO + HEADER_GAP
        username_y = y + 14

        dwg.add(dwg.text(
            username,
            insert=(username_x, username_y),
            font_size=13,
            font_weight="bold",
            font_family=USERNAME_FONT,
            fill=FG
        ))

        # Verified badge
        vx = username_x + 8 * len(username) + VERIFIED_GAP
        vy = username_y - VERIFIED_SIZE + 2
        scale = VERIFIED_SIZE / 24

        vg = dwg.g(transform=f"scale({scale}) translate({vx/scale},{vy/scale})")
        for p in VERIFIED_BADGE_PATHS:
            vg.add(dwg.path(d=p["d"], fill=p["fill"]))
        dwg.add(vg)

        # Awards
        add_inline_image(
            dwg=dwg,
            image_path=BADGE_PATH,
            x=username_x,
            y=username_y + BADGE_TOP_PAD,
            width=BADGE_WIDTH,
            height=BADGE_HEIGHT,
        )

        y += LOGO + LOGO_BOTTOM_PAD + HEADER_BOTTOM_PAD

        # Story
        for i, line in enumerate(wrap_text(story_text, STORY_SIZE, MAX_TEXT_WIDTH)):
            dwg.add(dwg.text(
                line,
                insert=(TEXT_START_X, y + i * STORY_LINE),
                font_size=STORY_SIZE,
                font_weight="bold",
                font_family=STORY_FONT,
                fill=FG
            ))

        y += story_lines * STORY_LINE + CONTENT_GAP - FOOTER_LIFT
        footer_center_y = y + ICON // 2
        x = TEXT_START_X

        # Upvotes
        scale = 0.6
        dwg.add(dwg.path(
            d=UPVOTE_PATH,
            fill=MUTED,
            transform=f"scale({scale}) translate({x/scale},{(y+ICON_OPTICAL_SHIFT)/scale})"
        ))
        dwg.add(dwg.text(
            upvotes,
            insert=(x + ICON + META_GAP, footer_center_y + TEXT_CENTER_OFFSET),
            font_size=META_SIZE,
            font_weight="bold",
            font_family=USERNAME_FONT,
            fill=MUTED
        ))

        # Comments
        UPVOTE_BLOCK_WIDTH = ICON + META_GAP + 45
        cx = x + UPVOTE_BLOCK_WIDTH + FOOTER_BLOCK_GAP

        dwg.add(dwg.path(
            d=COMMENT_PATH,
            fill=MUTED,
            transform=f"scale({scale}) translate({cx/scale},{(y+ICON_OPTICAL_SHIFT)/scale})"
        ))
        dwg.add(dwg.text(
            comments,
            insert=(cx + ICON + META_GAP, footer_center_y + TEXT_CENTER_OFFSET),
            font_size=META_SIZE,
            font_weight="bold",
            font_family=USERNAME_FONT,
            fill=MUTED
        ))

        # Share
        sx = CARD_WIDTH - RIGHT_PADDING - ICON * 4
        dwg.add(dwg.path(
            d=SHARE_PATH,
            fill=MUTED,
            transform=f"scale({scale}) translate({sx/scale},{(y+ICON_OPTICAL_SHIFT)/scale})"
        ))
        dwg.add(dwg.text(
            share_text,
            insert=(sx + ICON + META_GAP, footer_center_y + TEXT_CENTER_OFFSET),
            font_size=META_SIZE,
            font_weight="bold",
            font_family=USERNAME_FONT,
            fill=MUTED
        ))

        dwg.save()
        return out.resolve()

    except Exception as e:
        raise RuntimeError("Reddit SVG generation failed") from e
