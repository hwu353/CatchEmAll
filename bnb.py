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

rank = dict()
parent = dict()

def makeset(vertice):
    parent[vertice] = vertice
    rank[vertice] = 0

def find(vertice):
    if parent[vertice] == vertice:
        return parent[vertice]
    else:
        return find(parent[vertice])

def union(vertice1, vertice2):
    root1 = find(vertice1)
    root2 = find(vertice2)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
            if rank[root1] == rank[root2]:
               rank[root2] += 1

#parseEdges
def parseEdges(list, distancematrix):
    vertices = set()
    edges = []
    if len(list) == 0: return vertices,edges
    for i in range(0,len(list)):
        vertices.add(int(list[i]))
        for j in range(i, len(list)):
            edges.append({'u': int(list[i]), 'v' : int(list[j]), 'weight' : float(distancematrix[list[i], list[j]])})
            edges.append({'u': int(list[j]), 'v' : int(list[i]), 'weight' : float(distancematrix[list[j], list[i]])})
    return vertices,edges

#sort by weight
def weight(s):
    return s['weight']

def sortedges(edges):
    return sorted(edges, key = weight)

#computeMST
def computeMST(vertices, edges):
    edges = sortedges(edges)
    MST = 0
    MST_edges = []
    for each in vertices:
        makeset(each)
    for each in edges:
        u = each['u']
        v = each['v']
        weight1 = each['weight']
        if find(u) != find(v):
            union(u, v)
            MST_edges.append({'u': u, 'v' : v, 'weight' : weight1})
            MST += weight1
    return MST,MST_edges

       
# def TSPBnB(distancematrix):
#     visitedNodes = 0 # to keep track of how many nodes we 'visit'
#     optimalTour = None # Until we discover the first tour
#     priorityQueue = []
#     currentNode = [0]
#     heappush(priorityQueue, currentNode)
#
#
#     return 1

def getHead(n):
    list = []
    for i in range(0, n):
        list.append(i)
    return list

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

def main():
    data=readData('./DATA-2/Cincinnati.tsp')
    distancematrix = computeDistanceMatrix(data)
    n = distancematrix.shape[0]

    heap = []
    head = (0,[], getHead(n))
    heappush(heap, head)
    bestLen = float("inf")

    while len(heap) != 0:
        (tempLb, List1, List2) = heappop(heap)
        print List1
        print List2
        for i in range(0, len(List2)):
            tempList1 = list(List1)
            tempList1.append(List2[i])
            tempList2 = List2[:i] + List2[i+1 :]
            if len(tempList2) == 0:
                if calTotalLen(tempList1, distancematrix) < bestLen: bestLen = calTotalLen(tempList1, distancematrix)
            else:
                vertices,edges = parseEdges(tempList2, distancematrix)
                MST,MST_edges = computeMST(vertices,edges)
                lb = calPartLen(tempList1, distancematrix) + MST + \
                     findLbAB(tempList1[0], tempList2, distancematrix) + findLbAB(tempList1[-1], tempList2, distancematrix)
                if lb < bestLen:
                    heappush(heap, (lb, tempList1, tempList2))
    print bestLen
# vertices,edges = parseEdges([0,1,2,3,4,5,6,7,8,9], distancematrix)
# print computeMST(vertices,edges)


if __name__ == '__main__':
    # run the experiments
    main()
