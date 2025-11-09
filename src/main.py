from pathlib import Path
from typing import Callable
from instaui import ui
from instaui_tdesign import td, locales
from shared.css import apply_css
from shared.cmd import parse_no_server_flag
from shared.lang_select import I18nPageState

from page_loader import get_page_infos


td.use(theme="violet", locale="en_US")
apply_css()


class I18nState(I18nPageState, locale_dir=Path(__file__).parent / "locale"):
    pass


def wrapped_page(page_fn: Callable):
    def page():
        locale_dict, _ = locales.use_locale_dict(type="client")

        with td.config_provider(global_config=locale_dict):
            page_fn()

    return page


for info in get_page_infos():
    ui.page(info.web_url)(wrapped_page(info.page_fn))


if not parse_no_server_flag():
    ui.server(debug=True).run()
