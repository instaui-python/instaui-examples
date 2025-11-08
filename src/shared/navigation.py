from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from instaui import ui
from instaui_tdesign import td
from page_state import I18nState

if TYPE_CHECKING:
    from .example_extractor import ExampleInfo


@dataclass
class NavItem:
    title: str
    id: str
    children: list[NavItem] = field(default_factory=list)

    def to_py_dict(self):
        return {
            "title": self.title,
            "id": self.id,
            "href": f"#{self.id.lower().replace(' ', '-')}",
            "children": [item.to_py_dict() for item in self.children]
            if self.children
            else None,
        }


def nav_items_from_infos(infos: list[ExampleInfo]):
    return [
        NavItem(
            title=info.title,
            id=info.title_id,
            children=nav_items_from_infos(info.children),
        )
        for info in infos
    ]


def navigation_tree(infos: list[NavItem]):
    N_ = I18nState.get()
    infos_list = [info.to_py_dict() for info in infos]
    data = ui.unwrap_reactive(infos_list)

    search_input = ui.state("")
    items = ui.js_computed(
        inputs=[data, search_input],
        code=r"""(items, input)=>{
if(input.trim() === '') return items;

const inputText = input.trim();
let searchTerms;
let matchFn;

if (inputText.includes('+')) {
    // AND search with + separator
    searchTerms = inputText.split('+').map(t => t.trim().toLowerCase()).filter(t => t);
    matchFn = (text, terms) => terms.every(term => text.includes(term));
} else {
    // OR search with space separator
    searchTerms = inputText.split(' ').map(t => t.trim().toLowerCase()).filter(t => t);
    matchFn = (text, terms) => terms.some(term => text.includes(term));
}

return items
    .map(item => {
        const isRoot = item.children && item.children.length > 0
        const isMatch = matchFn(item.title.toLowerCase(), searchTerms) || 
                       matchFn(item.id.toLowerCase(), searchTerms);

        if (isRoot) {
            const filteredChildren = item.children.filter(
                child => matchFn(child.title.toLowerCase(), searchTerms) ||
                         matchFn(child.id.toLowerCase(), searchTerms)
            );

            // 本身命中，下层没有结果。也需要所有展示
            if (isMatch) {
                return {
                    ...item,
                    children: filteredChildren.length > 0 ? filteredChildren : item.children
                };
            }

            // 本身没有命中，下层有命中。
            if (!isMatch && filteredChildren.length > 0) {
                return {
                    ...item,
                    children: filteredChildren
                };
            }

            return null
        }

        return isMatch ? item : null;
    })
    .filter(Boolean); 
}""",
    )

    # ui

    with ui.column():
        with td.input(
            search_input, clearable=True, placeholder=N_("搜索")
        ).prefix_icon_slot():
            ui.icon(
                size="1rem",
                raw_svg=r'<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 24 24"><!-- Icon from Material Symbols by Google - https://github.com/google/material-design-icons/blob/master/LICENSE --><path fill="currentColor" d="m19.6 21l-6.3-6.3q-.75.6-1.725.95T9.5 16q-2.725 0-4.612-1.888T3 9.5t1.888-4.612T9.5 3t4.613 1.888T16 9.5q0 1.1-.35 2.075T14.7 13.3l6.3 6.3zM9.5 14q1.875 0 3.188-1.312T14 9.5t-1.312-3.187T9.5 5T6.313 6.313T5 9.5t1.313 3.188T9.5 14"/></svg>',
            )

        with td.anchor(target_offset=100, container=".example-list"):
            with ui.vfor(items) as info:
                with ui.match(info["children"]) as match:
                    with match.case(None):
                        td.anchor_item(
                            title=info["title"],
                            href=info["href"],
                        )

                    with match.default():
                        with td.anchor_item(
                            title=info["title"],
                            href=info["href"],
                        ):
                            with ui.vfor(info["children"]) as info:
                                td.anchor_item(
                                    title=info["title"],
                                    href=info["href"],
                                )
