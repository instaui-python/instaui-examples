from dataclasses import dataclass, field
from typing import Callable, Optional
from instaui import ui
from instaui_shiki import shiki
from instaui_tdesign import td
import inspect
import textwrap


@dataclass
class ExampleInfo:
    title: str
    title_id: str
    fn: Callable
    imports: Optional[list[str]] = field(default_factory=list)


def get_function_body(func, indent=4):
    source = inspect.getsource(func)
    lines = source.splitlines()
    if len(lines) <= 1:
        return ""

    body_start = next(
        (i for i, line in enumerate(lines) if line.lstrip().startswith("def ")), 0
    )

    body = textwrap.dedent("\n".join(lines[body_start + 1 :]))

    indent_str = " " * indent
    body = textwrap.indent(body, indent_str)
    return body


def use_example_infos():
    infos: list[ExampleInfo] = []

    def decorator(title: str, title_id: str, imports: Optional[list[str]] = None):
        def wrapper(fn: Callable):
            infos.append(ExampleInfo(title, title_id, fn, imports))

        return wrapper

    return decorator, infos


def chart_example(info: ExampleInfo):
    imports = info.imports or []
    imports = [
        "from instaui import ui",
        *imports,
        "from instaui_echarts import graphics as gh, echarts",
    ]
    imports_code = "\n".join(imports)

    fn_code = get_function_body(info.fn)
    code = f"""
{imports_code}

@ui.page()
def index():
{fn_code}

ui.server(debug=True).run()
"""

    with (
        td.card(title=info.title, header_bordered=True).props(
            {"id": f"{info.title_id.lower().replace(' ', '-')}"}
        ),
        ui.grid(columns=2),
    ):
        with td.card(body_style={"height": "100%"}):
            info.fn()
        shiki(code, line_numbers=True)
