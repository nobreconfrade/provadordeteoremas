"""
    OPAT
"""
import Formula


count = 0
cardinality = 0
rawGlobal = []
treeList = []
treeReadyList = []
formList = []

def createTree():
    if rawGlobal[0] == '*' or rawGlobal[0] == '+' or rawGlobal[0] == ')':
        formula = Formula.Formula
        formula.str = rawGlobal[0]
        rawGlobal.pop(0)
        formula.left = createTree()
        rawGlobal.pop(0)
        formula.right = createTree()
        treeList.insert(0,formula)
    elif rawGlobal[0] == '-':
        formula = Formula.Formula
        formula.str = rawGlobal[0]
        rawGlobal.pop(0)
        formula.left = createTree()
        formula.right = None
        treeList.insert(0,formula)
    elif rawGlobal[0].isdigit():
        formula = Formula.Formula
        formula.str == rawGlobal[0]
        rawGlobal.pop(0)
        formula.left = None
        formula.right = None
        treeList.insert(0,formula)
    else:
        '''
            O QUE????
        '''
    return formula

with open('test/test1.seq') as f:
    for l in f:
        if count == 0:
            cardinality = l
        else:
            formula = Formula.Formula
            raw = l.split(" ")
            raw[len(raw)-1] = raw[len(raw)-1].rstrip()
            # raw.insert(0,'1')
            formList.append(raw)
        count += 1
for i in formList:
    rawGlobal = i
    treeList = []
    treeReadyList.append(createTree())
