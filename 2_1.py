
file = open('2_1_input.txt', 'r')
lines = file.readlines()

twocount = 0
threecount = 0

for entry in lines:
  store = {}
  for char in entry:
    if not char in store:
      store[char] = 1
    else:
      store[char] += 1
  
  for k,v in store.items():
    if v == 2:
      twocount += 1
      break
  
  for k,v in store.items():
    if v == 3:
      threecount += 1
      break  
  
print(twocount*threecount)