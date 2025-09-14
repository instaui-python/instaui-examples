from instaui import ui, zero
import instaui_tdesign as td

td.use(theme="violet")


@ui.page()
def home():
    todos = ui.state(
        [
            {"id": 1, "name": "Task 1", "done": False},
            {"id": 2, "name": "Task 2", "done": True},
        ]
    )

    current_task = ui.state("")

    can_add_task = ui.js_computed(
        inputs=[current_task], code="(current_task) => Boolean(current_task.trim())"
    )

    active_tasks = ui.js_computed(
        inputs=[todos], code="(todos) => todos.filter(todo => !todo.done)"
    )

    completed_tasks = ui.js_computed(
        inputs=[todos], code="(todos) => todos.filter(todo => todo.done)"
    )

    task_description = ui.js_computed(
        inputs=[todos],
        code="""(todos) => {
            const done = todos.filter(todo => todo.done).length;
            const total = todos.length;
            const remaining = todos.filter(todo => !todo.done).length;
            return {
                done,
                total,
                remaining,
                percent: total > 0 ? (remaining / total * 100) : 0
            };
        }""",
    )

    add_task = ui.js_event(
        inputs=[todos, current_task],
        outputs=[todos, current_task],
        code="""(todos, current_task) => {
            if (current_task) {
                const id = Math.max(...todos.map(todo => todo.id), 0) + 1;
                todos.push({id, name: current_task, done: false});
                current_task = "";
            }
            return [todos, current_task];
        }""",
    )

    delete_task = ui.js_event(
        inputs=[todos],
        outputs=[todos],
        code="(todos, id) => todos.filter(todo => todo.id !== id)",
    )

    # ui

    with ui.container(size="2"), ui.column():
        with ui.row():
            td.input(
                value=current_task, placeholder="输入内容，按回车添加新任务"
            ).on_enter(add_task)
            with (
                td.button(disabled=ui.not_(can_add_task), shape="circle")
                .on_click(add_task)
                .add_slot("icon")
            ):
                ui.icon("td:add").classes("t-icon")

        with td.tabs(default_value="all"):
            with td.tab_panel(label="所有任务", value="all"):
                tasks_list_view(todos, delete_task)

            with td.tab_panel(label="进行中", value="active"):
                tasks_list_view(active_tasks, delete_task)

            with td.tab_panel(label="已完成", value="completed"):
                tasks_list_view(completed_tasks, delete_task)


def tasks_list_view(todos: list, delete_task):
    with ui.grid(columns="1fr auto", align="center", pt="2"):
        with ui.vfor(todos, key="item.id") as todo:
            td.checkbox(todo["done"], label=todo["name"])
            with (
                td.button(disabled=ui.not_(todo["done"]), shape="circle")
                .on_click(delete_task, extends=[todo["id"]])
                .add_slot("icon")
            ):
                ui.icon("td:delete-1-filled").classes("t-icon")


with zero() as z:
    home()
    z.to_html("main.html")


ui.server(debug=True).run()
