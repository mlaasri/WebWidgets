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

from abc import ABC, abstractmethod
from webwidgets.utility.representation import ReprMixin


class CSSSection(ABC, ReprMixin):
    """Abstract base class representing a section of a CSS file.

    All subclasses of :py:class:`CSSSection` must implement a :py:meth:`to_css`
    method that returns a string.
    """

    def __init__(self, title: str = None):
        """Creates a new section with an optional title.

        :param title: The title of the section. If provided, the section will
            be preceded by a comment containing the title in the output CSS
            code. If None, no title will be used to separate the section from
            the rest of the code.
        :type title: str
        """
        super().__init__()
        self.title = title

    @abstractmethod
    def to_css(self) -> str:
        """Converts the CSSSection object into CSS code.

        This method must be overridden by subclasses to compile specific CSS
        code.
        """
        pass
