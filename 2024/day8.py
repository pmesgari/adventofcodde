"""--- Day 8: Resonant Collinearity ---"""

from typing import List, Dict, Tuple
from collections import defaultdict
from itertools import combinations

Grid = List[List[str]]
Position = Tuple[int, int]


with open(0, encoding="utf-8") as f:
    input_grid = [list(l.strip()) for l in f.readlines()]


def print_grid(grid: Grid):
    """Pretty print grid"""
    for row in grid:
        print("".join(row))


def collect_freq(grid: Grid) -> Dict[str, List[Position]]:
    """Collect positions of equal frequencies"""
    freqs = defaultdict(list)
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val != ".":
                freqs[val].append((r, c))
    return freqs


def is_inside(p: Position, grid: Grid) -> bool:
    """Given a position determine if it falls inside of the grid"""
    rows, cols = len(grid), len(grid[0])
    r, c = p
    return 0 <= r < rows and 0 <= c < cols


def find_antinode(p: Position, direction: Tuple[int, int], distance: int) -> Position:
    """Find the antinode in the given direction and distance"""
    ra, ca = p
    dr, dc = direction

    return (ra + distance * dr, ca + distance * dc)


def count_antinode(grid: Grid, include_resonant=False) -> int:
    """Count antinode positions"""
    seen = set()
    freqs = collect_freq(grid)

    for antennas in freqs.values():
        for a, b in combinations(antennas, 2):
            ra, ca = a
            rb, cb = b
            dir_ab = (rb - ra, cb - ca)
            dir_ba = (-dir_ab[0], -dir_ab[1])

            # Add antinodes based on distance
            distances = (
                [2] if not include_resonant else range(1, max(len(grid), len(grid[0])))
            )
            for d in distances:
                ant1 = find_antinode(a, dir_ab, d)
                ant2 = find_antinode(b, dir_ba, d)
                if is_inside(ant1, grid):
                    seen.add(ant1)
                if is_inside(ant2, grid):
                    seen.add(ant2)

    return len(seen)


print(count_antinode(input_grid))
print(count_antinode(input_grid, True))
