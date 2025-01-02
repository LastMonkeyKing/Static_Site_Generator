from textnode import TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag or 'div'  # Default to 'div' if tag is None
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    '''
    def __repr__(self):
        try:
            # Log the flow to verify execution hasn't accidentally diverted
            print("Entering __repr__")
            if self.children:
                children_summary = [child.tag for child in self.children]
            else:
                children_summary = "No children"

            result = f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Children: {children_summary})"
        except Exception as e:
            print(f"Exception caught in __repr__: {e}")
            result = "Error in __repr__"
        finally:
            print("Exiting __repr__")
            return result  # Ensure this return statement always executes
    '''


    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid Tag: no value")
        if not isinstance(self.children, list):
            raise ValueError("Invalid Child: 'children' should be a list")

        text_string = "<" + self.tag + ">"
        
        if self.value:
            if isinstance(self.value, list):
                # If value is a list of nodes
                for val in self.value:
                    text_string += val.to_html()
            else:
                # If value is a string
                text_string += str(self.value)
                
        for child in self.children:
            #print(f"Processing child: {child}")
            text_string += child.to_html()
        
        text_string += "</" + self.tag + ">"
        
        return text_string

    def text_node_to_html_node(text_node):
        if text_node.type not in TextType:
            raise ValueError("Invalid text type")

        match text_node.type:
            case TextType.TEXT:
                return LeafNode(text=text_node.value)
            case TextType.BOLD:
                return LeafNode(tag="b", text=text_node.value)
            case TextType.ITALIC:
                return LeafNode(tag="i", text=text_node.value)
            case TextType.CODE:
                return LeafNode(tag="code", text=text_node.value)
            case TextType.QUOTE:
                return LeafNode(tag="quote", text=text_node.value)
            case TextType.LINK:
                props = {"href": text_node.props.get("href")}
                return LeafNode(tag="a", text=text_node.value, props=props)
            case TextType.IMAGE:
                props = {
                    "src": text_node.props.get("src", ""),
                    "alt": text_node.props.get("alt", "")
                }
                return LeafNode(tag="img", text="", props=props)

    
    def props_to_html(self):
        if not self.props:
            return ''
        return ' ' + ' '.join(f'{k}="{v}"' for k, v in self.props.items())

    
    def __eq__(self, html_node):
        if not isinstance(html_node, HTMLNode):
            return False
        
        return self.tag == html_node.tag and self.value == html_node.value and self.children == html_node.children and self.props == html_node.props

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(tag, None, children, props=None)