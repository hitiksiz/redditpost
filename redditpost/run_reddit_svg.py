from pathlib import Path
from reddit_svg import generate_reddit_svg

svg = generate_reddit_svg(
    logo_path=Path("assets/logo/TinyLlama_logo.png"),
    username="r/QuietThoughts",
    story_text="This is a test story",
    upvotes="1.2M",
    comments="84.3K",
    share_text="Share"
)

print(svg)
