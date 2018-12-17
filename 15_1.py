import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_15_1.txt'), 'r')
input = file.readlines()

height = len(input)
width = len(input[0])-1


class Field:
  def __init__(self):
    self.obj = None

class Wall(Field):
  def __init__(self):
    Field.__init__(self)
    dummy = 0
    
class Creature:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
  def __lt__(self, other):
    if (self.y == other.y):
      return self.x < other.x
    return self.y < other.y
    
  def isTargetReachable(self, world):
    neighbors = world.getAdjacentPoints((self.x, self.y))
    for neighbour in neighbors:
      obj = world.fields[neighbour[1]][neighbour[0]].obj
      if isinstance(obj, self.target):
        return True
    return False
    
  def pos(self):
    return (self.x, self.y)
    
  def turn(self, world):
    if not self.isTargetReachable(world):
      self.move(world)
  
  def move(self, world):
    points = []
    cheapest = 999
    walkmap = world.walkmap(self)
    #for y in walkmap:
    #  print(y)
    for unit in world.units:
      if isinstance(unit, self.target):
        #print(unit, self.target, unit.pos())
        adj = world.getAdjacentPoints(unit.pos())
        for point in adj:
          if walkmap[point[1]][point[0]] < cheapest:
            cheapest = walkmap[point[1]][point[0]]
            points = [point]
          elif walkmap[point[1]][point[0]] == cheapest and cheapest != 999:
            points.append(point)
    print(cheapest, points, '\n')
    
  
class Goblin(Creature):
  def __init__(self, x, y):
    Creature.__init__(self, x, y)
    self.target = Elf
    
class Elf(Creature):
  def __init__(self, x, y):
    Creature.__init__(self,x ,y)
    self.target = Goblin

class Dungeon:
  def __init__(self, w, h):
    self.width = w
    self.height = h
    print('World:', w, h)
    self.fields = [[None for x in range(w)] for y in range(h)]
    self.units = []
    
  def addTile(self, x, y, ch):
    if ch == '#':
      self.fields[y][x] = Wall()
    elif ch == '.':
      self.fields[y][x] = Field()
    elif ch == 'G':
      field = Field()
      field.obj = Goblin(x, y)
      self.units.append(field.obj)
      self.fields[y][x] = field
    elif ch == 'E':
      field = Field()
      field.obj = Elf(x, y)
      self.units.append(field.obj)
      self.fields[y][x] = field
    else:
      print(ch)
  
  def round(self):
    self.units.sort()
    for unit in self.units:
      unit.turn(self)
  
  def getAdjacentPoints(self, point):
    ret = []
    if point[1]-1 >= 0:
      ret.append((point[0], point[1]-1))
    if point[0]-1 >= 0:
      ret.append((point[0]-1, point[1]))
    if point[0]+1 < self.width:
      ret.append((point[0]+1, point[1]))
    if point[1]+1 < self.height:
      ret.append((point[0], point[1]+1))
    return ret
  
  def walkmap(self, creature):
    map = [[999 for x in range(self.width)] for y in range(self.height)]
    points = []
    map[creature.y][creature.x] = 0
    points.append((creature.x, creature.y))
    while len(points) > 0:
      point = points.pop(0)
      cost = map[point[1]][point[0]]+1
      neighbours = self.getAdjacentPoints(point)
      for neighbour in neighbours:
        field = self.fields[neighbour[1]][neighbour[0]]
        if (isinstance(field, Wall)):
          continue
        if field.obj != None:
          continue
        neighbourcost = map[neighbour[1]][neighbour[0]]
        if cost < neighbourcost:
          map[neighbour[1]][neighbour[0]] = cost
          points.append(neighbour)
    return map
    
dungeon = Dungeon(width, height)

for y in range(height):
  for x in range(width):
    dungeon.addTile(x, y, input[y][x])
    
dungeon.round()