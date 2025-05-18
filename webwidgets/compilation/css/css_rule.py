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

from typing import Dict
from webwidgets.utility.indentation import get_indentation
from webwidgets.utility.representation import ReprMixin
from webwidgets.utility.validation import validate_css_identifier, validate_css_selector


class CSSRule(ReprMixin):
    """A rule in a style sheet.
    """

    def __init__(self, name: str, declarations: Dict[str, str]):
        """Stores the name and declarations of the rule.

        :param name: The name of the rule.
        :type name: str
        :param declarations: The CSS declarations for the rule, specified as a
            dictionary where keys are property names and values are their
            corresponding values. For example: `{'color': 'red'}`
        :type declarations: Dict[str, str]
        """
        super().__init__()
        self.name = name
        self.declarations = declarations

    def to_css(self, indent_size: int = 4) -> str:
        """Converts the rule into CSS code.

        The rule's name is converted to a class selector.

        Note that the rule's name and all property names are validated before
        being converted. The rule's name is validated with
        :py:func:`validate_css_selector` while the property names are validated
        with :py:func:`validate_css_identifier`. 

        :param indent_size: The number of spaces to use for indentation in the
            CSS code. Defaults to 4.
        :type indent_size: int
        :return: The CSS code as a string.
        :rtype: str
        """
        # Defining indentation
        indentation = get_indentation(level=1, size=indent_size)

        # Validating the rule name as a selector
        validate_css_selector(self.name)

        # Writing down each property
        css_code = f".{self.name}" + " {\n"
        for property_name, value in self.declarations.items():
            validate_css_identifier(property_name)
            css_code += f"{indentation}{property_name}: {value};\n"
        css_code += "}"

        return css_code
