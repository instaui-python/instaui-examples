from instaui_tdesign import td
from instaui_shiki import shiki


def dependencies_zone(libs: list[str]):
    libs_code = " ".join(libs)

    with td.tabs(default_value="uv"):
        with td.tab_panel(value="pip", label="pip", destroy_on_hide=False):
            shiki(f"pip install {libs_code}")
        with td.tab_panel(value="uv", label="uv", destroy_on_hide=False):
            shiki(f"uv add {libs_code}")
