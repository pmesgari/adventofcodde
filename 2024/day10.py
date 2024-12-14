"""--- Day 10: Hoof It ---"""
from collections import defaultdict
from typing import List

with open(0) as f:
    grid_input = []
    for line in f:
        grid_input.append([
            int(char) if char != '.' else char
            for char in line.strip()
        ])



def adj(row, col, grid: List[List[int]]):
    """Return all adjacent neighbors of the given (row, col)"""
    deltas = [
        (-1, 0),  # UP
        (0, 1),  # RIGHT
        (1, 0),  # DOWN
        (0, -1),  # LEFT
    ]
    height = len(grid)
    width = len(grid[0])
    neighbors = []
    for dr, dc in deltas:
        rr = row + dr
        cc = col + dc
        if rr >= 0 and rr < height and cc >= 0 and cc < width:
            neighbors.append((rr, cc))

    return neighbors


# def calc_trailhead_score(row, col, grid: List[List[int]], rating=False):
#     """Given a start position calculate the trailhead score"""
#     to_explore = [(row, col)]
#     score = 0
#     seen = set((row, col))
#     nines = defaultdict(int)
#     while to_explore:
#         r, c = to_explore.pop()
#         neighbors = adj(r, c, grid)
#         for neigbor in neighbors:
#             rn, cn = neigbor
#             if (rn, cn) in seen:
#                 # if we are not rating we can't visit this again
#                 if not rating:
#                     continue
#                 # otherwise we should only skip if its not a 9
#                 if rating and grid[rn][cn] != 9:
#                     continue
#                 nines[(rn, cn)] += 1
#             if grid[rn][cn] == ".":
#                 seen.add(neigbor)
#                 continue
#             if grid[rn][cn] - grid[r][c] == 1:
#                 if grid[rn][cn] == 9:
#                     score += 1
#                     if rating:
#                         seen = set()
#                         nines[(rn, cn)] += 1
#                 to_explore.append((rn, cn))
#                 seen.add(neigbor)
#     print(row, col, nines)
#     return score

def calc_trailhead_score(row, col, grid: List[List[int]]):
    """Given a start position calculate the trailhead score"""
    to_explore = [(row, col)]
    score = 0
    seen = set((row, col))
    while to_explore:
        r, c = to_explore.pop()
        neighbors = adj(r, c, grid)
        for neigbor in neighbors:
            rn, cn = neigbor
            if (rn, cn) in seen:
                continue
            if grid[rn][cn] == ".":
                seen.add(neigbor)
                continue
            if grid[rn][cn] - grid[r][c] == 1:
                if grid[rn][cn] == 9:
                    score += 1
                to_explore.append((rn, cn))
                seen.add(neigbor)

    return score


def calc_trailhead_rating(row, col, grid: List[List[int]]):
    """Calculate the trailhead rating"""
    to_explore = [(row, col)]
    rating = 0
    seen = set((row, col))
    while to_explore:
        r, c = to_explore.pop()
        neighbors = adj(r, c, grid)
        if grid[r][c] == 9:
            rating += 1
            seen = set()
        for neigbor in neighbors:
            rn, cn = neigbor
            if (rn, cn) in seen:
                continue
            if grid[rn][cn] == ".":
                seen.add(neigbor)
                continue
            if grid[rn][cn] - grid[r][c] == 1:
                to_explore.append((rn, cn))
                seen.add(neigbor)

    return rating


def find_trailheads(grid: List[List[int]]) -> List[List[int]]:
    """Find all trailhead positions"""
    positions = []
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == 0:
                positions.append((r, c))
    return positions


print(
    sum(
        (
            calc_trailhead_score(th[0], th[1], grid_input)
            for th in find_trailheads(grid_input)
        ),
        0,
    )
)

print(
    sum(
        (
            calc_trailhead_rating(th[0], th[1], grid_input)
            for th in find_trailheads(grid_input)
        ),
        0,
    )
)
