from resources import Token
from Lexer import Lexer
from SyntaxAnalysis import Parser

class Test:
    """
    This is a test class
    It is used to test the functionality of the Lexer and Parser
    Given a test C file with many test inside, it will split them into a list of unique tests
    Use the EOF token to split the test cases
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.tests = [] # List of tokens for each test case
    
    def __read_file(self):
        with open(self.file_path, 'r') as file:
            self.file_content = file.read()
    
    def __split_tests(self):
        lex = Lexer(self.file_content)
        lex.walk_through_words()
        for token in lex.tokens:
            if token.value == "eof":
                self.tests.append(lex.tokens[:lex.tokens.index(token)])
                self.tests.append(Token("EOF",-1,"eof"))
                lex.tokens = lex.tokens[lex.tokens.index(token)+1:]
    
    def run_tests(self):
        """
        Run the tests independently
        Each test is a unique test case with only one last EOF token at the end of the test
        """
        self.__read_file()
        self.__split_tests()
        i = 0
        for test in self.tests:
            print(f"Test: {test}")
            # lex = Lexer(test)
            # lex.walk_through_words()
            # lex.tokens.append(Token("EOF",-1,"eof"))
            parser = Parser(test)
            parser.Compile()
            print("\n\n")
            i += 1