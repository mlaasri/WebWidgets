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
from webwidgets.utility.sanitizing import HTML_ENTITY_NAMES, \
    HTML_ENTITIES_INVERTED, sanitize_html_text


class TestSanitizingHTMLText:
    def test_html_entity_names(self):
        assert 'amp' in HTML_ENTITY_NAMES
        assert 'semi' in HTML_ENTITY_NAMES

    def test_html_entities_inverted(self):
        assert HTML_ENTITIES_INVERTED['&'] == (
            '&AMP', '&amp', '&AMP;', '&amp;')
        assert HTML_ENTITIES_INVERTED['>'] == ('&GT', '&gt', '&GT;', '&gt;')

    @pytest.mark.parametrize("html_entity", [
        '&AMP', '&lt;', '&gt;', '&sol;'
    ])
    def test_sanitize_html_text(self, html_entity):
        text = '<div>Some text &{} and more</div>'.format(html_entity)
        expected_text = '&lt;div&gt;Some text &amp;{} and more&lt;&sol;div&gt;'.format(
            html_entity)
        assert sanitize_html_text(text) == expected_text

    @ pytest.mark.parametrize("text, expected", [
        ("Some text abcdefghijklmnopqrstuvwxyz",
         "Some text abcdefghijklmnopqrstuvwxyz"),
        ("0123456789.!?#",
         "0123456789&period;&excl;&quest;&num;"),
        ("& &; &aamp; &amp &amp; &AMP;",
         "&amp; &amp;&semi; &amp;aamp&semi; &amp &amp; &AMP;"),
        ("&sool; &sol;/",
         "&amp;sool&semi; &sol;&sol;"),
        ('<div>Some text &sol;</div>',
         '&lt;div&gt;Some text &sol;&lt;&sol;div&gt;'),
        ('Some text\nand more',
         'Some text&NewLine;and more'),
        ('<p>&nbsp;</p>',
         '&lt;p&gt;&nbsp;&lt;&sol;p&gt;'),
    ])
    def test_sanitize_html_with_full_entity_replacement(self, text, expected):
        assert sanitize_html_text(text) == expected
        assert sanitize_html_text(text, replace_all_entities=True) == expected

    @ pytest.mark.parametrize("text, expected", [
        ("Some text abcdefghijklmnopqrstuvwxyz",
         "Some text abcdefghijklmnopqrstuvwxyz"),
        ("0123456789.!?#",
         "0123456789.!?#"),
        ("& &; &aamp; &amp &amp; &AMP;",
         "& &; &aamp; &amp &amp; &AMP;"),
        ("&sool; &sol;/",
         "&sool; &sol;&sol;"),
        ('<div>Some text &sol;</div>',
         '&lt;div&gt;Some text &sol;&lt;&sol;div&gt;'),
        ('Some text\nand more',
         'Some text&NewLine;and more'),
        ('<p>&nbsp;</p>',
         '&lt;p&gt;&nbsp;&lt;&sol;p&gt;'),
    ])
    def test_sanitize_html_with_partial_entity_replacement(self, text, expected):
        assert sanitize_html_text(text, replace_all_entities=False) == expected
