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
from typing import Dict, List
from webwidgets.compilation.html.html_node import HTMLNode


class CompiledCSS:
    """A utility class to hold compiled CSS rules.
    """

    def __init__(self, nodes: List[HTMLNode],
                 rules: Dict[str, Dict[str, str]] = {},
                 mapping: Dict[int, List[str]] = {}):
        """Stores compiled CSS rules.

        :param nodes: The HTML nodes at the origin of the compilation. These
            are typically the elements that have been styled with CSS
            properties.
        :type nodes: List[HTMLNode]
        :param rules: The compiled CSS rules, specified as a dictionary mapping
            the rule's selector to its corresponding CSS declarations. For
            example: `{'g0': {'color': 'red'}}`.
        :type rules: Dict[str, Dict[str, str]]
        :param mapping: A dictionary mapping each node ID to a list of rules
            that achieve the same style. Rules are specified by their selector.
        :type mapping: Dict[int, List[str]]
        """
        self.nodes = nodes
        self.rules = rules
        self.mapping = mapping


def compile_css(nodes: List[HTMLNode]) -> CompiledCSS:
    """Computes optimized CSS rules from the given nodes.

    The main purpose of this function is to reduce the number of CSS rules
    required to achieve a particular style across one or more HTML trees. The
    function takes a list of HTML nodes as input (not necessarily from the same
    tree) and computes an optimized set of CSS rules that achieves the same
    style across all nodes. The resulting :py:class:`CompiledCSS` object
    contains the optimized rules and their mapping to each node.

    For example, the following tree:

    .. code-block:: python

        node = HTMLNode(
            style={"margin": "0", "padding": "0"},
            children=[
                HTMLNode(style={"margin": "0", "padding": "0"}),
                HTMLNode(style={"margin": "0", "color": "blue"}),
            ]
        )

    can be stylistically described with only 3 CSS rules:

    .. code-block:: python

        >>> compiled_css = compile_css([node])
        >>> print(compiled_css.rules)
        {
            'g0': ('color', 'blue'),
            'g1': ('margin', '0'),
            'g2': ('padding', '0')
        }

    :param nodes: The nodes to optimize over. All children are recursively
        included in the compilation.
    :type nodes: List[HTMLNode]
    :return: The CompiledCSS object containing the optimized rules.
    :rtype: CompiledCSS
    """

    # For now, we just return a simple mapping where each CSS property defines
    # its own ruleset
    styles = {k: v for node in nodes for k, v in node.get_styles().items()}
    properties = set(itertools.chain.from_iterable(s.items()
                     for s in styles.values()))
    rules = {f"g{i}": p for i, p in enumerate(sorted(properties))}
    mapping = {node_id: [n for n, p in rules.items() if p in style.items()]
               for node_id, style in styles.items()}
    return CompiledCSS(nodes, rules, mapping)
