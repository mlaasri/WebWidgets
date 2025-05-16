# =======================================================================
#
#  This file is part of WebWidgets, a Python package for designing web
#  UIs.
#
#  You should have received a copy of the MIT License along with
#  WebWidgets. If not, see <https://opensource.org/license/mit>.
#
#  Copyright(C) 2025, mlaasri
#
# =======================================================================

from .render_page import render_page
import webwidgets as ww
from webwidgets.compilation.html import Div


class TestBox:

    # A simple color widget
    class Color(ww.Widget):
        def __init__(self, color: str):
            super().__init__()
            self.color = color

        def build(self):
            return Div(style={"background-color": self.color,
                              "height": "100%",
                              "width": "100%"})

    # A simple Page with one Box containing a variable number of Text widgets
    class SimplePage (ww.Page):
        def __init__(self, n: int = 2):
            box = ww.Box(ww.Direction.HORIZONTAL)
            for _ in range(n):
                box.add(TestBox.Color("red"))
            super().__init__(widgets=[box])

    def test_box(self, web_drivers_info):
        page = TestBox.SimplePage()
        for web_driver_info in web_drivers_info:
            result = render_page(page, web_driver_info, size=(800, 800))
            assert (result.shape[0], result.shape[1]) == (800, 800)
