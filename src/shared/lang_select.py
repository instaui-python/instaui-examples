from pathlib import Path
from instaui import ui
from instaui_tdesign import td
from .i18n import language_dict_sets


class I18nPageState(ui.PageState):
    def __init_subclass__(cls, locale_dir: Path, **kwargs):
        cls.locale_dir = locale_dir
        return super().__init_subclass__(**kwargs)

    def __init__(self) -> None:
        super().__init__()
        language_sets = language_dict_sets(
            ["en_US", "zh_CN"], locale_dir=self.locale_dir
        )
        current_language = ui.use_language()

        language_dict = ui.js_computed(
            inputs=[current_language, language_sets],
            code="(currentLanguage, languageSets) => languageSets[currentLanguage]",
        )

        def gettext(message: str):
            return language_dict[message]

        self._gettext = gettext

    def __call__(self, message: str) -> str:
        return self._gettext(message)


def lang_select():
    data = ui.data(
        [{"label": "english", "value": "en_US"}, {"label": "中文", "value": "zh_CN"}]
    )

    current = ui.use_language()
    options = ui.js_computed(
        inputs=[data, current],
        code=r"""(data,current)=>{
        const list = [...data];
        const idx = list.findIndex(item => item.value === current);
        if (idx > 0) {
            const [item] = list.splice(idx, 1);
            list.unshift(item);
        }
        return list;
}""",
    )

    mounted = ui.js_event(
        outputs=[current],
        code=r"""()=>{
const lang = navigator.language || navigator.userLanguage;
const isZh = lang.toLowerCase().startsWith('zh');
return isZh? 'zh_CN' : 'en_US';
}""",
    )

    return (
        td.select(
            options=options,
            value=current,
            borderless=True,
            auto_width=True,
        )
        .on_mounted(mounted)
        .style("width:unset;")
    )
