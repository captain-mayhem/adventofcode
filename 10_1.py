import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_10_1.txt'), 'r')
input = file.readlines()

class Point:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
     
    def step(self, num):
        self.x += num*self.vx
        self.y += num*self.vy

class Simulator:
    def __init__(self):
        self.points = []
    
    def addPoint(self, posx, posy, velx, vely):
        p = Point(posx, posy, velx, vely)
        self.points.append(p)
        
    def step(self, num):
        for p in self.points:
            p.step(num)
            
    def rect(self):
        xmin = 100000
        ymin = 100000
        xmax = -100000
        ymax = -100000
        for p in self.points:
            if p.x < xmin:
                xmin = p.x
            if p.x > xmax:
                xmax = p.x
            if p.y < ymin:
                ymin = p.y
            if p.y > ymax:
                ymax = p.y
        return (xmin,ymin,xmax-xmin,ymax-ymin)
            
    def display(self, xo, yo, w, h):
        count = 0
        field = [['.' for x in range(w)] for y in range(h)]
        for p in self.points:
            if p.x < xo or p.y < yo:
                continue
            if p.x >= w+xo or p.y >= h+yo:
                continue
            count += 1
            field[p.y-yo][p.x-xo] = '#'
        if count < 1:
            return
        str = ''
        for y in range(h):
            for x in range(w):
                str += field[y][x]
            str += '\n'
        print(str)

sim = Simulator()

for line in input:
    tmp1 = line.split('>')
    pos = tmp1[0].split('<')
    velo = tmp1[1].split('<')
    tmp1 = pos[1].split(',')
    posx = int(tmp1[0])
    posy = int(tmp1[1])
    tmp1 = velo[1].split(',')
    velx = int(tmp1[0])
    vely = int(tmp1[1])
    sim.addPoint(posx, posy, velx, vely)

minheight = 10000
minstep = 0
for i in range(20001):
    sim.step(1)
    r = sim.rect()
    if r[3] < minheight:
        minheight = r[3]
        minstep = i
sim.step(-20000)
print(minstep)
    
sim.step(minstep-2)
for i in range(5):
    print(minstep+i+-2+1)
    r = sim.rect()
    print(r)
    sim.step(1)
    sim.display(r[0], r[1], r[2], r[3])