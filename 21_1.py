import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_21_1.txt'), 'r')
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
        self.regs = [0]*6
        self.ip = 0
        self.ipreg = 0
        self.code = []
        
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
            print(self.regs[5])
                
    def setRegisters(self, regs):
        self.regs = regs[:]
        
    def compareRegisters(self, regs):
        for i in range(len(self.regs)):
            if self.regs[i] != regs[i]:
                return False
        return True
        
    def str2i(self, arr):
        ret = []
        for x in arr:
            ret.append(int(x))
        return ret
        
    def loadProgram(self, prog):
        for instr in prog:
          split = instr.split(' ')
          if (split[0] == '#ip'):
            self.ipreg = int(split[1])
            continue
          split[0] = str(getattr(self, split[0]))
          instr = self.str2i(split)
          self.code.append(instr)
  
    def step(self):
        #print(self.ip)
        self.regs[self.ipreg] = self.ip
        instr = self.code[self.ip]
        self.execInstr(instr[0], instr[1], instr[2], instr[3])
        self.ip = self.regs[self.ipreg]
        self.ip += 1
        if self.ip < 0 or self.ip >= len(self.code):
          return False
        return True
        
    def run(self):
      run = True
      count = 0
      while run:
        run = self.step()
        #print(self.ip,self.regs)
        count+= 1
        #if count > 40000:
            #print(self.regs)
            #break
                
vm = VM()
vm.regs[0] = 15615244
vm.loadProgram(input)
vm.run()
#print(vm.regs[0])