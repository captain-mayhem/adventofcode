import os

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
        self.plants = plants
        self.rules = rules
        self.start = 0
    
    def grow(self):
        self.spawnPlants(4)
        newplants = '.'*2
        for i in range(len(self.plants)-4):
            current = self.plants[i:i+5]
            plant = self.rules[current]
            newplants += plant
        #print(newplants)
        self.plants = newplants
        
    def spawnPlants(self, n):
        for i in range(n):
            if self.plants[i] == '#':
                self.plants = '.'*(n-i)+self.plants
                self.start -= (n-i)
                break
        for i in range(n):
            if self.plants[len(self.plants)-i-1] == '#':
                self.plants += '.'*(n-i)
                break
        #print(self.start, self.plants)
        
    def sumPlants(self):
        accu = 0
        for i in range(len(self.plants)):
            if self.plants[i] == '#':
                accu += i+self.start
        return accu

lab = Biolab(plants, rules)
for i in range(20):
    lab.grow()
print(lab.sumPlants())