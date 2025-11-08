from page_state import I18nState
from instaui import ui
from instaui_tdesign import td
from shared.example_extractor import use_example_infos

m_tdesign_import = "from instaui_tdesign import td"
m_pathlib_import = "from pathlib import Path"
m_shutil_import = "import shutil"


def index():
    N_ = I18nState.get()
    example, infos, root_node = use_example_infos()

    with root_node(N_("入门"), "introduction"):

        @example(N_("模板"), "template")
        def template():
            ui.text("hello world")

    with root_node(N_("状态管理"), "state manager"):

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

        @example(N_("通过索引访问状态"), "state-index", imports=[m_tdesign_import])
        def bind_nested_state_index():
            data: dict = ui.state(
                {"names": ["bar", "foo"], "other": {"name": "baz", "age": 30}}
            )

            with ui.column():
                ui.text(data, as_="pre")

                td.input(data["names"][0])
                td.input(data["names"][1])
                td.input(data["other"]["name"])
                td.input_number(data["other"]["age"])

        @example(
            N_("动态索引访问状态"),
            "dynamic-state-index",
            description=N_("你可以通过动态索引访问状态，同时保持其响应性。"),
            imports=[m_tdesign_import],
        )
        def bind_nested_state_dynamic_index():
            data = ui.state(["bar", "foo"])
            index = ui.state(0)

            with ui.column():
                ui.text(data, as_="pre")

                td.input_number(index, min=0, max=1, label="idx:")
                td.input(data[index], label="data[index]:")

        @example(
            N_("state 保存数据到本地存储"),
            "state-local-storage",
            description=N_(
                "你可以将状态保存到本地存储(local storage)，下次打开页面时可以恢复状态。"
            ),
            imports=[m_tdesign_import],
        )
        def state_local_storage():
            data = ui.local_storage(key="local_storage-my-data", value="")
            td.input(data)

        @example(
            N_("state 保存数据到会话存储"),
            "state-session-storage",
            description=N_(
                "你可以将状态保存到会话存储(session storage)，刷新页面时可以恢复状态，关闭标签页或窗口后数据清除。"
            ),
            imports=[m_tdesign_import],
        )
        def state_session_storage():
            data = ui.session_storage(key="session_storage-my-data", value="")
            td.input(data)

    with root_node(N_("状态绑定"), "state-binding"):

        @example(N_("绑定样式"), "style-binding", imports=[m_tdesign_import])
        def state_binding():
            color = ui.state("red")

            # ui
            td.select(["red", "blue", "green"], value=color)
            ui.text("text color").style({"color": color})

    with root_node(N_("文件下载和上传"), "file-download-upload"):

        @example(
            N_("文件下载"),
            "file-download",
            instaui_module_imports=["file_io"],
            imports=[m_tdesign_import, m_pathlib_import],
        )
        def file_download(
            content=N_(
                "此为静态文档，无法演示下载功能，请复制代码到本地运行查看效果。"
            ),
        ):
            # mark
            td.button("download").on_click(
                td.message_plugin.warning(
                    content=content,
                    placement="bottom",
                    duration=3000,
                )
            )

            # to
            # @ui.event(outputs=[file_io.download_file.output()])
            # def download():
            #     return file_io.download_file.prepare_download(Path("/path/to/file.txt"))

            # td.button("download").on_click(download)
            # end-to

            # end-mark

        @example(
            N_("文件下载-客户端(js)事件"),
            "file-download-client(js)-event",
            instaui_module_imports=["file_io"],
            imports=[m_tdesign_import, m_pathlib_import],
        )
        def file_download_client_event(
            content=N_(
                "此为静态文档，无法演示下载功能，请复制代码到本地运行查看效果。"
            ),
        ):
            # mark

            td.button("download").on_click(
                td.message_plugin.warning(
                    content=content,
                    placement="center",
                    duration=3000,
                )
            )

            # to
            # download = ui.js_event(
            #     inputs=[file_io.download_file.js_fn_input(Path("/path/to/file.txt"))],
            #     outputs=[file_io.download_file.output()],
            #     code="""fn=> fn()""",
            # )

            # td.button("download").on_click(download)
            # end-to

            # end-mark

        @example(
            N_("文件上传-小文件"),
            "file-upload-small-file",
            instaui_module_imports=["file_io"],
            imports=[m_tdesign_import, m_pathlib_import],
        )
        def file_upload_small_file(
            content=N_(
                "此为静态文档，无法演示上传功能，请复制代码到本地运行查看效果。"
            ),
        ):
            # mark

            on_click = ui.js_event(
                inputs=[ui.event_context.e(), content],
                code=r"""(e,msg)=> {$tdesign.MessagePlugin.warning({content:msg,placement:'center',duration:3000});e.preventDefault()}""",
            )

            td.upload().on("click", on_click)

            # to
            # @file_io.upload_file()
            # async def upload_file(file: file_io.TUploadFile) -> file_io.TUploadFileResult:
            #     save_path = Path(__file__).parent / file.filename
            #     content = await file.read()
            #     save_path.write_bytes(content)
            #     return {"status": 200}

            # td.upload(action=upload_file.url)
            # end-to

            # end-mark

        @example(
            N_("文件上传-大文件"),
            "file-upload-big-file",
            instaui_module_imports=["file_io"],
            imports=[m_tdesign_import, m_pathlib_import, m_shutil_import],
        )
        def file_upload_big_file(
            content=N_(
                "此为静态文档，无法演示上传功能，请复制代码到本地运行查看效果。"
            ),
        ):
            # mark

            on_click = ui.js_event(
                inputs=[ui.event_context.e(), content],
                code=r"""(e,msg)=> {$tdesign.MessagePlugin.warning({content:msg,placement:'center',duration:3000});e.preventDefault()}""",
            )

            td.upload().on("click", on_click)

            # to
            # @file_io.upload_file()
            # async def upload_file(file: file_io.TUploadFile) -> file_io.TUploadFileResult:
            #     save_path = Path(__file__).parent / file.filename
            #     with save_path.open("wb") as f:
            #         shutil.copyfileobj(file.file, f)
            #     return {"status": 200}

            # td.upload(action=upload_file.url)
            # end-to

            # end-mark

        @example(
            N_("文件上传-多文件"),
            "file-upload-multi-file",
            instaui_module_imports=["file_io"],
            imports=[m_tdesign_import, m_pathlib_import],
            translation_mapping={
                "d1": N_("每个文件单独上传，file 总是 list，list 长度为 1")
            },
        )
        def file_upload_multi_file(
            content=N_(
                "此为静态文档，无法演示上传功能，请复制代码到本地运行查看效果。"
            ),
        ):
            # mark

            on_click = ui.js_event(
                inputs=[ui.event_context.e(), content],
                code=r"""(e,msg)=> {$tdesign.MessagePlugin.warning({content:msg,placement:'center',duration:3000});e.preventDefault()}""",
            )

            td.upload().on("click", on_click)

            # to
            # @file_io.upload_file()
            # async def upload_file(file: list[file_io.TUploadFile]) -> file_io.TUploadFileResult:
            #     # N_(d1)
            #     assert isinstance(file, list)
            #     assert len(file) == 1
            #     for f in file:
            #         print(f)

            # td.upload(action=upload_file.url, multiple=True)
            # end-to

            # end-mark

        @example(
            N_("文件上传-多文件(合并上传)"),
            "file-upload-multi-file-merge",
            instaui_module_imports=["file_io"],
            imports=[m_tdesign_import, m_pathlib_import],
            translation_mapping={"d1": N_("所有文件合并到一个请求中")},
        )
        def file_upload_multi_file_merge(
            content=N_(
                "此为静态文档，无法演示上传功能，请复制代码到本地运行查看效果。"
            ),
        ):
            # mark

            on_click = ui.js_event(
                inputs=[ui.event_context.e(), content],
                code=r"""(e,msg)=> {$tdesign.MessagePlugin.warning({content:msg,placement:'center',duration:3000});e.preventDefault()}""",
            )

            td.upload().on("click", on_click)

            # to
            # @file_io.upload_file()
            # async def upload_file(file: list[file_io.TUploadFile]) -> file_io.TUploadFileResult:
            #     # N_(d1)
            #     assert isinstance(file, list)
            #     for f in file:
            #         print(f)

            # td.upload(
            #     action=upload_file.url,
            #     multiple=True,
            #     upload_all_files_in_one_request=True,
            # )
            # end-to

            # end-mark

    return infos
