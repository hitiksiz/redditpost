from pathlib import Path
from reddit_svg  import generate_reddit_svg
import svgwrite

result = generate_reddit_svg(
    logo_path=Path("assets/logo/TinyLlama_logo.png"),
    username="r/H_Reddits",
    story_text="This is a test story."
)

if result:
    print("Generated:", result)
else:
    print("Failed")
