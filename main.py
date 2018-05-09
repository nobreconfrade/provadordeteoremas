"""
    OPAT
"""
import Formula
import Tablo

count = 0
cardinality = 0
rawGlobal = []
formList = []
ramo = []
alfaRule = 0

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
    else: #(formula.str.isdigit()):
        formula.left = None
        formula.right = None
    return formula

def expAlfa(ramo,alfaRule):
    for i in ramo:
        if (i.valor == False):
            if (i.formula.str == ')'):
                tablo = Tablo.Tablo
                tablo.formula = i.formula.left
                tablo.valor = True
                ramo.append(tablo)
                tablo.formula = i.formula.right
                tablo.valor = False
                ramo.append(tablo)
                alfaRule += 1
            if (i.formula.str == '+'):
                tablo = Tablo.Tablo
                tablo.formula = i.formula.left
                tablo.valor = False
                ramo.append(tablo)
                tablo.formula = i.formula.right
                tablo.valor = False
                ramo.append(tablo)
                alfaRule += 1
            if (i.formula.str == '-'):
                tablo = Tablo.Tablo
                tablo.formula = i.formula.left
                tablo.valor = True
                ramo.append(tablo)

        if (i.valor == True):
            if (i.formula.str == '*'):
                tablo = Tablo.Tablo
                tablo.formula = i.formula.left
                tablo.valor = True
                ramo.append(tablo)
                tablo.formula = i.formula.right
                tablo.valor = True
                ramo.append(tablo)
                alfaRule += 1
            if (i.formula.str == '-'):
                tablo = Tablo.Tablo
                tablo.formula = i.formula.left
                tablo.valor = False
                ramo.append(tablo)
    return ramo

with open('test/3.seq') as f:
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
    tablo = Tablo.Tablo
    tablo.formula = i
    tablo.valor = True
    ramo.append(tablo)
ramo[len(ramo)-1].valor = False

ramo = expAlfa(ramo,alfaRule)
for i in ramo:
    i.tprint()
    print()
