import pytest
from webwidgets.compilation.html.html_node import HTMLNode, no_start_tag, no_end_tag, RawText


class TestHTMLNode:
    class CustomNode(HTMLNode):
        pass

    @no_start_tag
    class NoStartNode(HTMLNode):
        pass

    @no_end_tag
    class NoEndNode(HTMLNode):
        pass

    @no_start_tag
    @no_end_tag
    class NoStartEndNode(HTMLNode):
        pass

    class OneLineNode(HTMLNode):
        one_line = True

    class OneLineNoStartNode(NoStartNode):
        one_line = True

    def test_basic_node(self):
        node = HTMLNode()
        assert node.start_tag == "<htmlnode>"
        assert node.end_tag == "</htmlnode>"
        assert node.to_html() == "<htmlnode></htmlnode>"

    def test_custom_name(self):
        node = TestHTMLNode.CustomNode()
        assert node.start_tag == "<customnode>"
        assert node.end_tag == "</customnode>"
        assert node.to_html() == "<customnode></customnode>"

    def test_attributes(self):
        node = HTMLNode(attributes={'id': 'test-id', 'class': 'test-class'})
        assert node.start_tag == '<htmlnode id="test-id" class="test-class">'
        assert node.end_tag == '</htmlnode>'
        assert node.to_html() == '<htmlnode id="test-id" class="test-class"></htmlnode>'

    def test_no_start_tag(self):
        node = TestHTMLNode.NoStartNode()
        assert node.start_tag == ''
        assert node.end_tag == '</nostartnode>'
        assert node.to_html() == "</nostartnode>"

    def test_no_end_tag(self):
        node = TestHTMLNode.NoEndNode()
        assert node.start_tag == '<noendnode>'
        assert node.end_tag == ''
        assert node.to_html() == "<noendnode>"

    def test_no_start_end_tag(self):
        node = TestHTMLNode.NoStartEndNode()
        assert node.start_tag == ''
        assert node.end_tag == ''
        assert node.to_html() == ""

    def test_one_line_rendering(self):
        node = HTMLNode(children=[RawText('child1'),
                        RawText('child2')])
        expected_html = "<htmlnode>child1child2</htmlnode>"
        assert node.to_html(force_one_line=True) == expected_html

    def test_no_start_tag_with_one_line(self):
        node = TestHTMLNode.NoStartNode(children=[RawText('child1'),
                                                  RawText('child2')])
        expected_html = "child1child2</nostartnode>"
        assert node.to_html(force_one_line=True) == expected_html

    def test_no_end_tag_with_one_line(self):
        node = TestHTMLNode.NoEndNode(children=[RawText('child1'),
                                                RawText('child2')])
        expected_html = "<noendnode>child1child2"
        assert node.to_html(force_one_line=True) == expected_html

    def test_recursive_rendering(self):
        inner_node = HTMLNode(children=[RawText('inner_child')])
        node = TestHTMLNode.CustomNode(children=[inner_node])
        expected_html = '\n'.join([
            "<customnode>",
            "    <htmlnode>",
            "        inner_child",
            "    </htmlnode>",
            "</customnode>"
        ])
        assert node.to_html() == expected_html
        assert node.to_html(force_one_line=False) == expected_html

    def test_no_start_tag_with_recursive_rendering(self):
        inner_node = HTMLNode(children=[RawText('inner_child')])
        node = TestHTMLNode.NoStartNode(children=[inner_node])
        expected_html = '\n'.join([
            "    <htmlnode>",
            "        inner_child",
            "    </htmlnode>",
            "</nostartnode>"
        ])
        assert node.to_html() == expected_html

    def test_no_end_tag_with_recursive_rendering(self):
        inner_node = HTMLNode(children=[RawText('inner_child')])
        node = TestHTMLNode.NoEndNode(children=[inner_node])
        expected_html = '\n'.join([
            "<noendnode>",
            "    <htmlnode>",
            "        inner_child",
            "    </htmlnode>"
        ])
        assert node.to_html() == expected_html

    def test_recursive_rendering_one_line(self):
        inner_node = HTMLNode(children=[RawText('inner_child')])
        node = TestHTMLNode.CustomNode(children=[inner_node])
        expected_html = "<customnode><htmlnode>inner_child</htmlnode></customnode>"
        assert node.to_html(force_one_line=True) == expected_html

    def test_recursive_rendering_one_line_propagation(self):
        one_line = TestHTMLNode.OneLineNode(
            [HTMLNode(children=[RawText('inner_child')])]
        )
        node = HTMLNode(children=[one_line])
        expected_html = '\n'.join([
            "<htmlnode>",
            "    <onelinenode><htmlnode>inner_child</htmlnode></onelinenode>",
            "</htmlnode>"
        ])
        assert node.to_html() == expected_html

    def test_recursive_rendering_of_tagless_mix(self):
        children = [
            TestHTMLNode.NoEndNode([RawText("child1")]),
            TestHTMLNode.NoStartNode([RawText("child2")]),
            TestHTMLNode.NoEndNode([RawText("child3")]),
        ]
        inner_node = TestHTMLNode.NoStartNode(children=children)
        node = TestHTMLNode.NoEndNode(children=[inner_node])
        expected_html = '\n'.join([
            "<noendnode>",
            "        <noendnode>",
            "            child1",
            "            child2",
            "        </nostartnode>",
            "        <noendnode>",
            "            child3",
            "    </nostartnode>"
        ])
        assert node.to_html() == expected_html

    def test_recursive_rendering_of_tagless_mix_one_line(self):
        children = [
            TestHTMLNode.NoEndNode([RawText("child1")]),
            TestHTMLNode.OneLineNoStartNode([RawText("child2")]),
            TestHTMLNode.NoEndNode([RawText("child3")]),
        ]
        inner_node = TestHTMLNode.NoStartNode(children=children)
        node = TestHTMLNode.NoEndNode(children=[inner_node])
        expected_html = '\n'.join([
            "<noendnode>",
            "        <noendnode>",
            "            child1",
            "        child2</onelinenostartnode>",
            "        <noendnode>",
            "            child3",
            "    </nostartnode>"
        ])
        assert node.to_html() == expected_html

    def test_recursive_rendering_of_tagless_mix_force_one_line(self):
        children = [
            TestHTMLNode.NoEndNode([RawText("child1")]),
            TestHTMLNode.NoStartNode([RawText("child2")]),
            TestHTMLNode.NoEndNode([RawText("child3")]),
        ]
        inner_node = TestHTMLNode.NoStartNode(children=children)
        node = TestHTMLNode.NoEndNode(children=[inner_node])
        expected_html = "<noendnode><noendnode>child1child2</nostartnode>" + \
            "<noendnode>child3</nostartnode>"
        assert node.to_html(force_one_line=True) == expected_html

    def test_raw_text_as_orphan_node(self):
        node = HTMLNode(children=[
            TestHTMLNode.CustomNode(),
            RawText("raw_text")
        ])
        expected_html = '\n'.join([
            "<htmlnode>",
            "    <customnode></customnode>",
            "    raw_text",
            "</htmlnode>"
        ])
        assert node.to_html() == expected_html

    @pytest.mark.parametrize("indent_level", [0, 1, 2])
    @pytest.mark.parametrize("indent_size", [3, 4, 8])
    def test_indentation(self, indent_level: int, indent_size: int):
        """Test the to_html method with different indentation parameters."""

        # Creating a simple HTMLNode
        node = HTMLNode(children=[
            RawText('child1'),
            RawText('child2'),
            HTMLNode(children=[
                RawText('grandchild1'),
                RawText('grandchild2')
            ])
        ])

        # Expected output based on the test parameters
        expected_html = "\n".join([
            f"{' ' * indent_size * indent_level}<htmlnode>",
            f"{' ' * indent_size * (indent_level + 1)}child1",
            f"{' ' * indent_size * (indent_level + 1)}child2",
            f"{' ' * indent_size * (indent_level + 1)}<htmlnode>",
            f"{' ' * indent_size * (indent_level + 2)}grandchild1",
            f"{' ' * indent_size * (indent_level + 2)}grandchild2",
            f"{' ' * indent_size * (indent_level + 1)}</htmlnode>",
            f"{' ' * indent_size * indent_level}</htmlnode>"
        ])

        # Calling to_html with the test parameters
        actual_html = node.to_html(
            indent_level=indent_level, indent_size=indent_size)
        assert actual_html == expected_html

    @pytest.mark.parametrize("indent_level", [0, 1, 2])
    @pytest.mark.parametrize("indent_size", [3, 4, 8])
    def test_indentation_empty_node(self, indent_level, indent_size):
        node = HTMLNode()
        expected_html = f"{' ' * indent_size * indent_level}<htmlnode></htmlnode>"
        actual_html = node.to_html(
            indent_level=indent_level, indent_size=indent_size)
        assert actual_html == expected_html
