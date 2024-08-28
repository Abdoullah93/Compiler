from lexicalAnalysis import Lexer

file_path = "test.c"

with open(file_path, 'r') as file:
	file_content = file.read()

lex = Lexer(file_content)
print(lex.text)

token = lex.get_next_token()
while token.type != "EOF":
	print(token)
	token = lex.get_next_token()