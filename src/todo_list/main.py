from instaui import ui, zero
import instaui_tdesign as td
from components import app

td.use(theme="violet")


@ui.page()
def home():
    with ui.container(size="2"), ui.column(gap="3"):
        app()


zero(icons_svg_path="assets/icons/zero_icons.svg").to_html(
    home, file=r"instaui-todo-app\index.html"
)


ui.server(debug=True).run()
