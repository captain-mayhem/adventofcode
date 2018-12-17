input = 919901

receipes = [3, 7]
elves = [0, 1]

result = ''

while len(receipes) < input+10:
  r1 = receipes[elves[0]]
  r2 = receipes[elves[1]]
  combined = r1 + r2
  if combined >= 10:
    receipes.append(int(combined/10))
    if len(receipes) > input:
      result += str(int(combined/10))
    receipes.append(combined % 10)
    if len(receipes) > input and len(result) < 10:
      result += str(combined % 10)
  else:
    receipes.append(combined)
    if len(receipes) > input:
      result += str(combined)
  elves[0] = (elves[0]+r1+1)%len(receipes)
  elves[1] = (elves[1]+r2+1)%len(receipes)

print(result)