import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_17_1.txt'), 'r')
input = file.readlines()

def parseArg(arg):
    tmp = arg.split('=')
    if '.' in tmp[1]:
        rng = tmp[1].split('..')
        ret = (int(rng[0]), int(rng[1]))
    else:
        ret = (int(tmp[1]),int(tmp[1]))
    return tmp[0], ret

def parseLine(line):
    tmp = line.split(' ')
    a1,b1 = parseArg(tmp[0][:-1])
    a2,b2 = parseArg(tmp[1])
    if a1 == 'x':
        return ((b1[0], b2[0]), (b1[1], b2[1]))
    else:
        return ((b2[0], b1[0]), (b2[1], b1[1]))
    
maxx = 1
minx = 99999
miny = 99999
maxy = 1
for line in input:
    tmp = parseLine(line)
    if tmp[1][0] > maxx:
        maxx = tmp[1][0]
    if tmp[0][0] < minx:
        minx = tmp[0][0]
    if tmp[0][1] < miny:
        miny = tmp[0][1]
    if tmp[1][1] > maxy:
        maxy = tmp[1][1]
    #print(tmp);

minx -= 1
maxx += 1

width = maxx-minx
height = maxy

class Water:
  def __init__(self, x, y, dir):
    self.x = x
    self.y = y
    self.dir = dir
    
  def __repr__(self):
    ret = str(self.x) + ' ' + str(self.y) + '(' + str(self.dir)+ ')'
    return ret

class World:
  Sand = 0
  Clay = 1
  Water = 2
  WaterStill = 3
  
  def __init__(self, width, height, xoffset):
    print('World:', width, height, 'x offset:', xoffset)
    self.xoffset = xoffset
    self.fields = [[self.Sand for x in range(width+1)] for y in range(height+1)]
    self.flows = [Water(500, 1, 0)]
    
  def __repr__(self):
    ret = ''
    y = 0
    water = 0
    for line in self.fields:
      lret = ''
      for x in line:
        if x == self.Clay:
          lret += '#'
        elif x == self.Water:
          lret += '|'
          water += 1
        elif x == self.WaterStill:
          lret += '~'
          water += 1
        else:
          lret += '.'
      lret += '\n'
      ret += lret
      y += 1
      #if y > 500:
      #  break
    print(water)
    return ret
      
  def drawLine(self, start, end, type):
    #print(start, end)
    if start[0] == end[0]:
      for y in range(start[1], end[1]+1):
        #print(start[0]-self.xoffset, y)
        self.fields[y][start[0]-self.xoffset] = type
    else:
      for x in range(start[0], end[0]+1):
        self.fields[start[1]][x-self.xoffset] = type
  
  def flowDown(self, water):
    y = water.y+1
    while 1:
      if y >= len(self.fields):
        break
      f = self.fields[y][water.x-self.xoffset]
      if f != self.Sand:
        break
      y += 1
    y -= 1
    self.drawLine((water.x, water.y), (water.x, y), self.Water)
    if water.y != y and f != self.Water and y+1 < len(self.fields):
      self.flows.append(Water(water.x, y, 1))
    
  def spreadDir(self, water, dir):
    x = water.x+dir
    hole = False
    while 1:
      f = self.fields[water.y][x-self.xoffset]
      below = self.fields[water.y+1][x-self.xoffset]
      if f == self.Clay or f == self.WaterStill:
        break
      x += dir
      if below == self.Sand or below == self.Water:
        x -= dir
        hole = True
        if below != self.Water:
          self.flows.append(Water(x, water.y, 0))
        break
    x -= dir
    return x, hole
    
  def grow(self, xstart, xend, y):
    for x in range(xstart, xend+1):
      f = self.fields[y][x-self.xoffset]
      if f == self.Water:
        self.flows.append(Water(x, y, 1))
    
  def spread(self, water):
    xstart, hole_start = self.spreadDir(water, -1)
    xend, hole_end = self.spreadDir(water, 1)
    hole = hole_start or hole_end
    if hole:
      self.drawLine((xstart, water.y), (xend, water.y), self.Water)
    else:
      self.drawLine((xstart, water.y), (xend, water.y), self.WaterStill)
      self.grow(xstart, xend, water.y-1)
    
  
  def simulate(self):
    if len(self.flows) == 0:
      return False
    water = self.flows.pop(0)
    if water.dir == 0:
      self.flowDown(water)
    else:
      self.spread(water)
    return True
    
  def countWater(self, miny):
    y = 0
    water = 0
    for line in self.fields:
      y += 1
      xv = 0
      if y <= miny:
        continue
      for x in line:
        if x == self.WaterStill:
          water += 1
    return water

world = World(width, height, minx)

for line in input:
  tmp = parseLine(line)
  world.drawLine(tmp[0], tmp[1], world.Clay)

#for i in range(5576):
while 1:
  if not world.simulate():
    break
    
for line in input:
  tmp = parseLine(line)
  world.drawLine(tmp[0], tmp[1], world.Clay)
print(world)
print('Water', world.countWater(miny))
#print(world.flows)
    



