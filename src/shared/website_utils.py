from typing import Callable, Optional
from instaui import zero, cdn
from instaui_tdesign import cdn as td_cdn
from pathlib import Path
import xml.etree.ElementTree as ET

from .cmd import parse_offline_flag

SRC_ROOT = Path(__file__).parent.parent
ICONS_DIR = SRC_ROOT / "assets/icons"
SHARED_ICONS_SVG_FILE = ICONS_DIR / "shared.svg"
WEBSITE_DIR = SRC_ROOT.parent / "website"

if not WEBSITE_DIR.exists():
    WEBSITE_DIR.mkdir()


def zero_dist_to_website(
    render_fn: Callable,
    *,
    file: str,
    icons_svg_file: Optional[str] = None,
    output_dir: Optional[Path] = None,
    cdns: Optional[list] = None,
    # base_folder: Optional[Path] = None,
    debug_report: bool = False,
):
    output_dir = output_dir or WEBSITE_DIR

    def icons_svg_path_fn():
        shared_svg = add_td_prefix_to_symbols(SHARED_ICONS_SVG_FILE)
        page_svg = (
            add_td_prefix_to_symbols(ICONS_DIR / icons_svg_file)
            if icons_svg_file
            else None
        )

        if page_svg:
            return merge_svg_symbols(shared_svg, page_svg)

        return shared_svg

    offline = parse_offline_flag()
    cdn_resource_overrides = (
        None if offline else [cdn.override(), td_cdn.override(), *(cdns or [])]
    )

    file_path = output_dir / file
    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True)

    z = zero(
        icons_svg_path=icons_svg_path_fn,
        cdn_resource_overrides=cdn_resource_overrides,
    )

    if debug_report:
        z.to_debug_report(render_fn, file=output_dir / file)
        return

    z.to_html(render_fn, file=output_dir / file)


def add_td_prefix_to_symbols(
    svg_path: Path,
    prefix: Optional[str] = None,
) -> str:
    """
    Reads an SVG file, ensures all <symbol> elements have an ID prefixed with `prefix`.
    If an ID does not start with `prefix`, the prefix is added.
    Returns the modified SVG content as a string.

    This function attempts to handle SVGs with or without explicit namespace declarations.

    :param svg_path: Path to the input SVG file. Defaults to 'icons.svg' in the script's directory.
    :return: The modified SVG content as a string.
    """

    if svg_path.is_dir():
        if svg_path.name != "icons":
            svg_path = svg_path / "assets/icons"

        svg_path = svg_path / "i.svg"

    prefix = prefix or svg_path.stem.strip()
    prefix = f"{prefix}:" if prefix[-1] != ":" else prefix

    # Register the default SVG namespace.
    # This helps if the input SVG uses it, ensuring correct parsing and output formatting.
    # Even if the SVG doesn't use it, registering it is harmless for parsing.
    SVG_NAMESPACE = "http://www.w3.org/2000/svg"
    ET.register_namespace("", SVG_NAMESPACE)  # Register default namespace

    # Parse the SVG file
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # --- Robust Symbol Finding ---
    # Method 1: Try finding with a wildcard namespace. This often works.
    symbols = root.findall(".//symbol")

    # If that didn't work (e.g., if symbols are deeply namespaced in a weird way),
    # try finding with the registered default namespace prefix.
    # We need to build the prefixed tag name that ElementTree uses internally.
    if not symbols:
        # Get the prefix that ElementTree will use for our registered namespace
        # This is a bit of internal knowledge, but generally reliable.
        # Alternatively, we can directly use the full tag name format.
        symbol_tag_with_ns = f"{{{SVG_NAMESPACE}}}symbol"
        symbols = root.findall(f".//{symbol_tag_with_ns}")

    # If still not found, one could iterate recursively, but the above usually suffices.
    # For now, we proceed with 'symbols' found by the first (often sufficient) method.
    # -----------------------------

    # Iterate through each found symbol and check/modify its 'id' attribute
    for symbol in symbols:
        current_id = symbol.get("id")
        if current_id and not current_id.startswith(prefix):
            symbol.set("id", f"{prefix}{current_id}")

    # Convert the modified ElementTree back to a string
    # Using 'unicode' encoding returns a string, xml_declaration=False avoids adding <?xml...?> if not present
    return ET.tostring(root, encoding="unicode", xml_declaration=False)


def merge_svg_symbols(svg1: str, svg2: str) -> str:
    """
    合并两个包含 <symbol> 的 SVG 字符串。
    - 若有重复的 symbol id，会抛出 ValueError。
    - 返回一个新的 SVG 字符串，包含所有 symbol。
    """

    def extract_symbols(svg_str):
        svg_str = svg_str.strip()
        root = ET.fromstring(svg_str)
        symbols = []
        for elem in root.findall(".//{*}symbol") + root.findall(".//symbol"):
            symbols.append(elem)
        return symbols

    symbols1 = extract_symbols(svg1)
    symbols2 = extract_symbols(svg2)

    ids = [s.attrib.get("id") for s in symbols1 + symbols2 if "id" in s.attrib]
    duplicates = {i for i in ids if ids.count(i) > 1}
    if duplicates:
        raise ValueError(f"发现重复的 symbol id: {', '.join(duplicates)}")

    svg_root = ET.Element(
        "svg", attrib={"xmlns": "http://www.w3.org/2000/svg", "style": "display:none;"}
    )

    for s in symbols1 + symbols2:
        svg_root.append(s)

    return ET.tostring(svg_root, encoding="unicode")
