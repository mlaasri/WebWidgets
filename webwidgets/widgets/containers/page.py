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

from .container import Container
from webwidgets.compilation.html.html_node import RootNode
from webwidgets.compilation.html.html_tags import Body, Doctype, Head, Html


class Page(Container):
    """A widget representing a web page. It contains other widgets and is
    responsible for laying them out within the page.
    """

    def build(self) -> RootNode:
        """Builds the HTML representation of the page.

        This method constructs an HTML structure that includes a doctype
        declaration, a head section with meta tags, and a body section
        containing the widgets. The widgets are rendered recurisvely by calling
        their :py:meth:`build` method.

        :return: An :py:class:`RootNode` object representing the page.
        :rtype: RootNode
        """
        return RootNode(
            children=[
                Doctype(),
                Html(
                    children=[
                        Head(),
                        Body(children=[w.build() for w in self.widgets])
                    ]
                )
            ]
        )
