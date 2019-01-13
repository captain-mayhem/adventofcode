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
        self.distance = Inf
        
    def switchTool(self):
        if self.type == Rocky:
            if self.tool == Torch:
                return Gear
            else:
                return Torch
        if self.type == Wet:
            if self.tool == Gear:
                return Neither
            else:
                return Gear
        if self.type == Narrow:
            if self.tool == Torch:
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
        field.distance = 0
        field.tool = Torch
        queue = [field]
        while len(queue) > 0:
            field = queue.pop(0)
            adjFs = self.adjacentFields(field)
            for adj in adjFs:
                dist, tool = self.calcDistance(field, adj)
                if dist < adj.distance:
                    adj.distance = dist
                    adj.tool = tool
                    queue.append(adj)
            field.tool = field.switchTool()
            for adj in adjFs:
                dist, tool = self.calcDistance(field, adj)
                dist += 7
                if dist < adj.distance:
                    adj.distance = dist
                    adj.tool = tool
                    queue.append(adj)

    def calcDistance(self, f1, f2):
        dist = f1.distance+1
        tool = f1.tool
        if f2.type == Rocky and f1.tool == Neither:
            dist = Inf
            #tool = f1.switchTool()
        elif f2.type == Wet and f1.tool == Torch:
            dist = Inf
            #tool = f1.switchTool()
        elif f2.type == Narrow and f1.tool == Gear:
            dist = Inf
            #tool = f1.switchTool()
        elif f2.pos == self.target and f1.tool != Torch and dist < Inf:
            dist += 7
            tool = Torch
        return dist, tool


depth = int(input[0][7:])
tgt = input[1][8:].split(',')
tgt = vec2(int(tgt[0]), int(tgt[1]))
print('input',depth,tgt)
map = Map(tgt+vec2(100,100), tgt, depth)
map.calcDistances()

print(map.at(tgt).distance)

    



