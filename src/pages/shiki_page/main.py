from instaui import tailwind, ui
from instaui_shiki import __version__ as shiki_version
from instaui_tdesign import td

from page_state import I18nState
from shared.main_view import main_view

from . import shiki_examples


def page():
    tailwind.use_tailwind(version="v4")
    infos = shiki_examples.index()
    N_ = I18nState.get()

    main_view(
        header_title=N_("instaui-shiki 示例"),
        github_link="https://github.com/instaui-python/instaui-shiki",
        example_infos=infos,
        dependencies=[
            f"instaui[web]>={ui.__version__}",
            f"instaui_shiki>={shiki_version}",
            f"instaui_tdesign>={td.__version__}",
        ],
    )
