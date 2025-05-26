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
from .render_page import render_page
import webwidgets as ww


class TestRenderPage:
    """Test cases for the test utility function `render_page`.
    """

    class Red(ww.Widget):
        def build(self):
            return ww.compilation.html.Div(
                style={"background-color": "red",
                       "height": "100vh",
                       "width": "100vw"}
            )

    def test_return_type_and_shape(self, web_drivers):
        for web_driver in web_drivers:
            array = render_page(ww.Page(), web_driver)
            assert isinstance(array, np.ndarray)
            assert array.ndim == 3
            assert array.shape[0] >= 10
            assert array.shape[1] >= 10
            assert array.shape[2] in (3, 4)  # Some drivers add alpha channel

    def test_red_page(self, web_drivers):
        page = ww.Page([TestRenderPage.Red()])
        for web_driver in web_drivers:
            array = render_page(page, web_driver)
            assert isinstance(array, np.ndarray)
            assert np.all(array[..., 0] == 255)
            assert np.all(array[..., 1] == 0)
            assert np.all(array[..., 2] == 0)
