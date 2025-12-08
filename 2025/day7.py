with open(0, encoding='utf-8') as f:
    grid = [line.strip() for line in f.readlines()]

start = grid[0].index('S')
max_row = len(grid)
max_col = len(grid[0])

current_beams = {start}

splits = 0
for row in range(max_row):
    next_beams = set()
    for col in current_beams:
        if grid[row][col] in ['.', 'S']:
            next_beams.add(col)
        elif grid[row][col] == '^':
            next_beams.add(col - 1)
            next_beams.add(col + 1)
            splits += 1
    current_beams = next_beams

print(splits)


current_beams = {start: 1}

for row in range(max_row):
    next_beams = {}
    for col, val in current_beams.items():
        if grid[row][col] in ['.', 'S']:
            next_beams[col] = next_beams.get(col, 0) + current_beams[col]
        elif grid[row][col] == '^':
            next_beams[col - 1] = next_beams.get(col - 1, 0) + current_beams[col]
            next_beams[col + 1] = next_beams.get(col + 1, 0) + current_beams[col]
    current_beams = next_beams

print(sum(current_beams.values()))