from instaui import ui, html
from instaui_tdesign import td

from page_state import I18nState
from shared.page_header import header_view
from shared.cmd import parse_offline_flag
from shared.link import with_resolve_link_path


def page():
    N_ = I18nState.get()
    resolve_link_path = with_resolve_link_path()

    with ui.container():
        header_view(
            home_icon_level=None,
            github_link="https://github.com/instaui-python/instaui-examples",
        )

        with ui.row(justify="center", my="3"):
            ui.text("Insta-UI", size="7", weight="bold").style("color: green;")
            ui.text(N_("示例"), size="7", weight="bold")

        with ui.grid(columns=ui.grid.auto_columns(min_width="280px")):
            card(
                "index:feather", "instaui", N_("基础库"), resolve_link_path("./instaui")
            )
            card(
                "index:chart",
                "instaui echarts",
                N_("Echarts 图表"),
                resolve_link_path("./instaui-echarts"),
            )
            card(
                "index:code",
                "instaui shiki",
                N_("代码高亮"),
                resolve_link_path("./instaui-shiki"),
            )
            card(
                "index:td",
                "instaui tdesign",
                N_("TDesign 组件"),
                resolve_link_path("./instaui-tdesign"),
            )

        td.divider()

        with ui.box(mb="3", as_child=True):
            ui.heading(N_("更多示例"))

        with ui.grid(columns=ui.grid.auto_columns(min_width="280px", mode="auto-fill")):
            card(
                "index:gallery",
                "etch sketch",
                "etch sketch(solid js example)",
                resolve_link_path("./gallery/etch-sketch"),
            )

            card(
                "index:gallery",
                "todo list",
                "todo list app",
                resolve_link_path("./gallery/todo-list"),
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
