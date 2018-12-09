import sys

file = open('1_1_input_m.txt', 'r')
lines = file.readlines()
frequencies = {0 : True}
accu = 0
found = False
iter = 0
iter2 = 0
while True:
  iter += 1
  for entry in lines:
    iter2 += 1
    num = int(entry)
    accu += num
    if accu in frequencies:
      found = True
      print('Found: '+str(accu)+'/'+str(iter)+'/'+str(iter2))
      sys.exit(0)
    frequencies[accu] = True