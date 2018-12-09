import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_6_1.txt'), 'r')
input = file.readlines()

w = 400
h = 400

area = 0
for y in range(h):
    for x in range(w):
        sum = 0
        for spot in input:
            tmp = spot.split(',')
            a = int(tmp[0])
            b = int(tmp[1])
            dist = abs(x-a)+abs(y-b)
            sum += dist
        if sum < 10000:
            area += 1

print(area)
