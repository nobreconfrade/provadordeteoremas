"""
    OPAT
"""
import Formula
import Tablo
import sys

count         = 0
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

def treeToStr(f, s):
    s += f.str
    
    if (f.str in ['*','+',')']):
        s = treeToStr(f.left, s)
        s = treeToStr(f.right, s)
    
    elif (f.str == '-'):
        s = treeToStr(f.left, s)
    
    return s

def countNodes(f, n):
    n += 1
    
    if (not f.str.isdigit()):
        n = countNodes(f.left, n)
        n = countNodes(f.right, n)
    
    return n

def appRamo(val, subtree):
    global ramo, contnos
    
    tablo         = Tablo.Tablo()
    tablo.formula = subtree
    tablo.valor   = val
    tablo.string  = treeToStr(subtree, '')
    contnos      += 1
    ramo.append(tablo)

def expAlfa(ptam):
    global ramo, TamAtual, contregras
    
    for i in ramo[ptam::]:
        if (i.valor == False):
            
            if (i.formula.str == ')'):
                appRamo(True,  i.formula.left)
                appRamo(False, i.formula.right)
                TamAtual   += 2
                contregras += 1
            
            elif (i.formula.str == '+'):
                appRamo(False, i.formula.left)
                appRamo(False, i.formula.right)
                TamAtual   += 2
                contregras += 1
            
            elif (i.formula.str == '-'):
                appRamo(True, i.formula.left)
                TamAtual   += 1
                contregras += 1
            
            elif (not i.formula.str.isdigit()):
                betas.append([ramo.index(i), countNodes(i.formula, 0)])
                TamAtual   += 1
                contregras += 1
            
            else:
                TamAtual += 1
        
        else: # (i.valor == True):
            if (i.formula.str == '*'):
                appRamo(True, i.formula.left)
                appRamo(True, i.formula.right)
                TamAtual   += 2
                contregras += 1
            
            elif (i.formula.str == '-'):
                appRamo(False, i.formula.left)
                TamAtual   += 1
                contregras += 1
            
            elif (not i.formula.str.isdigit()):
                betas.append([ramo.index(i), countNodes(i.formula, 0)])
                TamAtual   += 1
                contregras += 1
            
            else:
                TamAtual += 1

    if(TamAtual > ptam):
        expAlfa(TamAtual)

    return

def expBeta(i):
    global TamAtual, ramo, betas, pilha
    # verificar quem é maior, para ir na pilha
    leftisBigger = True
    subtreeA  = ramo[i].formula.left
    subtreeB = ramo[i].formula.right

    tamleft  = len(treeToStr(subtreeA, ''))
    tamright = len(treeToStr(subtreeB, ''))

    if (tamleft < tamright):
        subtreeA = ramo[i].formula.right
        subtreeB = ramo[i].formula.left
        leftisBigger = False

    if (ramo[i].valor == False):
        if (ramo[i].formula.str == '*'):
            appRamo(False, subtreeA)
            pilha.append([False, subtreeB, TamAtual, betas.copy()])
    
    if (ramo[i].valor == True):
        if (ramo[i].formula.str == '+'):
            appRamo(True, subtreeA)
            pilha.append([True, subtreeB, TamAtual, betas.copy()])
        
        elif (ramo[i].formula.str == ')'):
            if (leftisBigger):
                appRamo(False, subtreeA)
                pilha.append([True, subtreeB, TamAtual, betas.copy()])
            else:
                appRamo(True, subtreeA)
                pilha.append([False, subtreeB, TamAtual, betas.copy()])

# checkBeta()

# def subformula():
#     global betas
#     for b in betas:
#         i = b[0]
#         if (ramo[i].valor == False):
#             if (ramo[i].formula.str == '*'):
#                 b1 = checkBeta(False, ramo[i].formula.left)
#                 b2 = checkBeta([False, ramo[i].formula.right, TamAtual, betas.copy()])
    
#         if (ramo[i].valor == True):
#             if (ramo[i].formula.str == '+'):
#                 b1 = checkBeta(True, ramo[i].formula.left)
#                 b2 = checkBeta([True, ramo[i].formula.right, TamAtual, betas.copy()])
            
#             elif (ramo[i].formula.str == ')'):
#                 b1 = checkBeta(False, ramo[i].formula.left)
#                 b2 = checkBeta([True, ramo[i].formula.right, TamAtual, betas.copy()]) 


#     return None

    # return i 

def closed():
    global ramo
    atoms = []

    for i in ramo:
        s = i.formula.str

        if(s.isdigit()):
            if([s, not i.valor] in atoms):
                return True
            
            else:
                atoms.append([s, i.valor])

    return atoms #ramo aberto

def proof():
    global ramo, pilha, betas, TamAtual, contRamos
    
    while(True):
        expAlfa(TamAtual)

        atoms = closed()

        if(atoms != True):
            if(betas == []):
                print("Não teorema")
                print(atoms)
                return atoms
            
            else:
                if(betas != []):
                    ibeta = None
                    # if ((ibeta = subformula()) != None):
                        # beta  = betas.pop(betas.index(ibeta))
                    # else:
                    betas = sorted(betas, key = lambda tup: tup[1], reverse = True)
                    beta  = betas.pop()
                    expBeta(beta[0])
        else:
            if(pilha != []):
                tip        = pilha.pop()
                betas      = tip[3]
                TamAtual   = tip[2]
                ramo       = ramo[:TamAtual]
                contRamos += 1
                appRamo(tip[0],  tip[1])
            
            else:
                print("Teorema")
                return True

with open(sys.argv[1]) as f:
    
    for l in f:
        raw = []
        
        if (count == 0):
            count += 1
        
        else:
            raw             = l.split(" ")
            raw[len(raw)-1] = raw[len(raw)-1].rstrip()
            rawGlobal       = raw
            formList.append(createTree())

for i in formList:
    tablo         = Tablo.Tablo()
    tablo.formula = i
    tablo.valor   = True
    tablo.string  = treeToStr(i, '')
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
