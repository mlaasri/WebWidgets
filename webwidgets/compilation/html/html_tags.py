from .html_node import HTMLNode, RawText, no_start_tag, no_end_tag, one_line
from typing import Dict


@one_line
class HeadingNode(HTMLNode):
    """A heading element like `<h1>`, `<h2>`, etc.

    A heading node renders on one line and only contains one child: a
    :py:class:`RawText` node with the heading text.
    """

    def __init__(self, text: str, attributes: Dict[str, str] = {}):
        """Creates a new heading node with the given text and attributes.

        :param text: The text content of the heading.
        :type text: str
        :param attributes: See :py:meth:`HTMLNode.__init__`. Default is an
            empty dictionary.
        :type attributes: Dict[str, str]
        """
        super().__init__(children=[
            RawText(text)
        ], attributes=attributes)


@one_line
class A(HTMLNode):
    """An `<a>` element representing a hyperlink."""

    def __init__(self, text: str, hyperlink: str,
                 other_attributes: Dict[str, str] = {}):
        """Creates a new anchor node `<a>` with the given text and link.

        :param text: The text content of the anchor.
        :type text: str
        :param hyperlink: The URL to which the anchor points. This value is
            used to populate the `href` attribute.
        :type hyperlink: str
        :param other_attributes: Other attributes to be added on top of the
            hyperlink. Must not contain a `href` key. Default is an empty
            dictionary.
        :type other_attributes: Dict[str, str]
        """

        assert "href" not in other_attributes, "'other_attributes' cannot " \
            "contain 'href' key."
        attributes = {
            "href": hyperlink,
            **other_attributes
        }
        super().__init__(children=[RawText(text)], attributes=attributes)


class Aside(HTMLNode):
    """An `<aside>` element containing supplementary content related to the
    main content of the page."""
    pass


class Body(HTMLNode):
    """The `<body>` element containing the visible content of a document."""
    pass


@one_line
class Button(HTMLNode):
    """A `<button>` element representing a clickable button."""
    pass


class Details(HTMLNode):
    """An `<details>` element providing additional information."""
    pass


class Div(HTMLNode):
    """A `<div>` element used for grouping elements."""
    pass


class Em(HTMLNode):
    """An `<em>` element representing emphasized text."""
    pass


@one_line
class Figcaption(HTMLNode):
    """A `<figcaption>` element providing a caption for a figure."""
    pass


class Figure(HTMLNode):
    """A `<figure>` element containing an image or other media along with its
    caption."""
    pass


class Form(HTMLNode):
    """A `<form>` element representing a form that can be submitted to a
    server."""
    pass


class H1(HeadingNode):
    """An `<h1>` element representing the most important heading."""
    pass


class H2(HeadingNode):
    """An `<h2>` element representing a secondary heading."""
    pass


class H3(HeadingNode):
    """An `<h3>` element representing a tertiary heading."""
    pass


class H4(HeadingNode):
    """An `<h4>` element representing a fourth-level heading."""
    pass


class H5(HeadingNode):
    """An `<h5>` element representing a fifth-level heading."""
    pass


class H6(HeadingNode):
    """An `<h6>` element representing the least important heading."""
    pass


class Head(HTMLNode):
    """The `<head>` element containing metadata about a document."""
    pass


class Header(HTMLNode):
    """A `<header>` element containing introductory content."""
    pass


class Hgroup(HTMLNode):
    """An `<hgroup>` element grouping related headings."""
    pass


class Html(HTMLNode):
    """The root `<html>` element of an HTML document."""
    pass


@no_end_tag
@one_line
class Img(HTMLNode):
    """An `<img>` element representing an image."""
    pass


@one_line
class Input(HTMLNode):
    """An `<input>` element for user input."""
    pass


@one_line
class Link(HTMLNode):
    """An `<link>` element for linking to external resources."""
    pass


class Main(HTMLNode):
    """The `<main>` element containing the main content of a document."""
    pass


@one_line
class Meta(HTMLNode):
    """A `<meta>` element providing metadata about a document."""
    pass


class Nav(HTMLNode):
    """A `<nav>` element containing navigation links."""
    pass


class Ol(HTMLNode):
    """An `<ol>` element representing an ordered list."""
    pass


class P(HTMLNode):
    """A `<p>` element representing a paragraph."""
    pass


class Script(HTMLNode):
    """A `<script>` element containing script code."""
    pass


class Section(HTMLNode):
    """The `<section>` element containing related content."""
    pass


@one_line
class Span(HTMLNode):
    """An `<span>` element for inline elements and content."""
    pass


class Summary(HTMLNode):
    """A `<summary>` element providing a brief summary of the contents of a
    `<details>` element."""
    pass


class Table(HTMLNode):
    """A `<table>` element representing tabular data."""
    pass


@one_line
class Td(HTMLNode):
    """A `<td>` element representing a data cell in a table."""
    pass


@one_line
class Th(HTMLNode):
    """A `<th>` element representing a header cell in a table."""
    pass


class Tr(HTMLNode):
    """An `<tr>` element representing a row in a table."""
    pass
