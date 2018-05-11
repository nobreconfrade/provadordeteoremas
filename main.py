"""
    OPAT
"""
import Formula
import Tablo
import time
import sys

count         = 0
cardinality   = 0
TamAtual      = 0
contregras    = 0
contnos       = 0
contRamos     = 0
rawGlobal     = []
formList      = []
ramo          = []
betas         = []
pilha         = []

def createTree():
    formula     = Formula.Formula()
    formula.str = rawGlobal[0]
    rawGlobal.pop(0)
    if (formula.str in ['*','+',')']):
        formula.left  = createTree()
        formula.right = createTree()
    elif (formula.str == '-'):
        formula.left  = createTree()
        formula.right = None
    else: #(formula.str.isdigit()):
        formula.left  = None
        formula.right = None
    return formula

def appRamo(val, subtree):
    global ramo, contnos
    tablo = Tablo.Tablo()
    tablo.formula = subtree
    tablo.valor   = val
    ramo.append(tablo)
    contnos += 1

def expAlfa(ptam):
    global ramo, TamAtual, contregras
    for i in ramo[ptam::]:
        if (i.valor == False):
            if (i.formula.str == ')'):
                appRamo(True,  i.formula.left)
                appRamo(False, i.formula.right)
                TamAtual += 2
                contregras += 1
            elif (i.formula.str == '+'):
                appRamo(False, i.formula.left)
                appRamo(False, i.formula.right)
                TamAtual += 2
                contregras += 1
            elif (i.formula.str == '-'):
                appRamo(True,  i.formula.left)
                TamAtual += 1
                contregras += 1
            elif (i.formula.str.isdigit() == False):
                betas.append(ramo.index(i))
                TamAtual += 1
                contregras += 1
            else:
                TamAtual += 1
        else: # (i.valor == True):
            if (i.formula.str == '*'):
                appRamo(True,  i.formula.left)
                appRamo(True, i.formula.right)
                TamAtual += 2
                contregras += 1
            elif (i.formula.str == '-'):
                appRamo(False,  i.formula.left)
                TamAtual += 1
                contregras += 1
            elif (i.formula.str.isdigit() == False):
                betas.append(ramo.index(i))
                TamAtual += 1
                contregras += 1
            else:
                TamAtual += 1
    if(TamAtual > ptam):
        expAlfa(TamAtual)
    return

def expBeta(i):
    global TamAtual, ramo, betas, pilha
    if (ramo[i].valor == False):
        if (ramo[i].formula.str == '*'):
            appRamo(False, ramo[i].formula.left)
            pilha.append([False, ramo[i].formula.right, TamAtual, betas.copy()])
    if (ramo[i].valor == True):
        if (ramo[i].formula.str == '+'):
            appRamo(True, ramo[i].formula.left)
            pilha.append([True, ramo[i].formula.right, TamAtual, betas.copy()])
        elif (ramo[i].formula.str == ')'):
            appRamo(False, ramo[i].formula.left)
            pilha.append([True, ramo[i].formula.right, TamAtual, betas.copy()])
    return

def closed():
    global ramo
    atoms = []
    for i in ramo:
        s = i.formula.str
        if(s.isdigit()):
            if([s, not i.valor] in atoms):
                #print("Ramo fechado")
                #print("Ramo:")
                #for i in ramo:
                #    i.tprint()
                #    print()
                #print("-------------")
                return True
            else:
                atoms.append([s, i.valor])
    return atoms #ramo aberto


def proof():
    global ramo, pilha, betas, TamAtual, contRamos
    while(True):
        #print(TamAtual)
        expAlfa(TamAtual)
        atoms = closed()
        if(atoms != True):
            if(betas == []):
                print("Não teorema")
                print(atoms)
                #print("Ramo:")
                #for i in ramo:
                #    i.tprint()
                #    print()
                return atoms
            else:
                if(betas != []):
                    beta = betas.pop()
                    expBeta(beta)
        else:
            if(pilha != []):
                tip = pilha.pop()
                betas = tip[3]
                TamAtual = tip[2]
                ramo = ramo[:TamAtual]
                appRamo(tip[0],  tip[1])
                contRamos += 1
            else:
                print("Teorema")
                return True

with open(sys.argv[1]) as f:
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

print("Ramo inicial:")
contRamos = 1
for i in ramo:
    i.tprint()
    print()

# print("Betas:")
# for i in betas:
#     ramo[i].tprint()
#     print()

proof()
print("Total de nós criados: ", contnos)
print("Total de regras aplicadas: ", contregras)
print("Total Ramos: ", contRamos)