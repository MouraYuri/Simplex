#
#
#
#

import numpy as np
from numpy.linalg import inv

def buidlingMatrixB(m, AB, A):
    ctrl = []
    B = []
    for x in range(m):
        for y in AB:
            ctrl.append(A[x][y - 1])

        B.append(ctrl)
        ctrl = []
    return B

def buildingInitialVectorX(n, XB, AB):
    ctrl = []
    for z in range(n):
        ctrl.append([0])

    counter = 0
    for y in range(n):
        for q in AB:
            if (y+1 == q):
                ctrl[y][0] = XB[counter][0]
                counter = counter + 1
                break
            else:
                ctrl[y][0] = 0
    return ctrl

def computingDVector(invB, A, IVNBCRN, AB, n):

    #db = -B^-1*Aj

    #Segurando os valores de Aj \/
    Aj = []
    for z in range(len(AB)):
        Aj.append([0])

    for z in range(len(AB)):
        Aj[z][0] = A[z][IVNBCRN-1]

    #Segurando os valores de db \/

    db = []

    invB = np.dot(invB, -1)
    db = np.dot(invB, Aj)


    d = []
    for w in range(n):
        d.append([0])

    counter = 0
    for y in range(n):
        for a in AB:
            if (y+1 == a):
                d[y][0] = db[counter][0]
                counter = counter + 1
                break
            if (y+1 == IVNBCRN):
                d[y][0] = 1
                break
            else:
                d[y][0] = 0

    return d

def buildingVectorCB(c, AB): #Construindo vetor custo dos índices da base
    CB = []
    for z in range(len(AB)):
        CB.append([0])
    counter = 0
    for y in AB:
        CB[counter][0] = c[y-1][0]
        counter = counter + 1

    return CB

def computingNonBasicReducedCost(c, AB, invB, A, n, CB):
    cBarra = []
    for w in range(n):
        cBarra.append([0])
    transposedCB = np.transpose(CB)
    for y in range(n):
        for z in AB:
            if (y+1 == z):
                cBarra[y][0] = 0
                break
            else:
                Aj = []
                for z in range(len(AB)):
                    Aj.append([0])

                for z in range(len(AB)):
                    Aj[z][0] = A[z][y]

                ctrl = np.dot(transposedCB, invB)
                ctrl = ctrl[0]
                ctrl = np.dot(ctrl, Aj)
                ctrl = (np.subtract(c[y], ctrl))
                cBarra[y][0] = ctrl[0]

    return cBarra

def choosingJValue(cBarra):
    counter = 0
    for z in cBarra:
        if (z[0]<0):
            return counter+1
        else:
            counter = counter +1
    return 0

def calculatingTheta(x, d, AB):
    theta = []
    ver = False
    for y in AB:
        if ((d[y-1][0] < 0)):
            ctrl = -1*(x[y-1][0])/d[y-1][0]
            if (ver == False):
                theta.append(ctrl)
                theta.append(y)
                ver = True
            if ((ctrl < theta[0])):
                theta[0] = ctrl
                theta[1] = y

    return theta

def calculatingVectorY(x, theta,d, n):
    ctrl = np.dot(theta[0], d)
    ctrl = np.add(x, ctrl)
    return ctrl

def updateValues(AB, B, y, IVNBCRN, theta, A, m):
    ctrlAB = AB
    ctrlB = []
    counter = 0
    ctrl = []
    for w in AB:
        if (w == theta[1]):
            ctrlAB[counter] = IVNBCRN
        counter = counter + 1

    for w in range(len(AB)):
        for y in ctrlAB:
            ctrl.append(A[w][y - 1])
        ctrlB.append(ctrl)
        ctrl = []


    return [ctrlAB, ctrlB]

run = True

B = []
'2 1 1 0 0; 1 1 0 1 0; 1 0 0 0 1'

A = [[2.0, 1.0, 1.0, 0, 0],
     [1.0, 1.0, 0, 1.0, 0],
     [1.0, 0, 0, 0, 1.0]]

m = len(A) #Número de restrições
#n = len(x) #Número de variáveis
n = 5

c = [[-3],
     [-2],
     [0],
     [0],
     [0]] #vetor C

b = [[100],
     [80],
     [40]] #vetor b


AB = [3, 4, 5] #Índices das colunas/variáveis básicas

#LEMBRAR DE DAR SORT NO VETOR AB

#========================================================================================================================================


B = buidlingMatrixB(m, AB, A)

invB = (inv(B)).astype(float)  # astype os valores para float

XB = np.dot(invB, b)  # Calcula o XB (Xís da base)

x = buildingInitialVectorX(n, XB, AB) #Base inicial

cBarraCounter = 0
dCounter = 0

while(run == True):

    invB = (inv(B)).astype(float)  # astype os valores para float

    XB = np.dot(invB, b)  # Calcula o XB (Xís da base)

    CB = buildingVectorCB(c, AB)  # Vetor custo com os índices da base

    cBarra = computingNonBasicReducedCost(c, AB, invB, A, n, CB) #vetor dos custos reduzidos

    for w in cBarra:
        if (w[0]>=0):
            cBarraCounter = cBarraCounter+1
    if (cBarraCounter==len(cBarra)):
        print('finished')
        break
    cBarraCounter = 0


    IVNBCRN = choosingJValue(cBarra) #Índice da Variável Não Básica com Custo Reduzido Negativo

    d = computingDVector(invB, A, IVNBCRN, AB, n)

    for p in d:
        if(p[0]<0):
            dCounter = dCounter+1
    if (dCounter==0):
        print('Custo ótimo = -infinito\nFINISHED')
        break
    dCounter = 0

    theta = calculatingTheta(x,d,AB) #Vetor com o primeiro valor sendo o theta ótimo e o segundo o L

    y = calculatingVectorY(x,theta,d,n)

    x = y

    upV = updateValues(AB, B, y, IVNBCRN, theta, A, m)

    B = upV[1]
    AB = upV[0]

    print('Vector x \/\n')
    print(x)
    print('cBarra \/\n')
    print(cBarra)
    print('AB \/\n')
    print(AB)
    print('========FIM DA ITERAÇÃO========')

print('===================')
print(x)
