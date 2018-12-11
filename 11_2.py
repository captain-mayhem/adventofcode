serial = 5535
w =300
h = 300

cells = [[0 for x in range(h)] for x in range(w)]

for y in range(h):
    for x in range(w):
        rackId = x + 1 + 10
        power = rackId * (y+1)
        power += serial
        power *= rackId
        power %= 1000
        power = int(power/100)
        power -= 5
        cells[y][x] = power

gmaxp = 0
gpoint = [0,0,0]
for size in range(1,301):
    maxpower = 0
    point = [0,0,size]        
    for y in range(h-size+1):
        for x in range(w-size+1):
            power = 0
            for b in range(size):
                for a in range(size):
                    power += cells[y+b][x+a]
            if power > maxpower:
                maxpower = power
                point[0] = x + 1
                point[1] = y + 1
    if maxpower > gmaxp:
        gmaxp = maxpower
        gpoint = point
    print(point, maxpower)
print(gpoint)
