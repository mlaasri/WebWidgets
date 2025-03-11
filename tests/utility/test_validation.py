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
import re
from webwidgets.utility.validation import validate_css_identifier, validate_html_class


class TestValidate:
    def test_valid_css_identifiers(self):
        """Test that valid CSS identifiers are accepted"""
        validate_css_identifier("i")
        validate_css_identifier("identifier")
        validate_css_identifier("identifier123")
        validate_css_identifier("myIdentifier")
        validate_css_identifier("myIdentifier123")
        validate_css_identifier("my-identifier-456")
        validate_css_identifier("my-Ident_ifier-456")
        validate_css_identifier("_identifier123")
        validate_css_identifier("_myIdentifier")
        validate_css_identifier("_my-Identifier456")
        validate_css_identifier("--myIdentifier")
        validate_css_identifier("--my-Identifier456")

    def test_invalid_css_identifier_empty(self):
        """Test that an invalid CSS identifier (that is empty) raises an exception"""
        with pytest.raises(ValueError, match="must start with"):
            validate_css_identifier("")

    def test_invalid_css_identifier_starting_with_digit(self):
        """Test that an invalid CSS identifier (starting with a digit) raises an exception"""
        with pytest.raises(ValueError, match="must start with"):
            validate_css_identifier("123my-class")

    def test_invalid_css_identifier_starting_with_single_hyphen(self):
        """Test that an invalid CSS identifier (starting with a single hyphen) raises an exception"""
        with pytest.raises(ValueError, match="must start with"):
            validate_css_identifier("-my-class")

    def test_invalid_css_identifier_starting_with_space(self):
        """Test that an invalid CSS identifier (starting with a space) raises an exception"""
        with pytest.raises(ValueError, match="must start with"):
            validate_css_identifier(" identifier")

    def test_invalid_css_identifier_ending_with_space(self):
        """Test that an invalid CSS identifier (ending with a space) raises an exception"""
        with pytest.raises(ValueError, match=r"Invalid character\(s\)"):
            validate_css_identifier("identifier ")

    def test_invalid_css_identifier_with_double_space(self):
        """Test that an invalid CSS identifier (containing double spaces) raises an exception"""
        with pytest.raises(ValueError, match=r"Invalid character\(s\).*  "):
            validate_css_identifier("myClass  myOtherClass")

    @pytest.mark.parametrize("char", "!@#$%^&*()<>?/|\\}{[\":;\'] ")
    def test_invalid_css_identifier_with_invalid_character(self, char):
        """Test that an invalid CSS identifier (containing an invalid character) raises an exception"""
        with pytest.raises(ValueError,
                           match=fr"Invalid character\(s\).*{re.escape(char)}"):
            validate_css_identifier(f"my-class-{char}")

    @pytest.mark.parametrize("chars", [
        "!@#", "$%&", "<>{}()[]", "*+=|;:'\""
    ])
    def test_invalid_characters_in_error_message(self, chars):
        """Test that invalid characters are all present in the error message"""
        with pytest.raises(ValueError, match=re.escape(', '.join(chars))):
            validate_css_identifier(f"my-class-{chars}")

    def test_valid_html_classes(self):
        """Test that valid HTML class attributes are accepted"""
        validate_html_class("z e r")
        validate_html_class("myClass myOtherClass")
        validate_html_class("myClass z myOtherClass3")
        validate_html_class("my-class123 my-other-class- _my-last-class4")

    def test_invalid_html_class_starting_with_space(self):
        """Test that an invalid HTML class attribute (starting with a space) raises an exception"""
        with pytest.raises(ValueError, match="cannot start nor end with a space"):
            validate_html_class(" myClass myOtherClass")

    def test_invalid_html_class_ending_with_space(self):
        """Test that an invalid HTML class attribute (ending with a space) raises an exception"""
        with pytest.raises(ValueError, match="cannot start nor end with a space"):
            validate_html_class("myClass myOtherClass ")

    def test_invalid_html_class_with_double_space(self):
        """Test that an invalid HTML class attribute (containing double spaces) raises an exception"""
        with pytest.raises(ValueError, match="cannot contain double spaces"):
            validate_html_class("myClass  myOtherClass")

    def test_invalid_html_class_with_invalid_identifiers(self):
        """Test that an invalid HTML class attribute with invalid CSS identifiers raises an exception"""
        with pytest.raises(ValueError, match=r"Invalid character\(s\).*!, @, #"):
            validate_html_class("my-class123 my-other-class-!@#")
        with pytest.raises(ValueError, match="must start with"):
            validate_html_class("my-class123 -er4 my-other-class")
