from pathlib import Path
from typing import Any, Dict, List, Literal
from instaui import ui, zero, html, cdn
import instaui_tdesign as td
from instaui_tdesign import cdn as td_cdn
import main_cell_slot

td.use(theme="violet", locale="zh-CN")


@ui.page("/")
def index():
    with ui.container():
        td.link(href=main_cell_slot.url, content="Cell Slot")


ui.page(main_cell_slot.url)(main_cell_slot.index)

ui.server(debug=True).run()
