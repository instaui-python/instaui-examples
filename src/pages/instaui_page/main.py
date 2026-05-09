from instaui import tailwind, ui
from instaui_tdesign import td

from page_state import I18nState
from shared.main_view import main_view

from . import views


def page():
    tailwind.use_tailwind(version="v4")
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
