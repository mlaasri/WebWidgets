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

import pytest
from typing import Any, Dict, List
from webwidgets.compilation.html.html_node import HTMLNode
from webwidgets.compilation.html.html_tags import TextNode
from webwidgets.compilation.css.css import compile_css, CSSRule, CompiledCSS, \
    apply_css, default_rule_namer


class TestCompileCSS:
    @staticmethod
    def _serialize_rules(rules: List[CSSRule]) -> List[Dict[str, Any]]:
        """Utility function to convert a list of :py:class:`CSSRule` objects
        into a dictionary that can be used in testing.

        :param rules: List of :py:class:`CSSRule` objects.
        :type rules: List[CSSRule]
        :return: List of the member variables of each :py:class:`CSSRule`.
        :rtype: Dict[int, Any]
        """
        return [vars(rule) for rule in rules]

    @staticmethod
    def _serialize_mapping(mapping: Dict[int, List[CSSRule]]) -> Dict[int, List[str]]:
        """Utility function to convert a :py:attr:`CompiledCSS.mapping` object
        into a dictionary that can be used in testing.

        :param mapping: :py:attr:`CompiledCSS.mapping` object.
        :type mapping: Dict[int, List[CSSRule]]
        :return: Dictionary mapping each node ID to the name of the rules that
            achieve the same style.
        """
        return {i: [r.name for r in rules] for i, rules in mapping.items()}

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
        expected_rules = [
            {"name": "r0", "declarations": {"a": "5"}},
            {"name": "r1", "declarations": {"b": "4"}}
        ]
        expected_mapping = {
            id(tree): ['r0', 'r1'],
            id(tree.children[0]): ['r0']
        }

        # Compile tree as single node object
        compiled_css = compile_css(tree)

        # Check results of compilation
        assert compiled_css.trees == [tree]
        assert [id(t) for t in compiled_css.trees] == [id(tree)]
        assert TestCompileCSS._serialize_rules(
            compiled_css.rules) == expected_rules
        assert TestCompileCSS._serialize_mapping(
            compiled_css.mapping) == expected_mapping

        # Compile tree as list of one node
        compiled_css2 = compile_css([tree])

        # Check results of compilation again (should be unchanged)
        assert compiled_css2.trees == [tree]
        assert [id(t) for t in compiled_css2.trees] == [id(tree)]
        assert TestCompileCSS._serialize_rules(
            compiled_css2.rules) == expected_rules
        assert TestCompileCSS._serialize_mapping(
            compiled_css2.mapping) == expected_mapping

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
        expected_rules = [
            {"name": "r0", "declarations": {"color": "blue"}},
            {"name": "r1", "declarations": {"margin": "0"}},
            {"name": "r2", "declarations": {"padding": "0"}}
        ]
        assert TestCompileCSS._serialize_rules(
            compiled_css.rules) == expected_rules

        # Check that the mapping is correctly generated
        expected_mapping = {id(node1): ['r1', 'r2'], id(
            node2): ['r0', 'r1'], id(node3): ['r1', 'r2']}
        assert TestCompileCSS._serialize_mapping(
            compiled_css.mapping) == expected_mapping

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
        expected_rules = [
            {"name": "r0", "declarations": {"color": "blue"}},
            {"name": "r1", "declarations": {"margin": "0"}},
            {"name": "r2", "declarations": {"margin": "5"}},
            {"name": "r3", "declarations": {"padding": "0"}}
        ]
        assert TestCompileCSS._serialize_rules(
            compiled_css.rules) == expected_rules

        # Check that the mapping is correctly generated
        expected_mapping = {
            id(tree): ['r1', 'r3'],
            id(tree.children[0]): ['r0', 'r2'],
            id(tree.children[1]): ['r0', 'r3'],
            id(tree.children[0].children[0]): [],
            id(tree.children[1].children[0]): []
        }
        assert TestCompileCSS._serialize_mapping(
            compiled_css.mapping) == expected_mapping

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
        expected_rules = [
            {"name": "r0", "declarations": {"color": "red"}},
            {"name": "r1", "declarations": {"margin": "10"}},
            {"name": "r2", "declarations": {"margin": "5"}},
            {"name": "r3", "declarations": {"padding": "0"}}
        ]
        assert TestCompileCSS._serialize_rules(
            compiled_css.rules) == expected_rules

        # Check that the mapping is correctly generated
        expected_mapping = {
            id(tree1): ['r1', 'r3'],
            id(tree1.children[0]): ['r0'],
            id(tree2): ['r2', 'r3'],
            id(tree2.children[0]): ['r1']
        }
        assert TestCompileCSS._serialize_mapping(
            compiled_css.mapping) == expected_mapping

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
        expected_rules = [
            {"name": "r0", "declarations": {"a": "10"}},
            {"name": "r1", "declarations": {"a": "5"}},
            {"name": "r2", "declarations": {"b": "10"}},
            {"name": "r3", "declarations": {"b": "4"}},
            {"name": "r4", "declarations": {"c": "5"}},
        ]
        assert TestCompileCSS._serialize_rules(
            compiled_css.rules) == expected_rules

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
        expected_rules = [
            {"name": "r0", "declarations": {"a": "5"}},
            {"name": "r1", "declarations": {"b": "10"}},
            {"name": "r2", "declarations": {"b": "4"}}
        ]
        expected_mapping = {
            id(tree): ['r0', 'r2'],
            id(tree.children[0]): ['r0'],
            id(tree.children[1]): ['r1']
        }
        compiled_css = compile_css([tree])
        assert compiled_css.trees == [tree]
        assert [id(t) for t in compiled_css.trees] == [id(tree)]
        assert TestCompileCSS._serialize_rules(
            compiled_css.rules) == expected_rules
        assert TestCompileCSS._serialize_mapping(
            compiled_css.mapping) == expected_mapping

        # Compiling the tree and one of its children, which should already be
        # included recursively from the tree itself and should not affect the
        # result
        compiled_css2 = compile_css([tree, tree.children[0]])
        assert compiled_css2.trees == [tree, tree.children[0]]
        assert [id(t) for t in compiled_css2.trees] == [
            id(tree), id(tree.children[0])]
        assert TestCompileCSS._serialize_rules(
            compiled_css2.rules) == expected_rules
        assert TestCompileCSS._serialize_mapping(
            compiled_css2.mapping) == expected_mapping

    @pytest.mark.parametrize("rule_namer, names", [
        (lambda _, i: f"rule{i}", ["rule0", "rule1", "rule2"]),
        (lambda _, i: f"rule-{i + 1}", ["rule-1", "rule-2", "rule-3"]),
        (lambda r, i: f"{list(r[i].declarations.items())[0][0]}{i}", [
            "az0", "bz1", "bz2"]),
        (lambda r, i: f"{list(r[i].declarations.items())[0][0][0]}{i}", [
            "a0", "b1", "b2"]),
        (lambda r, i: f"r{list(r[i].declarations.items())[0][1]}-{i}", [
            "r10-1", "r4-2", "r5-0"]),
    ])
    def test_custom_rule_names(self, rule_namer, names):
        tree = HTMLNode(
            style={"az": "5", "bz": "4"},
            children=[
                HTMLNode(style={"az": "5"}),
                HTMLNode(style={"bz": "10"}),
            ]
        )
        compiled_css = compile_css(tree, rule_namer=rule_namer)
        assert [r.name for r in compiled_css.rules] == names


