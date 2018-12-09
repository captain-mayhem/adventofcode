import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_3_1.txt'), 'r')
lines = file.readlines()

field = [[0 for x in range(1000)] for y in range(1000)]
occupied = 0

for entry in lines:
    tmp = entry.split('@')
    id = int(tmp[0][1:])
    tmp = tmp[1].split(',')
    x = int(tmp[0])
    tmp = tmp[1].split(':')
    y = int(tmp[0])
    tmp = tmp[1].split('x')
    w = int(tmp[0])
    h = int(tmp[1])
    for b in range(y, h+y):
        for a in range(x, w+x):
            if field[b][a] != 0:
                if field[b][a] > 0:
                    occupied += 1
                field[b][a] = -1
            else:
                field[b][a] = id
print(occupied)
    #print(id, x, y, w, h)