import re

class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return f'Token({self.type}, {self.value}, {self.line})'

class Lexer:
    """
    regarde uniquement le token
    """
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.advance()  # Skip the newline character
        self.line += 1

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/' and self.text[self.pos + 1] == '/':
                self.skip_comment()
                continue

            token_handlers = {
                'NUMBER': lambda: Token('NUMBER', self.number(), self.line),
                'ID': lambda: Token('ID', self._id(), self.line),
                'PLUS': lambda: Token('PLUS', '+', self.line),
                'MINUS': lambda: Token('MINUS', '-', self.line),
                'MUL': lambda: Token('MUL', '*', self.line),
                'DIV': lambda: Token('DIV', '/', self.line),
                'LPAREN': lambda: Token('LPAREN', '(', self.line),
                'RPAREN': lambda: Token('RPAREN', ')', self.line),
            }

            if self.current_char.isdigit():
                return token_handlers['NUMBER']()

            if self.current_char.isalpha():
                return token_handlers['ID']()

            if self.current_char in '+-*/()':
                token_type = {
                    '+': 'PLUS',
                    '-': 'MINUS',
                    '*': 'MUL',
                    '/': 'DIV',
                    '(': 'LPAREN',
                    ')': 'RPAREN',
                }[self.current_char]
                self.advance()
                return token_handlers[token_type]()

            raise Exception(f'Invalid character {self.current_char} at line {self.line}')

        return Token('EOF', None, self.line)
