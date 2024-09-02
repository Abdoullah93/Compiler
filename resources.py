class Node:
    def __init__(self, type:str, value:str):
        self.type = type
        self.value = value
        self.children = []

    def addChild(self, child:'Node')->None:
        self.children.append(child)

    def __repr__(self) -> str:
        return f"Node(type={self.type}, value={self.value}, children={self.children})"
    
class Token:
    def __init__(self, type, line, value):
        self.type = type
        self.line = line
        self.value = value

    def __repr__(self) -> str:
        return f"Token(type='{self.type}', line={self.line}, value='{self.value}')"
    
class Data: 
        def __init__(self):
            self.operatinsPriority = {
            'MUL': {'priority': 7, 'nd_name': "nd_MUL", 'associativity': 1},
            'DIV': {'priority': 7, 'nd_name': "nd_DIV", 'associativity': 1},
            '%': {'priority': 7, 'nd_name': "nd_MOD", 'associativity': 1},
            '+': {'priority': 6, 'nd_name': "nd_PLUS", 'associativity': 1},
            '-': {'priority': 6, 'nd_name': "nd_MINUS", 'associativity': 1},
            '>=': {'priority': 5, 'nd_name': "nd_GTE", 'associativity': 1},
            '<=': {'priority': 5, 'nd_name': "nd_LTE", 'associativity': 1},
            '>': {'priority': 5, 'nd_name': "nd_GT", 'associativity': 1},
            '<': {'priority': 5, 'nd_name': "nd_LT", 'associativity': 1},
            '==': {'priority': 4, 'nd_name': "nd_EQ", 'associativity': 1},
            '!=': {'priority': 4, 'nd_name': "nd_NEQ", 'associativity': 1},
            '&&': {'priority': 3, 'nd_name': "nd_AND", 'associativity': 1},
            '||': {'priority': 2, 'nd_name': "nd_OR", 'associativity': 1},
            '=': {'priority': 1, 'nd_name': "nd_ASSIGN", 'associativity': 0}
            }
            ## TODO manque la multiplication 
            self.valueToNodeType={
            "+": "nd_PLUS",
            "-": "nd_MINUS",
            "/": "nd_DIV",
            "%": "nd_MOD",
            "==": "nd_EQ",
            "!=": "nd_NEQ",
            ">=": "nd_GTE",
            "<=": "nd_LTE",
            ">": "nd_GT",
            "<": "nd_LT",
            "&&": "nd_AND",
            "||": "nd_OR",
            "=": "nd_ASSIGN",
            "*": "nd_MUL",
            }
            self.nodeTypeToAssembly = {
                # 'Node Type' : 'Assembly code' 
                "nd_PLUS":"add",
                "nd_MINUS":"sub",
                "nd_DIV": "div",
                "nd_MOD": "mod",
                "nd_MUL" : "mul",
            }
            self.symbolToNodeType = {
            "(": "nd_opened_parenthesis",
            ")": "nd_closed_parenthesis",
            "{": "nd_opened_curly_brack",
            "}": "nd_closed_curly_brack",
            "[": "nd_opened_bracket",
            "]": "nd_closed_bracket",
            ";": "nd_semicolon",
            ",": "nd_comma",
            }
            self.tokenTypeToNodeType = {
            "NUMERIC_LITERAL": "nd_numeric_literal",
            "IDENTIFIER": "nd_identifier",
            "KEYWORD": "nd_keyword",
            "STRING_LITERAL": "nd_string_literal",  
            "CHAR_LITERAL": "nd_char_literal",
            "PREPROCESSOR": "nd_preprocessor",
            }
            
        

