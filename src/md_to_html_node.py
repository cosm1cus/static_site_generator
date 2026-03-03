import os

from blocks_processing import markdown_to_blocks, block_to_block_type, BlockType, extract_title
from htmlnode import ParentNode, LeafNode
from text_convert import *
from textonde import TextNode, text_node_to_html_node

def md_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            clear_block = block.replace("\n", " ").strip()
            html_nodes.append(ParentNode("p", text_to_children(clear_block)))

        elif block_type == BlockType.HEADING:
            i = 0
            while block[i] == "#":
                if block[i] == "#":
                    i += 1
                elif block[i] == "# ":
                    break
            clear_block = block.replace("#" * i + " ", "")
            html_nodes.append(ParentNode(f"h{i}", text_to_children(clear_block)))

        elif block_type == BlockType.CODE:
            clear_block = block.replace("```\n", "").replace("```", "")
            child_node = [text_node_to_html_node(TextNode(clear_block, TextType.CODE))]
            html_nodes.append(ParentNode(f"pre", child_node))

        elif block_type == BlockType.QUOTE:
            lines = block.splitlines()
            clear_lines = [l.replace(">", "").strip() for l in lines if l.startswith(">")]
            clear_block = "\n".join(clear_lines)
            html_nodes.append(ParentNode("blockquote", text_to_children(clear_block)))

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.splitlines()
            clear_lines = [l.replace("-", "").strip() for l in lines if l.startswith("-")]
            unordered_list_nodes = []
            for line in clear_lines:
                unordered_list_nodes.append(ParentNode("li", text_to_children(line)))
            html_nodes.append(ParentNode("ul", unordered_list_nodes))

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.splitlines()
            unordered_list_nodes = []
            for line in lines:
                clear_line = line
                i = 0
                while i < len(line) and line[i].isdigit():
                    i += 1
                clear_line = clear_line[i:]
                if clear_line.startswith(". "):
                    clear_line = clear_line[2:].strip()
                unordered_list_nodes.append(ParentNode("li", text_to_children(clear_line)))
            html_nodes.append(ParentNode("ol", unordered_list_nodes))

    final_html_node = ParentNode("div", html_nodes)
    return final_html_node

def text_to_children(text):
    childrens = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        childrens.append(text_node_to_html_node(node))
    return childrens

def generate_page(from_path, template_path, dest_path, basepath):
    if not os.path.exists(from_path):
        raise Exception("From path doesn't exists")
    if not os.path.exists(template_path):
        raise Exception("Template path doesn't exists")

    print(f"Gathering page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md_contents = f.read()
    with open(template_path, "r") as f:
        template_contents = f.read()

    title = extract_title(md_contents)
    html_nodes = md_to_html_node(md_contents)
    html = html_nodes.to_html()

    complete_html = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", html)
    complete_html_with_paths = complete_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "x") as f:
        f.write(complete_html_with_paths)

def generate_all_htmls(from_path, template_path, dest_path, basepath):
    file_list = os.listdir(from_path)
    for file in file_list:
        if os.path.isfile(os.path.join(from_path, file)) and file == "index.md":
            generate_page(os.path.join(from_path, file), template_path, os.path.join(dest_path, "index.html"), basepath)
        else:
            generate_all_htmls(os.path.join(from_path, file), template_path, os.path.join(dest_path, file), basepath)

