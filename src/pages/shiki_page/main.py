from instaui import ui
from instaui_tdesign import td
from instaui_shiki import __version__ as shiki_version
from shared.main_view import main_view
from page_state import I18nState
from . import shiki_examples


def page():
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
