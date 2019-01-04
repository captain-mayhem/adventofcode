import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_20_1.txt'), 'r')
input = file.read()

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
    
       
class Room:
    def __init__(self, pos):
        self.pos = pos
        self.doors = {}
        self.distance = 999999

class Map:
    def __init__(self):
        self.pos = vec2(0,0)
        self.rooms = {}
        self.rooms[self.pos] = Room(self.pos)
        self.savedpos = []
        
    def addChar(self, ch):
        if ch == 'W':
            self.addDoor(vec2(-1, 0))
        elif ch == 'N':
            self.addDoor(vec2(0, -1))
        elif ch == 'E':
            self.addDoor(vec2(1, 0))
        elif ch == 'S':
            self.addDoor(vec2(0, 1))
        elif ch == '(':
        	    self.branch()
        elif ch == ')':
        	    self.endBranch()
        elif ch == '|':
        	    self.nextOption()
        elif ch == '^' or ch == '$' or ch == '\n':
        	    return
        else:
            print(ch)
        
    def addDoor(self, direct):
        room = self.rooms[self.pos]
        nextpos = self.pos + direct
        if nextpos not in self.rooms:
            nextroom = Room(nextpos)
            self.rooms[nextpos] = nextroom
        else:
            nextroom = self.rooms[nextpos]
        room.doors[direct] = nextroom
        nextroom.doors[-direct] = room
        self.pos = nextpos
        
    def branch(self):
        self.savedpos.append(self.pos)
        
    def endBranch(self):
        self.pos = self.savedpos.pop(-1)
        
    def nextOption(self):
        self.pos = self.savedpos[-1]
        
    def calcDistances(self):
        self.pos = vec2(0, 0)
        room = self.rooms[self.pos]
        room.distance = 0
        queue = [room]
        while len(queue) > 0:
            room = queue.pop(0)
            dist = room.distance+1
            for _,adj in room.doors.items():
                if dist < adj.distance:
                    adj.distance = dist
                    queue.append(adj)
                    
    def farthestRoom(self):
        farthest = 0
        for _,r in self.rooms.items():
            if r.distance > farthest:
                farthest = r.distance
        return farthest
        
    def __repr__(self):
        return str(self.rooms)

map = Map()
for ch in input:
    map.addChar(ch)
#print(map)
map.calcDistances()
print(map.farthestRoom())
    



