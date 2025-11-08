from instaui import ui
from instaui_tdesign import td
from shared.main_view import main_view
from page_state import I18nState
from . import views


def page():
    infos = views.index()
    N_ = I18nState.get()

    main_view(
        header_title=N_("instaui-tdesign 示例"),
        github_link="https://github.com/instaui-python/instaui-tdesign",
        example_infos=infos,
        dependencies=[
            f"instaui[web]>={ui.__version__}",
            f"instaui_tdesign>={td.__version__}",
        ],
    )
