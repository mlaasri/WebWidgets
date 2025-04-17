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
from webwidgets.widgets.containers.page import Page


class Website(ReprMixin):
    """A collection of :py:class:`Page` objects that make up the structure of a
    web site."""

    def __init__(self, pages: List[Page] = None):
        """Creates a new website with an optional list of pages.

        :param pages: The pages of the website. Defaults to an empty list.
        :type pages: List[Page]
        """
        self.pages = [] if pages is None else pages

    def add(self, page: Page):
        """Adds a new page to the website.

        :param page: The page to be added.
        :type page: Page
        """
        self.pages.append(page)
