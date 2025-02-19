from .html_node import HTMLNode, RawText, no_end_tag, one_line
from typing import Dict


@one_line
class TextNode(HTMLNode):
    """A one-line HTML element that only contains raw text (like `<h1>`).

    A text node renders on one line and only contains one child: a
    :py:class:`RawText` node with the text to be rendered.
    """

    def __init__(self, text: str, attributes: Dict[str, str] = {}):
        """Creates a new text node with the given text and attributes.

        :param text: The text content of the node.
        :type text: str
        :param attributes: See :py:meth:`HTMLNode.__init__`. Default is an
            empty dictionary.
        :type attributes: Dict[str, str]
        """
        super().__init__(children=[
            RawText(text)
        ], attributes=attributes)


class A(TextNode):
    """An `<a>` element representing a hyperlink."""

    def __init__(self, text: str, hyperlink: str,
                 other_attributes: Dict[str, str] = {}):
        """Creates a new anchor element `<a>` with the given text and link.

        :param text: The text content of the anchor.
        :type text: str
        :param hyperlink: The URL to which the anchor points. This value is
            used to populate the `href` attribute.
        :type hyperlink: str
        :param other_attributes: Other attributes to be added on top of the
            hyperlink. Must not contain a `href` key. Default is an empty
            dictionary.
        :type other_attributes: Dict[str, str]
        :raise AssertionError: If `other_attributes` contains the key `'href'`.
            The `href` attribute should be specified using the `hyperlink`
            argument.
        """
        assert "href" not in other_attributes, "'other_attributes' cannot " \
            "contain a key named 'href'. Use the 'hyperlink' argument to " \
            "specify the link instead."
        attributes = {
            "href": hyperlink,
            **other_attributes
        }
        super().__init__(text=text, attributes=attributes)


class Body(HTMLNode):
    """The `<body>` element containing the visible content of a document."""
    pass


class Button(TextNode):
    """A `<button>` element representing a clickable button."""
    pass


class Div(HTMLNode):
    """A `<div>` element used for grouping elements."""
    pass


class Em(TextNode):
    """An `<em>` element representing emphasized text."""
    pass


class Form(HTMLNode):
    """A `<form>` element representing a form that can be submitted to a
    server."""
    pass


class H1(TextNode):
    """An `<h1>` element representing the most important heading."""
    pass


class H2(TextNode):
    """An `<h2>` element representing a secondary heading."""
    pass


class H3(TextNode):
    """An `<h3>` element representing a tertiary heading."""
    pass


class H4(TextNode):
    """An `<h4>` element representing a fourth-level heading."""
    pass


class H5(TextNode):
    """An `<h5>` element representing a fifth-level heading."""
    pass


class H6(TextNode):
    """An `<h6>` element representing the least important heading."""
    pass


class Head(HTMLNode):
    """The `<head>` element containing metadata about a document."""
    pass


class Header(HTMLNode):
    """A `<header>` element containing introductory content."""
    pass


class Html(HTMLNode):
    """The root `<html>` element of an HTML document."""
    pass


@one_line
@no_end_tag
class Img(HTMLNode):
    """An `<img>` element representing an image."""

    def __init__(self, src: str, alt: str = None,
                 other_attributes: Dict[str, str] = {}):
        """Creates a new `<img>` element.

        :param src: The URL of the image.
        :type src: str
        :param alt: A text description of the image. If empty or None, it will not
            be added to the element at all. Default is None.
        :type alt: str
        :param other_attributes: Additional attributes to be added to the `<img>`
            element. Must not contain any key named `'src'` or `'alt'`. Default is
            an empty dictionary.
        :type other_attributes: Dict[str, str]
        :raise AssertionError: If `other_attributes` contains the key `'src'` or
            `'alt'`. These attributes should be specified using the `src` and `alt`
            arguments.
        """
        for k in ("src", "alt"):
            assert k not in other_attributes, "'other_attributes' cannot " \
                f"contain a key named '{k}'. Use the '{k}' argument to " \
                "specify the value instead."
        attributes = {"alt": alt} if alt else {}
        attributes |= {
            "src": src,
            **other_attributes
        }
        super().__init__(attributes=attributes)


@one_line
@no_end_tag
class Input(HTMLNode):
    """An `<input>` element for user input."""
    pass


@one_line
@no_end_tag
class Link(HTMLNode):
    """An `<link>` element for linking to external resources."""
    pass


class Main(HTMLNode):
    """The `<main>` element containing the main content of a document."""
    pass


@one_line
@no_end_tag
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


@one_line
class Script(HTMLNode):
    """A `<script>` element containing script code."""
    pass


class Section(HTMLNode):
    """The `<section>` element containing related content."""
    pass


class Span(TextNode):
    """An `<span>` element for inline elements and content."""
    pass


class Title(TextNode):
    """The `<title>` element providing the title of a document."""
    pass


class Ul(HTMLNode):
    """An `<ul>` element representing an unordered list."""
    pass
