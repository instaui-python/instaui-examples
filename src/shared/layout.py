from instaui import html, ui


def container():

    with ui.column().classes("items-center p-4"):
        box = (
            html.div()
            .classes("max-w-[1136px] w-full")
            .style(
                'font-family: -apple-system, BlinkMacSystemFont, "Segoe UI (Custom)", Roboto, "Helvetica Neue", "Open Sans (Custom)", system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";'
            )
        )

    return box
