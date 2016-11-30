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



