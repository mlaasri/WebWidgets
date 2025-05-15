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
from webwidgets.compilation.html import Div, RawText


class TestBox:

    # A simple text widget
    class Text(ww.Widget):
        def build(self):
            return Div([RawText("Hello, World!")])

    # A simple Page with one Box containing a variable number of Text widgets
    class SimplePage (ww.Page):
        def __init__(self, n: int = 2):
            box = ww.Box(ww.Direction.HORIZONTAL)
            for _ in range(n):
                box.add(TestBox.Text())
            super().__init__(widgets=[box])

    def test_box(self, web_drivers):
        page = TestBox.SimplePage()
        for web_driver in web_drivers:
            result = render_page(page, web_driver)
            assert result.shape
