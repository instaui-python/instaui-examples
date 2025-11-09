from dataclasses import dataclass
from typing import Callable, Optional


from pages.index_page.main import page as index_page
from pages.instaui_page.main import page as instaui_page
from pages.echarts_page.main import page as echarts_page
from pages.shiki_page.main import page as shiki_page
from pages.tdesign_page.main import page as tdesign_page
from pages.gallery_page.etch_sketch.main import page as etch_sketch_page
from pages.gallery_page.todo_list.main import page as todo_list_page


@dataclass
class PageInfo:
    page_fn: Callable
    web_url: str
    # website config
    file: str
    icons_svg_file: Optional[str] = None


def get_page_infos():
    infos = [
        PageInfo(
            index_page, web_url="/", file="index.html", icons_svg_file="index.svg"
        ),
        PageInfo(instaui_page, web_url="/instaui", file="instaui.html"),
        PageInfo(echarts_page, web_url="/instaui-echarts", file="instaui-echarts.html"),
        PageInfo(shiki_page, web_url="/instaui-shiki", file="instaui-shiki.html"),
        PageInfo(tdesign_page, web_url="/instaui-tdesign", file="instaui-tdesign.html"),
        PageInfo(
            etch_sketch_page,
            web_url="/gallery/etch-sketch",
            file="gallery/etch-sketch.html",
        ),
        PageInfo(
            todo_list_page,
            web_url="/gallery/todo-list",
            file="gallery/todo-list.html",
            icons_svg_file="todo_list.svg",
        ),
    ]

    return infos
