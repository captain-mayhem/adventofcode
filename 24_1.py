import os

path = os.path.dirname(__file__)
file = open(os.path.join(path,'input_24_1.txt'), 'r')
input = file.readlines()

class Group:
    def __init__(self, units, hp):
        self.units = units
        self.hitpoints = hp
        self.immune = []
        self.weak = []
        
    def power(self):
        return self.units*self.damage
        
    def __lt__(self, other):
        ep1 = self.power()
        ep2 = other.power()
        if ep1 == ep2:
            return self.initiative > other.initiative
        return ep1 > ep2
        
    def __repr__(self):
        return str(self.power())+' '+str(self.initiative)+str(self.immune)+str(self.weak)+str(self.initiative)
        
    def getDamage(self, group):
        if group.dtype in self.immune:
            return 0
        d = group.power()
        if group.dtype in self.weak:
            return d*2
        return d
        
class Attack:
    def __init__(self, att, defend):
        self.attacker = att
        self.defender = defend
        
    def __lt__(self, other):
        return self.attacker.initiative > other.attacker.initiative

    def __repr__(self):
        return str(self.attacker)+'->'+str(self.defender)

class Battle:
    def __init__(self):
        self.immune = []
        self.infect = []
        self.groups = []
        
    def fight(self):
        for group in self.groups:
            group.target = group.units > 0
        self.groups.sort()
        #print(self.groups)
        attacks = []
        for group in self.groups:
            target = self.target(group)
            if target:
                att = Attack(group, target)
                attacks.append(att)
        attacks.sort()
        #print(attacks)
        for att in attacks:
            damage = att.defender.getDamage(att.attacker)
            kills = int(damage/att.defender.hitpoints)
            #print(kills)
            att.defender.units -= kills
            if att.defender.units < 0:
                att.defender.units = 0
            
    def target(self, group):
        if group in self.immune:
            targets = self.infect
        else:
            targets = self.immune
        maxdamage = -1
        besttarget = None
        for target in targets:
            if not target.target:
                continue
            d = target.getDamage(group)
            #print(group, group.dtype, target, d)
            if d > maxdamage:
                maxdamage = d
                besttarget = target
            elif d == maxdamage:
                p1 = besttarget.power()
                p2 = target.power()
                if p1 == p2:
                    if target.initiative > besttarget.initiative:
                        besttarget = target
                elif p1 < p2:
                    besttarget = target
        if besttarget:
            besttarget.target = False
        return besttarget
        
    def alive(self):
        al = False
        for group in self.immune:
            if group.units > 0:
                al = True
                break
        if not al:
            return False
        for group in self.infect:
            if group.units > 0:
                al = True
                break
        return al
        
    def units(self):
        units = 0
        for group in self.groups:
            units += group.units
        return units

battle = Battle()

for line in input:
    tmp = line.split(' ')
    if tmp[0] == '\n':
        continue
    if tmp[0] == 'Immune':
        current = battle.immune
        continue
    if tmp[0] == 'Infection:\n':
        current = battle.infect
        continue
    #print(tmp)
    group = Group(int(tmp[0]), int(tmp[4]))
    group.initiative = int(tmp[-1])
    group.dtype = tmp[-5]
    group.damage = int(tmp[-6])
    specialsize = len(tmp)-18
    for i in range(7, 7+specialsize):
        w = tmp[i]
        if i == 7:
            w = w[1:]
        elif i == 7+specialsize-1:
            w = w[:-1]
        if w == 'immune':
            curr = group.immune
            continue
        elif w == 'weak':
            curr = group.weak
            continue
        elif w == 'to':
            continue
        if w[-1] == ',' or w[-1] == ';':
            curr.append(w[:-1])
        else:
            curr.append(w)
    current.append(group)
    battle.groups.append(group)

while battle.alive():
    battle.fight()
print(battle.units())