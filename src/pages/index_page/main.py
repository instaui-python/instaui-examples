from instaui import ui, html
from instaui_tdesign import td

from page_state import I18nState
from shared.page_header import header_view


def page():
    N_ = I18nState.get()

    with ui.container():
        header_view(
            home_icon_level=None,
            github_link="https://github.com/instaui-python/instaui-examples",
        )

        with ui.row(justify="center", my="3"):
            ui.text("Insta-UI", size="7", weight="bold").style("color: green;")
            ui.text(N_("示例"), size="7", weight="bold")

        with ui.grid(columns=ui.grid.auto_columns(min_width="280px")):
            card("index:feather", "instaui", N_("基础库"), "./instaui")
            card(
                "index:chart",
                "instaui echarts",
                N_("Echarts 图表"),
                "./instaui-echarts",
            )
            card("index:code", "instaui shiki", N_("代码高亮"), "./instaui-shiki")
            card(
                "index:td",
                "instaui tdesign",
                N_("TDesign 组件"),
                "./instaui-tdesign",
            )

        td.divider()

        with ui.box(mb="3", as_child=True):
            ui.heading(N_("更多示例"))

        with ui.grid(columns=ui.grid.auto_columns(min_width="280px", mode="auto-fill")):
            card(
                "index:gallery",
                "etch sketch",
                "etch sketch(solid js example)",
                "./gallery/etch-sketch",
            )


def card(icon: str, title: str, description: str, url_name: str):
    with (
        html.link(url_name).style("text-decoration:none;"),
        td.card(hover_shadow=True) as card,
    ):
        with card.add_slot("title"):
            with ui.row(align="center"):
                ui.icon(icon, color="#91e17fff", size="2rem")
                ui.text(title, weight="bold", size="7", text_wrap="nowrap")

        ui.text(description, size="4", weight="light")
