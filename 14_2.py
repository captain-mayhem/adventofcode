input = 919901
#input = 51589

digits = [int(d) for d in str(input)]
print(digits)

receipes = [3, 7]
elves = [0, 1]

def checkPattern(arr, pattern):
  for x in range(len(pattern)):
    if arr[len(arr)-1-x] != pattern[len(pattern)-1-x]:
      return False
  return True
  
def checkPattern2(arr, pattern):
  print(len(pattern))
  for x in range(len(pattern)):
    print(arr[len(arr)-1-x], pattern[len(pattern)-1-x])
    if arr[len(arr)-1-x] != pattern[len(pattern)-1-x]:
      print('No')
      return False
  print('yes')
  return True

while 1:
  r1 = receipes[elves[0]]
  r2 = receipes[elves[1]]
  combined = r1 + r2
  if combined >= 10:
    receipes.append(int(combined/10))
    if checkPattern(receipes, digits):
      break
    receipes.append(combined % 10)
    if checkPattern(receipes, digits):
      break
  else:
    receipes.append(combined)
    if checkPattern(receipes, digits):
      break
  elves[0] = (elves[0]+r1+1)%len(receipes)
  elves[1] = (elves[1]+r2+1)%len(receipes)

#print(receipes)
checkPattern2(receipes, digits)
print(len(receipes)-len(digits))

