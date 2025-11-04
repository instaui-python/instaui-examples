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
    description: str = ""
    fn: Optional[Callable] = None
    children: list[ExampleInfo] = field(default_factory=list)
    imports: Optional[list[str]] = field(default_factory=list)
    ignore_indent_condition: Optional[Callable[[str], bool]] = None
    translation_mapping: Optional[dict[str, str]] = None
    instaui_module_imports: Optional[list[str]] = None


def get_function_body(
    func, indent=4, ignore_indent_condition: Optional[Callable[[str], bool]] = None
):
    source = inspect.getsource(func)
    if not source.strip():
        return ""

    # Robust regex to match function definition including:
    # - def keyword
    # - function name
    # - parameter list (handling nested parentheses)
    # - ending colon
    pattern = r"^\s*def\s+\w+\s*\([^()]*(?:\([^()]*\)[^()]*)*\)\s*:"
    match = re.search(pattern, source, re.MULTILINE | re.DOTALL)
    if not match:
        return ""

    # Get the position after the function definition
    body_start = match.end()
    body = source[body_start:]

    # Remove leading empty lines
    lines = body.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    body = "\n".join(lines)

    # Remove common leading indentation
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


def use_example_infos(
    require_imports: Optional[list[str]] = None,
):
    infos: list[ExampleInfo] = []
    current_node: Optional[ExampleInfo] = None

    def decorator(
        title: str,
        title_id: str,
        description: str = "",
        imports: Optional[list[str]] = None,
        ignore_indent_condition: Optional[Callable[[str], bool]] = None,
        instaui_module_imports: Optional[list[str]] = None,
        *,
        translation_mapping: Optional[dict[str, str]] = None,
    ):
        def wrapper(fn: Callable):
            info = ExampleInfo(
                title,
                title_id,
                description,
                fn,
                imports=[*(imports or []), *(require_imports or [])],
                ignore_indent_condition=ignore_indent_condition,
                translation_mapping=translation_mapping,
                instaui_module_imports=instaui_module_imports,
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
    instaui_import = (
        f"from instaui import {', '.join(['ui', *(info.instaui_module_imports or [])])}"
    )
    imports = [instaui_import, *imports]
    imports_code = "\n".join(imports)

    prepage_code = _gen_prepage_code(imports)

    fn_code = get_function_body(
        info.fn, ignore_indent_condition=info.ignore_indent_condition
    )

    fn_code = transform_mark_blocks(fn_code)

    code = ui.js_computed(
        inputs=[
            imports_code,
            prepage_code,
            fn_code,
            ui.unwrap_reactive(info.translation_mapping)
            if info.translation_mapping
            else {},
        ],
        code=r"""(imports_code, prepage_code, code, t_data)=>{
    const realCode = code.replace(/N_\((\w+)\)/g, (match, key) => {
        // 如果映射里有对应的 key，就替换，否则保留原文
        return t_data[key] ? `${t_data[key]}` : match;
    });

    return `
${imports_code}
${prepage_code}

@ui.page()
def index():
${realCode}

ui.server(debug=True).run()
`
}""",
    )

    with (
        td.card(
            title=info.title, header_bordered=True, subtitle=info.description
        ).props({"id": f"{info.title_id.lower().replace(' ', '-')}"}),
        ui.grid(columns=2),
    ):
        with td.card(body_style={"height": "400px"}):
            info.fn()
        shiki(code, line_numbers=True, transformers=["notationHighlight"])


def example_list_view(infos: list[ExampleInfo]):
    goto_nav_node = ui.js_event(
        code=r"""()=>{
  const hash = window.location.hash;
  debugger
  if (hash) {
    const el = document.querySelector(hash);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }                                                           
}"""
    )

    with (
        ui.column(gap="4")
        .scoped_style("content-visibility: auto;", selector="> *")
        .scoped_style("contain-intrinsic-size:auto 22px", selector="> *.t-tag")
        .scoped_style("contain-intrinsic-size:auto 400px", selector="> *.t-card")
        .on_mounted(goto_nav_node)
    ):
        for info in infos:
            if info.children:
                td.tag(
                    info.title, variant="outline", size="large", theme="primary"
                ).props({"id": info.title_id.replace(" ", "-")}).style(
                    "width:fit-content;margin-top:1rem"
                )

                for child in info.children:
                    example_view(child)
            else:
                example_view(info)


def _gen_prepage_code(imports: list[str]):
    lang = ui.use_language()
    has_import_td = any(i.startswith("from instaui_tdesign") for i in imports)

    return ui.js_computed(
        inputs=[lang, has_import_td],
        code=r"""(lang, has_import_td)=> lang===`en_US` && has_import_td ? `td.use(locale="en_US")` : `` """,
    )
