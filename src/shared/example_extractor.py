from dataclasses import dataclass, field
from typing import Callable, Optional
from instaui import ui
from instaui_shiki import shiki
from instaui_tdesign import td
import inspect


@dataclass
class ExampleInfo:
    title: str
    title_id: str
    fn: Callable
    imports: Optional[list[str]] = field(default_factory=list)
    ignore_indent_condition: Optional[Callable[[str], bool]] = None


def get_function_body(
    func, indent=4, ignore_indent_condition: Optional[Callable[[str], bool]] = None
):
    source = inspect.getsource(func)
    lines = source.splitlines()
    if len(lines) <= 1:
        return ""

    body_start = next(
        (i for i, line in enumerate(lines) if line.lstrip().startswith("def ")), 0
    )

    body = "\n".join(lines[body_start + 1 :])

    # indent_str = " " * indent

    # indent_predicate = (
    #     None
    #     if ignore_indent_condition is None
    #     else lambda line: not ignore_indent_condition(line)
    # )
    # body = textwrap.indent(body, indent_str, predicate=indent_predicate)
    return body


def use_example_infos(require_imports: Optional[list[str]] = None):
    infos: list[ExampleInfo] = []

    def decorator(
        title: str,
        title_id: str,
        imports: Optional[list[str]] = None,
        ignore_indent_condition: Optional[Callable[[str], bool]] = None,
    ):
        def wrapper(fn: Callable):
            infos.append(
                ExampleInfo(
                    title,
                    title_id,
                    fn,
                    [*(imports or []), *(require_imports or [])],
                    ignore_indent_condition,
                )
            )

        return wrapper

    return decorator, infos


def example_view(info: ExampleInfo):
    imports = info.imports or []
    imports = ["from instaui import ui", *imports]
    imports_code = "\n".join(imports)

    fn_code = get_function_body(
        info.fn, ignore_indent_condition=info.ignore_indent_condition
    )
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
