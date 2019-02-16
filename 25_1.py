import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_25_1.txt'), 'r')
input = file.readlines()

inputt = '''0,0,0,0
	3,0,0,0
	0,3,0,0
	0,0,3,0
	0,0,0,3
	0,0,0,6
	9,0,0,0
	12,0,0,0'''.split('\n')

class vec4:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        
    def __repr__(self):
        ret = 'vec4('
        ret += str(self.x)+', '
        ret += str(self.y)+', '
        ret += str(self.z)+', '
        ret += str(self.w)
        ret += ')'
        return ret
        
    def __sub__(self, other):
        return vec4(self.x-other.x, self.y-other.y,self.z-other.z,self.w-other.w)
    
    def mhLen(self):
        return abs(self.x)+abs(self.y)+abs(self.z)+abs(self.w)   	

constell = []

for line in input:
    tmp = line.split(',')
    v = vec4(int(tmp[0]), int(tmp[1]), int(tmp[2]), int(tmp[3]))
    cons = [v]
    constell.append(cons)
    
def same(c1, c2):
    for v1 in c1:
        for v2 in c2:
            v = v2 - v1
            l = v.mhLen()
            if l <= 3:
                return True
    return False

def progress(constell):    
    newcons = []
    processed = []
    for i in range(len(constell)):
        if i in processed:
            continue
        found = False
        for j in range(i+1, len(constell)):
            c1 = constell[i]
            c2 = constell[j]
            if same(c1, c2):
                newcons.append(c1+c2)
                processed.append(j)
                found = True
                break
        if not found:
            newcons.append(constell[i])
    return newcons

newlen = len(constell)
oldlen = -1
while oldlen != newlen:
    oldlen = newlen  
    constell = progress(constell)
    newlen = len(constell)

print(constell)
print(len(constell))