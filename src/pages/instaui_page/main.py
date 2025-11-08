from typing import Callable
from instaui import ui
from instaui_tdesign import td, cdn as td_cdn
from instaui_shiki import cdn as shiki_cdn
from shared.main_view import main_view
from page_state import I18nState
from . import views


def page():
    N_ = I18nState.get()
    infos = views.index()

    main_view(
        header_title=N_("instaui 示例"),
        github_link="https://github.com/instaui-python/instaui",
        example_infos=infos,
        dependencies=[
            f"instaui[web]>={ui.__version__}",
            f"instaui_tdesign>={td.__version__}",
        ],
    )


# if not parse_no_server_flag():
#     ui.server(debug=True).run()


# def build_html():
#     zero_dist_to_website(
#         home,
#         base_folder=Path(__file__).parent,
#         cdns=[shiki_cdn.override(), td_cdn.override()],
#         file="instaui.html",
#     )


# if __name__ == "__main__":
#     build_html()
