
file = open('2_1_input.txt', 'r')
lines = file.readlines()

for entry in lines:
  for entry2 in lines:
    diffcount = 0
    lastdiffpos = 0
    for i in range(len(entry)):
      if entry[i] != entry2[i]:
        diffcount += 1
        lastdiffpos = i
    if diffcount == 1:
      result = entry[:lastdiffpos]
      result += entry[lastdiffpos+1:]
      print(result)
      break