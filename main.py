from Lexer import Lexer, Token
from SyntaxAnalysis import Parser

### Lexical Analysis ###
file_path = "test.c"
with open(file_path, 'r') as file:
	file_content = file.read()
test = "(-(!((3))))"
lex = Lexer(test)
lex.walk_through_words()
lex.tokens.append(Token("EOF",None,None))

### Syntax Analysis - Generate Assembly Code ###
parser = Parser(lex.tokens)
parser.Compile()

