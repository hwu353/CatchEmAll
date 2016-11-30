import math
import random as rd
import matplotlib.pyplot as plt
import numpy as np
import time
import sys
from scipy.spatial import distance
from heapq import *


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

    
       
def TSPBnB(distancematrix):
    visitedNodes = 0 # to keep track of how many nodes we 'visit'
    optimalTour = None # Until we discover the first tour
    priorityQueue = []
    currentNode = [0]
    heappush(priorityQueue, currentNode)
    

    return 1

     
startTime = time.time()
data = []
data=readData('./DATA-2/Roanoke.tsp')
distancematrix = computeDistanceMatrix(data)

print data


