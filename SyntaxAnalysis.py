from resources import Data, Token, Symb

Data = Data()
OperationsToAssembly = Data.operationsToAssembly
operationsPriority = Data.operationsPriority
valueToNodeType = Data.valueToNodeType
symbolsToNodeType = Data.symbolsToNodeType

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
        print(N)
        # self.AnaSem(N)
        # N = self.Optim(N)
        self.genCode(N)
        print("halt")#dbg\n

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
        if self.checkType(["NUMERIC_LITERAL"]): 
            A = Node("NUMERIC_LITERAL",self.tokens[self.currentPosition-1].value)
            return A
        elif self.checkValue(["("]):
            A = self.e(0)
            self.acceptValue([")"])
            return A
        # elif self.tokens[self.currentPosition].type == "EOF":
        #     return None
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
        une expression represente une valeur
        E:= M(e|'+'E|'-'E)
        E:=E'*'E|E'/'E|...|P
        """
        A1 = self.p()
        while (self.tokens[self.currentPosition].type!="EOF"):
            # print("value used:",self.tokens[self.currentPosition].value)
            priority = operationsPriority.get(self.tokens[self.currentPosition].value) # type: ignore # priority dict of the current token
            op = None if priority is None else priority.get("priority") #TODO:DONE Change with Data.operationsPriority 
            associativity = None if priority is None else priority.get("associativity")
            nd_type = valueToNodeType.get(self.tokens[self.currentPosition].value)
            tk_value = self.tokens[self.currentPosition].value
            # print("priority :",priority)
            # print("op: ",op)
            if (op is None or op<prio):
                return A1
            self.currentPosition += 1
            A2 = self.e(op+associativity)
            if (nd_type is None):
                raise TypeError("nd_type is none, value: ",self.tokens[self.currentPosition].value)
            A0 = Node(nd_type,tk_value)
            A0.addChild(A1)
            A0.addChild(A2)
            A1 = A0
        return A1
    

    def i(self)->Node:
        ## TODO there is an issue with choosing  between the types of the token and the node
        # # the case of an :'debug' E ';
        if (self.tokens[self.currentPosition].value == 'debug'):	## TODO add this type	(Not best practice)	'           
            I =  Node("nd_debug",self.tokens[self.currentPosition].value)
            self.currentPosition += 1
            E = self.e(0)
            I.addChild(E)
            self.acceptValue([";"])                         # TODO should be reviwed 
        #type: ignore # the case of an : '{'  I* '}'
        if (self.checkValue(['{'])):        
            I = Node("nd_block", None)                      # TODO Node Value is None ?????
            while(not self.checkValue(['}'])):
                self.currentPosition += 1
                I.addChild(self.i())
        else:                        # the case of an : E ';'
            I = Node("nd_drop", None)   # TODO Node Value is None ?????
            # self.currentPosition += 1
            I.addChild(self.e(0))
            self.acceptValue([";"])
        print("i(): ",I)
        return I

    def f(self)->Node : 
        return self.e(0)

    def genCode(self,Node:Node)->None:
        """
        voir photo
        """
        if Node is None:
            print("WARNING Node is None")
            return
        if (Node.type in OperationsToAssembly):
            for child in Node.children:
                self.genCode(child)
            print(OperationsToAssembly[Node.type])
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
            
            print("NODE TYPE UNKNOWN -> no assembly transformation :",Node)
    

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
    
    #Analyse Semantique
    # def begin() -> None:
    #     return
    
    # def end() -> None:
    #     return None
    
    # def declare(var:str,type:str) -> Symb:
    #     pass

    # def find(var:str) -> Symb:
    #     pass

