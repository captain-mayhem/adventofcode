import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_16_1.txt'), 'r')
input = file.readlines()

class VM:
    addr = 0
    addi = 1
    mulr = 2
    muli = 3
    banr = 4
    bani = 5
    borr = 6
    bori = 7
    setr = 8
    seti = 9
    gtir = 10
    gtri = 11
    gtrr = 12
    eqir = 13
    eqri = 14
    eqrr = 15
    
    
    def __init__(self):
        self.regs = [0]*4
        
    def execInstr(self, op, a, b, c):
        if op == self.addr:
            va = self.regs[a]
            vb = self.regs[b]
            self.regs[c] = va + vb
        elif op == self.addi:
            va = self.regs[a]
            self.regs[c] = va + b
        elif op == self.mulr:
            va = self.regs[a]
            vb = self.regs[b]
            self.regs[c] = va * vb
        elif op == self.muli:
            va = self.regs[a]
            self.regs[c] = va * b
        elif op == self.banr:
            va = self.regs[a]
            vb = self.regs[b]
            self.regs[c] = va & vb
        elif op == self.bani:
            va = self.regs[a]
            self.regs[c] = va & b
        elif op == self.borr:
            va = self.regs[a]
            vb = self.regs[b]
            self.regs[c] = va | vb
        elif op == self.bori:
            va = self.regs[a]
            self.regs[c] = va | b
        elif op == self.setr:
            self.regs[c] = self.regs[a]
        elif op == self.seti:
            self.regs[c] = a
        elif op == self.gtir:
            vb = self.regs[b]
            if a > vb:
                self.regs[c] = 1
            else:
                self.regs[c] = 0
        elif op == self.gtri:
            va = self.regs[a]
            if va > b:
                self.regs[c] = 1
            else:
                self.regs[c] = 0

        elif op == self.gtrr:
            va = self.regs[a]
            vb = self.regs[b]
            if va > vb:
                self.regs[c] = 1
            else:
                self.regs[c] = 0
        elif op == self.eqir:
            vb = self.regs[b]
            if a == vb:
                self.regs[c] = 1
            else:
                self.regs[c] = 0
        elif op == self.eqri:
            va = self.regs[a]
            if va == b:
                self.regs[c] = 1
            else:
                self.regs[c] = 0
        elif op == self.eqrr:            
            va = self.regs[a]
            vb = self.regs[b]
            if va == vb:
                self.regs[c] = 1
            else:
                self.regs[c] = 0
                
    def setRegisters(self, regs):
        self.regs = regs[:]
        
    def compareRegisters(self, regs):
        for i in range(len(self.regs)):
            if self.regs[i] != regs[i]:
                return False
        return True
                
vm = VM()

def str2i(arr):
    ret = []
    for x in arr:
        ret.append(int(x))
    return ret

opcodes = [[x for x in range(16)] for x in range(16)]
octable = {}

i = 0
while i < len(input):
    line = input[i]
    if line[0] != 'B':
        break
    regs = str2i(line[9:-2].split(','))
    
    line = input[i+1]
    instr = str2i(line.split(' '))
    
    line = input[i+2]
    regresult = str2i(line[9:-2].split(','))
    
    #print(regs, regresult, instr)
    matching = []
    for op in range(16):
        vm.setRegisters(regs)
        vm.execInstr(op, instr[1], instr[2], instr[3])
        if vm.compareRegisters(regresult):
            matching.append(op)
    
    possible = opcodes[instr[0]]
    newpossible = []
    for op in matching:
      if op in possible:
        newpossible.append(op)
    opcodes[instr[0]] = newpossible

    i += 4
    #print(matching)
    
for x in range(16):
  realoc = 0
  mapoc = 0
  for op in range(16):
    possibles = opcodes[op]
    if len(possibles) == 1:
      realoc = possibles[0]
      mapoc = op
      break
  octable[possibles[0]] = op
  for op in range(16):
    possibles = opcodes[op]
    if realoc in possibles:
      possibles.remove(realoc)

print(octable)