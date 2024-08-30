from Lexer import Token
from resources import Data

Data = Data()
OperationsToAssembly = Data.OperationsToAssembly

class Node:
    def __init__(self, type:str, value:str):
        self.type = type
        self.value = value
        self.children = []

    def addChild(self, child:'Node')->None:
        self.children.append(child)

    def __repr__(self) -> str:
        return f"Node(type={self.type}, value={self.value}, children={self.children})"
    

class Parser:
    """
    regarde le contexte local
    """
    def __init__(self,tokens: list[Token]):
        self.tokens = tokens
        self.currentPosition = 0

    def Compile(self)->None:
        """
        //compilateur
        print(".start")
        for (int i=1;i<argc;i++){
            analex(argv[i]);
            while(T.type!="EOF"){
                Node N = AnaSynt();
                AnaSem(N);
                N = Optim(N);
                genCode(N);
            }
        }
        print("dbg\nhalt")
        """
        print(".start")
        # while self.tokens[self.currentPosition].value!="EOF":
        N = self.AnaSynt()
        self.AnaSem(N)
        N = self.Optim(N)
        self.genCode(N)
        print("dbg\nhalt")

    def Optim(self, Node: Node)->Node:
        return Node

    def AnaSem(self, Node: Node)->None:
        return None

    def incrementTokenPos(self)->None:
        """
        """
        # TODO: use this function to increment
        if self.currentPosition >= len(self.tokens):
            raise Exception("No more tokens")
        else:
            self.currentPosition += 1

    def AnaSynt(self)->Node:
        """
        appelle la bonne fonction pour le token courant
        gros switch
        """
        return self.f()
    
    def a(self)->Node|None:
        """
        A:= cste | '('E')'
        """
        if self.checkType(["IDENTIFIER"]):
            A = Node("IDENTIFIER",self.tokens[self.currentPosition-1].value)
            return A
        elif self.checkValue(["("]):
            A = self.e()
            self.acceptValue([")"])
            return A
        elif self.tokens[self.currentPosition].type == "EOF":
            return None
        else:
            raise Exception(f"Atomic token expected. I got {self.tokens[self.currentPosition]}")

    def s(self)->Node:
        return self.a()

    def p(self)->Node:
        """
        operateur unaire
        P:= +P | -P | !P | S
        """
        if self.checkValue(["+"]):
            A = Node("PLUS_UNAIRE",self.tokens[self.currentPosition-1].value)
            A.addChild(self.p())
            return A
        elif self.checkValue(["-"]):
            A = Node("MOINS_UNAIRE",self.tokens[self.currentPosition-1].value)
            A.addChild(self.p())
            return A
        elif self.checkValue(["!"]):
            A = Node("NOT",self.tokens[self.currentPosition-1].value)
            A.addChild(self.p())
            return A
        else:
            return self.s()

    def m(self)->Node:
        """e pour epsilon
        M:= E'*'M | M := M(e|'+'E)
        """
        pass

    def e(self)->Node:
        """e pour epsilon
        operateur binaire
        E:= M(e|'+'E|'-'E)
        E:=E'*'E|E'/'E|...|P
        """
        if self.checkType(["NUMERIC_LITERAL"]): # move to a() ?
            A = Node("NUMERIC_LITERAL",self.tokens[self.currentPosition-1].value)
            return A
        return self.p()
    

    def i(self)->Node:
        return self.e()

    def f(self)->Node:
        return self.i()

    def genCode(self,Node:Node)->None:
        """
        voir photo
        """
        if (Node.type in OperationsToAssembly):
            for child in Node.children:
                self.genCode(self,child)
            print(OperationsToAssembly[Node.type])

        if Node is None:
            return None
        elif Node.type=="NUMERIC_LITERAL": #Const case
            print("push",Node.value)
        elif Node.type=="NOT":
            self.genCode(Node.children[0])
            print("not")
        elif Node.type=="MOINS_UNAIRE":
            print("push 0")
            self.genCode(Node.children[0])
            print("sub")
        else:
            print("NODE TYPE UNKNOWN -> no assembly transformation")
    

    def checkType(self,type: list[str])->bool:
        if (self.tokens[self.currentPosition].type not in type):
            return False
        else:
            self.currentPosition += 1
            return True
        

    def acceptType(self, type: list[str]) -> bool:
        if self.tokens[self.currentPosition].type not in type:
            raise Exception(f"Unexpected token type: {self.tokens[self.currentPosition].type}\nline {self.tokens[self.currentPosition].line}, token expected: {type}")
        else:
            self.currentPosition += 1
            return True
        
    def checkValue(self,value: list[str])->bool:
        if (self.tokens[self.currentPosition].value not in value):
            return False
        else:
            self.currentPosition += 1
            return True
        

    def acceptValue(self, value:list[str]) -> bool:
        if self.tokens[self.currentPosition].value not in value:
            raise Exception(f"Unexpected token value: {self.tokens[self.currentPosition].value}\nline {self.tokens[self.currentPosition].line}, token expected: {value}")
        else:
            self.currentPosition += 1
            return True

