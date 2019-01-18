import os
from queue import PriorityQueue

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_23_1.txt'), 'r')
input = file.readlines()

class vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __hash__(self):
        return self.z * 1000000 + self.y * 1000 + self.x
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __add__(self, other):
        return vec3(self.x+other.x, self.y+other.y, self.z+other.z)
    
    def __sub__(self, other):
        return vec3(self.x-other.x, self.y-other.y, self.z-other.z)
    
    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)
        
    def __repr__(self):
        return 'vec3('+str(self.x)+','+str(self.y)+','+str(self.z)+')'

    def mhLen(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

class Bot:
    def __init__(self, pos, radius):
        self.pos = pos
        self.r = radius
        
bots = []
maxrad = 0
maxbot = None

for line in input:
    tmp = line[5:-1].split('>')
    vec = tmp[0].split(',')
    pos = vec3(int(vec[0]), int(vec[1]), int(vec[2]))
    rad = int(tmp[1][4:])
    bot = Bot(pos, rad)
    if rad > maxrad:
        maxrad = rad
        maxbot = bot
    bots.append(bot)

def inRange(pos):
    botcount = 0    
    for bot in bots:
        vec = bot.pos - pos
        lenght = vec.mhLen()
        if lenght <= bot.r:
            botcount += 1
    return botcount
    
q = PriorityQueue()
for bot in bots: 
	    d = bot.pos.mhLen()
	    q.put((max(0, d - bot.r),1)) 
	    q.put((d + bot.r + 1,-1)) 
count = 0 
maxCount = 0 
result = 0 
while not q.empty(): 
	   dist,e = q.get() 
	   count += e 
	   if count > maxCount: 
	       result = dist 
	       maxCount = count 
print('dist:', result,'bots:',maxCount)

