from Lexer import Lexer

file_path = "test.c"


with open(file_path, 'r') as file:
	file_content = file.read()

lex = Lexer(file_content)

lex.walk_through_words()
tokens = lex.tokens

## TESTS
for token in lex.tokens: 
    print('Token: '+token.value+', Type: '+token.type)

