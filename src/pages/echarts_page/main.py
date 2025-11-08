from instaui import ui
from instaui_tdesign import td
from instaui_echarts import __version__ as echarts_version
from page_state import I18nState
from shared.main_view import main_view
from . import graphics_examples


def page():
    N_ = I18nState.get()
    infos = graphics_examples.index()

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


# if not parse_no_server_flag():
#     ui.server(debug=True).run()


# def build_state_html():
#     zero_dist_to_website(
#         home,
#         base_folder=Path(__file__).parent,
#         cdns=[shiki_cdn.override(), echarts_cdn.override()],
#         file="instaui-echarts.html",
#     )


# if __name__ == "__main__":
#     build_state_html()
