from instaui import ui

from shared.page_header import header_view
from .components import todo_app


def page():
    header_view(
        title="todo list",
        home_icon_level=2,
        github_link="https://github.com/instaui-python/instaui-examples/tree/main/src/gallery/todo_list",
    )

    with ui.container(size="2"), ui.column(gap="3", px="3", pb="2"):
        todo_app()
