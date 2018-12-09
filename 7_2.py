import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_7_1.txt'), 'r')
input = file.readlines()

class Node:
    def __init__(self,x):
        self.id = chr(ord('A')+x)
        self.parents = []
        self.children = []
        self.time = x + 1 + 60
    
    def __lt__(self, other):
        return self.id < other.id
      
    def __repr__(self):
        return self.id+str(self.time)

class Graph:
    def __init__(self,vertices): 
        self.graph = [Node(x) for x in range(vertices)]
        self.roots = []
        self.workers = []
        self.ret = ''
        self.time = 0

    def addEdge(self,u,v):
        u = ord(u) - ord('A')
        v = ord(v) - ord('A')
        frm = self.graph[u]
        to = self.graph[v]
        frm.children.append(to)
        to.parents.append(frm)
        
    def assignWork(self):
       num = min(5-len(self.workers), len(self.roots))
       for i in range(num):
           n = self.roots.pop(0)
           self.workers.append(n)
     
    def work(self):
        minval = 9999
        for n in self.workers:
            minval = min(minval, n.time)
        self.time += minval
        print(self.time, self.workers)
        newwork = []
        for n in self.workers:
            n.time -= minval
            if n.time == 0:
                self.finishWork(n)
            else:
                newwork.append(n)
        self.workers = newwork
        print(self.time, self.workers)
                   
    def finishWork(self, n):
        for chd in n.children:
            chd.parents.remove(n)            
            if len(chd.parents) == 0:
                self.roots.append(chd)
        self.roots.sort()
        self.ret += str(n)

    def sort(self):
        for node in self.graph:
            if len(node.parents) == 0:
                self.roots.append(node)
        self.roots.sort()
        while len(self.roots) > 0 or len(self.workers) > 0:
            #assign work
            self.assignWork()
            self.work()
        
        print(self.ret, self.time)

g = Graph(26)
for line in input:
    frm = line[5]
    to = line[36]
    g.addEdge(frm, to)
    
g.sort()