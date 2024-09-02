from Lexer import Token
from resources import Data
from resources import Node


Data = Data()
OperationsToAssembly = Data.OperationsToAssembly
symboleToNodeType = Data.symboleToNodeType


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
        if self.checkType(["NUMERIC_LITERAL"]): # move to a() ?
            A = Node("NUMERIC_LITERAL",self.tokens[self.currentPosition-1].value)
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
        return self.p()

    def e(self,prio:int)->Node:
        """e pour epsilon
        operateur binaire
        E:= M(e|'+'E|'-'E)
        E:=E'*'E|E'/'E|...|P
        """
        A1 = self.p()
        while (self.tokens[self.currentPosition].type!="EOF"):
            op = self.priority.get(self.tokens[self.currentPosition].value)
            if (op is None or op<prio):
                return A1
            self.currentPosition += 1
            A2 = self.e(op+1)
            nd_type = self.valueToNodeType.get(op)
            if (nd_type is None):
                Exception("nd_type is none")
            A1 = Node(nd_type)
            A1.addChild(A1)
            A1.addChild(A2)
    

    def i(self)->Node:
        ## TODO there is an issue with choosing  between the types of the token and the node
        if (self.tokens[self.currentPosition].type == 'nd_debug')	## TODO add this type		# the case of an :'debug' E ';'
            I =  Node("nd_debug",self.tokens[self.currentPosition].value)
            self.currentPosition += 1
            E = self.e()
            I.addChild(E)
        # TODO should be reviwed how to use symboleToNodeType
        if (checkType(self, symboleToNodeType['{'])) :		# the case of an : '{'  I* '}'
         	I = Node("nd_block", None)
        
        while(not 
ppppcheckType(symboleToNodeType['}'])):
     		self.currentPosition += 1
            I.addChild(self.i())
        # else:     					# the case of an : E ';'
        # 	I = Node("drop", )
        # 	accept(";") # ????
        # 	I.addChild(self.e())

	    return I

        return self.e()

    def f(self)->Node : 
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
            print("Node is None")
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

