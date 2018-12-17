import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_13_1.txt'), 'r')
input = file.readlines()

Left = 0
Up = 1
Right = 2
Down = 3

class Car:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.nextturn = Left
        
    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.y
        return self.y < other.y
        
    def __repr__(self):
        return str(self.x)+'/'+str(self.y)+'/'+str(self.dir)
        
    def move(self):
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
    
class Lane:
    def getDir(self, car):
        return car.dir
        
class Intersection:
    def getDir(self, car):
        turn = car.turn()
        if turn == Up:
            return car.dir
        if turn == Left:
            return (car.dir-1)%4
        if turn == Right:
            return (car.dir+1)%4
        
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


class World:
    def __init__(self, w, h):
        self.world = [[None for x in range(w)] for y in range(h)]
        self.cars = []
        print('World',w,'x',h)
        
    def addTile(self, x, y, tile):
        if tile == ' ':
            return
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
        car = Car(x, y, dir)
        self.cars.append(car)
        self.world[y][x] = Lane()
        
    def tick(self):
        self.cars.sort()
        for car in self.cars:
            car.move()
            if self.collide(car):
                print('Collision:',car.x, car.y)
                return False
            tile = self.world[car.y][car.x]
            car.dir = tile.getDir(car)
        #print(self.cars)
        return True
        
    def collide(self, car):
        for other in self.cars:
            if other.x == car.x and other.y == car.y and car != other:
                    return True
        return False

width = len(input[0])-1
height = len(input)

w = World(width, height)

for y in range(height):
    line = input[y]
    for x in range(width):
        tile = line[x]
        w.addTile(x, y, tile)

run = True
while run:        
    run = w.tick()
