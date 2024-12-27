"""--- Day 18: RAM Run ---"""

from collections import deque
from typing import Dict, Tuple

Position = Tuple[int, int]
Grid = Dict[Position, str]

with open(0) as f:
    byte_position_data = [
        list(map(int, pair.strip().split(","))) for pair in f.readlines()
    ]


def print_grid(grid: Grid):
    """Pretty print grid"""
    xmax = max([k[0] for k in grid.keys()]) + 1
    ymax = max([k[1] for k in grid.keys()]) + 1
    for y in range(ymax):
        line = []
        for x in range(xmax):
            line.append(grid[(x, y)])
        print("".join(line))


def make_grid(byte_position, xmax, ymax) -> Grid:
    """Given the byte position make a grid"""
    grid = {}
    for y in range(ymax):
        for x in range(xmax):
            grid[(x, y)] = "#" if [x, y] in byte_position else "."

    return grid


def draw_path(path, grid):
    for item in path:
        grid[item] = "O"
    print_grid(grid)


def find_path(grid: Grid, start: Position, end: Position) -> int:
    """Find a path from start to end"""
    deltas = [
        (0, -1),  # UP
        (1, 0),  # RIGHT
        (0, 1),  # DOWN
        (-1, 0),  # LEFT
    ]

    open_set = deque([start])
    parent = {start: None}
    while open_set:
        x, y = open_set.popleft()
        if (x, y) == end:
            break
        for dx, dy in deltas:
            xn = x + dx
            yn = y + dy
            if (xn, yn) not in grid or grid[(xn, yn)] == "#":
                continue
            if (xn, yn) in parent:
                continue
            parent[(xn, yn)] = (x, y)
            open_set.append((xn, yn))
    path = set()
    current = end
    while current in parent:
        if parent[current]:
            path.add(parent[current])
        current = parent[current]
    return path


def find_block_byte(byte_position, start: Position, end: Position):
    """Find the byte that blocks the path"""
    left = 1
    right = len(byte_position)

    # When this loop exits, left is the smallest number of bytes
    # needed to block the path
    while left < right:
        mid = (left + right) // 2
        grid = make_grid(byte_position_data[:mid+1], 71, 71)
        path = find_path(grid, start, end)
        if path:
            left = mid + 1
        else:
            right = mid
    return left, byte_position_data[left]

grid_data = make_grid(byte_position_data[:1024], 71, 71)
path = find_path(grid_data, (0, 0), (70, 70))
print(len(path))
print(find_block_byte(byte_position_data, (0, 0), (70, 70)))
