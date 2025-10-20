import sys
from pathlib import Path

# 获取 src 的路径（上上级目录）
SRC_DIR = Path(__file__).resolve().parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from instaui import ui
from instaui_tdesign import td, locales
from instaui import ui
from instaui_shiki import cdn as shiki_cdn
from instaui_tdesign import td, locales
from instaui_echarts import cdn as echarts_cdn
import components
from utils import chart_example

from shared.lang_select import I18nPageState
from shared.website_utils import zero_dist_to_website


class I18nState(I18nPageState, locale_dir=Path(__file__).parent / "locale"):
    pass


td.use(theme="violet", locale="en_US")


@ui.page()
def home():
    from graphics_examples import infos

    locale_dict, _ = locales.use_locale_dict(type="client")
    _ = I18nState.get()

    with td.config_provider(global_config=locale_dict):
        components.lang_select()

        with ui.grid(columns="auto 1fr"):
            components.navigation_tree(infos)

            with ui.container(size="4"), ui.column(gap="4"):
                ui.heading(_("instaui-echarts 示例"))

                components.dependencies_zone()

                for info in infos:
                    chart_example(info)

            td.back_top(container=".insta-main", shape="circle", theme="primary")


zero_dist_to_website(
    home,
    base_folder=Path(__file__).parent,
    cdns=[shiki_cdn.override(), echarts_cdn.override()],
    file="instaui-echarts.html",
)


# ui.server(debug=True).run()
