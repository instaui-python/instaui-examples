from dataclasses import dataclass
from instaui import ui
from instaui_tdesign import td


@dataclass
class NavItem:
    title: str
    id: str


def navigation_tree(infos: list[NavItem]):
    ids = [info.id.lower().replace(" ", "-") for info in infos]
    titles = [info.title for info in infos]

    search_input = ui.state("")
    items = ui.js_computed(
        inputs=[ids, search_input, *titles],
        code=r"""(ids, input,...titles)=>{
const items = [];
for (let i = 0; i < ids.length; i++) {
    items.push({
        title: titles[i],
        id: ids[i],
        href: `#${ids[i]}`,
    });
}
if(input.trim() === '') return items;

const search_text = input.trim().toLowerCase();
return items.filter(item => item.title.toLowerCase().includes(search_text)  || item.id.includes(search_text));

}""",
    )

    with ui.box(), td.affix():
        with ui.column(mt="4"):
            td.input(search_input, clearable=True)
        with td.anchor():
            with ui.vfor(items) as info:
                td.anchor_item(
                    title=info["title"],
                    href=info["href"],
                )
