from lexicalAnalysis import Lexer

txt = "int a = 5;"
lex = Lexer(txt)
print(lex.text)