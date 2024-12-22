"""--- Day 16: Reindeer Maze ---"""

import heapq
from copy import copy
from collections import namedtuple
from typing import Tuple, List, Dict

Position = Tuple[int, int]
Heading = Tuple[int, int]
Grid = Dict[Position, str]
State = namedtuple("State", ["pos", "heading"])

with open(0) as f:
    grid_data = {}
    start = None
    end = None
    for r, row in enumerate(f):
        for c, col in enumerate(row):
            if col == "S":
                start = (r, c)
            if col == "E":
                end = (r, c)
            grid_data[(r, c)] = col


def heuristic_cost_estimate(start, goal):
    return abs(goal[0] - start[0]) + abs(goal[1] - start[1])


def move(pos: Position, heading: Heading):
    """Move to the next position in the given heading"""
    dr, dc = heading
    r, c = pos
    return (r + dr, c + dc)


def turn(heading: Heading, direction: str):
    """Return the new heading after a 90 degree turn in the given direction"""
    if direction == "R":
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
    idx = deltas.index(heading)
    return deltas[(idx + 1) % 4]


def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        pos, heading = came_from[current]
        path.append((pos, heading))
        current = came_from[current]
    path.reverse()
    return path


def print_grid(grid: Grid):
    """Pretty print grid"""
    max_row = max([k[0] for k in grid.keys()]) + 1
    max_col = max([k[1] for k in grid.keys()]) + 1
    for r in range(max_row):
        line = []
        for c in range(max_col):
            line.append(grid[(r, c)])
        print("".join(line), end="")


def print_path(path, grid):
    new_grid = copy(grid)
    deltas = [
        (-1, 0),  # UP
        (0, 1),  # RIGHT
        (1, 0),  # DOWN
        (0, -1),  # LEFT
    ]

    move_symbols = ["^", ">", "v", "<"]
    for pos, heading in path:
        new_grid[pos] = move_symbols[deltas.index(heading)]

    print_grid(new_grid)


def astar(grid: Grid, start: State, end: Position):
    """Perform A-star search to find the lowest cost path"""
    open_set: List[State] = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    while open_set:
        cost, current = heapq.heappop(open_set)
        if current.pos == end:
            return cost, came_from, current
        for action in ("L", "R", "MV"):
            if action in ("L", "R"):
                cost = 1000
                next_state = State(current.pos, turn(current.heading, action))
            else:
                cost = 1
                next_position = move(current.pos, current.heading)
                next_state = State(next_position, current.heading)
            if grid.get(next_state.pos) == "#" or next_state.pos not in grid:
                cost = float("inf")
            tentative_g_score = g_score[current] + cost
            if next_state not in g_score or tentative_g_score <= g_score[next_state]:
                g_score[next_state] = tentative_g_score
                f_score = tentative_g_score + heuristic_cost_estimate(
                    next_state.pos, end
                )
                heapq.heappush(open_set, (f_score, next_state))
                came_from[(next_state)] = current


def astar2(grid: Grid, start: State, end: Position):
    """Perform search for all lowest cost paths to reach the end"""
    open_set = []
    heapq.heappush(open_set, (0, start, {start}))
    best = float("inf")
    all_paths = []
    scores = {}
    count = 0
    while open_set:
        count += 1
        current_cost, head, path = heapq.heappop(open_set)
        if current_cost > best:
            continue
        if head.pos == end:
            all_paths.append(path)
            best = current_cost
            continue
        for action in ("L", "R", "MV"):
            if action in ("L", "R"):
                cost = 1000
                next_state = State(head.pos, turn(head.heading, action))
            else:
                cost = 1
                next_position = move(head.pos, head.heading)
                next_state = State(next_position, head.heading)
            if grid.get(next_state.pos) == "#" or next_state.pos not in grid:
                continue
            if next_state not in scores or current_cost + cost <= scores[next_state]:
                scores[next_state] = current_cost + cost
                new_path = copy(path)
                new_path.add(next_state)
                heapq.heappush(open_set, (current_cost + cost, next_state, new_path))
    return all_paths, best


all_paths, best = astar2(grid_data, State(start, (0, 1)), end)
print(best)
print(len(all_paths))
sets = []
for path in all_paths:
    sets.append(set([p.pos for p in path]))

print(len(set.union(*sets)))
