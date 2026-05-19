from instaui import ui
from instaui_tdesign import td

from .dependency_view import dependencies_zone
from .example_extractor import ExampleInfo, example_list_view
from .navigation import nav_items_from_infos, navigation_tree
from .page_header import header_view


def main_view(
    header_title: str,
    github_link: str,
    example_infos: list[ExampleInfo],
    dependencies: list[str],
):
    goto_nav_node = ui.js_event(
        code=r"""()=>{
    const hash = window.location.hash.slice(1);

    if (hash) {
        const el = document.getElementById(hash);
        if (el) {
            setTimeout(() => {
                el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 800);
        }
    }   

}"""
    )

    with (
        ui.column()
        .classes("h-full overflow-y-hidden p-4 gap-2")
        .on_mounted(goto_nav_node)
    ):
        header_view(
            title=header_title,
            github_link=github_link,
        )

        with ui.grid(columns="auto 1fr").classes("grow overflow-y-hidden gap-2"):
            navigation_tree(nav_items_from_infos(example_infos))

            with (
                ui.column()
                .classes("example-list gap-4 overflow-y-auto")
                .scoped_style("flex:0 0 auto", selector="> *")
            ):
                dependencies_zone(dependencies)

                example_list_view(example_infos)

    td.back_top(container=".example-list", shape="circle", theme="primary")
