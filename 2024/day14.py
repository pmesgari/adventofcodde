"""--- Day 14: Restroom Redoubt ---"""

import math
from statistics import mean
from collections import Counter
from typing import Tuple, List, Dict

Position = Tuple[int, int]
Velocity = Tuple[int, int]
RobotCounts = Dict[Position, int]

with open(0) as f:
    lines = [l.strip() for l in f.readlines()]
    robots_input = []
    position_data = []
    velocity_data = []
    for line in lines:
        position, velocity = line.split(" ")
        position_data.append(list(map(int, position[2:].split(","))))
        velocity_data.append(list(map(int, velocity[2:].split(","))))

WIDTH = 101
HEIGHT = 103


def print_robots(robot_counts: RobotCounts):
    """Print robots positions on a grid"""
    for i in range(HEIGHT):
        line = []
        for j in range(WIDTH):
            char = "."
            if (j, i) in robot_counts:
                char = str(robot_counts[(j, i)])
            line.append(char)
        print("".join(line))


def move(start: Position, velocity: Velocity, t: int) -> Position:
    """Move the robot"""
    x1, y1 = start
    vx, vy = velocity
    x2 = (x1 + vx * t) % WIDTH
    y2 = (y1 + vy * t) % HEIGHT

    return (x2, y2)


# # move 1 second at a time
# assert move((2, 4), (2, -3), 1) == (4, 1), f"{move((2,4), (2, -3), 1)} != (4, 1)"
# assert move((4, 1), (2, -3), 1) == (6, 5), f"{move((4,1), (2, -3), 1)} != (6, 5)"
# assert move((6, 5), (2, -3), 1) == (8, 2), f"{move((6,5), (2, -3), 1)} != (8, 2)"
# assert move((8, 2), (2, -3), 1) == (10, 6), f"{move((8,2), (2, -3), 1)} != (10, 6)"
# assert move((10, 6), (2, -3), 1) == (1, 3), f"{move((10,6), (2, -3), 1)} != (1, 3)"

# # move 5 seconds at once
# assert move((2, 4), (2, -3), 5) == (1, 3), f"{move((2,4), (2, -3), 5)} != (1, 3)"


def simulate(
    positions: List[Position], velocities: List[Velocity], t: int
) -> RobotCounts:
    """Simulate movement of the robots"""
    counter = Counter()
    for idx, pos in enumerate(positions):
        new_pos = move(pos, velocities[idx], t)
        counter[new_pos] += 1
    print_robots(counter)

    quadrants = {"top-left": 0, "top-right": 0, "bottom-left": 0, "bottom-right": 0}
    for (x, y), count in counter.items():
        if x < WIDTH // 2 and y < HEIGHT // 2:
            quadrants["top-left"] += count
        elif x > WIDTH // 2 and y < HEIGHT // 2:
            quadrants["top-right"] += count
        elif x < WIDTH // 2 and y > HEIGHT // 2:
            quadrants["bottom-left"] += count
        elif x > WIDTH // 2 and y > HEIGHT // 2:
            quadrants["bottom-right"] += count

    return math.prod(quadrants.values())


def distance(p1, p2) -> int:
    """Return taxicab distance between p1 and p2"""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def find_easter_egg(positions: List[Position], velocities: List[Velocity]):
    """Simulate robot movements until easter egg emerges"""
    tmax = 10000
    best_mean = float("inf")
    best_t = 0
    for t in range(tmax):
        counter = Counter()
        for idx, pos in enumerate(positions):
            new_pos = move(pos, velocities[idx], t)
            counter[new_pos] += 1
        Xs = [pos[0] for pos in counter.keys()]
        Ys = [pos[1] for pos in counter.keys()]
        center = (mean(Xs), mean(Ys))
        new_mean = mean(distance(p, center) for p in counter.keys())
        if new_mean < best_mean:
            best_mean = new_mean
            best_t = t
    print(best_mean, best_t)


print(simulate(position_data, velocity_data, 100))
print(find_easter_egg(position_data, velocity_data))
# print(simulate(position_data, velocity_data, 7492))
