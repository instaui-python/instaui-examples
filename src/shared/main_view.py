from instaui import ui
from instaui_tdesign import td
from .example_extractor import ExampleInfo
from .navigation import navigation_tree, nav_items_from_infos
from .dependency_view import dependencies_zone
from .example_extractor import example_list_view
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

    with ui.column(height="100%", overflow_y="hidden").on_mounted(goto_nav_node):
        header_view(
            title=header_title,
            github_link=github_link,
        )

        with ui.grid(columns="auto 1fr", flex_grow="1", overflow_y="hidden"):
            navigation_tree(nav_items_from_infos(example_infos))

            with (
                ui.column(gap="4", overflow_y="auto")
                .classes("example-list")
                .scoped_style("flex:0 0 auto", selector="> *")
            ):
                dependencies_zone(dependencies)

                example_list_view(example_infos)

    td.back_top(container=".example-list", shape="circle", theme="primary")
