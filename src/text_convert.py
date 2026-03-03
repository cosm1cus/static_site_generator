import re

from textonde import TextNode, TextType

def text_to_textnodes(text):
    splited_nodes = [TextNode(text, TextType.TEXT)]
    splited_nodes = split_nodes_delimiter(splited_nodes, "**", TextType.BOLD)
    splited_nodes = split_nodes_delimiter(splited_nodes, "_", TextType.ITALIC)
    splited_nodes = split_nodes_delimiter(splited_nodes, "`", TextType.CODE)
    splited_nodes = split_nodes_image(splited_nodes)
    splited_nodes = split_nodes_link(splited_nodes)
    return splited_nodes

def split_nodes_delimiter(old_nodes, delimeter, text_type):
    splited_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            splited_nodes.append(node)
            continue
        raw_lines = node.text.split(delimeter)
        if len(raw_lines) % 2 == 0:
            raise Exception(f"Invalid markdown syntax: {delimeter} not found in line")
        for i, l in enumerate(raw_lines):
            if len(l) < 1:
                continue
            elif i % 2 == 0:
                splited_nodes.append(TextNode(l, TextType.TEXT))
            else:
                splited_nodes.append(TextNode(l, text_type))
    return splited_nodes

def split_nodes_image(old_nodes):
    splited_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            splited_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            splited_nodes.append(node)
            continue
        text = node.text
        for image in images:
            image_alt = image[0]
            image_link = image[1]
            sections = text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections[0]) > 0:
                splited_nodes.append(TextNode(sections[0], TextType.TEXT))
                splited_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                text = sections[1]
            else:
                splited_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                text = sections[1]
        if len(text) > 0:
            splited_nodes.append(TextNode(text, TextType.TEXT))
    return splited_nodes

def split_nodes_link(old_nodes):
    splited_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            splited_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            splited_nodes.append(node)
            continue
        text = node.text
        for link in links:
            link_anc = link[0]
            url = link[1]
            sections = text.split(f"[{link_anc}]({url})", 1)
            if len(sections[0]) > 0:
                splited_nodes.append(TextNode(sections[0], TextType.TEXT))
                splited_nodes.append(TextNode(link_anc, TextType.LINK, url))
                text = sections[1]
            else:
                splited_nodes.append(TextNode(link_anc, TextType.LINK, url))
                text = sections[1]
        if len(text) > 0:
            splited_nodes.append(TextNode(text, TextType.TEXT))
    return splited_nodes

def extract_markdown_images(text):
   extracted_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
   return extracted_images

def extract_markdown_links(text):
   extracted_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
   return extracted_links