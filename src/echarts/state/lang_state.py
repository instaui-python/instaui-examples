from instaui import ui
from i18n import language_dict_sets


class I18nPageState(ui.PageState):
    def __init__(self) -> None:
        super().__init__()
        language_sets = language_dict_sets(["en_US", "zh_CN"])
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
