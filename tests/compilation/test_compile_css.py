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

from webwidgets.compilation.html.html_node import HTMLNode
from webwidgets.compilation.html.html_tags import TextNode
from webwidgets.compilation.css.css import compile_css


class TestCompileCSS:
    def test_basic_compilation(self):

        # Create some HTML nodes with different styles
        node1 = HTMLNode(style={"margin": "0", "padding": "0"})
        node2 = HTMLNode(style={"margin": "0", "color": "blue"})
        node3 = HTMLNode(style={"margin": "0", "padding": "0"})

        # Compile the CSS for the trees
        compiled_css = compile_css([node1, node2, node3])

        # Check that the trees are correctly saved in the result
        assert compiled_css.trees == [node1, node2, node3]
        assert [id(t) for t in compiled_css.trees] == [
            id(node1), id(node2), id(node3)]

        # Check that the rules are correctly generated
        expected_rules = {
            'g0': {'color': 'blue'},
            'g1': {'margin': '0'},
            'g2': {'padding': '0'}
        }
        assert compiled_css.rules == expected_rules

        # Check that the mapping is correctly generated
        expected_mapping = {id(node1): ['g1', 'g2'], id(
            node2): ['g0', 'g1'], id(node3): ['g1', 'g2']}
        assert compiled_css.mapping == expected_mapping

    def test_nested_compilation_one_tree(self):

        # Create some nested HTML nodes
        tree = HTMLNode(
            style={"margin": "0", "padding": "0"},
            children=[
                TextNode("Hello World!", style={
                         "margin": "5", "color": "blue"}),
                TextNode("Another text node", style={
                         "padding": "0", "color": "blue"})
            ]
        )

        # Compile the CSS for the tree
        compiled_css = compile_css([tree])

        # Check that the tree is correctly saved
        assert compiled_css.trees == [tree]
        assert [id(t) for t in compiled_css.trees] == [id(tree)]

        # Check that the rules are correctly generated
        expected_rules = {
            'g0': {'color': 'blue'},
            'g1': {'margin': '0'},
            'g2': {'margin': '5'},
            'g3': {'padding': '0'}
        }
        assert compiled_css.rules == expected_rules

        # Check that the mapping is correctly generated
        expected_mapping = {
            id(tree): ['g1', 'g3'],
            id(tree.children[0]): ['g0', 'g2'],
            id(tree.children[1]): ['g0', 'g3'],
            id(tree.children[0].children[0]): [],
            id(tree.children[1].children[0]): []
        }
        assert compiled_css.mapping == expected_mapping

    def test_nested_compilation_two_trees(self):

        # Create 2 trees
        tree1 = HTMLNode(
            style={"margin": "10", "padding": "0"},
            children=[
                HTMLNode(style={"color": "red"})
            ]
        )
        tree2 = HTMLNode(
            style={"margin": "5", "padding": "0"},
            children=[
                HTMLNode(style={"margin": "10"})
            ]
        )

        # Compile the CSS for the trees
        compiled_css = compile_css([tree1, tree2])

        # Check that the tree is correctly saved
        assert compiled_css.trees == [tree1, tree2]
        assert [id(t) for t in compiled_css.trees] == [
            id(tree1), id(tree2)]

        # Check that the rules are correctly generated
        expected_rules = {
            'g0': {'color': 'red'},
            'g1': {'margin': '10'},
            'g2': {'margin': '5'},
            'g3': {'padding': '0'}
        }
        assert compiled_css.rules == expected_rules

        # Check that the mapping is correctly generated
        expected_mapping = {
            id(tree1): ['g1', 'g3'],
            id(tree1.children[0]): ['g0'],
            id(tree2): ['g2', 'g3'],
            id(tree2.children[0]): ['g1']
        }
        assert compiled_css.mapping == expected_mapping
