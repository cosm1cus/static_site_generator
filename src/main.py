from textonde import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)

    html_node = HTMLNode(
        tag="wow",
        value="value",
        children="123123",
    )
    print(html_node)

    leaf_node = LeafNode("a", "Here's some text", {"href": "www.bootdev.com"})
    print(leaf_node.to_html())

    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    print(parent_node.to_html())

    node = TextNode("This is a text node", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    print(html_node.to_html())
main()