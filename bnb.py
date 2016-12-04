import math
import numpy as np
import time
import sys
#from scipy.spatial import distance
from heapq import *
from hc import *
from MST1 import *
import glob


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

def computeDistanceMatrix1(data):
    inf = float("inf")
    distancemetric = distance.squareform(distance.pdist(data))
    nnode = data.shape[0]
    distancemetric += np.diag(np.ones(nnode) * inf)
    return distancemetric

def computeDistanceMatrix(data):
    inf = float("inf")
    nnode = data.shape[0]
    distancemetric = np.zeros((nnode,nnode))
    for i in range(nnode):
        ix = data[i,0]
        iy = data[i,1]
        for j in range(nnode):
            if j != i:
                jx = data[j,0]
                jy = data[j,1]
                distancemetric[i,j] = math.sqrt((ix - jx)**2 + (iy - jy)**2)
            else:
                distancemetric[i,i] = inf 
    return distancemetric



def getHead(n):
    list = []
    for i in range(0, n):
        list.append(i)
    return list


def getLowerBoundbyReduction(distancematrix,tempList1): 
    distancematrix1 = np.copy(distancematrix)
    inf = float("inf")
    pathsum = 0
    if len(tempList1)!=0 and len(tempList1)!=1:
        for i in range(len(tempList1)-1):
            pathsum = pathsum+distancematrix1[tempList1[i],tempList1[i+1]]
            distancematrix1[tempList1[i+1],tempList1[i]] = inf
        distancematrix1 = distancematrix1[tempList1[:-1],] 
        distancematrix1 = distancematrix1[:,tempList1[1:]] 
    rowmin = distancematrix1.min(axis = 1)
    temprowsum = rowmin.sum()
    colmin = distancematrix1.min(axis = 0)
    tempcolsum = colmin.sum()
    return tempcolsum+temprowsum+pathsum
    

   

def dfs(list1, list2, edges, distancematrix,cuttime):
    global best
    global bestpath
    global start_time

    total_time = (time.time() - start_time)
    if total_time > cuttime:
        return
    tempheapq = []
    
    
    for i in range(0, len(list2)):
        tempList1 = list(list1)
        tempList1.append(list2[i])
        tempList2 = list2[:i] + list2[i+1 :]
        lb = calMst(tempList1, tempList2, edges, distancematrix)
        heappush(tempheapq,(lb,tempList1,tempList2))

    while len(tempheapq)!=0:
        (tempLb, tempList1, tempList2) = heappop(tempheapq)
        if tempLb > best:
            return 
        if len(tempList2) == 0:
            best = tempLb
            bestpath = list1
            total_time = (time.time() - start_time)
            print best,bestpath,total_time
            return       
        dfs(tempList1, tempList2, edges, distancematrix,cuttime)

    return 


def bfs(heap, edges, distancematrix,cuttime):
     global best
     global bestpath
     global start_time

     while len(heap) != 0:
        (tempLb, List1, List2) = heappop(heap)
        for i in range(0, len(List2)):
            tempList1 = list(List1)
            tempList1.append(List2[i])
            tempList2 = List2[:i] + List2[i+1 :]
            total_time = (time.time() - start_time)
            if total_time > cuttime:
                return
            if len(tempList2) == 0:
                if calTotalLen(tempList1, distancematrix) < best: 
                    best = calTotalLen(tempList1, distancematrix)
                    bestpath = tempList1
                    print best,bestpath,total_time
                    
            else:
                tempV = set(tempList2)
                tempE = getEdge(tempList2, edges)
                MST = computeMST(tempV,tempE)
#               lb = getLowerBoundbyReduction(distancematrix,tempList1)
                lb = calPartLen(tempList1, distancematrix) + MST + \
                     findLbAB(tempList1[0], tempList2, distancematrix) + findLbAB(tempList1[-1], tempList2, distancematrix)
                if lb < best:
                    heappush(heap, (len(tempList2), tempList1, tempList2))
                    



def TSP(filename,isInitialize,isDFS,cuttime):
    global best
    global start_time
    data=readData(filename)
    distancematrix = computeDistanceMatrix(data)
    n = distancematrix.shape[0]
    edges = getTotalEdge(n, distancematrix)

    
    if isInitialize: 
        hc = []
        iniSol = initsol(len(data))
        randSol(iniSol)
        move = True
        while move == True:
            move = False
            move = doNeigbhour(iniSol, data, move)
            hc.append(calTotalDis(iniSol, data))
    else:
        best = float("inf")

    print best
    start_time = time.time()
    if isDFS:
        dfs([0],range(1,n), edges, distancematrix,cuttime)
    else:
        heap = []
        head = (0,[], getHead(n))
        heappush(heap, head)
        bfs(heap, edges, distancematrix,cuttime)
        




if __name__ == '__main__':
    # run the experiments
    isInitialize = 0
    isDFS=1
    cuttime = 3600
    ifile = int(sys.argv[1])

    allfilename = glob.glob('./DATA-2/*.tsp')
    print allfilename
    filename = allfilename[ifile]
    cityname = filename[9:-4]
    print cityname
    TSP(filename,isInitialize,isDFS,cuttime)
    print best,bestpath,cityname
