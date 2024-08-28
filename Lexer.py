class Lexer:
    def __init__(self, code):
        self.code = code
        self.current_position = 0
        self.keywords = {"int", "return", "if", "else", "while", "for", "void", "char", "float", "double","continu","break","send","recv","debug"}  # C keywords
        self.tokens = []

    class Token:
        def __init__(self, type, line, value):
            self.type = type
            self.line = line
            self.value = value

    def walk_through_words(self):
        while self.current_position < len(self.code):
            while self.current_position < len(self.code) and self.code[self.current_position].isspace():
                self.current_position += 1
            
            if self.current_position >= len(self.code):
                return
            
            word = self.get_word()
            if word:
                self.tokenize_word(word)

    def get_word(self):
        token_string = ''
        
        if self.code[self.current_position] == '#':
            # Handle preprocessor directives
            while self.current_position < len(self.code) and not self.code[self.current_position].isspace():
                token_string += self.code[self.current_position]
                self.current_position += 1
            return token_string

        if self.code[self.current_position] == '"':
            # Handle string literals
            token_string += self.code[self.current_position]
            self.current_position += 1
            while self.current_position < len(self.code) and self.code[self.current_position] != '"':
                token_string += self.code[self.current_position]
                self.current_position += 1
            if self.current_position < len(self.code):
                token_string += self.code[self.current_position]
                self.current_position += 1
            return token_string

        if self.code[self.current_position] == "'":
            # Handle character literals
            token_string += self.code[self.current_position]
            self.current_position += 1
            while self.current_position < len(self.code) and self.code[self.current_position] != "'":
                token_string += self.code[self.current_position]
                self.current_position += 1
            if self.current_position < len(self.code):
                token_string += self.code[self.current_position]
                self.current_position += 1
            return token_string

        if self.code[self.current_position] == '/':
            # Handle comments
            if self.current_position + 1 < len(self.code) and self.code[self.current_position + 1] == '/':
                while self.current_position < len(self.code) and self.code[self.current_position] != '\n':
                    self.current_position += 1
                return ''  # Skip the comment
            elif self.current_position + 1 < len(self.code) and self.code[self.current_position + 1] == '*':
                self.current_position += 2
                while self.current_position + 1 < len(self.code) and (self.code[self.current_position] != '*' or self.code[self.current_position + 1] != '/'):
                    self.current_position += 1
                self.current_position += 2  # Skip the '*/'
                return ''  # Skip the comment

        while self.current_position < len(self.code):
            current_char = self.code[self.current_position]

            # Check for multi-character operators (&&, ||, ==, !=, etc.)
            if self.current_position + 1 < len(self.code):
                next_char = self.code[self.current_position + 1]
                if (current_char == '&' and next_char == '&') or (current_char == '|' and next_char == '|'):
                    token_string = current_char + next_char
                    self.current_position += 2
                    break
                elif (current_char == '=' and next_char == '=') or \
                     (current_char == '!' and next_char == '=') or \
                     (current_char == '<' and next_char == '=') or \
                     (current_char == '>' and next_char == '='):
                    token_string = current_char + next_char
                    self.current_position += 2
                    break

            if current_char.isspace() or current_char in "{}[]();,+-*/%&|^~!=<>":
                if token_string:
                    break
                else:
                    token_string = current_char
                    self.current_position += 1
                    break
            token_string += current_char
            self.current_position += 1
        
        return token_string

    def tokenize_word(self, word):
        token_type = self.check_token(word)
        currentToken = self.Token(token_type, self.current_position, word)
        self.tokens.append(currentToken)

    def check_token(self, word):
        # Check if the word is a keyword
        if word in self.keywords:
            return "KEYWORD"

        # Check if the word is a preprocessor directive
        if word.startswith("#"):
            return "PREPROCESSOR"

        # Check if the word is a string literal
        if word.startswith('"') and word.endswith('"'):
            return "STRING_LITERAL"

        # Check if the word is a character literal
        if word.startswith("'") and word.endswith("'"):
            return "CHAR_LITERAL"

        # Check if the word is an identifier (starts with a letter or underscore)
        if word[0].isalpha() or word[0] == '_':
            return "IDENTIFIER"

        # Check if the word is a numeric literal
        if word.isdigit():
            return "NUMERIC_LITERAL"

        # Check if the word is a single or multi-character operator
        if word in ["+", "-", "*", "/", "%", "&&", "||", "&", "|", "^", "~", "!", "=", "==", "!=", "<", ">", "<=", ">="]:
            return "OPERATOR"

        # Check if the word is a delimiter
        if word in "{}[]();,":
            return "DELIMITER"

        # Handle unknown tokens
        return "UNKNOWN"


# # # TESTING
# code = """
# #include <stdio.h>

# int main() { 
#     // this is a comment
#     int x1 = 1;
#     int y = 1;
#     if (x1 == 1 && y == 1) {
#         int z = x1 + y;
#     }
#     printf("Hello, world!\n");
#     return 0;
# }
# """
# lexer = Lexer(code)
# lexer.walk_through_words()
# for token in lexer.tokens: 
#     print('Token: ' + token.value + ', Type: ' + token.type)
