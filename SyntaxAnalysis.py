from lexicalAnalysis import Token

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
        pass

    def toAssembly(self)->None:
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
        while self.tokens[self.currentPosition].value!="EOF":
            N = self.AnaSynt()
            # TODO
        print("dbg\nhalt")

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
        # TODO
        pass
    
    def a(self)->Node:
        """
        voir photo
        """
        if self.checkType("IDENTIFIER"):
            A = Node("IDENTIFIER",self.tokens[self.currentPosition-1])
            return A
        elif self.checkValue("("):
            A = self.e(self)
            self.acceptValue(")")
            return A
        else:
            raise Exception("Atomique token expected")

    def s(self)->Node:
        return self.a()

    def p(self)->Node:
        """
        voir photo
        """
        if self.checkValue("+"):
            A = Node("PLUS_UNAIRE",self.tokens[self.currentPosition-1])
            A.addChild(self.p())
            return A
        elif self.checkValue("-"):
            A = Node("MOINS_UNAIRE",self.tokens[self.currentPosition-1])
            A.addChild(self.p())
            return A
        elif self.checkValue("!"):
            A = Node("NOT",self.tokens[self.currentPosition-1])
            A.addChild(self.p())
            return A
        else:
            return self.s()

    def e(self)->Node:
        return self.p()

    def i(self)->Node:
        return self.e()

    def f(self)->Node:
        return self.i()

    def genCode(self,Node:Node)->None:
        """
        voir photo
        """
        if Node.type=="IDENTIFIER":
            print("push",Node.value)
        elif Node.type=="NOT":
            self.genCode(Node.children[0])
            print("not")
        elif Node.type=="MOINS_UNAIRE":
            print("push 0")
            self.genCode(Node.children[0])
            print("sub")
        else:
            Warning("NODE TYPE UNKNOWN -> no assembly transformation")
    

    def checkType(self,type)->bool:
        if (self.tokens[self.currentPosition]!=type):
            return False
        else:
            self.currentPosition += 1
            return True
        

    def acceptType(self, type) -> bool:
        if self.tokens[self.currentPosition] != type:
            raise Exception(f"Unexpected token type: {self.tokens[self.currentPosition]}\nline {self.tokens[self.currentPosition].line}, token expected: {type}")
        else:
            self.currentPosition += 1
            return True
        
    def checkValue(self,value)->bool:
        if (self.tokens[self.currentPosition]!=value):
            return False
        else:
            self.currentPosition += 1
            return True
        

    def acceptValue(self, value) -> bool:
        if self.tokens[self.currentPosition] != value:
            raise Exception(f"Unexpected token value: {self.tokens[self.currentPosition]}\nline {self.tokens[self.currentPosition].line}, token expected: {value}")
        else:
            self.currentPosition += 1
            return True

