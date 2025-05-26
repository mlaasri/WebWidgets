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
from webwidgets.utility.validation import validate_css_comment


class CSSSection(ABC, ReprMixin):
    """Abstract base class representing a section of a CSS file.

    All subclasses of :py:class:`CSSSection` must implement a
    :py:meth:`compile_content` method that returns a string.
    """

    @staticmethod
    def pad_title(title: str, max_length: int) -> str:
        """Returns a padded version of the given title with decorative
        characters `=` around it.

        This function will add the maximum number of decorative characters to
        the title while keeping symmetry and remaining under the given maximum
        length.

        :param title: The title to pad. It should be shorter than `max_length`;
            otherwise, an error will be raised.
        :type title: str
        :param max_length: The maximum length of the padded title. It should be
            at least the length of `title`; otherwise, an error will be raised.
        :type max_length: int
        :return: The padded title.
        :rtype: str
        :raises ValueError: If the title is shorter than `max_length`.
        """
        # Checking consistency between arguments
        if len(title) > max_length:
            raise ValueError(f"Cannot pad title '{title}' of length "
                             f"{len(title)} with max length {max_length}")

        # If the title is too long, we don't add decorative characters
        remaining = max_length - (len(title) + 2)
        if remaining <= 1:
            return title

        # Otherwise, we add decorative characters around the title
        characters = "=" * (remaining // 2)
        return characters + ' ' + title + ' ' + characters

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

        If the section has a title, it will be padded with
        :py:meth:`CSSSection.pad_title` and turned into a comment. That comment
        will be validated with :py:func:`validate_css_comment` and inserted
        before the result of :py:meth:`CSSSection.compile_content` in the CSS
        code.

        If the section has no title, this function will produce the same result
        as :py:meth:`CSSSection.compile_content`.

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

        max_length = max(40, len(self.title))
        comment = ' ' + CSSSection.pad_title(self.title, max_length) + ' '
        validate_css_comment(comment)

        return "/*" + comment + "*/\n\n" + \
            self.compile_content(*args, **kwargs)
