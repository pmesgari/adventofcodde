"""--- Day 1: Historian Hysteria ---"""
from collections import defaultdict

with open(0, encoding='utf-8') as f:
    lines = [list(map(int, l.split())) for l in f.readlines()]
    columns = list(zip(*lines))
    l1, l2 = [list(col) for col in columns]

l1.sort()
l2.sort()

TOTAL_DISTANCE = 0
for i, score in enumerate(l1):
    TOTAL_DISTANCE += abs(score - l2[i])

print(TOTAL_DISTANCE)

count = defaultdict(int)
for num in l2:
    count[num] += 1

SIMILARITY_SCORE = 0
for num in l1:
    SIMILARITY_SCORE += num * count[num]

print(SIMILARITY_SCORE)
