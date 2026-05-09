from instaui import html, ui
from instaui_tdesign import td

from page_state import I18nState
from shared.cmd import parse_offline_flag
from shared.layout import container
from shared.link import with_resolve_link_path
from shared.page_header import header_view


def page():
    N_ = I18nState.get()
    resolve_link_path = with_resolve_link_path()

    with container():
        header_view(
            home_icon_level=None,
            github_link="https://github.com/instaui-python/instaui-examples",
        )

        with ui.row(justify="center").classes("gap-2 my-4"):
            ui.text("Insta-UI").classes("text-3xl font-bold").style("color: green;")
            ui.text(N_("示例")).classes("text-3xl font-bold")

        with ui.grid(columns=ui.grid.auto_columns(min_width="280px")).classes("gap-2"):
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

        html.h1(N_("更多示例")).classes("m-2 text-2xl")

        with ui.grid(
            columns=ui.grid.auto_columns(min_width="280px", mode="auto-fill")
        ).classes("gap-2"):
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
        html.a(href=url_name),
        td.card(hover_shadow=True) as card,
    ):
        with card.add_slot("title"):
            with ui.row(align="center").classes("gap-2"):
                ui.icon(icon, color="#91e17fff", size="2rem")
                ui.text(title).classes(
                    "font-bold text-2xl sm:text-3xl tracking-tight whitespace-nowrap"
                )

        ui.text(description).classes(
            "text-gray-600 text-base sm:text-lg leading-relaxed mt-2"
        )
