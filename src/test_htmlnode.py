import unittest

from htmlnode import HTMLNode, LeafNode

test_dict = {"href": "https://www.google.com", "target": "blank"}
test_list = ['One', 'Two', 'Three']

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("my_tag", "my_value", test_list, test_dict)
        node2 = HTMLNode("my_tag", "my_value", test_list, test_dict)
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("my_tag", "my_value", test_list, test_dict)
        node.props_to_html()
    
    def test_html_repr(self):
        node = HTMLNode("my_tag", "my_value", test_list, test_dict)
        node.__repr__()
    
    def test_to_html_no_children(self):
        node = LeafNode("p", "Blast")
        self.assertEqual(node.to_html(), "<p>Blast</p>")

if __name__ == "__main__":
    unittest.main()