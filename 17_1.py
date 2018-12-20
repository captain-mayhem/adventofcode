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
        return (b1, b2)
    else:
        return (b2, b1)
    
maxx = 1
minx = 99999
miny = 0
maxy = 1
for line in input:
    tmp = parseLine(line)
    if tmp[0][1] > maxx:
        maxx = tmp[0][1]
    if tmp[0][0] < minx:
        minx = tmp[0][0]
    if tmp[1][1] > maxy:
        maxy = tmp[1][1]
    #print(tmp);

minx -= 1
maxx += 1

width = maxx-minx
height = maxy

field = [[None for x in range(width)] for y in range(height)]

for line in input:
    tmp = parseLine(line)
    



