"""--- Day 25: Code Chronicle ---"""

with open(0) as f:
    locks = []
    keys = []
    blocks = f.read().split('\n\n')
    for block in blocks:
        block = block.split('\n')
        transposed = [list(row) for row in zip(*block)]
        if all([char == '#' for char in block[0]]):
            locks.append([row.count('#') - 1 for row in transposed])
        else:
            keys.append([row.count('#') - 1 for row in transposed])

count = 0
for lock in locks:
    for key in keys:
        if all(x + y <= 5 for x, y in zip(lock, key)):
            count += 1

print(count)