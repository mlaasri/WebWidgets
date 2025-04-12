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

import webwidgets as ww
from webwidgets.widgets.widget import Widget


class TestPage:
    def test_page_is_widget(self):
        page = ww.Page()
        assert isinstance(page, Widget)

    def test_rendering_empty_page(self):
        page = ww.Page()
        expected_html = "\n".join([
            "<!DOCTYPE html>",
            "<html>",
            "    <head></head>",
            "    <body></body>",
            "</html>"
        ])
        page.build().to_html() == expected_html
