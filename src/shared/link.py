from typing import Optional
from shared.cmd import parse_offline_flag


def with_resolve_link_path(offline: Optional[bool] = None):
    if offline is None:
        offline = parse_offline_flag()

    def resolve_link_path(link_path: str) -> str:
        return f"{link_path}.html" if offline else link_path

    return resolve_link_path
