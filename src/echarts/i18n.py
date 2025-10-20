# i18n.py
from pathlib import Path
import os
import polib

LOCALE_DIR = Path(__file__).parent / "locale"


def load_language_dict(lang_code: str, *, domain="messages"):
    """
    Load specified language's translation dictionary.

    Args:
        lang_code (str): Language code.
        localedir (str, optional): Locale directory. Defaults to "messages".
        domain (str, optional): Domain name. Defaults to "messages".

    Usage:
        >>> load_language_dict("zh_CN")
        {'Hello world': '你好，世界', 'This is a test': '这是一个测试'}

    """
    po_path = LOCALE_DIR / "messages" / lang_code / "LC_MESSAGES" / f"{domain}.po"
    if not po_path.exists():
        raise FileNotFoundError(f"PO file not found: {po_path}")

    po = polib.pofile(po_path)

    translations = {}
    for entry in po:
        # if entry.msgstr:  # 只收录有翻译的
        translations[entry.msgid] = entry.msgstr or entry.msgid

    return translations


def language_dict_sets(lang_codes: list[str], *, domain="messages"):
    return {
        lang_code: load_language_dict(lang_code, domain=domain)
        for lang_code in lang_codes
    }


"""
# 提取翻译模板
pybabel extract -F ./locale/babel.cfg -o ./locale/messages.pot .

# 更新. 在 locales.pot 文件中添加翻译
pybabel update -i ./locale/messages.pot -d ./locale/messages

# 生成目录
pybabel init -i ./locale/messages.pot -d ./locale/messages -l zh_CN
pybabel init -i ./locale/messages.pot -d ./locale/messages -l en_US


# 更新翻译
pybabel compile -d ./locale/messages
"""
