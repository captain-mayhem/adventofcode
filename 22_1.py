import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_22_1.txt'), 'r')
input = file.readlines()

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

class Map:
    def __init__(self, target, depth):
        self.target = target
        self.dims = target + vec2(1,1)
        self.depth = depth
        self.fields = [[Field() for x in range(self.dims.x)] for y in range(self.dims.y)]        
        for y in range(self.dims.y):
            for x in range(self.dims.x):
                self.calcGeo(vec2(x,y))
                
    def at(self, pos):
         return self.fields[pos.y][pos.x]
                
    def calcGeo(self, pos):
        field = self.at(pos)
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
        for y in range(self.dims.y):
            for x in range(self.dims.x):
                sum += self.at(vec2(x,y)).type
        return sum

depth = int(input[0][7:])
tgt = input[1][8:].split(',')
tgt = vec2(int(tgt[0]), int(tgt[1]))
print('input',depth,tgt)
map = Map(tgt, depth)

print(map.risk())

    



