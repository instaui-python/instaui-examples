from instaui import ui
from instaui_tdesign import td
from utils import ExampleInfo


def navigation_tree(infos: list[ExampleInfo]):
    with td.affix(offset_top=50):
        with ui.box(mt="4"), td.anchor(target_offset=200):
            for info in infos:
                td.anchor_item(
                    title=info.title,
                    href=f"#{info.title_id.lower().replace(' ', '-')}",
                )