class TestCompiledCSS:
    def test_export_custom_compiled_css(self):
        rules = [
            CSSRule(name="r0", declarations={"margin": "0", "padding": "0"}),
            CSSRule(name="r1", declarations={"color": "blue"}),
            CSSRule(name="r2", declarations={
                    "background-color": "white", "font-size": "16px"})
        ]
        compiled_css = CompiledCSS(trees=None,
                                   rules=rules,
                                   mapping=None)
        expected_css = '\n'.join([
            ".r0 {",
            "    margin: 0;",
            "    padding: 0;",
            "}",
            "",
            ".r1 {",
            "    color: blue;",
            "}",
            "",
            ".r2 {",
            "    background-color: white;",
            "    font-size: 16px;",
            "}"
        ])
        assert compiled_css.to_css() == expected_css

    def test_export_real_compiled_css(self):
        tree = HTMLNode(
            style={"margin": "0", "padding": "0"},
            children=[
                TextNode("a", style={"margin": "0", "color": "blue"}),
                HTMLNode(style={"margin": "0", "color": "green"})
            ]
        )
        compiled_css = compile_css(tree)
        expected_css = '\n'.join([
            ".r0 {",
            "    color: blue;",
            "}",
            "",
            ".r1 {",
            "    color: green;",
            "}",
            "",
            ".r2 {",
            "    margin: 0;",
            "}",
            "",
            ".r3 {",
            "    padding: 0;",
            "}"
        ])
        assert compiled_css.to_css() == expected_css

    def test_export_empty_style(self):
        node = HTMLNode()
        css = compile_css(node).to_css()
        assert css == ""
        other_css = CompiledCSS(trees=None,
                                rules={},
                                mapping=None).to_css()
        assert other_css == ""

    def test_export_invalid_style(self):
        node = HTMLNode(style={"marg!in": "0", "padding": "0"})
        compiled_css = compile_css(node)
        with pytest.raises(ValueError, match="marg!in"):
            compiled_css.to_css()

    @pytest.mark.parametrize("indent_size", [0, 2, 4, 8])
    def test_css_indentation(self, indent_size):
        node = HTMLNode(style={"a": "0", "b": "1"})
        expected_css = '\n'.join([
            ".r0 {",
            f"{' ' * indent_size}a: 0;",
            "}",
            "",
            ".r1 {",
            f"{' ' * indent_size}b: 1;",
            "}"
        ])
        css = compile_css(node).to_css(indent_size=indent_size)
        assert css == expected_css


