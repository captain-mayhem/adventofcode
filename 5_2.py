import os
import re

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_5_1.txt'), 'r')
originput = file.read()
for c in range(ord('a'), ord('z')+1):
    ch = chr(c)
    input = originput
    input = re.sub('['+ch+ch.upper()+']', '', input)
    changed = True
    while changed:
        changed = False
        output = ''
        i = 0
        while i < len(input)-1:
            c1 = input[i]
            c2 = input[i+1]
            i += 1
        
            if c1.lower() == c2.lower() and c1 != c2:
                changed = True
                i += 1
                continue
        
            output += c1
            if i == len(input)-1:
                output += c2
        #print(len(output))
        input = output
    print(ch,len(input))