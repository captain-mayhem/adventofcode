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
    self.strength = 3
    self.lives = 200
    
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
    
  def isAlive(self):
    return self.lives > 0
    
  def turn(self, world):
    if self.lives <= 0:
      return False
    didSomething = False
    if not self.isTargetReachable(world):
      didSomething |= self.move(world)
    didSomething |= self.attack(world)
    return didSomething
  
  def move(self, world):
    points = []
    cheapest = 999
    walkmap = world.walkmap(self.pos())
    #for y in walkmap:
    #  print(y)
    for unit in world.units:
      if unit.isAlive() and isinstance(unit, self.target):
        #print(unit, self.target, unit.pos())
        adj = world.getAdjacentPoints(unit.pos())
        for point in adj:
          if walkmap[point[1]][point[0]] < cheapest:
            cheapest = walkmap[point[1]][point[0]]
            points = [point]
          elif walkmap[point[1]][point[0]] == cheapest and cheapest != 999:
            points.append(point)
            
    #no move possible
    if len(points) == 0:
        return False
        
    #destination found, search best step
    dest = self.getPreferredPoint(points)
    
    points = []
    cheapest = 999
    walkmap = world.walkmap(dest)
    adj = world.getAdjacentPoints(self.pos())
    for point in adj:
      if walkmap[point[1]][point[0]] < cheapest:
        cheapest = walkmap[point[1]][point[0]]
        points = [point]
      elif walkmap[point[1]][point[0]] == cheapest and cheapest != 999:
        points.append(point)
    step = self.getPreferredPoint(points)
    #print(cheapest, self.pos(), points, step, '\n')
    
    #now let's move
    world.fields[self.y][self.x].obj = None
    self.y = step[1]
    self.x = step[0]
    world.fields[self.y][self.x].obj = self  
    return True
  
  def getPreferredPoint(self, points):
    minx = 999
    miny = 999
    for point in points:
        if point[1] == miny:
            if point[0] < minx:
                minx = point[0]
        elif point[1] < miny:
            miny = point[1]
            minx = point[0]
    return (minx, miny)
    
  def attack(self, world):
    #select target
    enemies = []
    minlives = 999
    neighbors = world.getAdjacentPoints((self.x, self.y))
    for neighbour in neighbors:
      obj = world.fields[neighbour[1]][neighbour[0]].obj
      if isinstance(obj, self.target):
        if obj.lives < minlives:
          minlives = obj.lives
          enemies = [obj.pos()]
        elif obj.lives == minlives:
          enemies.append(obj.pos())
    if len(enemies) == 0:
      return False
    enemypos = self.getPreferredPoint(enemies)
    enemy = world.fields[enemypos[1]][enemypos[0]].obj
    
    enemy.lives -= self.strength
    if not enemy.isAlive():
      world.fields[enemypos[1]][enemypos[0]].obj = None
    return True
    
  
class Goblin(Creature):
  def __init__(self, x, y):
    Creature.__init__(self, x, y)
    self.target = Elf
    
class Elf(Creature):
  def __init__(self, x, y, strength):
    Creature.__init__(self,x ,y)
    self.target = Goblin
    self.strength = strength

class Dungeon:
  def __init__(self, w, h, strength):
    self.width = w
    self.height = h
    self.strength = strength
    print('Strength:', strength)
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
      field.obj = Elf(x, y, self.strength)
      self.units.append(field.obj)
      self.fields[y][x] = field
    else:
      print(ch)
  
  def round(self):
    self.units.sort()
    gameRunning = False
    for unit in self.units:
      gameRunning |= unit.turn(self)
    return gameRunning
  
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
  
  def walkmap(self, pos):
    map = [[999 for x in range(self.width)] for y in range(self.height)]
    points = []
    map[pos[1]][pos[0]] = 0
    points.append(pos)
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
    
  def sumLives(self):
    sum = 0
    for unit in self.units:
      if unit.isAlive():
        sum += unit.lives
    return sum
    
  def elvesDied(self):
    for unit in self.units:
      if isinstance(unit, Elf):
        if not unit.isAlive():
          return True
    return False
      
  def __repr__(self):
    result = ''
    for line in self.fields:
      lineret = ''
      for tile in line:
        if isinstance(tile, Wall):
          lineret += '#'
        elif isinstance(tile.obj, Goblin):
          lineret += 'G'
        elif isinstance(tile.obj, Elf):
          lineret += 'E'
        else:
          lineret += '.'
      lineret += '\n'
      result += lineret
    return result

elvesDied = True
strength = 3
while elvesDied:
  strength += 1
  dungeon = Dungeon(width, height, strength)

  for y in range(height):
    for x in range(width):
      dungeon.addTile(x, y, input[y][x])

  gameRunning = True 
  rounds = 0
  while gameRunning:   
    gameRunning = dungeon.round()
    if gameRunning:
      rounds += 1
  rounds -= 1

  #print(dungeon)
  livesLeft = dungeon.sumLives()
  print(rounds, livesLeft)
  print('Outcome:', rounds*livesLeft)
  elvesDied = dungeon.elvesDied()

