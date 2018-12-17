import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_13_1.txt'), 'r')
inputt = file.readlines()

Left = 0
Up = 1
Right = 2
Down = 3

class Car:
    def __init__(self, x, y, dir, id):
        self.x = x
        self.y = y
        self.dir = dir
        self.nextturn = Left
        self.crashed = False
        self.id = id
        
    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y
        
    def __repr__(self):
        return str(self.x)+'/'+str(self.y)+'/'+str(self.dir)
        
    def back(self):
        if self.dir == Up:
            self.y += 1
        elif self.dir == Right:
            self.x -= 1
        elif self.dir == Down:
            self.y -= 1
        elif self.dir == Left:
            self.x += 1
        else:
          print('Invalid')
    
    def move(self):
        #print(self.id, self.x, self.y)
        if self.dir == Up:
            self.y -= 1
        elif self.dir == Right:
            self.x += 1
        elif self.dir == Down:
            self.y += 1
        elif self.dir == Left:
            self.x -= 1
        else:
            print('Invalid direction',self.dir)
            
    def turn(self):
        turn = self.nextturn
        self.nextturn = (turn + 1) % 3
        return turn
        
class Grass:
    def __repr__(self):
      return ' '
    
class Lane:
    def getDir(self, car):
        return car.dir
        
    def __repr__(self):
      return '.'
        
class Intersection:
    def getDir(self, car):
        turn = car.turn()
        if turn == Up:
            return car.dir
        if turn == Left:
            return (car.dir-1)%4
        if turn == Right:
            return (car.dir+1)%4
        print('What')
        
    def __repr__(self):
      return '+'
        
class CurveRight:
    def getDir(self, car):
        if car.dir == Up:
            return Right
        if car.dir == Right:
            return Up
        if car.dir == Down:
            return Left
        if car.dir == Left:
            return Down
        print('What')
        
    def __repr__(self):
      return '/'

class CurveLeft:
    def getDir(self, car):
        if car.dir == Up:
            return Left
        if car.dir == Right:
            return Down
        if car.dir == Down:
            return Right
        if car.dir == Left:
            return Up
        print('What')
        
    def __repr__(self):
      return '\\'


class World:
    def __init__(self, w, h):
        self.world = [[None for x in range(w)] for y in range(h)]
        self.cars = []
        print('World',w,'x',h)
        
    def addTile(self, x, y, tile):
        if tile == ' ':
            self.world[y][x] = Grass()
        elif tile == '-' or tile == '|':
            self.world[y][x] = Lane()
        elif tile == '+':
            self.world[y][x] = Intersection()
        elif tile == '/':
            self.world[y][x] = CurveRight()
        elif tile == '\\':
            self.world[y][x] = CurveLeft()        
        elif tile == '^':
            self.addCar(x, y, Up)
        elif tile == '>':
            self.addCar(x, y, Right)
        elif tile == 'v':
            self.addCar(x, y, Down)
        elif tile == '<':
            self.addCar(x, y, Left)
        else:
            print(tile)
            
    def addCar(self, x, y, dir):
        car = Car(x, y, dir, len(self.cars)+1)
        self.cars.append(car)
        self.world[y][x] = Lane()
        
    def tick(self):
        self.cars.sort()
        #print(self.cars)
        for car in self.cars:
            if car.crashed:
                continue
            car.move()
            if self.collide(car):
                print('Collision:',car.x, car.y)
                #print(self)
                #continue
            tile = self.world[car.y][car.x]
            car.dir = tile.getDir(car)
        #print(self.cars)
        alive = 0
        lastcar = None
        for car in self.cars:
            if not car.crashed:
                alive += 1
                lastcar = car
        if alive == 1:
            #lastcar.back()
            #lastcar.move()
            print('Last car', lastcar.x,lastcar.y)
        return alive > 1
        
    def collide(self, car):
        for other in self.cars:
            if other.crashed:
                continue
            if other.x == car.x and other.y == car.y and car.id != other.id:
                    car.crashed = True
                    other.crashed = True
                    print('Cars:',car.id,other.id)
                    return True
        return False
        
    def __repr__(self):
      for car in self.cars:
        if car.id == 5:
          cx = car.x
          cy = car.y
          break
      world = ''
      for y in range(cy-2, cy+3):
        yl = self.world[y]
        line = ''
        for x in range(cx-2, cx+3):
          tile = yl[x]
          ch = str(tile)
          for car in self.cars:
            if car.x == x and car.y == y:
              if car.dir == Up:
                ch = '^'
              if car.dir == Left:
                ch = '<'
              if car.dir == Right:
                ch = '>'
              if car.dir == Down:
                ch = 'v'
          line += ch
        world += line+'\n'
      return world
      

width = len(inputt[0])-1
height = len(inputt)

w = World(width, height)

for y in range(height):
    line = inputt[y]
    print(line)
    for x in range(width):
        tile = line[x]
        w.addTile(x, y, tile)
        
print(w)

run = True
while run:
    run = w.tick()
    #print(w)
    #ch = input('a')
    #if ch == 'q':
    #  break
