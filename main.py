from Lexer import Lexer

file_path = "test.c"


with open(file_path, 'r') as file:
	file_content = file.read()

lex = Lexer(file_content)

lex.walk_through_words()

## TESTS
for tok in lex.tokens:
	print(tok)

# TODO: correct line in token
