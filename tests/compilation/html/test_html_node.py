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