class TestApplyCSS:
    @pytest.mark.parametrize("class_in, class_out", [
        (None, "r0 r1"),  # No class attribute
        ("", "r0 r1"),  # Empty class
        ("z", "z r0 r1"),  # Existing class
        ("r1", "r1 r0"),  # Existing rule
        ("z r1", "z r1 r0"),  # Existing class and rule
        ("r1 z", "r1 z r0")  # Existing rule and class
    ])
    def test_apply_css_to_node(self, class_in, class_out):
        tree = HTMLNode(attributes=None if class_in is None else {"class": class_in},
                        style={"a": "0", "b": "1"})
        apply_css(compile_css(tree), tree)
        assert tree.attributes["class"] == class_out
        assert tree.to_html() == f'<htmlnode class="{class_out}"></htmlnode>'

    @pytest.mark.parametrize("cl1_in, cl1_out", [
        (None, "r2 r3"),  # No class attribute
        ("", "r2 r3"),  # Empty class
        ("c", "c r2 r3"),  # Existing class
        ("r3", "r3 r2"),  # Existing rule
        ("c r3", "c r3 r2"),  # Existing class and rule
        ("r3 c", "r3 c r2"),  # Existing rule and class
        ("rr3", "rr3 r2 r3")  # Rule decoy
    ])
    @pytest.mark.parametrize("cl2_in, cl2_out", [
        (None, "r1 r2"),  # No class attribute
        ("", "r1 r2"),  # Empty class
        ("z", "z r1 r2"),  # Existing class
        ("r1", "r1 r2"),  # Existing rule
        ("z r1", "z r1 r2"),  # Existing class and rule
        ("r1 z", "r1 z r2"),  # Existing rule and class
        ("rr1", "rr1 r1 r2")  # Rule decoy
    ])
    @pytest.mark.parametrize("mix", [False, True])
    def test_apply_css_to_tree(self, cl1_in, cl1_out, cl2_in, cl2_out, mix):
        # Creating a tree with some nodes and styles
        tree = HTMLNode(
            attributes=None if cl1_in is None else {"class": cl1_in},
            style={"margin": "0", "padding": "0"},
            children=[
                TextNode("a", style={"margin": "0", "color": "blue"}) if mix
                else HTMLNode(style={"margin": "0", "color": "blue"}),
                HTMLNode(attributes=None if cl2_in is None else {"class": cl2_in},
                         style={"margin": "0", "color": "green"})
            ]
        )

        # Compiling and applying CSS to the tree
        compiled_css = compile_css(tree)
        assert TestCompileCSS._serialize_rules(compiled_css.rules) == [
            {"name": "r0", "declarations": {"color": "blue"}},
            {"name": "r1", "declarations": {"color": "green"}},
            {"name": "r2", "declarations": {"margin": "0"}},
            {"name": "r3", "declarations": {"padding": "0"}}
        ]
        apply_css(compiled_css, tree)

        # Checking the tree's new classes
        assert tree.attributes["class"] == cl1_out
        assert tree.children[0].attributes["class"] == "r0 r2"
        assert tree.children[1].attributes["class"] == cl2_out

        # Checking the final HTML code
        mix_node = '<textnode class="r0 r2">a</textnode>' if mix else \
            '<htmlnode class="r0 r2"></htmlnode>'
        expected_html = '\n'.join([
            f'<htmlnode class="{cl1_out}">',
            f'    {mix_node}',
            f'    <htmlnode class="{cl2_out}"></htmlnode>',
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
        assert compiled_css.rules == []
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

    @pytest.mark.parametrize("class_in, class_out", [
        (None, "r0 r1"),
        ("", "r0 r1"),
        ("z", "z r0 r1"),
        ("r0", "r0 r1"),
        ("r1", "r1 r0"),
    ])
    def test_apply_css_multiple_times(self, class_in, class_out):
        tree = HTMLNode(style={"a": "0", "b": "1"}) if class_in is None else \
            HTMLNode(attributes={"class": class_in},
                     style={"a": "0", "b": "1"})
        html_before = '<htmlnode></htmlnode>' if class_in is None else \
            f'<htmlnode class="{class_in}"></htmlnode>'
        html_after = f'<htmlnode class="{class_out}"></htmlnode>'

        assert tree.to_html() == html_before
        compiled_css = compile_css(tree)
        apply_css(compiled_css, tree)
        assert tree.attributes["class"] == class_out
        assert tree.to_html() == html_after
        apply_css(compiled_css, tree)
        assert tree.attributes["class"] == class_out
        assert tree.to_html() == html_after

    def test_empty_style(self):
        """Tests that no classes are added if style exists but is empty."""
        tree = HTMLNode(style={})
        assert tree.to_html() == '<htmlnode></htmlnode>'
        compiled_css = compile_css(tree)
        apply_css(compiled_css, tree)
        assert "class" not in tree.attributes
        assert tree.to_html() == '<htmlnode></htmlnode>'


class TestDefaultRuleNamer:
    def test_default_rule_namer(self):
        rules = [CSSRule(None, {"color": "red"}),
                 CSSRule(None, {"margin": "0"})]
        for i, rule in enumerate(rules):
            rule.name = default_rule_namer(rules=rules, index=i)
        assert rules[0].name == "r0"
        assert rules[1].name == "r1"

    def test_default_rule_namer_override(self):
        rules = [CSSRule("first", {"color": "red"}),
                 CSSRule("second", {"margin": "0"})]
        assert rules[0].name == "first"
        assert rules[1].name == "second"
        for i, rule in enumerate(rules):
            rule.name = default_rule_namer(rules=rules, index=i)
        assert rules[0].name == "r0"
        assert rules[1].name == "r1"
