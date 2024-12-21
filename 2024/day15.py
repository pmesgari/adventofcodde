"""--- Day 15: Warehouse Woes ---"""

from typing import Tuple, List, Dict, Set
from collections import deque

Position = Tuple[int, int]
Direction = Tuple[int, int]
Grid = Dict[Position, str]

with open(0) as f:
    warehouse = []
    grid_data = {}
    move_data = []
    start = None
    for r, line in enumerate(f):
        warehouse.append(line.strip())
        if line == "\n":
            break
        if "@" in line:
            start = (r, line.find("@"))
        for c, col in enumerate(line.strip()):
            grid_data[(r, c)] = col

    for line in f:
        move_data.extend(list(line.strip()))

deltas = [
    (-1, 0),  # UP
    (0, 1),  # RIGHT
    (1, 0),  # DOWN
    (0, -1),  # LEFT
]

move_symbols = ["^", ">", "v", "<"]

move_data = [deltas[move_symbols.index(symbol)] for symbol in move_data]


def print_grid(grid: Grid):
    """Pretty print grid"""
    max_row = max([k[0] for k in grid.keys()]) + 1
    max_col = max([k[1] for k in grid.keys()]) + 1
    for r in range(max_row):
        line = []
        for c in range(max_col):
            line.append(grid[(r, c)])
        print("".join(line))


def sweep(position: Position, direction: Direction, grid: Grid) -> Set[Position]:
    """Perform a sweep from this position in the given direction
    and collect all the boxes
    """
    r, c = position
    dr, dc = direction
    boxes = set()
    while True:
        nr = r + dr
        nc = c + dc
        if grid[(nr, nc)] not in ["O", "[", "]"]:
            break
        boxes.add((nr, nc))
        r = nr
        c = nc

    return boxes


def get_boxes(position: Position, direction: Direction, grid: Grid) -> List[Position]:
    boxes = set()
    r, c = position
    dr, dc = direction

    nr = r + dr
    nc = c + dc
    # linear box push
    if grid.get((nr, nc)) in ["O", "[", "]"]:
        boxes = sweep(position, direction, grid)
        return boxes

    # non-linear box push
    to_explore = None
    if grid.get((nr, nc)) in ["[", "]"]:
        to_explore = deque([(nr, nc)])

    while to_explore:
        current = to_explore.pop()
        boxes.add(current)
        # determine if the current is the left or right half of the box
        # then find the complement and add it to the boxes
        # left half
        if grid[(current)] == "[":
            left = current
            right = (current[0], current[1] + 1)
            boxes.add(right)
        # right half
        if grid[(current)] == "]":
            right = current
            left = (current[0], current[1] - 1)
            boxes.add(left)
        # for each half we need to see if there is another box connected
        # to it, this happens if there is a half box above/below the current halft
        for r, c in [left, right]:
            if grid[(r + dr, c + dc)] in ["[", "]"]:
                to_explore.append((r + dr, c + dc))
    return boxes


def make_move(position: Position, direction: Direction, grid: Grid) -> Grid:
    """Move the robot and boxes if any"""
    new_grid = grid.copy()
    dr, dc = direction
    r, c = position
    # get all the moveable boxes
    moveable = get_boxes(position, direction, new_grid)
    if any(new_grid[(b[0] + dr, b[1] + dc)] == "#" for b in moveable):
        return new_grid

    # determine the new locations of all the moveable boxes
    new_locations = {}
    for br, bc in moveable:
        new_locations[(br + dr, bc + dc)] = new_grid[(br, bc)]
    # empty out all their previous locations
    for br, bc in moveable:
        new_grid[(br, bc)] = "."
    # now move all the boxes to their new location
    new_grid.update(new_locations)

    # finally update the position of the robot
    if new_grid[(r + dr, c + dc)] == ".":
        new_grid[(r + dr, c + dc)] = "@"
        new_grid[(r, c)] = "."

    return new_grid


def find_start(grid: Grid) -> Position:
    """Find the start position in the grid"""
    for key, val in grid.items():
        if val == "@":
            return key


def calc_gps_coordinates(start: Position, grid: Grid, moves: List[str]) -> int:
    """Calculate the GPS coordinates after performing all the moves"""
    for move in moves:
        grid = make_move(start, move, grid)
        start = find_start(grid)
    total = 0
    for key, val in grid.items():
        if val == "O":
            r, c = key
            total += (r) * 100 + c
        if val == "[":
            r, c = key
            total += (r) * 100 + c
    return total


print(calc_gps_coordinates(start, grid_data, move_data))

# double the warehouse
grid_data = {}
start = None
for r, line in enumerate(warehouse):
    extline = (
        line.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
    )
    if "@" in extline:
        start = (r, extline.find("@"))
    for c, col in enumerate(extline):
        grid_data[(r, c)] = col
print(calc_gps_coordinates(start, grid_data, move_data))
