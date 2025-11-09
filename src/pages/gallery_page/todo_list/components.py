from typing import Literal
from instaui import ui
from instaui_tdesign import td
from page_state import I18nState
from .state import State, TTodo
from .snippets import fancy_logo_text


def todo_app():
    N_ = I18nState.get()

    # ui
    heading_view()
    new_task_view()

    # tasks list
    with td.tabs(default_value="all"):
        with td.tab_panel(label=N_("所有任务"), value="all"):
            tasks_list_view("all")

        with td.tab_panel(label=N_("进行中"), value="active"):
            tasks_list_view("active")

        with td.tab_panel(label=N_("已完成"), value="completed"):
            tasks_list_view("completed")

    task_description_view()


def heading_view():
    dark = ui.use_dark()
    with ui.grid(columns="1fr auto", align="center", mt="2"):
        with ui.box(mx="auto", as_child=True):
            fancy_logo_text("TODO List")

        with ui.row(align="center"):
            with td.switch(value=dark, size="large").add_slot("label") as p:
                with ui.match(p.slot_props("value")) as mt:
                    with mt.case(True):
                        ui.icon("todo_list:mode-dark-filled")

                    with mt.case(False):
                        ui.icon("todo_list:mode-light-filled")


def new_task_view():
    state = State.get()
    N_ = I18nState.get()

    with ui.row():
        td.input(
            value=state.current_task,
            placeholder=N_("输入内容，按回车添加新任务"),
            clearable=True,
        ).on_enter(state.add_task)
        td.button(
            icon="todo_list:add", disabled=ui.not_(state.can_add_task), shape="circle"
        ).on_click(state.add_task)


def tasks_list_view(type: Literal["all", "active", "completed"]):
    state = State.get()

    todos = state.todos

    def task_item(todo: TTodo):
        N_ = I18nState.get()
        show = ui.js_computed(
            inputs=[todo["done"], type],
            code="(done,type) => type === 'all' || (type === 'active' && !done) || (type === 'completed' && done)",
        )

        switch_edit = ui.js_event(
            inputs=[todo["edit"]],
            outputs=[todo["edit"]],
            code="e => !e",
        )

        # ui
        with ui.vif(show):
            with ui.box(py="1", px="2"):
                with ui.match(todo["edit"]) as mt:
                    with mt.case(False):
                        with ui.grid(columns="1fr auto auto", align="center", pt="2"):
                            td.checkbox(todo["done"], label=todo["name"])

                            td.button(
                                icon="todo_list:edit",
                                shape="circle",
                                variant="outline",
                                theme="primary",
                            ).on_click(state.show_edit_input, extends=[todo["id"]])

                            td.button(
                                icon="todo_list:delete-1-filled",
                                disabled=ui.not_(todo["done"]),
                                shape="circle",
                                variant="dashed",
                            ).on_click(state.delete_task, extends=[todo["id"]])

                    with mt.case(True):
                        with ui.grid(columns="1fr auto", align="center", pt="2"):
                            td.input(value=todo["name"]).on_enter(switch_edit)
                            td.button(N_("确定")).on_click(switch_edit)

    # ui
    with ui.vfor(todos, key="item.id") as todo:
        task_item(todo)


def task_description_view():
    state = State.get()
    N_ = I18nState.get()

    with ui.row(align="center", mt="2"):
        with ui.row(gap="1"):
            ui.text(N_("有"))
            td.tag(
                state.task_description["remaining"], theme="primary", variant="outline"
            )
            ui.text(N_("个进行中的任务"))

        ui.row(flex_grow="1")
        td.button(
            N_("清空已完成任务"),
            variant="outline",
            disabled=ui.len_(state.completed_tasks) < 1,
        ).on_click(state.clear_completed_tasks)
