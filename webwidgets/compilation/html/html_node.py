from typing import Dict, List, Union


class HTMLNode:
    """
    Represents an HTML node (for example, a div or a span).
    """

    one_line: bool = False

    def __init__(self, children: List['HTMLNode'] = [], attributes: Dict[str, str] = {}):
        self.children = children
        self.attributes = attributes

    def add(self, child: Union['HTMLNode', str]) -> None:
        self.children.append(child)

    def _get_tag_name(self) -> str:
        return self.__class__.__name__.lower()

    @property
    def start_tag(self) -> str:

        # Rendering attributes
        attributes = self._render_attributes()
        maybe_space = ' ' if attributes else ''

        # Building start tag
        return f"<{self._get_tag_name()}{maybe_space}{attributes}>"

    @property
    def end_tag(self) -> str:
        return f"</{self._get_tag_name()}>"

    def _render_attributes(self) -> str:
        return ' '.join(
            f'{key}="{value}"' for key, value in self.attributes.items()
        )

    def to_html(self, indent_level: int = 0, indent_size: int = 4, force_one_line: bool = False) -> str:

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
