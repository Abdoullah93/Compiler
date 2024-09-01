from Lexer import Lexer, Token
from SyntaxAnalysis import Parser

file_path = "test.c"
with open(file_path, 'r') as file:
	file_content = file.read()
test = "(-(!((3))))"

### Lexical Analysis ###
lex = Lexer(test)
lex.walk_through_words()
lex.tokens.append(Token("EOF",None,None)) ## to be added to the end of the lex.walk-through_words()

### Syntax Analysis - Generate Assembly Code ###
parser = Parser(lex.tokens)
parser.Compile()




