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
import webwidgets as ww
from webwidgets.compilation.html.html_node import HTMLNode, RawText


class TestWebsite:
    class Text(ww.Widget):
        def __init__(self, text: str):
            super().__init__()
            self.text = text

        def build(self):
            return HTMLNode(children=[RawText(self.text)])

    @pytest.mark.parametrize("num_pages", [1, 2, 3])
    @pytest.mark.parametrize("num_widgets", [1, 2, 3])
    @pytest.mark.parametrize("text", ["a", "b", "c"])
    def test_compile_website_without_css(self, num_pages, num_widgets, text):
        # Create a new website object
        website = ww.Website()
        for _ in range(num_pages):
            website.add(ww.Page([TestWebsite.Text(text)] * num_widgets))

        # Compile the website to HTML
        compiled = website.compile()

        # Check if the compiled HTML contains the expected code
        expected_html = "\n".join([
            "<!DOCTYPE html>",
            "<html>",
            "    <head></head>",
            "    <body>"
        ]) + "\n" + "\n".join([
            "        <htmlnode>",
            f"            {text}",
            "        </htmlnode>",
        ] * num_widgets) + "\n" + "\n".join([
            "    </body>",
            "</html>"
        ])
        assert len(compiled.html_code) == num_pages
        assert all(c == expected_html for c in compiled.html_code)

        # Check if the compiled CSS contains the expected code
        assert compiled.css_code == ""  # No CSS is generated for this case
