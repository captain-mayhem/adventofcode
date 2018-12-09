import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_4_1.txt'), 'r')
lines = file.readlines()
lines.sort()
idx = 0
guards = []
while(idx < len(lines)):
    entry = lines[idx]
    guard = entry.split('#')[1]
    guard = int(guard.split(' ')[0])
    idx += 1
    
    while idx < len(lines) and not '#' in lines[idx]:
        sleep = lines[idx].split(']')[0]
        sleep = int(sleep.split(':')[1])
        
        awake = lines[idx+1].split(']')[0]
        awake = int(awake.split(':')[1])
        
        idx += 2
        
        guards.append((guard, sleep, awake))

times = {}
for guard in guards:
    time = guard[2] - guard[1]
    if not guard[0] in times:
        times[guard[0]] = 0
    times[guard[0]] += time

maxtime = 0
maxguard = 0
for guard,time in times.items():  
    if time > maxtime:
        maxtime = time
        maxguard = guard

times = [0 for x in range(60)]        
for guard in guards:
    if guard[0] != maxguard:
        continue
    for minute in range(guard[1], guard[2]):
        times[minute] += 1

maxmin = 0
maxamount = 0
for m in range(60):
    amount = times[m]  
    if amount > maxamount:
        maxamount = amount
        maxmin = m
print(maxguard, maxmin, maxguard*maxmin)
#print(guards)
