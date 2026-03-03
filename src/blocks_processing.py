from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = []
    raw_blocks = markdown.split("\n\n")
    for b in raw_blocks:
        if b == "":
            continue
        blocks.append(b.strip())
    return blocks

def block_to_block_type(block):
    if (block.startswith("# ") or block.startswith("## ") or
    block.startswith("### ") or block.startswith("#### ") or
    block.startswith("##### ") or block.startswith("###### ")):
        return BlockType.HEADING

    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    elif block.startswith(">"):
        lines = block.split("\n")
        check = all(l.startswith(">") for l in lines)
        if check:
            return BlockType.QUOTE
        return BlockType.PARAGRAPH

    elif block.startswith("- "):
        lines = block.split("\n")
        check = all(l.startswith("- ") for l in lines)
        if check:
            return BlockType.UNORDERED_LIST
        return BlockType.PARAGRAPH

    elif block.startswith("1. "):
        lines = block.split("\n")
        valid = False
        i = 1
        for l in lines:
            if l.startswith(f"{i}. "):
                valid = True
                i += 1
            else:
                return BlockType.PARAGRAPH
        if valid == True:
            return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Title doesn't exist")