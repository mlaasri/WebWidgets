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
from typing import Dict
import webwidgets as ww
from webwidgets.compilation.html.html_node import HTMLNode, RawText


class TestWebsite:
    class Text(ww.Widget):
        def __init__(self, text: str, style: Dict[str, str] = None):
            super().__init__()
            self.text = text
            self.style = style

        def build(self):
            return HTMLNode(children=[RawText(self.text)], style=self.style)

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
        assert compiled.css_code == ""  # No CSS in this case

    @pytest.mark.parametrize("num_pages", [1, 2, 3, 4, 5, 6])
    @pytest.mark.parametrize("num_widgets", [1, 2, 3])
    @pytest.mark.parametrize("text", ["a", "b", "c"])
    def test_compile_website_with_css(self, num_pages, num_widgets, text):
        # Defining a set of styles to pick from
        styles = [{"margin": "0"}, {"color": "blue"}, {"font-size": "16px"}]

        # Compile expected rule names based on number of pages involved
        rule_names = {
            1: ["r0"],
            2: ["r1", "r0"],
            3: ["r2", "r0", "r1"]
        }
        for k in range(4, num_pages + 1):
            rule_names[k] = [rule_names[3][i % len(styles)] for i in range(k)]

        # Create a new website object
        website = ww.Website()
        for i in range(num_pages):
            website.add(
                ww.Page([
                    TestWebsite.Text(text, styles[i % len(styles)])
                ] * num_widgets))

        # Compile the website to HTML
        compiled = website.compile()

        # Check if the compiled HTML contains the expected code
        expected_html = [(
            "\n".join([
                "<!DOCTYPE html>",
                "<html>",
                "    <head>",
                '        <link href="styles.css" rel="stylesheet">',
                "    </head>",
                "    <body>"
            ]) + "\n" + "\n".join([
                f'        <htmlnode class="{rule_names[num_pages][i % len(rule_names)]}">',
                f"            {text}",
                "        </htmlnode>",
            ] * num_widgets) + "\n" + "\n".join([
                "    </body>",
                "</html>"
            ])) for i in range(num_pages)]
        assert compiled.html_code == expected_html

        # Check if the compiled CSS contains the expected code
        sorted_rules = sorted(list(set(
            zip(rule_names[num_pages],
                [list(styles[i % len(styles)].items())[0]
                 for i in range(num_pages)]))), key=lambda x: x[0])
        expected_css = "\n\n".join([
            '\n'.join([
                f".{name} " + "{",
                f"    {p}: {v};",
                "}"
            ]) for name, (p, v) in sorted_rules
        ])
        assert compiled.css_code == expected_css
