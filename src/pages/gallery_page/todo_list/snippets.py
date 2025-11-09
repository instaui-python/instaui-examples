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


def page_background():
    style = r"""
    body {
      /* 底层渐变 */
      background: linear-gradient(135deg, #74ebd5 0%, #9face6 100%);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
      /* color: #222;
      position: relative; */
      /* 包含绝对定位的 SVG */
      /* overflow: hidden; */
    }

    /* SVG 作为背景覆盖（不阻挡鼠标） */
    .bg-svg {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 0;
      display: block;
    }
"""
    ui.add_style(style)

    """
  <svg class="bg-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" preserveAspectRatio="none"
    aria-hidden="true">
    <defs>
      <!-- 轻微模糊让线条更柔和 -->
      <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="6" result="blur" />
        <feBlend in="SourceGraphic" in2="blur" />
      </filter>
    </defs>

    <!-- 稀疏的几条曲线，透明度都很低，不会抢眼 -->
    <path d="M -80 240 C 120 160, 360 360, 620 290 C 820 240, 1020 380, 1280 300" fill="none" stroke="white"
      stroke-width="2.5" stroke-opacity="0.12" filter="url(#soft)" />
    <path d="M -80 420 C 220 480, 440 320, 700 380 C 940 440, 1100 300, 1280 340" fill="none" stroke="white"
      stroke-width="2" stroke-opacity="0.10" />
    <path d="M -80 120 C 180 60, 380 180, 640 140 C 880 110, 1080 200, 1280 160" fill="none" stroke="white"
      stroke-width="1.6" stroke-opacity="0.09" />
    <path d="M -80 560 C 260 520, 480 640, 720 600 C 960 560, 1120 680, 1280 640" fill="none" stroke="white"
      stroke-width="2" stroke-opacity="0.08" />
  </svg>
    
    """

    with (
        ui.element("svg")
        .classes("bg-svg")
        .props(
            r'xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" preserveAspectRatio="none" aria-hidden="true"'
        )
    ):
        with ui.element("defs"):
            with ui.element("filter").props(
                r'id="soft" x="-20%" y="-20%" width="140%" height="140%"'
            ):
                ui.element("feGaussianBlur").props(r'stdDeviation="6" result="blur"')
                ui.element("feBlend").props(r'in="SourceGraphic" in2="blur"')

        ui.element("path").props(
            r'd="M -80 240 C 120 160, 360 360, 620 290 C 820 240, 1020 380, 1280 300" fill="none" stroke="white" stroke-width="2.5" stroke-opacity="0.12" filter="url(#soft)"'
        )
        ui.element("path").props(
            r'd="M -80 420 C 220 480, 440 320, 700 380 C 940 440, 1100 300, 1280 340" fill="none" stroke="white" stroke-width="2" stroke-opacity="0.10"'
        )
        ui.element("path").props(
            r'd="M -80 120 C 180 60, 380 180, 640 140 C 880 110, 1080 200, 1280 160" fill="none" stroke="white" stroke-width="1.6" stroke-opacity="0.09"'
        )
        ui.element("path").props(
            r'd="M -80 560 C 260 520, 480 640, 720 600 C 960 560, 1120 680, 1280 640" fill="none" stroke="white" stroke-width="2" stroke-opacity="0.08"'
        )
