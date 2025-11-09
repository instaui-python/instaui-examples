from instaui import ui
from .components import todo_app


def page():
    with ui.container(size="2"), ui.column(gap="3", px="3", pb="2"):
        todo_app()
