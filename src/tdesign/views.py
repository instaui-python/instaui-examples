from utils import I18nState
from instaui import ui
from instaui_tdesign import td
from shared.example_extractor import use_example_infos

m_tdesign_import = "from instaui_tdesign import td"


def index():
    pass

    N_ = I18nState.get()
    example, infos, root_node = use_example_infos(require_imports=[m_tdesign_import])

    with root_node(title=N_("表格"), title_id="table"):

        @example(N_("普通使用"), "table-base")
        def table_base():
            data = [
                {"name": "foo", "age": 10},
                {"name": "bar", "age": 20},
            ]

            td.table(data)

        @example(N_("列插槽"), "table-column-slot")
        def table_column_slot():
            data = ui.state(
                [
                    {"name": "foo", "age": 10, "btn": "", "input-name": ""},
                    {"name": "bar", "age": 20, "btn": "", "input-name": ""},
                ]
            )

            table = td.table(data)

            with table.add_cell_slot("btn") as cell:
                td.button(cell.param("row")["name"])

            with table.add_cell_slot("input-name") as cell:
                td.input(cell.param("row")["name"])

    with root_node(title=N_("其他"), title_id="others"):

        @example(N_("按钮"), "button")
        def button():
            td.button("test")

    return infos
