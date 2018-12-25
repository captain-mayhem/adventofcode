import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_18_1.txt'), 'r')
input = file.readlines()

text = '''.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.'''
#input = text.split('\n')

Empty = 0
Trees = 1
Lumber = 2

class Forest:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fields = [[Empty for x in range(width)] for y in range(height)]
        
    def __repr__(self):
      ret = ''
      for line in self.fields:
        lret = ''
        for x in line:
          if x == Empty:
            lret += '.'
          elif x == Trees:
            lret += '|'
          elif x == Lumber:
            lret += '#'
        lret += '\n'
        ret += lret
      return ret

    def addField(self, x, y, field):
        if field == '.':
            return
        elif field == '#':
            self.fields[y][x] = Lumber
        elif field == '|':
            self.fields[y][x] = Trees
        else:
            print(field)
            
    def getAdjacencies(self, x, y):
      ret = []
      if y > 0:
        ret.append(self.fields[y-1][x])
        if x > 0:
          ret.append(self.fields[y-1][x-1])
        if x < self.width-1:
          ret.append(self.fields[y-1][x+1])
      if y < self.height-1:
        ret.append(self.fields[y+1][x])
        if x > 0:
          ret.append(self.fields[y+1][x-1])
        if x < self.width-1:
          ret.append(self.fields[y+1][x+1])
      if x > 0:
        ret.append(self.fields[y][x-1])
      if x < self.width-1:
        ret.append(self.fields[y][x+1])
      return ret
      
    def getCounts(self, adj):
      counts = [0,0,0]
      for a in adj:
        counts[a] += 1
      return counts
        
    def simulate(self):
      newfield = [[Empty for x in range(self.width)] for y in range(self.height)]
      for y in range(self.height):
        for x in range(self.width):
          field = self.fields[y][x]
          counts = self.getCounts(self.getAdjacencies(x, y))
          if field == Empty:
            if counts[Trees] >= 3:
              newfield[y][x] = Trees
            else:
              newfield[y][x] = Empty
          if field == Trees:
            if counts[Lumber] >= 3:
              newfield[y][x] = Lumber
            else:
              newfield[y][x] = Trees
          if field == Lumber:
            if counts[Lumber] >= 1 and counts[Trees] >= 1:
              newfield[y][x] = Lumber
            else:
              newfield[y][x] = Empty
      self.fields = newfield
      
    def countResources(self):
      trees = 0
      lumber = 0
      for y in range(self.height):
        for x in range(self.width):
          if self.fields[y][x] == Trees:
            trees += 1
          if self.fields[y][x] == Lumber:
              lumber += 1
      return trees, lumber

f = Forest(50, 50)

for y in range(len(input)):
    line = input[y]
    for x in range(len(line)-1):
        f.addField(x, y, line[x])

last_tree = 0
last_lumber = 0
for iter in range(10):
  for x in range(100):
    #print(f)
    f.simulate()
  #print(f)
    
  t,l = f.countResources()
  
  print(t, l, t*l, t-last_tree, l-last_lumber, t*l-last_tree*last_lumber)
  last_tree = t
  last_lumber = l
print(f)

iter = int((1000000000-1000)/700)*700
target = 1000000000-iter
print(target)


