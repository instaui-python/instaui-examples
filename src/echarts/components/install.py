from instaui_tdesign import td
from instaui_echarts import __version__ as echarts_version
from instaui_shiki import shiki


def dependencies_zone():
    libs = f"instaui[web] instaui_echarts>={echarts_version} instaui_tdesign>={td.__version__} polars"

    with td.tabs(default_value="uv"):
        with td.tab_panel(value="pip", label="pip", destroy_on_hide=False):
            shiki(f"pip install {libs}")
        with td.tab_panel(value="uv", label="uv", destroy_on_hide=False):
            shiki(f"uv add {libs}")
