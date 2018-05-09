class Tablo(object):
    """docstring for Tablo."""
    def __init__(self):
        pass
    def tprint(self):
        print("VALOR:",self.valor,self.formula.str,end="")
        if(self.formula.left is not None):
            self.formula.left.tprint()
        if(self.formula.right is not None):
            self.formula.right.tprint()
