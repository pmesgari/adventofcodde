from collections import defaultdict

with open(0) as f:
    lines = [list(map(int, l.split())) for l in f.readlines()]
    columns = list(zip(*lines))
    l1, l2 = [list(col) for col in columns]

l1.sort()
l2.sort()

total_distance = 0
for i in range(len(l1)):
    total_distance += abs(l1[i] - l2[i])

print(total_distance)

count = defaultdict(int)
for num in l2:
    count[num] += 1

similarity_score = 0
for num in l1:
    similarity_score += num * count[num]

print(similarity_score)