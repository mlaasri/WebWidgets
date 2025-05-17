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

import numpy as np
import pytest
from .render_page import render_page
import webwidgets as ww
from webwidgets.compilation.html import Div


class TestBox:

    # A simple color widget
    class Color(ww.Widget):
        def __init__(self, color: str, expand: ww.Direction):
            super().__init__()
            self.color = color
            self.expand = expand

        def build(self):
            h_unit = "vh" if self.expand == ww.Direction.HORIZONTAL else "%"
            v_unit = "vw" if self.expand == ww.Direction.VERTICAL else "%"
            return Div(style={"background-color": self.color,
                              "height": "100" + h_unit,
                              "width": "100" + v_unit})

    # A simple Page with one Box containing a variable number of Text widgets
    class SimplePage(ww.Page):

        # Red, green, blue
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

        def __init__(self, box_direction: ww.Direction, n: int = 2):
            box = ww.Box(box_direction)
            css_colors = [f"rgb{c}" for c in TestBox.SimplePage.colors]
            for i in range(n):
                color = css_colors[i % len(css_colors)]
                box.add(TestBox.Color(color, box_direction))
            super().__init__(widgets=[box])

    @pytest.mark.parametrize("n", [1, 2, 3])
    def test_even_horizontal_box(self, n, web_drivers):
        """Tests the even distribution of multiple colors by a Box
        """
        page = TestBox.SimplePage(ww.Direction.HORIZONTAL, n)
        for web_driver in web_drivers:
            result = render_page(page, web_driver)
            xs = [int(result.shape[1] * (1 / (2.0 * n) + k / n))
                  for k in range(n)]
            xs_colors = zip(xs, TestBox.SimplePage.colors)
            assert all(np.all(result[result.shape[0] // 2, x, :3] ==
                              np.array(color)) for x, color in xs_colors)
