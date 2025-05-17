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
            return Div(style={"background-color": self.color,
                              "height": "100%",
                              "width": "100%"})

    # A Box that fills the entire viewport
    class FullSizedBox(ww.Box):
        def build(self, *args, **kwargs):
            node = super().build(*args, **kwargs)
            node.style["width"] = "100vw"
            node.style["height"] = "100vh"
            return node

    # A simple Page with one Box containing a variable number of Text widgets
    class SimplePage(ww.Page):

        # Red, green, blue
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

        def __init__(self, box_direction: ww.Direction, n: int = 2):
            box = TestBox.FullSizedBox(box_direction)
            css_colors = [f"rgb{c}" for c in TestBox.SimplePage.colors]
            for i in range(n):
                color = css_colors[i % len(css_colors)]
                box.add(TestBox.Color(color, box_direction))
            super().__init__(widgets=[box])

    @pytest.mark.parametrize("direction", [ww.Direction.HORIZONTAL,
                                           ww.Direction.VERTICAL])
    @pytest.mark.parametrize("n", [1, 2, 3])
    def test_even_box(self, direction, n, web_drivers):
        """Tests the even distribution of multiple colors by a Box.

        The test renders a page with a box and checks the color of each box
        item at its center. For example, with 3 colored widgets per box, the
        test will look for the color at the following positions (X) in the
        rendered image, depending on the direction:

        ```

                +-------+-------+-------+           +-------+
                |       |       |       |           |   X   |
                |   X   |   X   |   X   |           +-------+
                |       |       |       |           |   X   |
                +-------+-------+-------+           +-------+
                                                    |   X   |
                                                    +-------+

                        HORIZONTAL                  VERTICAL
        ```
        """
        page = TestBox.SimplePage(direction, n)
        x_axis = 1 if direction == ww.Direction.HORIZONTAL else 0
        y_axis = 1 - x_axis
        for web_driver in web_drivers:
            result = render_page(page, web_driver)
            xs = [int(result.shape[x_axis] * (1 / (2.0 * n) + k / n))
                  for k in range(n)]
            half_y = result.shape[y_axis] // 2
            for x, color in zip(xs, TestBox.SimplePage.colors):
                coords = (half_y, x) if direction == ww.Direction.HORIZONTAL \
                    else (x, half_y)
                assert np.all(result[*coords, :3] == np.array(color))
