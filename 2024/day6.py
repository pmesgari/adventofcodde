"""--- Day 6: Guard Gallivant ---"""

import copy
from typing import List, Tuple, Set

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
directions = [UP, RIGHT, DOWN, LEFT]
headings = ["^", ">", "v", "<"]

Grid = List[List[str]]
Position = Tuple[int, int]
# (row, col, (dr, dc))
State = Tuple[int, int, Tuple[int, int]]

with open(0, encoding="utf-8") as f:
    input_grid = [list(l.strip()) for l in f.readlines()]


def print_grid(grid: Grid):
    """Pretty print grid"""
    for row in grid:
        print(" ".join(row))


def find_start(grid: Grid) -> Position:
    """Find the start point"""
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col in headings:
                idx = headings.index(col)
                return (r, c, directions[idx])


def is_out_of_bounds(state: State, grid: Grid) -> bool:
    """Determine if current position is out of bounds"""
    height = len(grid)
    width = len(grid[0])
    row, col, _ = state
    if row >= height or col >= width:
        return True
    if row < 0 or col < 0:
        return True
    return False


def next_state(current: State, grid: Grid) -> State:
    """Determine next state"""
    row, col, direction = current
    dr, dc = direction
    rr = row + dr
    cc = col + dc

    if is_out_of_bounds((rr, cc, direction), grid):
        return (rr, cc, direction)
    if grid[rr][cc] == "#":
        idx = directions.index(direction)
        return (row, col, directions[(idx + 1) % 4])
    return (rr, cc, direction)


def get_visited_positions(grid: Grid, start: State) -> Set[Tuple[int, int]]:
    """Get all distinct positions visited"""
    visited = set()
    current = start
    while True:
        row, col, _ = current
        visited.add((row, col))
        current = next_state(current, grid)
        if is_out_of_bounds(current, grid):
            break
        if (row, col) not in visited:
            visited.add((row, col))
    return visited


def count_positions(grid: Grid, start: State) -> int:
    """Count distinct positions visited"""
    positions = get_visited_positions(grid, start)
    return len(positions)


def is_loop(grid: Grid, start: State) -> bool:
    """Determine if the guard is in a loop"""
    current = start
    visited = set()
    while True:
        current = next_state(current, grid)
        if is_out_of_bounds(current, grid):
            return False
        if current in visited:
            return True
        visited.add(current)


def count_obstructions(grid: Grid, start: State) -> int:
    """Count obstruction positions"""
    positions = get_visited_positions(input_grid, find_start(input_grid))
    total = 0
    for pos in positions:
        copy_grid = copy.deepcopy(grid)
        row, col = pos
        if is_out_of_bounds((row, col, ""), copy_grid):
            continue
        copy_grid[row][col] = "#"
        if is_loop(copy_grid, start):
            total += 1
    return total


print(count_positions(input_grid, find_start(input_grid)))
print(count_obstructions(input_grid, find_start(input_grid)))
