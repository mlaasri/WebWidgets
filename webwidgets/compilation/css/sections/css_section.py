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
from typing import Any
from webwidgets.utility.representation import ReprMixin


class CSSSection(ABC, ReprMixin):
    """Abstract base class representing a section of a CSS file.

    All subclasses of :py:class:`CSSSection` must implement a
    :py:meth:`compile_content` method that returns a string.
    """

    @staticmethod
    def compile_title(title: str) -> str:
        """Compiles a section title into CSS code and returns it.

        The title is converted into a single-line CSS comment that can be used
        to identify a CSS section within the rest of the code.

        :param title: The title to convert into a CSS comment.
        :type title: str
        :return: A string representing the CSS comment for the title.
        :rtype: str
        """
        # Defining the CSS comment's start and end tokens
        start, end = "/* ", " */"

        # If the title is too long, we don't add decorative characters
        remaining = 80 - len(start) - (len(title) + 2) - len(end)
        if remaining <= 0:
            return start + title + end

        # Otherwise, we add decorative characters around the title
        symbols = "=" * (remaining // 2)
        return start + symbols + ' ' + title + ' ' + symbols + end

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
    def compile_content(self) -> str:
        """Converts the content of the CSSSection object (excluding the title)
        into CSS code.

        This method must be overridden by subclasses to compile specific CSS
        code.
        """
        pass

    def to_css(self, *args: Any, **kwargs: Any) -> str:
        """Converts the CSSSection object into CSS code.

        This function just wraps around :py:meth:`CSSSection.compile_title` and
        :py:meth:`CSSSection.compile_content` to produce the final CSS code. If
        the section has no title, :py:meth:`CSSSection.compile_title` is
        skipped and this function will produce the same result as
        :py:meth:`CSSSection.compile_content`.

        :param args: Arguments to pass to
            :py:meth:`CSSSection.compile_content`.
        :type args: Any
        :param kwargs: Keyword arguments to pass to
            :py:meth:`CSSSection.compile_content`.
        :type kwargs: Any
        :return: The CSS code for the section.
        :rtype: str
        """
        if self.title is None:
            return self.compile_content(*args, **kwargs)
        return CSSSection.compile_title(self.title) + "\n\n" + \
            self.compile_content(*args, **kwargs)
