from typing import Dict, List, Union


class HTMLNode:
    """Represents an HTML node (for example, a div or a span).
    """

    one_line: bool = False

    def __init__(self, children: List['HTMLNode'] = [], attributes: Dict[str, str] = {}):
        """Creates an HTMLNode with optional children and attributes.

        :param children: List of child HTML nodes. Defaults to an empty list.
        :param attributes: Dictionary of attributes for the node. Defaults to an empty dictionary.
        """
        self.children = children
        self.attributes = attributes

    def _get_tag_name(self) -> str:
        """Returns the tag name of the HTML node.

        The tag name of a node object is the name of its class in lowercase.

        :return: The tag name of the HTML node.
        :rtype: str
        """
        return self.__class__.__name__.lower()

    def _render_attributes(self) -> str:
        """Renders the attributes of the HTML node into a string that can be added to the start tag.

        :return: A string containing all attribute key-value pairs separated by spaces.
        :rtype: str
        """
        return ' '.join(
            f'{key}="{value}"' for key, value in self.attributes.items()
        )

    def add(self, child: Union['HTMLNode', str]) -> None:
        """
        Adds a child to the HTML node.

        :param child: The child to be added. Can be either an instance of HTMLNode or a string.
        """
        self.children.append(child)

    @property
    def start_tag(self) -> str:
        """Returns the opening tag of the HTML node, including any attributes.

        :return: A string containing the opening tag of the element with its attributes.
        :rtype: str
        """
        # Rendering attributes
        attributes = self._render_attributes()
        maybe_space = ' ' if attributes else ''

        # Building start tag
        return f"<{self._get_tag_name()}{maybe_space}{attributes}>"

    @property
    def end_tag(self) -> str:
        """Returns the closing tag of the HTML node.

        :return: A string containing the closing tag of the element.
        :rtype: str
        """
        return f"</{self._get_tag_name()}>"

    def to_html(self, indent_level: int = 0, indent_size: int = 4, force_one_line: bool = False) -> str:
        """Converts the HTML node into a HTML code.

        :param indent_level: The current level of indentation in the HTML output.
        :type indent_level: int
        :param indent_size: The number of spaces to use for each indentation level.
        :type indent_size: int
        :param force_one_line: If True, forces all child elements to be rendered on a single line without additional
            indentation. Defaults to False.
        :type force_one_line: bool
        :return: A string containing the HTML representation of the element.
        :rtype: str
        """
        # Indenting
        indentation = "" if force_one_line else ' ' * indent_size * indent_level
        html_code = indentation

        # Opening the element
        html_code += self.start_tag

        # If content must be in one line
        if self.one_line or force_one_line:
            for child in self.children:
                if isinstance(child, str):
                    html_code += child
                else:
                    html_code += child.to_html(indent_level=0,
                                               force_one_line=True)
            html_code += self.end_tag

        # If content spans multi-line
        else:
            html_code += '\n'
            for child in self.children:
                if isinstance(child, str):
                    html_code += indentation + ' ' * indent_size + child
                else:
                    html_code += child.to_html(indent_level=indent_level + 1)
                html_code += '\n'
            html_code += indentation + self.end_tag

        return html_code


def no_start_tag(cls):
    """Decorator to remove the start tag from an HTMLNode subclass.

    :param cls: A subclass of HTMLNode whose start tag should be removed.
    :return: The given class with an empty start tag.
    """
    cls.start_tag = property(
        lambda _: '', doc="This element does not have a start tag")
    return cls


def no_end_tag(cls):
    """Decorator to remove the end tag from an HTMLNode subclass.

    :param cls: A subclass of HTMLNode whose end tag should be removed.
    :return: The given class with an empty end tag.
    """
    cls.end_tag = property(
        lambda _: '', doc="This element does not have an end tag")
    return cls
