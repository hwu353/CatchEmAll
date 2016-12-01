import math
import random as rd
import time
import sys
import matplotlib.pyplot as plt

def readData(tspfile, data):
    count = 0
    for line in open(tspfile,'r'):
            #skip line
            if(count <= 4):
                pass
            else:
                if(line.split()[0] == "EOF"):
                    break
                index = int(line.split()[0])
                x = float(line.split()[1])
                y = float(line.split()[2])
                data.append([x,y])
            count += 1

def calTwoPoint(data, i, j):
    ix = data[i][0]
    iy = data[i][1]
    jx = data[j][0]
    jy = data[j][1]
    return math.sqrt((ix - jx)**2 + (iy - jy)**2)

def initsol(num):
    sol = []
    for i in range(num):
        sol.append(i)
    return sol

def swap(array, i, j):
    temp = array[i]
    array[i] = array[j]
    array[j] = temp

def randSol(sol):
    length = len(sol)
    for i in range(0, length - 1):
        tempRand = rd.randint(i + 1, length - 1)
        swap(sol, i, tempRand)
    return sol

def calTotalDis(sol, data):
    length = len(sol)
    distance = calTwoPoint(data, sol[0], sol[length - 1])
    for i in range(length - 1):
        distance += calTwoPoint(data, sol[i], sol[i + 1])
    return distance


def chooseNeighbor(sol, b, d):
    reverse = []
    for i in range(d, b - 1, -1):
        reverse.append(sol[i])
    for i in range(b, d + 1):
        sol[i] = reverse[i - b]

def doNeigbhour(sol, data, T):
    length = len(sol)
    firstRd = rd.randint(0, length - 1)
    secondRd = rd.randint(0, length - 1)
    a = min(firstRd, secondRd)
    c = max(firstRd, secondRd)
    if c - a <= 2:
        return
    b = a + 1
    d = c - 1
    sa = sol[a]
    sb = sol[b]
    sc = sol[c]
    sd = sol[d]
    dE = (calTwoPoint(data, sa, sb) + calTwoPoint(data, sd, sc)) - (calTwoPoint(data, sa, sd) + calTwoPoint(data, sb, sc))
    if dE >= 0:
        p = 1
    else:
        p = math.e**(dE/T)
    if p == 1:
        chooseNeighbor(sol, b, d)
    elif rd.uniform(0,1) < p:
        chooseNeighbor(sol, b, d)

def hillClimb (sol, data, move):

    length = len(sol)
    maxSteps = length**2
    steps=1

    while steps < maxSteps:
        firstRd = rd.randint(0, length - 1)
        secondRd = rd.randint(0, length - 1)
        a = min(firstRd, secondRd)
        c = max(firstRd, secondRd)
        if c - a <= 2:
            continue
        b = a + 1
        d = c - 1
        sa = sol[a]
        sb = sol[b]
        sc = sol[c]
        sd = sol[d]
        dE = (calTwoPoint(data, sa, sb) + calTwoPoint(data, sd, sc)) - (calTwoPoint(data, sa, sd) + calTwoPoint(data, sb, sc))
        steps+=1
        if dE > 0:
            chooseNeighbor(sol, b, d)
            move = True
            break
    return move


def HC_run(cutoff,data):
    start_time = time.time()
    dist=0
    iniSol = initsol(len(data))
    randSol(iniSol)
    calTotalDis(iniSol, data)
    move = True
    while move:
        if (time.time()-start_time)*1000 >= cutoff:
            break
        #count+=1
        move = False
        move = hillClimb(iniSol, data, move)
        dist = int(calTotalDis(iniSol,data))

    return dist

def main(runtime):
    data = []
    readData('./data/Roanoke.tsp',data)
    #running time for each instance in millisec
    distlist = []
    s = time.time()
    for i in range(50):
        sin = time.time()
        distan = HC_run(runtime,data)
        distlist.append(distan)
        endin = time.time()-sin
        print endin
    end = time.time()-s
    print end
    print distlist

if __name__ == '__main__':
    main(1150)


