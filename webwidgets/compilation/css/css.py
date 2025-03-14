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

import itertools
from typing import Dict, List, Union
from webwidgets.compilation.html.html_node import HTMLNode
from webwidgets.utility.validation import validate_css_identifier


class CompiledCSS:
    """A utility class to hold compiled CSS rules.
    """

    def __init__(self, trees: List[HTMLNode], rules: Dict[str, Dict[str, str]],
                 mapping: Dict[int, List[str]]):
        """Stores compiled CSS rules.

        :param trees: The HTML trees at the origin of the compilation. These
            are the elements that have been styled with CSS properties.
        :type trees: List[HTMLNode]
        :param rules: The compiled CSS rules, specified as a dictionary mapping
            the rule's name to its corresponding CSS declarations. For example:
            `{'r0': {'color': 'red'}}`.
        :type rules: Dict[str, Dict[str, str]]
        :param mapping: A dictionary mapping each node ID to a list of rules
            that achieve the same style. Rules must be specified by their name.
            For example: `{123: ['r0', 'r2'], 456: ['r1']}`.
        :type mapping: Dict[int, List[str]]
        """
        self.trees = trees
        self.rules = rules
        self.mapping = mapping

    def to_css(self, indent_size: int = 4) -> str:
        """Converts the `rules` dictionary of the :py:class:`CompiledCSS`
        object into CSS code.

        Each rule name is converted to a class selector and each property name
        is validated with :py:func:`validate_css_identifier` before being
        converted.

        :param indent_size: The number of spaces to use for indentation in the
            CSS code. Defaults to 4.
        :type indent_size: int
        :return: The CSS code as a string.
        :rtype: str
        """
        # Initializing code and defining indentation
        css_code = ""
        indentation = ' ' * indent_size

        # Writing down each rule from the rules dictionary
        for i, (name, declarations) in enumerate(self.rules.items()):
            css_code += f".{name}" + " {\n"
            for property_name, value in declarations.items():
                validate_css_identifier(property_name)
                css_code += f"{indentation}{property_name}: {value};\n"
            css_code += "}" + ('\n\n' if i < len(self.rules) - 1 else '')

        return css_code


def compile_css(trees: Union[HTMLNode, List[HTMLNode]]) -> CompiledCSS:
    """Computes optimized CSS rules from the given HTML trees.

    The main purpose of this function is to reduce the number of CSS rules
    required to achieve a particular style across one or more HTML trees. The
    function takes a list of HTML nodes as input (not necessarily from the same
    tree) and computes an optimized set of CSS rules that achieves the same
    style across all nodes. The resulting :py:class:`CompiledCSS` object
    contains the optimized rules and their mapping to each node.

    For example, the following tree:

    .. code-block:: python

        tree = HTMLNode(
            style={"margin": "0", "padding": "0"},
            children=[
                HTMLNode(style={"margin": "0", "padding": "0"}),
                HTMLNode(style={"margin": "0", "color": "blue"}),
            ]
        )

    can be stylistically described with only 3 CSS rules:

    .. code-block:: python

        >>> compiled_css = compile_css(tree)
        >>> print(compiled_css.rules)
        {
            'r0': {'color': 'blue'},
            'r1': {'margin': '0'},
            'r2': {'padding': '0'}
        }

    :param trees: A single tree or a list of trees to optimize over. All
        children are recursively included in the compilation.
    :type trees: Union[HTMLNode, List[HTMLNode]]
    :return: The :py:class:`CompiledCSS` object containing the optimized rules.
        Every HTML node present in one or more of the input trees is included
        in the :py:attr:`CompiledCSS.mapping` attribute, even if the node does
        not have a style. Rules are alphabetically ordered by name in the
        mapping.
    :rtype: CompiledCSS
    """
    # Handling case of a single tree
    if isinstance(trees, HTMLNode):
        trees = [trees]

    # For now, we just return a simple mapping where each CSS property defines
    # its own ruleset
    styles = {k: v for tree in trees for k, v in tree.get_styles().items()}
    properties = set(itertools.chain.from_iterable(s.items()
                     for s in styles.values()))
    rules = {f"r{i}": dict([p]) for i, p in enumerate(sorted(properties))}
    mapping = {node_id: sorted([n for n, r in rules.items() if
                                set(r.items()).issubset(style.items())])
               for node_id, style in styles.items()}
    return CompiledCSS(trees, rules, mapping)


def apply_css(css: CompiledCSS, tree: HTMLNode) -> None:
    """Applies the CSS rules to the given tree.

    Rules are added as HTML classes to each node with a style in the tree. If a
    node does not have a `class` attribute yet, it will be created for that
    node. Nodes that do not have any style are left untouched.

    Note that this function is recursive and calls itself on each child node of
    the tree.

    :param css: The compiled CSS object containing the rules to apply and the
        mapping to each node. It should have been created by invoking
        :py:func:`compile_css` on the given tree, but it can be modified before
        passing it to this function, as long as its content remains consistent.
    :type css: CompiledCSS
    :param tree: The tree to which the CSS rules should be applied. It will be
        modified in place by this function. If you want to keep the original
        tree unchanged, make a deep copy of it using its
        :py:meth:`HTMLNode.copy` method and pass this copy instead.
    :type tree: HTMLNode
    """
    # Only modifying nodes if they have a style (and therefore if the list of
    # rules mapped to them in `css.mapping` is not empty)
    if tree.style:

        # Listing rules to add as classes. We do not add rules that are already
        # there.
        rules_to_add = [r for r in css.mapping[id(tree)] if r and r not in
                        tree.attributes.get('class', '').split(' ')]

        # Updating the class attribute. If it already exists and is not empty,
        # we need to insert a space before adding the CSS classes.
        maybe_space = ' ' if tree.attributes.get(
            'class', None) and rules_to_add else ''
        tree.attributes['class'] = tree.attributes.get(
            'class', '') + maybe_space + ' '.join(rules_to_add)

    # Recursively applying the CSS rules to all child nodes of the tree
    for child in tree.children:
        apply_css(css, child)
