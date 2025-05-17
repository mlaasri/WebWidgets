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

    def test_return_type(self, web_drivers):
        for web_driver in web_drivers:
            array = render_page(ww.Page(), web_driver)
            assert isinstance(array, np.ndarray)
