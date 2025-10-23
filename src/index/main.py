import sys
from pathlib import Path
from instaui import ui, html
from instaui_tdesign import td, locales

SRC_DIR = Path(__file__).resolve().parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shared.lang_select import I18nPageState
from shared.website_utils import zero_dist_to_website
from shared.page_header import header_view

td.use(theme="violet", locale="en_US")


class I18nState(I18nPageState, locale_dir=Path(__file__).parent / "locale"):
    pass


@ui.page()
def home():
    locale_dict, _ = locales.use_locale_dict(type="client")
    _ = I18nState.get()

    with td.config_provider(global_config=locale_dict):
        with ui.container():
            header_view(
                home_icon_level=None,
                github_link="https://github.com/instaui-python/instaui-examples",
            )

            with ui.row(justify="center", my="3"):
                ui.text("Insta-UI", size="7", weight="bold").style("color: green;")
                ui.text(_(" 示例"), size="7", weight="bold")

            with ui.grid(columns=ui.grid.auto_columns(min_width="280px")):
                card("i:feather", "instaui", _("基础库"), "./instaui.html")
                card(
                    "i:chart",
                    "instaui echarts",
                    _("Echarts 图表"),
                    "./instaui-echarts.html",
                )
                card("i:code", "instaui shiki", _("代码高亮"), "./instaui-shiki.html")
                card(
                    "i:td",
                    "instaui tdesign",
                    _("TDesign 组件"),
                    "./instaui-tdesign.html",
                )

            td.divider()

            with ui.box(mb="3", as_child=True):
                ui.heading(_("更多示例"))

            with ui.grid(
                columns=ui.grid.auto_columns(min_width="280px", mode="auto-fill")
            ):
                card(
                    "i:gallery",
                    "etch sketch",
                    "etch sketch(solid js example)",
                    "./gallery/etch_sketch.html",
                )


def card(icon: str, title: str, description: str, url_name: str):
    with (
        html.link(url_name).props({"target": "_blank"}).style("text-decoration:none;"),
        td.card(hover_shadow=True) as card,
    ):
        with card.add_slot("title"):
            with ui.row(align="center"):
                ui.icon(icon, color="#91e17fff", size="2rem")
                ui.text(title, weight="bold", size="7", text_wrap="nowrap")

        ui.text(description, size="4", weight="light")


def build_state_html():
    zero_dist_to_website(
        home,
        base_folder=Path(__file__).parent,
        file="index.html",
    )


# ui.server(debug=True).run()

if __name__ == "__main__":
    build_state_html()
