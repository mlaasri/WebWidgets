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

from typing import List
from webwidgets.utility.representation import ReprMixin


class CompiledWebsite(ReprMixin):
    """A utility class to store compiled HTML and CSS code obtained from a
    :py:class:`Website` object.
    """

    def __init__(self, html_code: List[str], css_code: str):
        """Stores compiled HTML and CSS code.

        :param html_code: The compiled HTML code of each page in the website.
        :type html_code: List[str]
        :param css_code: The compiled CSS code of the website, shared across
            all pages.
        :type css_code: str
        """
        super().__init__()
        self.html_code = html_code
        self.css_code = css_code
