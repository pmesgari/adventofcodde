"""--- Day 12: Garden Groups ---"""

from typing import List, Tuple, Set

with open(0) as f:
    grid_input = [list(l.strip()) for l in f.readlines()]


Position = Tuple[int, int]
Grid = List[List[str]]
Region = Set[Position]


def print_grid(grid: Grid):
    """Pretty print grid"""
    for row in grid:
        print(" ".join(row))


def adj(row, col, grid: Grid):
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


def explore(start: Position, parent: dict, grid: Grid):
    """Explore the grid from the start position"""
    seen = set()
    seen.add(start)

    def _explore(start: Position, parent: dict, grid: Grid):
        cr, cc = start
        neighbors = adj(cr, cc, grid)
        for n in neighbors:
            nr, nc = n
            if n not in parent and grid[cr][cc] == grid[nr][nc]:
                parent[n] = start
                seen.add(n)
                _explore(n, parent, grid)

    _explore(start, parent, grid)
    return seen


def calc_perimeter(region: Region, grid: Grid) -> int:
    """Calculate region perimeter"""
    total = 0
    for pr, pc in region:
        deltas = [
            (-1, 0),  # UP
            (0, 1),  # RIGHT
            (1, 0),  # DOWN
            (0, -1),  # LEFT
        ]
        height = len(grid)
        width = len(grid[0])
        for dr, dc in deltas:
            rr = pr + dr
            cc = pc + dc
            if rr < 0 or rr >= height or cc < 0 or cc >= width:
                total += 1
                continue
            elif grid[pr][pc] != grid[rr][cc]:
                total += 1
    return total


def make_turn(direction, turn):
    """Make a 90 degree right turn"""
    if turn == "R":
        deltas = [
            (-1, 0),  # UP
            (0, 1),  # RIGHT
            (1, 0),  # DOWN
            (0, -1),  # LEFT
        ]
    else:
        deltas = [
            (-1, 0),  # UP
            (0, -1),  # LEFT
            (1, 0),  # DOWN
            (0, 1),  # RIGHT
        ]
    idx = deltas.index(direction)
    return deltas[(idx + 1) % 4]


def has_edge(row, col, delta, region: Region, grid: Grid):
    """Determine if there is an edge in the given direction"""
    dr, dc = delta
    return (row + dr, col + dc) not in region


def calc_sides(region: Region, grid: Grid) -> int:
    """Calculate region sides"""
    segments = {}
    deltas = [
        (-1, 0),  # UP
        (0, 1),  # RIGHT
        (1, 0),  # DOWN
        (0, -1),  # LEFT
    ]
    # make a map of all the segments tha has an edge
    for pr, pc in region:
        for idx, delta in enumerate(deltas):
            if has_edge(pr, pc, delta, region, grid):
                segments[(pr, pc, idx)] = True

    # pick a random point and start walking in both 90 and 270 directions
    for pr, pc in region:
        for idx, delta in enumerate(deltas):
            if not has_edge(pr, pc, delta, region, grid):
                continue
            if (pr, pc, idx) in segments and not segments[(pr, pc, idx)]:
                continue
            # now walk in 90 and 270 degrees parallel to the current
            # direction where we detected an edge and cross out every
            # segment we find
            for new_delta in [make_turn(delta, 'R'), make_turn(delta, 'L')]:
                start = (pr, pc)
                while True:
                    # calculate the new position
                    nr = start[0] + new_delta[0]
                    nc = start[1] + new_delta[1]
                    # outside of the region, can't go there
                    if (nr, nc) not in region:
                        break
                    # it doesn't have an edge, then we are jumping
                    # over a segment without edge and we might end up
                    # crossing other edges which we shouldn't
                    # we can only cross out edges that are continous
                    if not has_edge(nr, nc, delta, region, grid):
                        break
                    if (nr, nc, idx) in segments:
                        segments[(nr, nc, idx)] = False
                    start = (nr, nc)
                    
    # whatever segment is left over determines the number of sides
    return sum((val for _, val in segments.items()), 0)


def calc_total_fence_price(grid: Grid):
    """Calculate total fencing price"""
    seen = set()
    height = len(grid)
    width = len(grid[0])
    total = 0
    discounted_total = 0
    for r in range(height):
        for c in range(width):
            if (r, c) in seen:
                continue
            region = explore((r, c), {}, grid)
            for plot in region:
                seen.add(plot)
            perimeter = calc_perimeter(region, grid)
            area = len(region)
            total += perimeter * area
            sides = calc_sides(region, grid)
            discounted_total += area * sides
    return total, discounted_total


print(calc_total_fence_price(grid_input))
