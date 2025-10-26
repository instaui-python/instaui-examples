from instaui import ui
from instaui_tdesign import td
from instaui_shiki import shiki
from shared.example_extractor import use_example_infos
from utils import I18nState


m_tdesign_import = "from instaui_tdesign import td"
m_shiki_import = "from instaui_shiki import shiki"

_t = I18nState.get()
example, infos, _ = use_example_infos(require_imports=[m_shiki_import])


@example(_t("基础使用"), "basic usage")
def base():
    code = 'print("Hello, world!")'
    shiki(code)


@example(_t("code 参数联动"), "code parameter linkage", imports=[m_tdesign_import])
def code_parameter_linkage():
    code = ui.state('print("Hello, world!")')

    td.textarea(code)
    shiki(code)


@example(_t("diff 标记"), "diff marker")
def diff_marker():
    code = r"""
a = 1
b = 2  # [!code --]
c = 3
d = 4  # [!code ++]
    """

    shiki(code, transformers=["notationDiff"])


@example(_t("行高亮标记"), "line highlight marker")
def line_highlight_marker():
    ui.add_style(r"""
.line.highlighted{
    background-color: rgba(142, 150, 170, .14);
    transition: background-color .5s;
    margin: 0 -24px;
    padding: 0 24px;
    width: calc(100% + 48px);
    display: inline-block;
}
""")

    code = r"""

a = 1
b = 2 # [!code highlight]
c = 3

# [!code highlight:2]
a = 1
b = 2
c = 3
    """

    shiki(code, transformers=["notationHighlight"])


@example(_t("单词高亮标记"), "word highlight marker")
def word_highlight_marker():
    ui.add_style(r"""
.highlighted-word {
    border: 1px solid red;
    padding: 1px 3px;
    border-radius: 4px;
}
""")

    code = r"""
#  [!code word:Hello]
message = "Hello, world!"
print(message) # prints "Hello, world!"
    """

    shiki(code, transformers=["notationWordHighlight"])


@example(_t("聚焦行"), "focus line")
def focus_line():
    ui.add_style(r"""
pre.has-focused .line:not(.focused) {
    filter: blur(.095rem);
    opacity: .4;
    transition: filter .35s,opacity .35s;
}
                 
.shiki-code:hover pre.has-focused .line:not(.focused) {
    filter: blur(0);
    opacity: 1;                 
}
""")

    code = r"""

a = 1
b = 2 # [!code focus]
c = 3

# [!code focus:2]
a = 1
b = 2
c = 3
    """

    shiki(code, transformers=["notationFocus"])
