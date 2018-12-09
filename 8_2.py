import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_8_1.txt'), 'r')
input = file.read()

input = input.split(' ')
idx = 0

class Node():
    def __init__(self):
        global idx
        children = int(input[idx])
        data = int(input[idx+1])
        idx += 2
        self.children = []
        self.values = []
        for i in range(children):
            n = Node()
            self.children.append(n)
        for i in range(data):
            v = int(input[idx])
            self.values.append(v)
            idx += 1
            
    def value(self):
        if len(self.children) == 0:
            return sum(self.values)
        self.sum = 0
        for val in self.values:
            idx = val-1
            if idx >= 0 and idx < len(self.children):
                n = self.children[idx]
                self.sum += n.value()
        return self.sum
            
while idx < len(input):   
    n = Node()
    
print(n.value())
