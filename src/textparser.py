import re
from htmlnode import HTMLNode
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_node = []
    for node in old_nodes: 
        if node.text_type != TextType.TEXT:
            new_node.append(TextNode(node.text, node.text_type, node.url))
            continue

        node_text = node.text
        first_delimiter = node_text.find(delimiter)    
        if first_delimiter == -1:
            new_node.append(node)
            continue 
        
        second_delimiter = node_text.find(delimiter, first_delimiter + len(delimiter))
        if second_delimiter == -1:
            new_node.append(node)
            continue 
        first_string = node_text[:first_delimiter]
        second_string = node_text[first_delimiter: second_delimiter].replace(delimiter, "")
        third_string = node_text[second_delimiter:].replace(delimiter, "")

        new_node.append(TextNode(first_string, TextType.TEXT))
        new_node.append(TextNode(second_string, text_type))
        new_node.append(TextNode(third_string, TextType.TEXT))

        #print(node)
    return new_node


def extract_markdown_images(text):
    parts = re.split(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    delimiters = parts[::3]  # Every third element starting at 0
    matches = []
    # Start at index 1, grab pairs of elements (alt_text, url)
    for i in range(1, len(parts)-1, 3):
        alt_text = parts[i]
        url = parts[i+1]
        matches.append((alt_text, url))
    return matches, delimiters
            

def split_nodes_image(old_nodes):
    new_node = []
    for node in old_nodes:
        if node.text_type != TextType.IMAGE: 
            new_node.append(TextNode(node.text, TextType.TEXT))
        else:
            image_text = extract_markdown_images(node.text)
            for item in image_text:
                new_node.append(TextNode(item[0][0], TextType.IMAGE, item[0][1]))
    return new_node



def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)



def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.LINK:
            print(f"Validating link node: text='{node.text}', url='{node.url}'")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        text = node.text
        pattern = r'\[(.*?)\]\((.*?)\)'
        
        # First, check if there are any matches
        if not re.search(pattern, text):
            new_nodes.append(node)
            continue
        
        current_position = 0
        for match in re.finditer(pattern, text):
            # Add text before the match
            if match.start() > current_position:
                pre_text = text[current_position:match.start()]
                new_nodes.append(TextNode(pre_text, TextType.TEXT))
        
            # Add the link
            link_text = match.group(1)
            url = match.group(2)
            #print(f"Created link node: text='{link_text}', url='{url}'")
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            
            current_position = match.end()

        # Don't forget text after last match
        if current_position < len(text):
            remaining_text = text[current_position:]
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = []
    matches, delimiters = extract_markdown_images(text)
    for i in range(len(matches)):
        nodes.append(TextNode(delimiters[i], TextType.TEXT))
        nodes.append(TextNode(matches[i][0], TextType.IMAGE, matches[i][1]))
    nodes.append(TextNode(delimiters[-1], TextType.TEXT))
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, ">", TextType.QUOTE)

    return nodes


def markdown_to_blocks(markdown):
    
    text = markdown.split("\n\n")
    return_list = [line.strip() for line in text if line.strip() != ""]

    return return_list  


def block_to_block_type(text):
    text = text.splitlines() 

    if re.match(r"^#+\ ", text[0]):
        return "heading"   
    elif text[0] == "```" and text[-1] == "```":
            return "code"    
    elif all(line.startswith('>') for line in text):
        return "quote"
    elif all(line.startswith('* ')for line in text) or all(line.startswith('- ') for line in text):
        return "unordered_list"
    elif all(re.match(r"\d+\.\s", line) for line in text):
        return "ordered_list"
      
    return "paragraph"


def markdown_to_html_node(markdown):
    new_nodes = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks: 
        #url_matches = re.findall(r"\[([^\][]+)\]\((https?:\/\/[^\s)]+)\)", block)
        #for match in url_matches:
            #print(f"Match: [{match[0]}]({match[1]})")
        block_data = block_to_block_type(block)
        match block_data:
            case "heading":
                hash_count = 0
                while hash_count < len(block) and block[hash_count] == '#':
                    hash_count += 1
                heading_content = block[hash_count:].strip()
                processed_nodes = text_to_textnodes(heading_content)
                heading_tag = f"h{hash_count}"
                heading_block = HTMLNode(heading_tag, None, processed_nodes)
                new_nodes.append(heading_block)  
            case "code":
                processed_nodes = text_to_textnodes(block)
                code_block = HTMLNode("code", processed_nodes)
                pre_block = HTMLNode("pre", None, [code_block])
                new_nodes.append(pre_block)
            case "quote":
                cleaned_block = "\n".join(line.lstrip('> ') for line in block.splitlines())
                processed_nodes = text_to_textnodes(cleaned_block)
                quote_block = HTMLNode("blockquote", processed_nodes)
                new_nodes.append(quote_block)
            case "unordered_list":
                list_items = block.splitlines()
                li_block = []
                for item in list_items:
                    item = item.strip()
                    if item.startswith(("* ", "- ")):
                        # Process the content after the * or -
                        processed_content = text_to_textnodes(item[2:].strip())
                        li_node = HTMLNode('li', processed_content)
                        li_block.append(li_node)
                    elif item and not item.startswith(('*', "-")):
                        processed_content = text_to_textnodes(item)
                        temp_node = HTMLNode("p", processed_content)
                        li_block.append(temp_node)
                ul_block = HTMLNode("ul", None, li_block)
                new_nodes.append(ul_block)
            case "ordered_list":
                list_items = block.splitlines()
                li_block = []
                for item in list_items:
                    item = item.strip()
                    if re.match(r"\d+\.\s", item):
                        content_start_index = re.match(r"\d+\.\s", item).end()
                        # Process the content after the number
                        processed_content = text_to_textnodes(item[content_start_index:].strip())
                        li_node = HTMLNode('li', processed_content)
                        li_block.append(li_node)
                    elif item and not re.match(r"\d+\.\s", item):
                        processed_content = text_to_textnodes(item)
                        temp_node = HTMLNode("p", processed_content)
                        li_block.append(temp_node)
                ol_block = HTMLNode("ol", None, li_block)
                new_nodes.append(ol_block)
            case _:
                processed_nodes = text_to_textnodes(block)
                #for node in processed_nodes:
                    #print(f"!!! {node.url}")
                paragraph_node = HTMLNode("p", processed_nodes)
                new_nodes.append(paragraph_node)

    html_node = HTMLNode("div", new_nodes)
    return html_node


def extract_title(markdown):
    markdown_data = markdown.split('\n')
    for data in markdown_data:
        if re.match(r"^#\ ", data):
            title = data.replace("#", "")
            return title.strip()
    
    raise ValueError("No title found in file")

