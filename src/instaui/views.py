from utils import I18nState
from instaui import ui
from instaui_tdesign import td
from shared.example_extractor import use_example_infos

m_tdesign_import = "from instaui_tdesign import td"


def index():
    pass

    N_ = I18nState.get()
    example, infos, root_node = use_example_infos()

    with root_node("入门", "introduction"):

        @example(N_("模板"), "template")
        def template():
            ui.text("hello world")

    with root_node("状态管理", "state manager"):

        @example(N_("可读写状态-state"), "read-write-state", imports=[m_tdesign_import])
        def read_write_state():
            s = ui.state("hello world")

            # ui
            td.input(s)
            ui.text(s)

        @example(
            N_("只读状态-computed(服务端)"),
            "only-read-computed-server",
            imports=[m_tdesign_import],
            translation_mapping={"d1": N_("函数在服务端执行")},
        )
        def computed_server():
            s = ui.state("hello world")

            # mark
            new_text = ui.js_computed(inputs=[s], code=r"s=> `new: ${s}`")

            # to
            # @ui.computed(inputs=[s])
            # def new_text(old: str):
            #     # [!code highlight:1]
            #     # N_(d1)
            #     return f"new: {old}"
            # end-to

            # end-mark

            # ui
            td.input(s)
            ui.text(new_text)

        @example(
            N_("只读状态-js_computed(客户端)"),
            "only-read-computed-client",
            imports=[m_tdesign_import],
            translation_mapping={"d1": N_("计算无须经过服务端")},
        )
        def computed_client():
            s = ui.state("hello world")
            # [!code highlight:1]
            # N_(d1)
            new_text = ui.js_computed(inputs=[s], code=r"s=> `new: ${s}`")

            # ui
            td.input(s)
            ui.text(new_text)

    with root_node("状态绑定", "state-binding"):

        @example(N_("绑定样式"), "style-binding", imports=[m_tdesign_import])
        def state_binding():
            color = ui.state("red")

            # ui
            td.select(["red", "blue", "green"], value=color)
            ui.text("text color").style({"color": color})

    return infos
