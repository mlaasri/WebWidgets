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
    """Computes optimal CSS rules from the given styled nodes.

    :param nodes: The nodes to optimize over. All children are recursively
        included.
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
