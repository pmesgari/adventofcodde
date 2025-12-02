import re


with open(0, encoding='utf-8') as f:
    rotations = []
    for line in f.readlines():
        match = re.search(r'([LR])(\d+)', line)
        rotations.append((match.group(1), int(match.group(2))))

prev = 0
new = 0
current = 50
total = 0
for d, a in rotations:
    if d == 'R':
        prev = current // 100
        current += a
        new = current // 100
    else:
        prev = (current - 1) // 100
        current -= a
        new = (current - 1) // 100

    total += abs(prev - new)

print(total)