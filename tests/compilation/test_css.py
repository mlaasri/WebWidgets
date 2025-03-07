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
from webwidgets.compilation.css.css import compile_css, apply_css


class TestCompileCSS:
    def test_argument_type(self):
        """Compares compilation when given a node object versus a list of
        nodes.
        """
        # Create a tree
        tree = HTMLNode(
            style={"a": "5", "b": "4"},
            children=[
                HTMLNode(style={"a": "5"})
            ]
        )

        # Define expected compilation results
        expected_rules = {
            'r0': {'a': '5'},
            'r1': {'b': '4'}
        }
        expected_mapping = {
            id(tree): ['r0', 'r1'],
            id(tree.children[0]): ['r0']
        }

        # Compile tree as single node object
        compiled_css = compile_css(tree)

        # Check results of compilation
        assert compiled_css.trees == [tree]
        assert [id(t) for t in compiled_css.trees] == [id(tree)]
        assert compiled_css.rules == expected_rules
        assert compiled_css.mapping == expected_mapping

        # Compile tree as list of one node
        compiled_css2 = compile_css([tree])

        # Check results of compilation again (should be unchanged)
        assert compiled_css2.trees == [tree]
        assert [id(t) for t in compiled_css2.trees] == [id(tree)]
        assert compiled_css2.rules == expected_rules
        assert compiled_css2.mapping == expected_mapping

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
            'r0': {'color': 'blue'},
            'r1': {'margin': '0'},
            'r2': {'padding': '0'}
        }
        assert compiled_css.rules == expected_rules

        # Check that the mapping is correctly generated
        expected_mapping = {id(node1): ['r1', 'r2'], id(
            node2): ['r0', 'r1'], id(node3): ['r1', 'r2']}
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
        compiled_css = compile_css(tree)

        # Check that the tree is correctly saved
        assert compiled_css.trees == [tree]
        assert [id(t) for t in compiled_css.trees] == [id(tree)]

        # Check that the rules are correctly generated
        expected_rules = {
            'r0': {'color': 'blue'},
            'r1': {'margin': '0'},
            'r2': {'margin': '5'},
            'r3': {'padding': '0'}
        }
        assert compiled_css.rules == expected_rules

        # Check that the mapping is correctly generated
        expected_mapping = {
            id(tree): ['r1', 'r3'],
            id(tree.children[0]): ['r0', 'r2'],
            id(tree.children[1]): ['r0', 'r3'],
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
            'r0': {'color': 'red'},
            'r1': {'margin': '10'},
            'r2': {'margin': '5'},
            'r3': {'padding': '0'}
        }
        assert compiled_css.rules == expected_rules

        # Check that the mapping is correctly generated
        expected_mapping = {
            id(tree1): ['r1', 'r3'],
            id(tree1.children[0]): ['r0'],
            id(tree2): ['r2', 'r3'],
            id(tree2.children[0]): ['r1']
        }
        assert compiled_css.mapping == expected_mapping

    def test_rules_numbered_in_order(self):
        """Test that rules are numbered in lexicographical order"""
        tree = HTMLNode(
            style={"a": "5", "b": "4"},
            children=[
                HTMLNode(style={"a": "10"}),
                HTMLNode(style={"b": "10"}),
                HTMLNode(style={"c": "5"})
            ]
        )
        compiled_css = compile_css(tree)
        expected_rules = {
            'r0': {'a': '10'},
            'r1': {'a': '5'},
            'r2': {'b': '10'},
            'r3': {'b': '4'},
            'r4': {'c': '5'}
        }
        assert compiled_css.rules == expected_rules

    def test_duplicate_node(self):
        """Test that adding the same node twice does not impact compilation"""
        # Compiling a tree
        tree = HTMLNode(
            style={"a": "5", "b": "4"},
            children=[
                HTMLNode(style={"a": "5"}),
                HTMLNode(style={"b": "10"}),
            ]
        )
        expected_rules = {
            'r0': {'a': '5'},
            'r1': {'b': '10'},
            'r2': {'b': '4'}
        }
        expected_mapping = {
            id(tree): ['r0', 'r2'],
            id(tree.children[0]): ['r0'],
            id(tree.children[1]): ['r1']
        }
        compiled_css = compile_css([tree])
        assert compiled_css.trees == [tree]
        assert [id(t) for t in compiled_css.trees] == [id(tree)]
        assert compiled_css.rules == expected_rules
        assert compiled_css.mapping == expected_mapping

        # Compiling the tree and one of its children, which should already be
        # included recursively from the tree itself and should not affect the
        # result
        compiled_css2 = compile_css([tree, tree.children[0]])
        assert compiled_css2.trees == [tree, tree.children[0]]
        assert [id(t) for t in compiled_css2.trees] == [
            id(tree), id(tree.children[0])]
        assert compiled_css2.rules == expected_rules
        assert compiled_css2.mapping == expected_mapping


