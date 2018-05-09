"""
    OPAT
"""
import Formula


count = 0
cardinality = 0
rawGlobal = []
formList = []

def createTree():
    formula = Formula.Formula
    formula.str = rawGlobal[0]
    rawGlobal.pop(0)
    if (rawGlobal[0] in ['*','+',')']):        
        formula.left = createTree()
        formula.right = createTree()
    elif (rawGlobal[0] == '-'):
        formula.left = createTree()
        formula.right = None
    elif (rawGlobal[0].isdigit()):
        formula.left = None
        formula.right = None
    else:
        '''
            O QUE????
        '''
    return formula

with open('test/test1.seq') as f:
    for l in f:
        if (count == 0):
            cardinality = l
        else:
            formula = Formula.Formula
            raw = l.split(" ")
            raw[len(raw)-1] = raw[len(raw)-1].rstrip()
            # raw.insert(0,'1')
            formList.append(raw)
        count += 1
        rawGlobal = l
        formList.append(createTree)
