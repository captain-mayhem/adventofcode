import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_7_1.txt'), 'r')
input = file.readlines()

from collections import defaultdict

class Graph:
    def __init__(self,vertices): 
        self.graph = defaultdict(list)
        self.V = vertices

    def addEdge(self,u,v):
        u = ord(u) - ord('A')
        v = ord(v) - ord('A')
        self.graph[u].append(v)

    def topologicalSortUtil(self,v,visited,stack):
        visited[v] = True
        for i in self.graph[v]:
            if visited[i] == False:
                self.topologicalSortUtil(i,visited,stack)
        stack.insert(0,v)

    def topologicalSort(self):
        visited = [False]*self.V
        stack = []
        for i in range(self.V-1,-1,-1):
            if visited[i] == False:
                self.topologicalSortUtil(i,visited,stack)
        ret = ''
        for s in stack:
            ret += chr(ord('A')+s)
        print(ret)

g = Graph(26)
diff = ord('A')
for line in input:
    frm = line[5]
    to = line[36]
    g.addEdge(frm, to)
    
g.topologicalSort()