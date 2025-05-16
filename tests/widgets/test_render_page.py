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

import pytest
from .render_page import render_page
import webwidgets as ww


class TestRenderPage:
    """Test cases for the test utility function `render_page`.
    """

    class Red(ww.Widget):
        def build(self):
            return ww.compilation.html.Div(
                style={"background-color": "red",
                       "height": "3000px",
                       "width": "3000px"}
            )

    @pytest.mark.parametrize("size", [
        (800, 800), (1234, 800), (800, 1234), (1280, 720)
    ])
    def test_render_empty_page_size(self, size, web_drivers_info):
        for web_driver_info in web_drivers_info:
            array = render_page(ww.Page(), web_driver_info, size)
            assert (array.shape[0], array.shape[1]) == (size[1], size[0])

    @pytest.mark.parametrize("size", [
        (800, 800), (1000, 800), (800, 1000)
    ])
    def test_render_full_page_size(self, size, web_drivers_info):
        for web_driver_info in web_drivers_info:
            array = render_page(
                ww.Page([TestRenderPage.Red()]), web_driver_info, size)
            assert (array.shape[0], array.shape[1]) == (size[1], size[0])