class TestApplyCSS:
    def test_apply_css_to_node(self):
        tree = HTMLNode(style={"a": "0", "b": "1"})
        apply_css(compile_css(tree), tree)
        assert tree.attributes["class"] == "r0 r1"
        assert tree.to_html() == '<htmlnode class="r0 r1"></htmlnode>'

    def test_apply_css_to_tree(self):
        # Creating a tree with some nodes and styles
        tree = HTMLNode(
            style={"margin": "0", "padding": "0"},
            children=[
                HTMLNode(style={"margin": "0", "color": "blue"}),
                HTMLNode(style={"margin": "0", "color": "green"})
            ]
        )

        # Compiling and applying CSS to the tree
        compiled_css = compile_css(tree)
        assert compiled_css.rules == {
            "r0": {"color": "blue"},
            "r1": {"color": "green"},
            "r2": {"margin": "0"},
            "r3": {"padding": "0"}
        }
        apply_css(compiled_css, tree)

        # Checking the tree's new classes
        assert tree.attributes["class"] == "r2 r3"
        assert tree.children[0].attributes["class"] == "r0 r2"
        assert tree.children[1].attributes["class"] == "r1 r2"

        # Checking the final HTML code
        expected_html = '\n'.join([
            '<htmlnode class="r2 r3">',
            '    <htmlnode class="r0 r2"></htmlnode>',
            '    <htmlnode class="r1 r2"></htmlnode>',
            '</htmlnode>'
        ])
        assert tree.to_html() == expected_html

    def test_apply_css_to_node_with_empty_class(self):
        tree = HTMLNode(attributes={"class": ""},
                        style={"a": "0", "b": "1"})
        apply_css(compile_css(tree), tree)
        assert tree.attributes["class"] == "r0 r1"
        assert tree.to_html() == '<htmlnode class="r0 r1"></htmlnode>'

    def test_apply_css_to_tree_with_empty_class(self):
        # Creating a tree with some nodes and styles
        tree = HTMLNode(
            attributes={"class": ""},
            style={"margin": "0", "padding": "0"},
            children=[
                HTMLNode(style={"margin": "0", "color": "blue"}),
                HTMLNode(attributes={"class": ""},
                         style={"margin": "0", "color": "green"})
            ]
        )

        # Compiling and applying CSS to the tree
        compiled_css = compile_css(tree)
        assert compiled_css.rules == {
            "r0": {"color": "blue"},
            "r1": {"color": "green"},
            "r2": {"margin": "0"},
            "r3": {"padding": "0"}
        }
        apply_css(compiled_css, tree)

        # Checking the tree's new classes
        assert tree.attributes["class"] == "r2 r3"
        assert tree.children[0].attributes["class"] == "r0 r2"
        assert tree.children[1].attributes["class"] == "r1 r2"

        # Checking the final HTML code
        expected_html = '\n'.join([
            '<htmlnode class="r2 r3">',
            '    <htmlnode class="r0 r2"></htmlnode>',
            '    <htmlnode class="r1 r2"></htmlnode>',
            '</htmlnode>'
        ])
        assert tree.to_html() == expected_html

    def test_apply_css_to_node_with_class(self):
        tree = HTMLNode(attributes={"class": "z"},
                        style={"a": "0", "b": "1"})
        apply_css(compile_css(tree), tree)
        assert tree.attributes["class"] == "z r0 r1"
        assert tree.to_html() == '<htmlnode class="z r0 r1"></htmlnode>'

    def test_apply_css_to_tree_with_class(self):
        # Creating a tree with some nodes and styles
        tree = HTMLNode(
            attributes={"class": "c"},
            style={"margin": "0", "padding": "0"},
            children=[
                HTMLNode(style={"margin": "0", "color": "blue"}),
                HTMLNode(attributes={"class": "z"},
                         style={"margin": "0", "color": "green"})
            ]
        )

        # Compiling and applying CSS to the tree
        compiled_css = compile_css(tree)
        assert compiled_css.rules == {
            "r0": {"color": "blue"},
            "r1": {"color": "green"},
            "r2": {"margin": "0"},
            "r3": {"padding": "0"}
        }
        apply_css(compiled_css, tree)

        # Checking the tree's new classes
        assert tree.attributes["class"] == "c r2 r3"
        assert tree.children[0].attributes["class"] == "r0 r2"
        assert tree.children[1].attributes["class"] == "z r1 r2"

        # Checking the final HTML code
        expected_html = '\n'.join([
            '<htmlnode class="c r2 r3">',
            '    <htmlnode class="r0 r2"></htmlnode>',
            '    <htmlnode class="z r1 r2"></htmlnode>',
            '</htmlnode>'
        ])
        assert tree.to_html() == expected_html

    def test_apply_css_to_mixed_tree(self):
        # Creating a tree with some nodes and styles
        tree = HTMLNode(
            style={"margin": "0", "padding": "0"},
            children=[
                TextNode("a", style={"margin": "0", "color": "blue"}),
                HTMLNode(attributes={"class": "z"},
                         style={"margin": "0", "color": "green"})
            ]
        )

        # Compiling and applying CSS to the tree
        compiled_css = compile_css(tree)
        assert compiled_css.rules == {
            "r0": {"color": "blue"},
            "r1": {"color": "green"},
            "r2": {"margin": "0"},
            "r3": {"padding": "0"}
        }
        apply_css(compiled_css, tree)

        # Checking the tree's new classes
        assert tree.attributes["class"] == "r2 r3"
        assert tree.children[0].attributes["class"] == "r0 r2"
        assert tree.children[1].attributes["class"] == "z r1 r2"

        # Checking the final HTML code
        expected_html = '\n'.join([
            '<htmlnode class="r2 r3">',
            '    <textnode class="r0 r2">a</textnode>',
            '    <htmlnode class="z r1 r2"></htmlnode>',
            '</htmlnode>'
        ])
        assert tree.to_html() == expected_html

    def test_apply_css_without_styles(self):
        # Compiling and applying CSS to a tree with no styles
        tree = HTMLNode(
            children=[
                TextNode("a"),
                HTMLNode(attributes={"class": "z"})
            ]
        )
        html_before = tree.to_html()
        compiled_css = compile_css(tree)
        assert compiled_css.rules == {}
        apply_css(compiled_css, tree)
        html_after = tree.to_html()

        # Checking the tree's new classes
        assert "class" not in tree.attributes
        assert "class" not in tree.children[0].attributes
        assert tree.children[1].attributes["class"] == "z"

        # Checking the final HTML code
        expected_html = '\n'.join([
            '<htmlnode>',
            '    <textnode>a</textnode>',
            '    <htmlnode class="z"></htmlnode>',
            '</htmlnode>'
        ])
        assert html_before == expected_html
        assert html_after == expected_html

    def test_apply_css_with_partial_styles(self):
        # Compiling and applying CSS to a tree where some nodes have styles but
        # others do not
        tree = HTMLNode(
            children=[
                TextNode("a", style={"margin": "0", "color": "blue"}),
                HTMLNode(attributes={"class": "z"})
            ]
        )
        compiled_css = compile_css(tree)
        apply_css(compiled_css, tree)

        # Checking the tree's new classes
        assert "class" not in tree.attributes
        assert tree.children[0].attributes["class"] == "r0 r1"
        assert tree.children[1].attributes["class"] == "z"

        # Checking the final HTML code
        expected_html = '\n'.join([
            '<htmlnode>',
            '    <textnode class="r0 r1">a</textnode>',
            '    <htmlnode class="z"></htmlnode>',
            '</htmlnode>'
        ])
        assert tree.to_html() == expected_html

    def test_apply_css_multiple_times(self):
        tree = HTMLNode(style={"a": "0", "b": "1"})
        assert tree.to_html() == '<htmlnode></htmlnode>'
        compiled_css = compile_css(tree)
        apply_css(compiled_css, tree)
        assert tree.attributes["class"] == "r0 r1"
        assert tree.to_html() == '<htmlnode class="r0 r1"></htmlnode>'
        apply_css(compiled_css, tree)
        assert tree.attributes["class"] == "r0 r1"
        assert tree.to_html() == '<htmlnode class="r0 r1"></htmlnode>'

    def test_apply_css_multiple_times_with_empty_class(self):
        tree = HTMLNode(attributes={"class": ""},
                        style={"a": "0", "b": "1"})
        assert tree.to_html() == '<htmlnode class=""></htmlnode>'
        compiled_css = compile_css(tree)
        apply_css(compiled_css, tree)
        assert tree.attributes["class"] == "r0 r1"
        assert tree.to_html() == '<htmlnode class="r0 r1"></htmlnode>'
        apply_css(compiled_css, tree)
        assert tree.attributes["class"] == "r0 r1"
        assert tree.to_html() == '<htmlnode class="r0 r1"></htmlnode>'

    def test_apply_css_multiple_times_with_existing_r0(self):
        tree = HTMLNode(attributes={"class": "r0"},
                        style={"a": "0", "b": "1"})
        assert tree.to_html() == '<htmlnode class="r0"></htmlnode>'
        compiled_css = compile_css(tree)
        apply_css(compiled_css, tree)
        assert tree.attributes["class"] == "r0 r1"
        assert tree.to_html() == '<htmlnode class="r0 r1"></htmlnode>'
        apply_css(compiled_css, tree)
        assert tree.attributes["class"] == "r0 r1"
        assert tree.to_html() == '<htmlnode class="r0 r1"></htmlnode>'

    def test_apply_css_multiple_times_with_existing_r1(self):
        tree = HTMLNode(attributes={"class": "r1"},
                        style={"a": "0", "b": "1"})
        assert tree.to_html() == '<htmlnode class="r1"></htmlnode>'
        compiled_css = compile_css(tree)
        apply_css(compiled_css, tree)
        assert tree.attributes["class"] == "r1 r0"
        assert tree.to_html() == '<htmlnode class="r1 r0"></htmlnode>'
        apply_css(compiled_css, tree)
        assert tree.attributes["class"] == "r1 r0"
        assert tree.to_html() == '<htmlnode class="r1 r0"></htmlnode>'

    def test_apply_css_with_existing_rules(self):
        # Creating a tree with some nodes and styles
        tree = HTMLNode(
            attributes={"class": "r3"},
            style={"margin": "0", "padding": "0"},
            children=[
                TextNode("a", style={"margin": "0", "color": "blue"}),
                HTMLNode(attributes={"class": "r1 z"},
                         style={"margin": "0", "color": "green"})
            ]
        )

        # Compiling and applying CSS to the tree
        compiled_css = compile_css(tree)
        assert compiled_css.rules == {
            "r0": {"color": "blue"},
            "r1": {"color": "green"},
            "r2": {"margin": "0"},
            "r3": {"padding": "0"}
        }
        apply_css(compiled_css, tree)

        # Checking the tree's new classes
        assert tree.attributes["class"] == "r3 r2"
        assert tree.children[0].attributes["class"] == "r0 r2"
        assert tree.children[1].attributes["class"] == "r1 z r2"

        # Checking the final HTML code
        expected_html = '\n'.join([
            '<htmlnode class="r3 r2">',
            '    <textnode class="r0 r2">a</textnode>',
            '    <htmlnode class="r1 z r2"></htmlnode>',
            '</htmlnode>'
        ])
        assert tree.to_html() == expected_html
