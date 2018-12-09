import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_6_1.txt'), 'r')
input = file.readlines()

w = 400
h = 400
idx = 0
field = [[(-1,999) for x in range(w)] for y in range(h)]

for spot in input:
    tmp = spot.split(',')
    a = int(tmp[0])
    b = int(tmp[1])
    for y in range(h):
        for x in range(w):
            dist = abs(x-a)+abs(y-b)
            if dist == field[y][x][1]:
                field[y][x] = (-1, dist)
            if dist < field[y][x][1]:
                field[y][x] = (idx, dist)
    idx += 1

border = {}
for x in range(w):
    border[field[0][x][0]] = True
    border[field[h-1][x][0]] = True
for y in range(h):
    border[field[y][0][0]] = True
    border[field[y][w-1][0]] = True

area = [0 for x in range(len(input))]
for y in range(h):
    for x in range(w):
        entry = field[y][x]
        if entry[0] in border:
            continue
        area[entry[0]] += 1

print(max(area))