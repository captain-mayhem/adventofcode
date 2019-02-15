class Group:
    def __init__(self, side, line, boost=0):
        self.side = side
        
        attribs, attack = line.split(';')
        units, hp, *type_mods = attribs.split()
        units=int(units)
        hp=int(hp)
        weak = []
        immune = []
        cur = None
        for w in type_mods:
            if w == "weak":
                cur = weak
            elif w == "immune":
                cur = immune
            else:
                cur.append(w)
                
        self.units = units
        self.hp = hp
        self.weak = weak
        self.immune = immune
        attack_amount, attack_type, initiative = attack.split()
        attack_amount = int(attack_amount)
        initiative = int(initiative)
        self.attack = attack_amount + boost
        self.attack_type = attack_type
        self.initiative = initiative
        self.attacker = None
        self.target = None
        
    def clear(self):
        self.attacker = None
        self.target = None
        
    def choose(self, groups):
        assert self.target is None
        cands = [group for group in groups
                if group.side != self.side
                and group.attacker is None
                and self.damage_prio(group)[0] > 0]        
        if cands:
            self.target = max(cands, key=lambda group: self.damage_prio(group))
            assert self.target.attacker is None
            self.target.attacker = self
            
    def effective_power(self):
        return self.units * self.attack
        
    def target_prio(self):
        return (-self.effective_power(), -self.initiative)
        
    def damage_prio(self, target):
        if target.units == 0:
            return (0, 0, 0)
        if self.attack_type in target.immune:
            return (0, 0, 0)
        mul = 1
        if self.attack_type in target.weak:
            mul = 2
        return (mul * self.units * self.attack, target.effective_power(), target.initiative)
        
    def do_attack(self, target):
        total_attack = self.damage_prio(target)[0]
        killed = total_attack // target.hp
        print(self.id, target.id, total_attack,killed)
        target.units = max(0, target.units - killed) 
        
# immune_system_input = """17 5390 weak radiation bludgeoning;4507 fire 2 # 989 1274 immune fire weak bludgeoning slashing;25 slashing 3""" # # infection_input = """801 4706 weak radiation;116 bludgeoning 1 # 4485 2961 immune radiation weak fire cold;12 slashing 4""" 

immune_system_input = """228 8064 weak cold;331 cold 8
284 5218 immune slashing fire weak radiation;160 radiation 10
351 4273 immune radiation;93 bludgeoning 2
2693 9419 immune radiation weak bludgeoning;30 cold 17
3079 4357 weak radiation cold;13 radiation 1
906 12842 immune fire;100 fire 6
3356 9173 immune fire weak bludgeoning;24 radiation 9
61 9474;1488 bludgeoning 11
1598 10393 weak fire;61 cold 20
5022 6659 immune bludgeoning fire cold;12 radiation 15""" 

infection_input = """120 14560 weak radiation bludgeoning immune cold;241 radiation 18
8023 19573 immune bludgeoning radiation weak cold slashing;4 bludgeoning 4
3259 24366 weak cold immune slashing radiation bludgeoning;13 slashing 16
4158 13287;6 fire 12
255 26550;167 bludgeoning 5
5559 21287;5 slashing 13
2868 69207 weak bludgeoning immune fire;33 cold 14
232 41823 immune bludgeoning;359 bludgeoning 3
729 41762 weak bludgeoning fire;109 fire 7
3690 36699;17 slashing 19""" 


immune_system_input = """4082 2910;5 cold 15
2820 9661 immune slashing;27 cold 8
4004 4885 weak slashing;10 bludgeoning 13
480 7219 weak bludgeoning;134 radiation 18
8734 4421 immune bludgeoning;5 slashing 14
516 2410 weak slashing;46 bludgeoning 5
2437 11267 weak slashing;38 fire 17
1815 7239 weak cold;33 slashing 10
4941 10117 immune bludgeoning;20 fire 9
617 7816 weak bludgeoning, slashing;120 bludgeoning 4"""

infection_input = """2877 20620 weak radiation bludgeoning;13 cold 11
1164 51797 immune fire;63 fire 7
160 31039 weak radiation immune bludgeoning;317 bludgeoning 2
779 24870 immune radiation bludgeoning weak slashing;59 slashing 12
1461 28000 immune radiation weak bludgeoning;37 slashing 16
1060 48827;73 slashing 3
4422 38291;14 slashing 1
4111 14339 immune fire bludgeoning cold;6 radiation 20
4040 49799 immune bludgeoning cold weak slashing fire;24 fire 19
2198 41195 weak radiation;36 slashing 6"""


def solve(boost):
    immune_system_groups = [Group(False, line, boost) for line in immune_system_input.split("\n")]
    infection_groups = [Group(True, line) for line in infection_input.split("\n")]
    groups = immune_system_groups + infection_groups
    i = 0
    for group in groups:
        i += 1
        group.id = i
    old = (-1, -1)
    while True:
        groups = sorted(groups, key=lambda group: group.target_prio())
        for group in groups:
            group.clear()
        for group in groups:
            group.choose(groups)   
        groups = sorted(groups, key=lambda group: -group.initiative)
        for group in groups:
            if group.target:
                group.do_attack(group.target)
        
        immune_system_units = sum(group.units for group in groups if group.side == False)
        infection_units = sum(group.units for group in groups if group.side == True)
        if (immune_system_units, infection_units) == old:
            return (immune_system_units, infection_units)
        old = (immune_system_units, infection_units)
        
# star 1
#print(solve(0)[1])

# star 2
for boost in range(43,44):
    ans = solve(boost)
    if ans[1] == 0:
        print(boost, ans[0])
        break
