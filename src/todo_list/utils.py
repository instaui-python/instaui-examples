from typing import Callable
from instaui import zero
from pathlib import Path
import xml.etree.ElementTree as ET


def zero_dist(render_fn: Callable):
    zero(icons_svg_path=add_td_prefix_to_symbols).to_html(
        render_fn, file=r"instaui-todo-app\index.html"
    )


def add_td_prefix_to_symbols(
    svg_path: Path = Path(__file__).parent / "assets/icons/td.svg",
) -> str:
    """
    Reads an SVG file, ensures all <symbol> elements have an ID prefixed with 'td-'.
    If an ID does not start with 'td-', the prefix is added.
    Returns the modified SVG content as a string.

    This function attempts to handle SVGs with or without explicit namespace declarations.

    :param svg_path: Path to the input SVG file. Defaults to 'icons.svg' in the script's directory.
    :return: The modified SVG content as a string.
    """
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
        if current_id and not current_id.startswith("td-"):
            symbol.set("id", f"td-{current_id}")

    # Convert the modified ElementTree back to a string
    # Using 'unicode' encoding returns a string, xml_declaration=False avoids adding <?xml...?> if not present
    return ET.tostring(root, encoding="unicode", xml_declaration=False)
