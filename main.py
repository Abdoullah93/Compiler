# from Lexer import Lexer, Token
# from SyntaxAnalysis import Parser

# file_path = "test.c"
# with open(file_path, 'r') as file:
# 	file_content = file.read()
# # test = "(-(!((3+2))))"
# test = "(3+2)"

# ### Lexical Analysis ###
# lex = Lexer(test)
# lex.walk_through_words()
# lex.tokens.append(Token("EOF",-1,"eof")) ## to be added to the end of the lex.walk-through_words()

# ### Syntax Analysis - Generate Assembly Code ###
# parser = Parser(lex.tokens)
# parser.Compile()


#### Output ####
from Test import Test

test = Test("test.c")
test.run_tests()



