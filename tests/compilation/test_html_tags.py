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
from webwidgets.compilation.html.html_tags import *


class TestIndividualHTMLTags:
    def test_text_node(self):
        text_node = TextNode("Hello, World!")
        assert text_node.to_html() == "<textnode>Hello, World!</textnode>"

    def test_a(self):
        a_tag = A("Click Here", "https://example.com")
        assert a_tag.to_html() == '<a href="https://example.com">Click Here</a>'

    def test_body(self):
        body_tag = Body(children=[RawText("content")])
        expected_html = '\n'.join([
            "<body>",
            "    content",
            "</body>"
        ])
        assert body_tag.to_html() == expected_html

    def test_button(self):
        button_tag = Button("Submit", {"type": "submit"})
        assert button_tag.to_html() == '<button type="submit">Submit</button>'

    def test_div(self):
        div_tag = Div(children=[RawText("content")])
        expected_html = '\n'.join([
            "<div>",
            "    content",
            "</div>"
        ])
        assert div_tag.to_html() == expected_html

    def test_em(self):
        em_tag = Em("This is emphasized text")
        assert em_tag.to_html() == '<em>This is emphasized text</em>'

    def test_form(self):
        form_tag = Form(children=[RawText("content")])
        expected_html = '\n'.join([
            "<form>",
            "    content",
            "</form>"
        ])
        assert form_tag.to_html() == expected_html

    @pytest.mark.parametrize("heading_level, heading_class", [
        (1, H1), (2, H2), (3, H3), (4, H4), (5, H5), (6, H6)
    ])
    def test_headings(self, heading_level, heading_class):
        h_tag = heading_class(f"Heading {heading_level}")
        assert h_tag.to_html() == f"<h{heading_level}>" \
            f"Heading {heading_level}</h{heading_level}>"

    def test_head(self):
        head_tag = Head(children=[RawText("content")])
        expected_html = '\n'.join([
            "<head>",
            "    content",
            "</head>"
        ])
        assert head_tag.to_html() == expected_html

    def test_header(self):
        header_tag = Header(children=[RawText("content")])
        expected_html = '\n'.join([
            "<header>",
            "    content",
            "</header>"
        ])
        assert header_tag.to_html() == expected_html

    def test_html(self):
        html_tag = Html(children=[RawText("content")])
        expected_html = '\n'.join([
            "<html>",
            "    content",
            "</html>"
        ])
        assert html_tag.to_html() == expected_html

    def test_img_without_alt(self):
        img_tag = Img(src="image.jpg")
        assert img_tag.to_html() == '<img src="image.jpg">'

    def test_img(self):
        img_tag = Img(src="image.jpg", alt="Image")
        assert img_tag.to_html() in [
            '<img src="image.jpg" alt="Image">',
            '<img alt="Image" src="image.jpg">'
        ]
