from instaui import ui, zero, cdn
from instaui_shiki import shiki, cdn as shiki_cdn


@ui.page()
def index():
    shiki('print("Hello, world!')


config = zero(cdn_resource_overrides=[cdn.override(), shiki_cdn.override()])

config.to_debug_report(index, file="debug.html")
config.to_html(index, file="index.html")


ui.server(debug=True).run()
