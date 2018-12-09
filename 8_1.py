import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_8_1.txt'), 'r')
input = file.read()

input = input.split(' ')
idx = 0
sum = 0

class Node():
    def __init__(self):
        global idx
        children = int(input[idx])
        data = int(input[idx+1])
        idx += 2
        for i in range(children):
            n = Node()
        for i in range(data):
            global sum
            v = int(input[idx])
            sum += v
            idx += 1
            
while idx < len(input):   
    n = Node()
    
print(sum)
