from pathlib import Path
from shared.lang_select import I18nPageState


class I18nState(I18nPageState, locale_dir=Path(__file__).parent / "locale"):
    pass
