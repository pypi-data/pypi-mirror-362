from pathlib import Path

from PIL import Image

CURRENT_DIR = Path(__file__).parent

if __name__ == "__main__":
    im = Image.new("RGB", (3_000, 3_000), "black")
    im.save(CURRENT_DIR / "black.png")
