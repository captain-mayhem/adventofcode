import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_22_1.txt'), 'r')
input = file.readlines()

Rocky = 0
Wet = 1
Narrow = 2

Neither = 0
Torch = 1
Gear = 2   

Inf = 99999


class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __hash__(self):
        return self.y * 1000 + self.x
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        return vec2(self.x+other.x, self.y+other.y)
    
    def __neg__(self):
        return vec2(-self.x, -self.y)
        
    def __repr__(self):
        return 'vec2('+str(self.x)+','+str(self.y)+')'
    
       
class Field:
    def __init__(self):
        self.geoidx = 0
        self.erosion = 0
        self.distance = [Inf, Inf, Inf]
        
    def getTool(self, tool):
        if self.type == Rocky:
            if tool == 1:
                return Gear
            else:
                return Torch
        if self.type == Wet:
            if tool == 1:
                return Neither
            else:
                return Gear
        if self.type == Narrow:
            if tool == 1:
                return Neither
            else:
                return Torch

class Map:
    def __init__(self, dims, target, depth):
        self.target = target
        self.dims = dims
        self.depth = depth
        self.fields = [[Field() for x in range(self.dims.x)] for y in range(self.dims.y)]        
        for y in range(self.dims.y):
            for x in range(self.dims.x):
                self.calcGeo(vec2(x,y))
                
    def at(self, pos):
         return self.fields[pos.y][pos.x]
                
    def calcGeo(self, pos):
        field = self.at(pos)
        field.pos = pos
        if pos == vec2(0,0) or pos == self.target:
            field.geoidx = 0
        elif pos.y == 0:
            field.geoidx = 16807*pos.x
        elif pos.x == 0:
            field.geoidx = 48271*pos.y
        else:
            f1 = self.at(pos+vec2(-1,0))
            f2 = self.at(pos+vec2(0,-1))
            field.geoidx = f1.erosion*f2.erosion
        field.erosion = (field.geoidx+self.depth)%20183
        field.type = field.erosion%3
        
    def risk(self):
        sum = 0
        for y in range(self.target.y+1):
            for x in range(self.target.x+1):
                sum += self.at(vec2(x,y)).type
        return sum
        
    def adjacentFields(self, f):
        adj = []
        if f.pos.x > 0:
            adj.append(self.at(f.pos+vec2(-1,0)))
        if f.pos.y > 0:
            adj.append(self.at(f.pos+vec2(0,-1)))
        if f.pos.x < self.dims.x-1:
            adj.append(self.at(f.pos+vec2(1,0)))
        if f.pos.y < self.dims.y-1:
            adj.append(self.at(f.pos+vec2(0,1)))
        
        return adj
        
    def calcDistances(self):
        self.pos = vec2(0, 0)
        field = self.at(self.pos)
        field.distance[Torch] = 0
        queue = [field]
        while len(queue) > 0:
            field = queue.pop(0)
            t1 = field.getTool(0)
            t2 = field.getTool(1)
            if field.distance[t1] + 7 < field.distance[t2]:
              field.distance[t2] = field.distance[t1] + 7
            if field.distance[t2] + 7 < field.distance[t1]:
              field.distance[t1] = field.distance[t2] + 7
            adjFs = self.adjacentFields(field)
            for adj in adjFs:
                dist = self.calcDistance(field, adj, t1)
                if dist < adj.distance[t1]:
                    adj.distance[t1] = dist
                    queue.append(adj)
            for adj in adjFs:
                dist = self.calcDistance(field, adj, t2)
                if dist < adj.distance[t2]:
                    adj.distance[t2] = dist
                    queue.append(adj)

    def calcDistance(self, f1, f2, tool):
        dist = f1.distance[tool]+1
        if f2.type == Rocky and tool == Neither:
            dist = Inf
            #tool = f1.switchTool()
        elif f2.type == Wet and tool == Torch:
            dist = Inf
            #tool = f1.switchTool()
        elif f2.type == Narrow and tool == Gear:
            dist = Inf
            #tool = f1.switchTool()
        return dist


depth = int(input[0][7:])
tgt = input[1][8:].split(',')
tgt = vec2(int(tgt[0]), int(tgt[1]))
print('input',depth,tgt)
map = Map(tgt+vec2(100,100), tgt, depth)
map.calcDistances()

print(map.at(tgt).distance[Torch])

    



