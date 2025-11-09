from pathlib import Path
from typing import Callable
from instaui import ui
from instaui_tdesign import td, locales
from shared.css import apply_css
from shared.cmd import parse_no_server_flag
from shared.lang_select import I18nPageState

# from shared.website_utils import zero_dist_to_website
from pages.index_page.main import page as index_page
from pages.instaui_page.main import page as instaui_page
from pages.echarts_page.main import page as echarts_page
from pages.shiki_page.main import page as shiki_page
from pages.tdesign_page.main import page as tdesign_page
from pages.gallery_page.etch_sketch.main import page as etch_sketch_page
from pages.gallery_page.todo_list.main import page as todo_list_page

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


ui.page("/")(wrapped_page(index_page))
ui.page("/instaui")(wrapped_page(instaui_page))
ui.page("/instaui-echarts")(wrapped_page(echarts_page))
ui.page("/instaui-shiki")(wrapped_page(shiki_page))
ui.page("/instaui-tdesign")(wrapped_page(tdesign_page))
ui.page("/gallery/etch-sketch")(wrapped_page(etch_sketch_page))
# ui.page("/gallery/todo-list")(wrapped_page(todo_list_page))


if not parse_no_server_flag():
    ui.server(debug=True).run()
