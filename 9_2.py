stones = 70901*100
players = 429

circle = [0]
scores = [0 for x in range(players)]
current = 0

for d in range(stones):
    if d % 10000 == 0:
        print(d)
    stone = d + 1
    if stone % 23 == 0:
        remove = (current - 7) % len(circle)
        val = circle.pop(remove)
        p = d % players
        scores[p] += stone + val
        current = remove
        continue
    insert = (current + 2) % len(circle)
    if insert == 0:
        insert = len(circle)
    circle.insert(insert, stone)
    current = insert
    
#print(circle,scores)
print(max(scores))

