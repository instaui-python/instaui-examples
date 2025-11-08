from instaui import ui, html
from shared.page_header import header_view

# https://www.solidjs.com/examples/ethasketch


def page():
    ui.add_style(r".cell {outline: 1px solid #1f1f1f;}")
    ui.add_js_code(r"""
    function randomHexColorString() {
    return "#" + Math.floor(Math.random() * 16777215).toString(16);
    }
    """)

    max_grid_pixel_width = 500
    mouse_enter = ui.js_event(
        inputs=[ui.event_context.e()],
        code=r"""(event)=>{
    const eventEl = event.currentTarget;

    eventEl.style.backgroundColor = randomHexColorString();

    setTimeout(() => {
        eventEl.style.backgroundColor = "initial";
    }, 500);  
}
""",
    )

    grid_size = ui.state(10)

    template_str = ui.js_computed(
        inputs=[grid_size, max_grid_pixel_width],
        code=r"""
    (grid_size, max_grid_pixel_width) => `repeat(${grid_size}, ${max_grid_pixel_width/grid_size}px)`
""",
    )

    cells = ui.js_computed(
        inputs=[grid_size], code=r" (grid_size) => Array(grid_size**2).fill(0)"
    )

    header_view(
        title="etch sketch",
        home_icon_level=2,
        github_link="https://github.com/instaui-python/instaui-examples/tree/main/src/gallery/etch_sketch",
    )

    with ui.container():
        with ui.column(m="4"):
            with ui.box(mx="auto", as_child=True):
                html.number(min=4, max=20, value=grid_size)

            with ui.grid(columns=template_str, rows=template_str, gap="0", mx="auto"):
                with ui.vfor(cells):
                    ui.element("div").classes("cell").on("mouseenter", mouse_enter)
