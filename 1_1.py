
file = open('1_1_input.txt', 'r')
lines = file.readlines()
accu = 0
for entry in lines:
  num = int(entry)
  accu += num
print(accu)