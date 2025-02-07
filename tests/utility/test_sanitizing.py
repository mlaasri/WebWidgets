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
    def test_no_empty_html_entities(self):
        assert all(e for _, e in HTML_ENTITIES_INVERTED.items())

    @pytest.mark.parametrize("name", [
        'amp', 'lt', 'gt', 'semi', 'sol', 'apos', 'quot'
    ])
    def test_html_entity_names(self, name):
        assert name in HTML_ENTITY_NAMES

    def test_html_entities_inverted(self):
        assert set(HTML_ENTITIES_INVERTED['&']) == set((
            '&amp;', '&AMP', '&amp', '&AMP;'))
        assert HTML_ENTITIES_INVERTED['&'][0] == '&amp;'
        assert set(HTML_ENTITIES_INVERTED['>']) == set((
            '&gt;', '&GT', '&gt', '&GT;'))
        assert HTML_ENTITIES_INVERTED['>'][0] == '&gt;'
        assert HTML_ENTITIES_INVERTED['\u0391'] == ('&Alpha;',)

    @pytest.mark.parametrize("html_entity", [
        '&AMP', '&lt;', '&gt;', '&sol;'
    ])
    def test_sanitize_html_text(self, html_entity):
        text = '<div>Some text &{} and more</div>'.format(html_entity)
        expected_text = '&lt;div&gt;Some text &amp;{} and more&lt;&sol;div&gt;'.format(
            html_entity)
        assert sanitize_html_text(text) == expected_text

    @pytest.mark.parametrize("text, expected", [
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
         'Some text<br>and more'),
        ('<p>&nbsp;</p>',
         '&lt;p&gt;&nbsp;&lt;&sol;p&gt;'),
        ("This 'quote' is not \"there\".",
         "This &apos;quote&apos; is not &quot;there&quot;&period;"),
        ("This is a mix < than 100% & 3/5",
         "This is a mix &lt; than 100&percnt; &amp; 3&sol;5")
    ])
    def test_sanitize_html_with_full_entity_replacement(self, text, expected):
        assert sanitize_html_text(text) == expected
        assert sanitize_html_text(text, replace_all_entities=True) == expected

    @pytest.mark.parametrize("text, expected", [
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
         'Some text<br>and more'),
        ('<p>&nbsp;</p>',
         '&lt;p&gt;&nbsp;&lt;&sol;p&gt;'),
        ("This 'quote' is not \"there\".",
         "This &apos;quote&apos; is not &quot;there&quot;."),
        ("This is a mix < than 100% & 3/5",
         "This is a mix &lt; than 100% & 3&sol;5")
    ])
    def test_sanitize_html_with_partial_entity_replacement(self, text, expected):
        assert sanitize_html_text(text, replace_all_entities=False) == expected
