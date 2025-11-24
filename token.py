# Token Class for Lexical Analysis and Parsing
class Token:
    def __init__(self, type, content):
        self.type = type
        self.content = content
    
    def getType(self):
        return self.type
    
    def getContent(self):
        return self.content
    
    def __repr__(self):
        return f"({self.type}, {self.content})"