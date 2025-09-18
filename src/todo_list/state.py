from typing import TypedDict
from instaui import ui


class TTodo(TypedDict):
    id: int
    name: str
    done: bool
    edit: bool


class State(ui.PageState):
    def __init__(self):
        self.todos: list[TTodo] = ui.local_storage(
            "todos",
            [
                {"id": 1, "name": "Task 1", "done": False, "edit": False},
                {"id": 2, "name": "Task 2", "done": True, "edit": False},
            ],
        )

        self.current_task = ui.state("")

        self.can_add_task = ui.js_computed(
            inputs=[self.current_task],
            code="(current_task) => Boolean(current_task.trim())",
        )

        self.active_tasks = ui.js_computed(
            inputs=[self.todos], code="(todos) => todos.filter(todo => !todo.done)"
        )

        self.completed_tasks = ui.js_computed(
            inputs=[self.todos], code="(todos) => todos.filter(todo => todo.done)"
        )

        self.task_description = ui.js_computed(
            inputs=[self.todos],
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

        self.add_task = ui.js_event(
            inputs=[self.todos, self.current_task],
            outputs=[self.todos, self.current_task],
            code="""(todos, current_task) => {
                if (current_task) {
                    const id = Math.max(...todos.map(todo => todo.id), 0) + 1;
                    todos.push({id, name: current_task, done: false, edit:false});
                    current_task = "";
                }
                return [todos, current_task];
            }""",
        )

        self.delete_task = ui.js_event(
            inputs=[self.todos],
            outputs=[self.todos],
            code="(todos, id) => todos.filter(todo => todo.id !== id)",
        )

        self.clear_completed_tasks = ui.js_event(
            inputs=[self.todos],
            outputs=[self.todos],
            code="(todos) => todos.filter(todo => !todo.done)",
        )

        self.show_edit_input = ui.js_event(
            inputs=[self.todos],
            outputs=[self.todos],
            code=r"""(todos, id) => {
            const todo = todos.find(todo => todo.id === id);
            todo.edit = !todo.edit;
            return todos;
    }""",
        )
