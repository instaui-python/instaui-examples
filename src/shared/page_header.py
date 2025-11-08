from typing import Optional
from instaui import ui, html
from instaui_tdesign import td
from .lang_select import lang_select as lang_select_view


class header_view:
    def __init__(
        self,
        *,
        title: Optional[str] = None,
        lang_select=True,
        github_link: Optional[str] = None,
        home_icon_level: Optional[int] = 1,
    ):
        pass

        with ui.row(align="center", px="3", pb="2").style(
            "border-bottom: 1px solid #e5e5e5;"
        ):
            if home_icon_level is not None:
                with ui.link(href=("." * home_icon_level) + "/"):
                    ui.icon(
                        raw_svg=r"""<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 16 16"><!-- Icon from OpenSearch UI by OpenSearch Contributors - https://github.com/opensearch-project/oui/blob/main/LICENSE.txt --><path fill="#888888" fill-rule="evenodd" d="M14.516 9H10.5a.5.5 0 0 1 0-1h4.016L13.11 5.948c-.171-.252-.137-.62.079-.821s.531-.159.703.092l2 2.916a.65.65 0 0 1 .108.397a.64.64 0 0 1-.108.332l-2 2.918A.48.48 0 0 1 13.5 12a.46.46 0 0 1-.312-.127a.65.65 0 0 1-.079-.82zM3 15H1a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h7.8c.274 0 .537.113.726.312l2.2 2.428c.176.186.274.433.274.689V7h-1V5H8.5a.5.5 0 0 1-.5-.5V2H3v12h8v-4h1v4a1 1 0 0 1-1 1zm-1-1V2H1v12z"/></svg>"""
                    )

            if title:
                ui.heading(title, size="3", weight="bold")

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
                            ui.icon("shared:github", size="1.5rem")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def actions_slot(self):
        return self.__action_box
