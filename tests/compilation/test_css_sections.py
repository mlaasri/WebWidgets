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
from webwidgets.compilation.css.sections.css_section import CSSSection


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
