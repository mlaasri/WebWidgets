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
from webwidgets.compilation.css.css_rule import CSSRule
from webwidgets.compilation.css.sections.css_section import CSSSection
from webwidgets.compilation.css.sections.rule_section import RuleSection


class TestCSSSection:
    def test_css_section_is_abstract(self):
        with pytest.raises(TypeError, match="compile_content"):
            CSSSection("title")

    @pytest.mark.parametrize("title", ["Title", "Section", "a" * 71])
    def test_compile_short_title(self, title: str):
        compiled_title = CSSSection.compile_title(title)
        symbols = '=' * ((72 - len(title)) // 2)
        assert compiled_title == f"/* {symbols} {title} {symbols} */"

    @pytest.mark.parametrize("title", ["Title" * 80, "Section" * 80, "a" * 72])
    def test_compile_long_title(self, title: str):
        compiled_title = CSSSection.compile_title(title)
        assert compiled_title == f"/* {title} */"


class TestRuleSection:
    def test_compile_content_one_rule(self):
        section = RuleSection([
            CSSRule("rule", {"property": "value"})
        ])
        expected_css = '\n'.join([
            ".rule {",
            "    property: value;",
            "}"
        ])
        assert section.compile_content() == expected_css
        section.title = "title"  # Shouldn't impact content
        assert section.compile_content() == expected_css

    def test_compile_content_multiple_rules(self):
        section = RuleSection([
            CSSRule("ruleA", {"p1": "v1", "p2": "v2"}),
            CSSRule("ruleB", {"p1": "x", "q1": "y"}),
            CSSRule("rC", {"a": "u", "b": "v"})
        ])
        expected_css = '\n'.join([
            ".ruleA {",
            "    p1: v1;",
            "    p2: v2;",
            "}",
            "",
            ".ruleB {",
            "    p1: x;",
            "    q1: y;",
            "}",
            "",
            ".rC {",
            "    a: u;",
            "    b: v;",
            "}"
        ])
        assert section.compile_content() == expected_css
        section.title = "title"  # Shouldn't impact content
        assert section.compile_content() == expected_css

    @pytest.mark.parametrize("indent_size", [0, 2, 3, 4])
    def test_compile_content_indentation(self, indent_size: int):
        section = RuleSection([
            CSSRule("rule", {"property": "value"})
        ])
        expected_css = '\n'.join([
            ".rule {",
            f"{' ' * indent_size}property: value;",
            "}"
        ])
        assert section.compile_content(
            indent_size=indent_size) == expected_css

    def test_to_css_no_title(self):
        section = RuleSection([
            CSSRule("rule", {"property": "value"}),
        ])
        expected_css = '\n'.join([
            ".rule {",
            "    property: value;",
            "}"
        ])
        assert section.to_css() == expected_css

    def test_to_css_with_title(self):
        section = RuleSection([
            CSSRule("rule", {"property": "value"}),
        ], "title")
        symbols = "=" * 33
        expected_css = '\n'.join([
            f"/* {symbols} title {symbols} */",
            "",
            ".rule {",
            "    property: value;",
            "}"
        ])
        assert section.to_css() == expected_css

    @pytest.mark.parametrize("indent_size", [0, 2, 3, 4])
    def test_to_css_passes_down_indentation_no_title(self, indent_size: int):
        section = RuleSection([
            CSSRule("rule", {"property": "value"}),
        ])
        expected_css = '\n'.join([
            ".rule {",
            f"{' ' * indent_size}property: value;",
            "}"
        ])
        assert section.to_css(indent_size=indent_size) == expected_css

    @pytest.mark.parametrize("indent_size", [0, 2, 3, 4])
    @pytest.mark.parametrize("title", ["title", "Hello", "World"])
    def test_to_css_passes_down_indentation_with_title(self,
                                                       indent_size: int,
                                                       title: str):
        section = RuleSection([
            CSSRule("rule", {"property": "value"}),
        ], title)
        symbols = "=" * 33
        expected_css = '\n'.join([
            f"/* {symbols} {title} {symbols} */",
            "",
            ".rule {",
            f"{' ' * indent_size}property: value;",
            "}"
        ])
        assert section.to_css(indent_size=indent_size) == expected_css
