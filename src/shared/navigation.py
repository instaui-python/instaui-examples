from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from instaui import ui
from instaui_tdesign import td

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

    with ui.box(), td.affix():
        with ui.column(mt="4"):
            td.input(search_input, clearable=True)
        with td.anchor(target_offset=100):
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
