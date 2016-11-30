import math
import random as rd
import matplotlib.pyplot as plt
import numpy as np
import time
import sys
from scipy.spatial import distance
from heapq import *
from MST import *


def readData(tspfile):
    data = []
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
    return np.array(data)
    
def computeDistanceMatrix(data):
    inf = float("inf")
    distancemetric = distance.squareform(distance.pdist(data))
    nnode = data.shape[0]
    distancemetric += np.diag(np.ones(nnode) * inf)
    return distancemetric


def calTotalLen(list, distancematrix):
    sum = distancematrix[list[0], list[-1]]
    for i in range(0, len(list) - 1):
        sum += distancematrix[list[i], list[i + 1]]
    return sum

def calPartLen(list, distancematrix):
    sum = 0
    for i in range(0, len(list) - 1):
        sum += distancematrix[list[i], list[i + 1]]
    return sum

def findLbAB(a, list, distancematrix):
    min = float("inf")
    for i in range(0, len(list)):
        if distancematrix[a, list[i]] < min: min = distancematrix[a, list[i]]
    return min
    
def getlowerboundbyMST(distancematrix,tempList1,tempList2):
    vertices,edges = parseEdges(tempList2, distancematrix)
    MST,MST_edges = computeMST(vertices,edges)
    lb = calPartLen(tempList1, distancematrix) + MST + \
        findLbAB(tempList1[0], tempList2, distancematrix) + findLbAB(tempList1[-1], tempList2, distancematrix)
    return lb
    
    
def main():
    data=readData('./DATA-2/Cincinnati.tsp')
    distancematrix = computeDistanceMatrix(data)
    n = distancematrix.shape[0]

    heap = []
    head = (0,[], range(n))
    heappush(heap, head)
    bestLen = float("inf")
    while len(heap) != 0:
        (tempLb, List1, List2) = heappop(heap)

        for i in range(0, len(List2)):
            tempList1 = list(List1)
            tempList1.append(List2[i])
            tempList2 = List2[:i] + List2[i+1 :]
            if len(tempList2) == 0:
                if calTotalLen(tempList1, distancematrix) < bestLen: bestLen = calTotalLen(tempList1, distancematrix)
            else:
                lb = getlowerboundbyMST(distancematrix,tempList1,tempList2)
                if lb < bestLen:
                    heappush(heap, (lb, tempList1, tempList2))
    print bestLen
# vertices,edges = parseEdges([0,1,2,3,4,5,6,7,8,9], distancematrix)
# print computeMST(vertices,edges)


if __name__ == '__main__':
    # run the experiments
    main()
