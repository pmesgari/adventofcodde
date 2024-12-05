"""--- Day 4: Ceres Search ---"""

with open(0, encoding="utf-8") as f:
    grid = [list(l.strip()) for l in f.readlines()]


HEIGHT = len(grid)
WIDTH = len(grid[0])
XMAS = "XMAS"


def get_sequence(grid, start, direction, length):
    """Retrieve a sequence of characters in the given direction"""
    height = len(grid)
    weidth = len(grid[0])
    sequence = ""
    r, c = start
    dr, dc = direction
    rr = r
    cc = c
    for _ in range(length):
        rr += dr
        cc += dc
        if rr < 0 or rr >= height or cc < 0 or cc >= weidth:
            return ""
        sequence += grid[rr][cc]

    return sequence


def count_xmas():
    """Count how many times XMAS appears"""
    dirs = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))
    total = 0
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if grid[r][c] != "X":
                continue
            start = (r, c)
            for dir in dirs:
                if grid[r][c] + get_sequence(grid, start, dir, len(XMAS) - 1) == XMAS:
                    total += 1

    return total


def is_xmas_cross(grid):
    """Given a 3x3 grid verify if it forms an X-MAS
    An X-MAS is one of the following:

    M   S
      A
    M   S

    M   M
      A
    S   S

    S   M
      A
    S   M

    S   S
      A
    M   M
    """
    if grid[0][0] + get_sequence(grid, (0, 0), (1, 1), 2) in ["MAS", "SAM"]:
        if grid[0][2] + get_sequence(grid, (0, 2), (1, -1), 2) in ["MAS", "SAM"]:
            return True
    return False


def count_xmas_cross():
    """Count how many times X-MAS appears"""
    total = 0
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if grid[r][c] not in ["M", "S"]:
                continue
            # make a smaller grid of size 3x3
            if r + 2 >= HEIGHT or c + 2 >= WIDTH:
                continue
            grid_3x3 = []
            for i in range(3):
                row = []
                for j in range(3):
                    row.append(grid[r + i][c + j])
                grid_3x3.append(row)
            if is_xmas_cross(grid_3x3):
                total += 1

    return total


print(count_xmas())
print(count_xmas_cross())
