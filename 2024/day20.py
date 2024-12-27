"""--- Day 20: Race Condition ---"""

from typing import Tuple, List, Dict
import heapq

Position = Tuple[int, int]
Grid = Dict[Position, str]

with open(0) as f:
    grid_data = {}
    start = None
    end = None
    for y, row in enumerate(f):
        for x, col in enumerate(row):
            if col == "S":
                start = (x, y)
            if col == "E":
                end = (x, y)
            grid_data[(x, y)] = col

def dijkstra(grid, start, end) -> Dict[Position, int]:
    """Run dijkstra to find the min distance from start to every other node"""
    deltas = [
        (0, -1),  # UP
        (1, 0),  # RIGHT
        (0, 1),  # DOWN
        (-1, 0),  # LEFT
    ]
    open_set: List[Tuple[int, Position]] = []
    heapq.heappush(open_set, (0, start))
    distances = {} 
    distances[start] = 0
    parent = {start: None}
    while open_set:
        d, pos = open_set.pop()
        x, y = pos
        for dx, dy in deltas:
            xn = x + dx
            yn = y + dy
            if (xn, yn) not in grid or grid[(xn, yn)] == '#':
                continue
            if (xn, yn) not in distances:
                distances[((xn, yn))] = d + 1
                parent[(xn, yn)] = (x, y)
                heapq.heappush(open_set, (d + 1, (xn, yn)))

    path = []
    current = end
    while current in parent:
        if parent[current]:
            path.append(parent[current])
        current = parent[current]
    
    count = 0
    for p1, d in distances.items():
        x1, y1 = p1
        for dx, dy in deltas:
            p2 = (x1 + dx, y1 + dy)
            if grid[p2] == '#':
                x2, y2 = p2
                p3 = (x2 + dx, y2 + dy)
                if p3 in distances and (distances[p1] - distances[p3] >= 102):
                    count += 1
    print(count)

    def adj(point, radius):
        """Find all neighbors of the given point within the radius
        We can traverse up to 20 cells in each cheat. Any of these
        patterns are eligible for a cheat, X is the start point. A cheat will be
        either horizontal, vertical or L-shaped.

        ---X----

           |
           |
           X
           |
           |
           
              |
              |
        ---X--|   ---X--|
                        |
                        |
        """
        result = []
        x, y = point
        for dx in range(-radius, radius + 1):
            for dy in range(-(radius - abs(dx)), radius - abs(dx) + 1):
                result.append((x + dx, y + dy))
        return result
    
    def manhattan_distance(p, q) -> int:
        return abs(p[0] - q[0]) + abs(p[1] - q[1])
    
    count = 0
    for p1, d in distances.items():
        for p2 in adj(p1, 20):
            if p2 in distances and (distances[p1] - distances[p2] >= 100 + manhattan_distance(p1, p2)):
                count += 1

    print(count)

dijkstra(grid_data, start, end)
