from typing import Tuple, Dict
from collections import deque


Position = Tuple[int, int]
Direction = Tuple[int, int]
Grid = Dict[Position, str]

with open(0, encoding='utf-8') as f:
    grid = {}
    for r, line in enumerate(f):
        for c, val in enumerate(line.strip()):
            grid[(r, c)] = val

max_row = max([k[0] for k in grid.keys()]) + 1
max_col = max([k[1] for k in grid.keys()]) + 1

def adj(row, col):
    """Return all adjacent neighbors of the given (row, col)"""
    deltas = [
        (-1, 0),  # UP
        (-1, +1), # UP-RIGHT
        (0, 1),  # RIGHT
        (1, 1), # DOWN-RIGHT
        (1, 0),  # DOWN
        (1, -1), # DOWN-LEFT
        (0, -1),  # LEFT
        (-1, -1), # UP-LEFT
    ]
    neighbors = []
    for dr, dc in deltas:
        rr = row + dr
        cc = col + dc
        if rr >= 0 and rr < max_row and cc >= 0 and cc < max_col:
            neighbors.append((rr, cc))

    return neighbors


def count_rolls(neighbors: list, grid: Grid):
    count = 0
    for r, c in neighbors:
        if grid[(r, c)] == '@':
            count += 1
    
    return count


def find_rolls():
    count = 0
    for r in range(max_row):
        for c in range(max_col):
            if grid[(r, c)] == '@':
                neighbors = adj(r, c)
                if count_rolls(neighbors, grid) < 4:
                    count += 1
    return count


print(find_rolls())


def get_roll_count(r, c, grid):
    count = 0
    for rr, cc in adj(r, c):
        if grid[(rr, cc)] == '@':
            count += 1
    return count


def get_roll_counts():
    counts = {}
    for r in range(max_row):
        for c in range(max_col):
            if grid[(r, c)] != '@':
                continue
            if (r, c) not in counts:
                counts[(r, c)] = 0
            counts[(r, c)] = get_roll_count(r, c, grid)

    return counts


def remove_max_rolls():
    queue = deque()
    seen = set()
    counts = get_roll_counts()

    for key, val in counts.items():
        if val < 4:
            queue.append(key)
            seen.add(key)
    
    removed = 0
    while queue:
        r, c = queue.popleft()
        removed += 1
        neighbors = adj(r, c)
        for nr, nc in neighbors:
            if grid[(nr, nc)] != '@':
                continue
            counts[(nr, nc)] -= 1
            if counts[(nr, nc)] < 4 and (nr, nc) not in seen:
                queue.append((nr, nc))
                seen.add((nr, nc))

    return removed


print(remove_max_rolls())