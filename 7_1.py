import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_7_1.txt'), 'r')
input = file.readlines()

class Node:
    def __init__(self,x):
        self.id = chr(ord('A')+x)
        self.parents = []
        self.children = []
    
    def __lt__(self, other):
        return self.id < other.id
      
    def __repr__(self):
        return self.id

class Graph:
    def __init__(self,vertices): 
        self.graph = [Node(x) for x in range(vertices)]
        self.roots = []

    def addEdge(self,u,v):
        u = ord(u) - ord('A')
        v = ord(v) - ord('A')
        frm = self.graph[u]
        to = self.graph[v]
        frm.children.append(to)
        to.parents.append(frm)

    def sort(self):
        for node in self.graph:
            if len(node.parents) == 0:
                self.roots.append(node)
        self.roots.sort()
        ret = ''
        while len(self.roots) > 0:
            n = self.roots.pop(0)
            for chd in n.children:
                chd.parents.remove(n)
                val = str(chd)
                if chd not in self.roots and val not in ret and len(chd.parents) == 0:
                    self.roots.append(chd)
            self.roots.sort()
            ret += str(n)
        print(self.roots)
        
        print(ret)

g = Graph(26)
for line in input:
    frm = line[5]
    to = line[36]
    g.addEdge(frm, to)
    
g.sort()