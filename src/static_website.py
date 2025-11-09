from instaui_tdesign import td
from shared.css import apply_css

from shared.website_utils import zero_dist_to_website
from pages.index_page.main import page as index_page
from pages.instaui_page.main import page as instaui_page
from pages.echarts_page.main import page as echarts_page
from pages.shiki_page.main import page as shiki_page
from pages.tdesign_page.main import page as tdesign_page
from pages.gallery_page.etch_sketch.main import page as etch_sketch_page

td.use(theme="violet", locale="en_US")
apply_css()


def build_website():
    zero_dist_to_website(index_page, file="index.html", icons_svg_file="index.svg")
    zero_dist_to_website(instaui_page, file="instaui.html")
    zero_dist_to_website(echarts_page, file="instaui-echarts.html")
    zero_dist_to_website(shiki_page, file="instaui-shiki.html")
    zero_dist_to_website(tdesign_page, file="instaui-tdesign.html")
    zero_dist_to_website(etch_sketch_page, file="gallery/etch-sketch.html")

    print("✅ All html pages generated successfully. see website folder.")


if __name__ == "__main__":
    build_website()
