from instaui import ui

from shared.layout import container
from shared.page_header import header_view

from .components import todo_app


def page():

    with container():
        header_view(
            title="todo list",
            home_icon_level=2,
            github_link="https://github.com/instaui-python/instaui-examples/tree/main/src/gallery/todo_list",
        )

        with ui.column().classes("gap-3 px-3 pb-2"):
            todo_app()
