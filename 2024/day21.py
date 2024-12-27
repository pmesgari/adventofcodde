"""--- Day 21: Keypad Conundrum ---"""

import heapq
from copy import copy
from itertools import product
from dataclasses import dataclass
from collections import namedtuple
from typing import Tuple, Dict, List


with open(0) as f:
    code_data = [l.strip() for l in f.readlines()]


@dataclass(frozen=True)
class Point2D:
    x: int
    y: int

    def diff_to_char(self, other):
        diff = other - self
        match diff:
            case Point2D(0, -1):
                return "^"
            case Point2D(1, 0):
                return ">"
            case Point2D(0, 1):
                return "v"
            case Point2D(-1, 0):
                return "<"
        raise Exception("Illegal diff")

    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return isinstance(other, Point2D) and (self.x, self.y) == (other.x, other.y)

    def __lt__(self, other):
        pass

    def __gt__(self, other):
        pass


deltas = [
    Point2D(0, -1),  # UP
    Point2D(1, 0),  # RIGHT
    Point2D(0, 1),  # DOWN
    Point2D(-1, 0),  # LEFT
]

"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""
numeric_pad: Dict[Point2D, str] = {
    Point2D(0, 0): "7",
    Point2D(1, 0): "8",
    Point2D(2, 0): "9",
    Point2D(0, 1): "4",
    Point2D(1, 1): "5",
    Point2D(2, 1): "6",
    Point2D(0, 2): "1",
    Point2D(1, 2): "2",
    Point2D(2, 2): "3",
    Point2D(1, 3): "0",
    Point2D(2, 3): "A",
}
numeric_pad_inv = {v: k for k, v in numeric_pad.items()}
"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
directional_pad: Dict[Point2D, str] = {
    Point2D(1, 0): "^",
    Point2D(2, 0): "A",
    Point2D(0, 1): "<",
    Point2D(1, 1): "v",
    Point2D(2, 1): ">",
}
directional_pad_inv = {v: k for k, v in directional_pad.items()}


State = namedtuple("State", ["cost", "path"])


def find_lowest_cost_paths(
    start: Point2D, end: Point2D, pad: Dict[Point2D, str]
) -> List[str]:
    """Find all the lowest cost paths between two points"""
    open_set = []

    heapq.heappush(open_set, State(0, [start]))
    best = float("inf")
    all_paths = []
    while open_set:
        current_cost, path = heapq.heappop(open_set)
        if current_cost > best:
            continue
        head = path[-1]
        if head == end:
            all_paths.append(
                [p1.diff_to_char(p2) for p1, p2 in list(zip(path, path[1:]))] + ["A"]
            )
            best = current_cost
            continue
        for action in deltas:
            next_position = head + action
            if next_position not in pad:
                continue
            new_path = copy(path)
            new_path.append(head + action)
            next_state = State(current_cost + 1, new_path)
            heapq.heappush(open_set, next_state)

    return all_paths


all_pairs_numeric_paths: Dict[Tuple[str, str], List[str]] = {}
for pair in list(product(numeric_pad.keys(), repeat=2)):
    start, end = pair
    all_pairs_numeric_paths[numeric_pad[start], numeric_pad[end]] = (
        find_lowest_cost_paths(start, end, numeric_pad)
    )

all_pairs_directional_paths: Dict[Tuple[str, str], List[str]] = {}
for pair in list(product(directional_pad.keys(), repeat=2)):
    start, end = pair
    all_pairs_directional_paths[directional_pad[start], directional_pad[end]] = (
        find_lowest_cost_paths(start, end, directional_pad)
    )


def find_cost(code: Tuple[str, str], levels: int) -> int:
    """Find the cost for executing the given code"""

    def total_presses(path: List[str], level: int) -> int:
        total = 0
        for pair in zip(["A"] + list(path), (["A"] + list(path))[1:]):
            total += cache[(level, *pair)]
        return total

    cache = {}
    for pair in list(product(directional_pad.keys(), repeat=2)):
        start, end = pair
        cache[(0, directional_pad[start], directional_pad[end])] = 1

    for level in range(1, levels):
        keypad = numeric_pad if level == levels - 1 else directional_pad
        all_paths = (
            all_pairs_numeric_paths
            if level == levels - 1
            else all_pairs_directional_paths
        )
        for pair in list(product(keypad.keys(), repeat=2)):
            start, end = pair
            paths = all_paths[(keypad[start], keypad[end])]
            candidates = []
            for path in paths:
                press = total_presses(path, level - 1)
                candidates.append(press)

            cache[(level, keypad[start], keypad[end])] = min(candidates)

    return total_presses(code, levels - 1)


def complexity(code, cost):
    return int("".join([char for char in code if char.isdigit()])) * cost


print(sum((complexity(code, find_cost(code, 4)) for code in code_data), 0))
print(sum((complexity(code, find_cost(code, 27)) for code in code_data), 0))
