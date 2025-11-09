from instaui_tdesign import td
from shared.css import apply_css
from shared.cmd import parse_offline_flag
from shared.website_utils import zero_dist_to_website
from page_loader import get_page_infos


td.use(theme="violet", locale="en_US")
apply_css()


def build_website():
    offline = parse_offline_flag()
    print(f"🔧 Building website[offline={offline}]...")

    for info in get_page_infos():
        zero_dist_to_website(
            info.page_fn, file=info.file, icons_svg_file=info.icons_svg_file
        )

    print("✅ All html pages generated successfully. see website folder.")


if __name__ == "__main__":
    build_website()
