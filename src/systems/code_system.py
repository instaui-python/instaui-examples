import inspect
import textwrap
import re
from typing import Callable, Optional


def get_function_body(func):
    source = inspect.getsource(func)
    if not source.strip():
        return ""

    # Robust regex to match function definition including:
    # - def keyword
    # - function name
    # - parameter list (handling nested parentheses)
    # - ending colon
    pattern = r"^\s*def\s+\w+\s*\([^()]*(?:\([^()]*\)[^()]*)*\)\s*:"
    match = re.search(pattern, source, re.MULTILINE | re.DOTALL)
    if not match:
        return ""

    # Get the position after the function definition
    body_start = match.end()
    body = source[body_start:]

    # Remove leading empty lines
    lines = body.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    body = "\n".join(lines)

    return body


def transform_mark_blocks(code: str) -> str:
    lines = code.splitlines(True)  # keep line endings
    result = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        if re.match(r"^\s*# mark\b", line):
            # Enter mark block
            i += 1
            mark_block = []

            # Collect mark block lines
            while i < n and not re.match(r"^\s*# end-mark\b", lines[i]):
                mark_block.append(lines[i])
                i += 1
            i += 1  # Skip # end-mark

            # Extract and convert "to" block
            inside_to = False
            converted = []
            for ml in mark_block:
                if re.match(r"^\s*# to\b", ml):
                    inside_to = True
                    continue
                if re.match(r"^\s*# end-to\b", ml):
                    inside_to = False
                    continue
                if inside_to:
                    # Only remove a single leading '# ' keeping indentation
                    converted.append(re.sub(r"^(\s*)# ?", r"\1", ml))

            result.extend(converted)

        else:
            result.append(line)
            i += 1

    return "".join(result)


def adjust_indent_excluding_noindent(src: str, indent: str = " " * 4):
    """
    对字符串做缩进，但保留 # <noindent> 块中第二行开始的原始缩进
    """
    marker = "<NOINDENT_BLOCK>"

    # 匹配 noindent 块
    pattern = re.compile(
        r"^[ \t]*# <noindent>[^\n]*\n"  # 开始行
        r"(?P<body>.*?)"  # 内容体
        r"^[ \t]*# </noindent>[^\n]*\n?",  # 结束行
        re.DOTALL | re.MULTILINE,
    )

    saved_blocks = []

    def replacer(m: re.Match):
        body = m.group("body")
        lines = body.splitlines(True)
        if not lines:
            return ""
        first_line = lines[0].rstrip("\n")
        rest = "".join(lines[1:]) if len(lines) > 1 else ""
        saved_blocks.append(rest)
        # 把 marker 放在第一行的同一行，用于后续替换
        return f"{first_line}{marker}"

    # 1️⃣ 替换 noindent 块
    temp_src = pattern.sub(replacer, src)

    # 2️⃣ 执行整体 dedent + indent
    adjusted_src = textwrap.indent(textwrap.dedent(temp_src), indent)

    # 3️⃣ 恢复保存的块（加换行）
    def restore(_):
        return "\n" + saved_blocks.pop(0)

    restored = re.sub(marker, restore, adjusted_src)

    # 4️⃣ 去掉多余空行
    restored = re.sub(r"\n{3,}", "\n\n", restored).rstrip() + "\n"

    return restored
