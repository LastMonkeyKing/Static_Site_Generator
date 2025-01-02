from enum import Enum 

class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"    
    CODE = "code"  
    LINK = "link"
    IMAGE = "image"
    QUOTE = "quote"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text 
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        print("### ", self.url)
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url    
        )
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    
    def to_html(self):
        if self.text_type == TextType.TEXT:
            return self.text
        elif self.text_type == TextType.BOLD:
            return f"<b>{self.text}</b>"
        elif self.text_type == TextType.ITALIC:
            return f"<i>{self.text}</i>"
        elif self.text_type == TextType.CODE:
            return f"<code>{self.text}</code>"
        elif self.text_type == TextType.LINK:
            test = f"<a href=\"{self.url}\">{self.text}</a>"
            return f"<a href=\"{self.url}\">{self.text}</a>"
        elif self.text_type == TextType.IMAGE:
            return f"<img src=\"{self.url}\" alt=\"{self.text}\">"
        elif self.text_type == TextType.QUOTE:
            return f"<blockquote>{self.text}</blockquote>"
        else:
            raise ValueError(f"Invalid text type: {self.text_type}")
    
