from pathlib import Path
from instaui import ui

CSS_FILE_DIR = Path(__file__).parent / "css_file"


def apply_css():
    ui.add_style((CSS_FILE_DIR / "index.css").read_text(encoding="utf-8"))
