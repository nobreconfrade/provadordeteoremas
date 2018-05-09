"""
    OPAT
"""
import Formula


count = 0
cardinality = 0
rawGlobal = []
formList = []

def createTree():
    formula = Formula.Formula()
    formula.str = rawGlobal[0]
    rawGlobal.pop(0)
    if (formula.str in ['*','+',')']):
        formula.left = createTree()
        formula.right = createTree()
    elif (formula.str == '-'):
        formula.left = createTree()
        formula.right = None
    elif (formula.str.isdigit()):
        formula.left = None
        formula.right = None
    else:
        '''
            O QUE????
        '''
    return formula

with open('test/test1.seq') as f:
    for l in f:
        raw = []
        if (count == 0):
            cardinality = l
            count += 1
        else:
            raw = l.split(" ")
            raw[len(raw)-1] = raw[len(raw)-1].rstrip()
            # print(raw)
            rawGlobal = raw
            formList.append(createTree())
for i in formList:
    i.tprint()
    print()
