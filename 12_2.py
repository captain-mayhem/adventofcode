import os
import re

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_12_1.txt'), 'r')
input = file.readlines()

plants = input[0][15:-1]
rules = {}

for i in range(2, len(input)):
    line = input[i]
    tmp = line.split(' ')
    rules[tmp[0]] = tmp[2][0]
    

class Biolab:
    def __init__(self, plants, rules):
        self.plants = self.transform(plants)
        self.newplants = [0 for x in range(len(self.plants))]
        self.rules = {}
        for k,v in rules.items():
            key = self.transform(k)
            numkey = self.toNum(key, 0)
            self.rules[numkey] = self.transform(v)[0]
        self.start = 0
        
    def transform(self, arg):
        ret = []
        for x in arg:
            if x == '#':
                ret.append(1)
            else:
                ret.append(0)
        return ret
        
    def toNum(self, arr, start):
        num = 0
        factor = 1
        for x in range(start+4, start-1, -1):
            num += arr[x]*factor
            factor *= 2
        return num
    
    def grow(self):
        self.spawnPlants(4)
        for i in range(len(self.plants)-4):
            #current = self.plants[i:i+5]
            #print(current)
            current = self.toNum(self.plants, i)
            #print(current)
            plant = self.rules[current]
            self.newplants[i] = plant
        #print(self.plants)
        #print(newplants)
        tmp = self.plants
        self.plants = self.newplants
        self.newplants = tmp
        self.start += 2
        
    def spawnPlants(self, n):
        for i in range(n):
            if self.plants[i] == 1:
                self.plants = [0]*(n-i)+self.plants
                self.start -= (n-i)
                self.newplants += [0]*(n-i)
                break
        for i in range(n):
            if self.plants[len(self.plants)-i-1] == 1:
                self.plants += [0]*(n-i)
                self.newplants += [0]*(n-i)
                break
        #print(self.start, self.plants)
        
    def sumPlants(self):
        accu = 0
        for i in range(len(self.plants)):
            if self.plants[i] == 1:
                accu += i+self.start
        return accu

lab = Biolab(plants, rules)
#for i in range(50000000000):
prev = 0
for i in range(4000):
    if i % 1000 == 0:
        val = lab.sumPlants()
        print(i, val, val-prev)
        prev = val
    lab.grow()
print(lab.sumPlants())
numiter = int(50000000000/1000)
#numiter = 5
val = (numiter-1)*62000+2385+59106
print(val)