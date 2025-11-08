import sys
from pathlib import Path


from instaui import ui
from instaui_tdesign import td, locales
from instaui_shiki import cdn as shiki_cdn
from instaui_echarts import cdn as echarts_cdn, __version__ as echarts_version

SRC_DIR = Path(__file__).resolve().parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from utils import I18nState
from shared.cmd import parse_no_server_flag
from shared.main_view import main_view
from shared.website_utils import zero_dist_to_website
from shared.css import apply_css

td.use(theme="violet", locale="en_US")
apply_css()


@ui.page()
def home():
    from graphics_examples import infos

    locale_dict, _ = locales.use_locale_dict(type="client")
    N_ = I18nState.get()

    with td.config_provider(global_config=locale_dict):
        main_view(
            header_title=N_("instaui-echarts 示例"),
            github_link="https://github.com/instaui-python/instaui-echarts",
            example_infos=infos,
            dependencies=[
                f"instaui[web]>={ui.__version__}",
                f"instaui_echarts>={echarts_version}",
                f"instaui_tdesign>={td.__version__}",
                "polars",
            ],
        )


if not parse_no_server_flag():
    ui.server(debug=True).run()


def build_state_html():
    zero_dist_to_website(
        home,
        base_folder=Path(__file__).parent,
        cdns=[shiki_cdn.override(), echarts_cdn.override()],
        file="instaui-echarts.html",
    )


if __name__ == "__main__":
    build_state_html()
