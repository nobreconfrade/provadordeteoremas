"""
    OPAT
"""
import Formula
import Tablo
import time

count         = 0
cardinality   = 0
TamAtual      = 0
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
    global ramo
    tablo = Tablo.Tablo()
    tablo.formula = subtree
    tablo.valor   = val
    ramo.append(tablo)

def expAlfa(ptam):
    global TamAtual, ramo
    for i in ramo[ptam::]:
        if (i.valor == False):
            if (i.formula.str == ')'):
                appRamo(True,  i.formula.left)
                appRamo(False, i.formula.right)
                TamAtual += 2
            elif (i.formula.str == '+'):
                appRamo(False, i.formula.left)
                appRamo(False, i.formula.right)
                TamAtual += 2
            elif (i.formula.str == '-'):
                appRamo(True,  i.formula.left)
                TamAtual += 1
            elif (i.formula.str.isdigit() == False):
                betas.append(ramo.index(i))
        else: # (i.valor == True):
            if (i.formula.str == '*'):
                appRamo(True,  i.formula.left)
                appRamo(True, i.formula.right)
                TamAtual += 2
            elif (i.formula.str == '-'):
                appRamo(False,  i.formula.left)
                TamAtual += 1
            elif (i.formula.str.isdigit() == False):
                betas.append(ramo.index(i))
    return ramo

def expBeta(i):
    global TamAtual, ramo, betas, pilha
    if (ramo[i].valor == False):
        if (ramo[i].formula.str == '*'):
            appRamo(False, ramo[i].formula.left)
            pilha.append([ramo[i].formula.right, TamAtual, betas.copy()]) # tem que mudar a valorização antes né
            TamAtual += 1
            #reproduzir nas outras betas
    if (ramo[i].valor == True):
        if (ramo[i].formula.str == '+'):
            appRamo(True, ramo[i].formula.left)
            pilha.append([ramo[i].formula.right, TamAtual, betas.copy()])
            TamAtual += 1
        if (ramo[i].formula.str == ')'):
            appRamo(False, ramo[i].formula.left)
            pilha.append([ramo[i].formula.right, TamAtual, betas.copy()])
            TamAtual += 1
    return

def closed():
    global ramo
    atoms = []
    for i in ramo:
        s = i.formula.str
        if(s.isdigit()):
            if([s, not i.valor] in atoms):
                if([s, i.valor] in atoms):
                    print("Ramo fechado")
                    return True
            else:
                atoms.append([s, i.valor])
    return atoms #ramo aberto


def proof():
    global ramo, pilha, betas, TamAtual
    while(True):
        expAlfa(TamAtual)
        atoms = closed()
        # print(atoms)
        if(atoms != True):
            # print(betas)
            if(betas == [] and pilha == []):
                print("Não teorema")
                return False
            else:
                if (pilha != []):
                    pass
                else:
                    beta = betas.pop()
                    print(pilha)
                    # print(beta)
                    # print("Ramo:")
                    # for i in ramo:
                    #     i.tprint()
                    #     print()
                    # time.sleep(2)
                    expBeta(beta)
        else:
            return False
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

# expAlfa(TamAtual)

print("Ramo:")
for i in ramo:
    i.tprint()
    print()

# print("Betas:")
# for i in betas:
#     ramo[i].tprint()
#     print()

proof()
