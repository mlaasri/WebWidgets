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
        """Tests the even distribution of multiple colored widgets by a Box.

        The test renders a page with a box and checks the color of each box
        item at its center. For example, with 3 colored widgets per box, the
        test will look for the color at the following positions `X` in the
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

        Since the box should span each child evenly, the colors at the marked
        `X` should match a predictable pattern.
        """
        # To locate the box items, the test uses a (x, y) coordinate system
        # with the x-axis in the direction of the box and the y-axis across it.
        # This system is the most intuitive for a horizontal box, with a
        # standard horizontal x-axis and a vertical y-axis. For a vertical box,
        # these axes are swapped in the code. This swap allows to reuse most of
        # the test implementation for horizontal boxes.

        # Swapping the axes if the box is vertical so we can reuse the same
        # code for both directions
        x_axis = 1 if direction == ww.Direction.HORIZONTAL else 0
        y_axis = 1 - x_axis

        # Rendering the page
        page = TestBox.SimplePage(direction, n)
        for web_driver in web_drivers:
            result = render_page(page, web_driver)
            xs = [int(result.shape[x_axis] * (1 / (2.0 * n) + k / n))
                  for k in range(n)]
            half_y = result.shape[y_axis] // 2
            for x, color in zip(xs, TestBox.SimplePage.colors):
                coords = (half_y, x) if direction == ww.Direction.HORIZONTAL \
                    else (x, half_y)  # Swapping the indices for vertical boxes

                assert np.all(
                    result[coords[0], coords[1], :3] == np.array(color))
