class Formula(object):
    """docstring for Formula."""
    def __init__(self):
        pass
    def tprint(self):        
        print(self.str,end="")
        if(self.left is not None):
            self.left.tprint()
        if(self.right is not None):
            self.right.tprint()
