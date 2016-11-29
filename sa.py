import math
import random as rd
import matplotlib.pyplot as plt
import time
import sys

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
    if c - a <= 2: return
    b = a + 1
    d = c - 1
    sa = sol[a]
    sb = sol[b]
    sd = sol[d]
    sc = sol[c]
    dE = calTwoPoint(data, sa, sb) + calTwoPoint(data, sd, sc) - \
         (calTwoPoint(data, sa, sd) + calTwoPoint(data,sb, sc))
    if dE > 0:
        p = 1.0
    else:
        p = math.exp(dE/T)
    if p == 1.0:
        chooseNeighbor(sol, b, d)
    elif rd.uniform(0,1) < p:
        chooseNeighbor(sol, b, d)

def main():
    startTime = time.time() #time in seconds
    data = []
    plot = []
    Temperature = []
    T =  10000.0;
    coolingRate = 0.0001
    Tmin = 1
    readData('./DATA-2/Toronto.tsp',data)
    iniSol = initsol(len(data))
    randSol(iniSol)

    while(T > Tmin):
        doNeigbhour(iniSol, data, T)
        T *= 1 - coolingRate
        plot.append(calTotalDis(iniSol, data))
        Temperature.append(T)
    print plot[-1]
    total_time = (time.time() - startTime) * 1000
    print total_time
    plt.plot(plot)
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.title('Solution for Toronto by SA')
    plt.show()


if __name__ == '__main__':
    main()