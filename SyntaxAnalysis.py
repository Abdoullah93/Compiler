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
    

class Syntaxer:
    """
    regarde le contexte local
    """
    def __init__(self,tokens: list[Token]):
        self.tokens = tokens
        self.currentPosition = 0
        pass

    def f1(self):
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
        pass

    def a(self)->Node:
        """
        voir photo
        """
        
        pass

    def s(self)->Node:
        return self.a(self)

    def p(self)->Node:
        """
        voir photo
        """
        pass

    def e(self)->Node:
        return self.p(self)

    def i(self)->Node:
        return self.e(self)

    def f(self)->Node:
        return self.i(self)

    def genCode(self,Node)->None:
        """
        voir photo
        """
        pass