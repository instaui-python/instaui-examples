from instaui import ui, zero
import instaui_tdesign as td
from components import todo_app
import utils

td.use(theme="violet")


@ui.page()
def home():
    with ui.container(size="2"), ui.column(gap="3"):
        todo_app()


utils.zero_dist(home)


ui.server(debug=True).run()
