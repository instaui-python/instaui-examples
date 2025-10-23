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
from shared.navigation import navigation_tree, NavItem
from shared.dependency_view import dependencies_zone
from shared.website_utils import zero_dist_to_website
from shared.example_extractor import example_view
from shared.page_header import header_view

td.use(theme="violet", locale="en_US")


@ui.page()
def home():
    from graphics_examples import infos

    locale_dict, _ = locales.use_locale_dict(type="client")
    _ = I18nState.get()

    with td.config_provider(global_config=locale_dict):
        header_view(
            title=_("instaui-echarts 示例"),
            github_link="https://github.com/instaui-python/instaui-examples/tree/main/src/echarts",
        )

        with ui.grid(columns="auto 1fr"):
            navigation_tree(
                [NavItem(title=info.title, id=info.title_id) for info in infos]
            )

            with ui.container(size="4"), ui.column(gap="4"):
                dependencies_zone(
                    [
                        "instaui[web]",
                        f"instaui_echarts>={echarts_version}",
                        f"instaui_tdesign>={td.__version__}",
                        "polars",
                    ]
                )

                for info in infos:
                    example_view(info)

            td.back_top(container=".insta-main", shape="circle", theme="primary")


def build_state_html():
    zero_dist_to_website(
        home,
        base_folder=Path(__file__).parent,
        cdns=[shiki_cdn.override(), echarts_cdn.override()],
        file="instaui-echarts.html",
    )


ui.server(debug=True).run()

if __name__ == "__main__":
    build_state_html()
