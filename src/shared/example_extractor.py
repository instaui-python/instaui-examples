from __future__ import annotations
from typing import Callable, Optional
from dataclasses import dataclass, field
from contextlib import contextmanager
import textwrap
from instaui import ui
from instaui_shiki import shiki
from instaui_tdesign import td
from systems import code_system


@dataclass
class ExampleInfo:
    title: str
    title_id: str
    description: str = ""
    fn: Optional[Callable] = None
    children: list[ExampleInfo] = field(default_factory=list)
    imports: Optional[list[str]] = field(default_factory=list)
    translation_mapping: Optional[dict[str, str]] = None
    instaui_module_imports: Optional[list[str]] = None


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

    fn_code = code_system.get_function_body(info.fn)
    fn_code = code_system.transform_mark_blocks(fn_code)
    fn_code = code_system.adjust_indent_excluding_noindent(fn_code, " " * 4)

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
        ui.box(as_child=True, height={"xs": "80dvh", "md": "500px"}),
        ui.lazy_render(height="500px").props(
            {"id": f"{info.title_id.lower().replace(' ', '-')}"}
        ),
        ui.column(height="100%", gap="0", as_child=True),
        td.card(
            title=info.title,
            header_bordered=True,
            subtitle=info.description,
            body_style={"flex": "1", "overflow-y": "hidden"},
        ),
        ui.grid(
            columns={"xs": 1, "md": 2},
            rows={"xs": "2fr 1fr", "md": 1},
            height="100%",
            overflow_y="hidden",
        ),
    ):
        with (
            ui.box(overflow_y="auto", as_child=True),
            td.card(body_style={"height": "100%"}),
        ):
            info.fn()
        shiki(code, line_numbers=True)


def example_list_view(infos: list[ExampleInfo]):
    with ui.column(gap="4"):
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
