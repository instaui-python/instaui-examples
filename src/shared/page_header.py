from typing import Optional
from instaui import ui, html
from .lang_select import lang_select as lang_select_view


class header_view:
    def __init__(self, *, lang_select=True, github_link: Optional[str] = None):
        pass

        with ui.row(align="center", px="3"):
            ui.box(flex_grow="1")
            self.__action_box = ui.row(align="center")

            if lang_select:
                with self.__action_box:
                    lang_select_view()

                    if github_link:
                        with (
                            html.link(github_link)
                            .props({"target": "_blank"})
                            .style("display:inline-flex; align-items:center;")
                        ):
                            ui.icon("i:github", size="1.5rem")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def actions_slot(self):
        return self.__action_box
