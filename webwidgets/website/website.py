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

from .compiled_website import CompiledWebsite
from typing import List
from webwidgets.compilation.css import compile_css, apply_css
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
        super().__init__()
        self.pages = [] if pages is None else pages

    def add(self, page: Page):
        """Adds a new page to the website.

        :param page: The page to be added.
        :type page: Page
        """
        self.pages.append(page)

    def compile(self) -> CompiledWebsite:
        """Compiles the website into HTML and CSS code."""
        # Building the HTML representation of each page
        trees = [page.build() for page in self.pages]

        # Compiling HTML and CSS code
        compiled_css = compile_css(trees)
        for tree in trees:
            apply_css(compiled_css, tree)
        html_content = [tree.to_html() for tree in trees]
        css_content = compiled_css.to_css()

        # Storing the result in a new CompiledWebsite object
        return CompiledWebsite(html_content, css_content)
