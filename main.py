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
TamAtual = 0
countBetaRule = 0
betas = []

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

def alfaRule(val, subtree, ramo):
    tablo = Tablo.Tablo()
    tablo.formula = subtree
    tablo.valor = val
    ramo.append(tablo)
    return ramo

def expAlfa(ramo):
    global TamAtual
    for i in ramo[TamAtual::]:
        if (i.valor == False):
            if (i.formula.str == ')'):
                ramo = alfaRule(True,  i.formula.left,  ramo)
                ramo = alfaRule(False, i.formula.right, ramo)
                TamAtual += 1
            elif (i.formula.str == '+'):
                ramo = alfaRule(False, i.formula.left,  ramo)
                ramo = alfaRule(False, i.formula.right, ramo)
                TamAtual += 1
            elif (i.formula.str == '-'):
                ramo = alfaRule(True,  i.formula.left,  ramo)
                TamAtual += 1
            else:
                betas.append(ramo.index(i))
        else: # (i.valor == True):
            if (i.formula.str == '*'):
                ramo = alfaRule(True,  i.formula.left,  ramo)
                ramo = alfaRule(True, i.formula.right, ramo)
                TamAtual += 1
            elif (i.formula.str == '-'):
                ramo = alfaRule(False,  i.formula.left,  ramo)
                TamAtual += 1
            else:
                betas.append(ramo.index(i))
    return ramo

def expBeta(ramo):
    global countBetaRule
    for i in ramo:
        if (i.valor == False):
            if (i.formula.str == '*'):
                ramo = betaRule()
                ramo = betaRule()
                countBetaRule += 1
            if (i.formula.str == '-'):
                ramo = betaRule()
                countBetaRule += 1
        if (i.valor == True):
            if (i.formula.str == '+'):
                ramo = betaRule()
                ramo = betaRule()
                countBetaRule += 1
            if (i.formula.str == ')'):
                ramo = betaRule()
                ramo = betaRule()
                countBetaRule += 1
            if (i.formula.str == '-'):
                ramo = betaRule()
                countBetaRule += 1
    return

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
    tablo = Tablo.Tablo()
    tablo.formula = i
    tablo.valor = True
    ramo.append(tablo)
ramo[len(ramo)-1].valor = False

ramo = expAlfa(ramo)

print("Ramo:")
for i in ramo:
    i.tprint()
    print()

print("Betas:")
for i in betas:
    ramo[i].tprint()
    print()
