from __future__ import annotations
from dataclasses import dataclass, field
import textwrap
import re
from typing import Callable, Optional
import inspect
from contextlib import contextmanager
from instaui import ui
from instaui_shiki import shiki
from instaui_tdesign import td


@dataclass
class ExampleInfo:
    title: str
    title_id: str
    fn: Optional[Callable] = None
    children: list[ExampleInfo] = field(default_factory=list)
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
    body = textwrap.dedent(body)

    indent_str = " " * indent

    indent_predicate = (
        None
        if ignore_indent_condition is None
        else lambda line: not ignore_indent_condition(line)
    )
    body = textwrap.indent(body, indent_str, predicate=indent_predicate)
    return body


def transform_mark_blocks(code: str) -> str:
    lines = code.splitlines(True)  # keep line endings
    result = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        if re.match(r"^\s*# mark\b", line):
            # Enter mark block
            i += 1
            mark_block = []

            # Collect mark block lines
            while i < n and not re.match(r"^\s*# end-mark\b", lines[i]):
                mark_block.append(lines[i])
                i += 1
            i += 1  # Skip # end-mark

            # Extract and convert "to" block
            inside_to = False
            converted = []
            for ml in mark_block:
                if re.match(r"^\s*# to\b", ml):
                    inside_to = True
                    continue
                if re.match(r"^\s*# end-to\b", ml):
                    inside_to = False
                    continue
                if inside_to:
                    # Only remove a single leading '# ' keeping indentation
                    converted.append(re.sub(r"^(\s*)# ?", r"\1", ml))

            result.extend(converted)

        else:
            result.append(line)
            i += 1

    return "".join(result)


def use_example_infos(require_imports: Optional[list[str]] = None):
    infos: list[ExampleInfo] = []
    current_node: Optional[ExampleInfo] = None

    def decorator(
        title: str,
        title_id: str,
        imports: Optional[list[str]] = None,
        ignore_indent_condition: Optional[Callable[[str], bool]] = None,
    ):
        def wrapper(fn: Callable):
            info = ExampleInfo(
                title,
                title_id,
                fn,
                imports=[*(imports or []), *(require_imports or [])],
                ignore_indent_condition=ignore_indent_condition,
            )

            if current_node:
                current_node.children.append(info)

            else:
                infos.append(info)

        return wrapper

    @contextmanager
    def root_node(
        title: str,
        title_id: str,
    ):
        nonlocal current_node
        current_node = ExampleInfo(title, title_id)
        infos.append(current_node)
        yield
        current_node = None

    return decorator, infos, root_node


def example_view(info: ExampleInfo):
    if info.fn is None:
        return

    imports = info.imports or []
    imports = ["from instaui import ui", *imports]
    imports_code = "\n".join(imports)

    fn_code = get_function_body(
        info.fn, ignore_indent_condition=info.ignore_indent_condition
    )

    fn_code = transform_mark_blocks(fn_code)

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


def example_list_view(infos: list[ExampleInfo]):
    for info in infos:
        if info.children:
            td.tag(info.title, variant="outline", size="large", theme="primary").props(
                {"id": info.title_id.replace(" ", "-")}
            ).style("width:fit-content;margin-top:1rem")

            for child in info.children:
                example_view(child)
        else:
            example_view(info)
