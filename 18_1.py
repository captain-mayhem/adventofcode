import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_18_1.txt'), 'r')
input = file.readlines()

Empty = 0
Trees = 1
Lumber = 2

class Forest:
    def __init__(self, width, height):
        self.fields = [[Empty for x in range(50)] for y in range(height)]

    def addField(self, x, y, field):
        if field == '.':
            return
        elif field == '#':
            self.fields[y][x] = Lumber
        elif field == '|':
            self.fields[y][x] = Trees
        else:
            print(field)

f = Forest(50, 50)

for y in range(len(input)):
    line = input[y]
    for x in range(len(line)-1):
        f.addField(x, y, line[x])
    



