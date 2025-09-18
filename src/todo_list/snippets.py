from instaui import ui


def fancy_logo_text(text: str):
    return ui.text(text, size="8", weight="bold").style(r"""
  background-image: linear-gradient(45deg, #d7c0ff 30%, #c700ff);
  background-size: 200% 200%; 
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
""")
