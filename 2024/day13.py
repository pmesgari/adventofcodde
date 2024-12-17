"""--- Day 13: Claw Contraption ---"""

import re

with open(0) as f:
    chunks = []
    while True:
        # Read three lines
        chunk = [f.readline().strip() for _ in range(3)]
        if not any(chunk):
            break
        chunks.append(chunk)

        # Skip one line
        _ = f.readline()

    machines = []
    for chunk in chunks:
        machine = []
        for line in chunk[:2]:
            matches = re.findall(r"Button (A|B): X\+(\d+), Y\+(\d+)", line)
            for match in matches:
                machine.append([int(m) for m in match[1:]])
        prize_line = re.findall(r"Prize: X\=(\d+), Y\=(\d+)", chunk[-1])[0]
        machine.append([int(m) for m in prize_line])
        machines.append(machine)


def calc_tokens(machines, distance=0):
    """Calculate fewest number of tokens to win the faraway prize"""
    tokens = []
    for machine in machines:
        a, b, prize = machine
        xa, ya = a
        xb, yb = b
        xt, yt = prize
        xt += distance
        yt += distance
        best = float("inf")
        # A coefficient
        ca = (xt * yb - xb * yt) / (xa * yb - xb * ya)
        # B coefficient
        cb = (xt * ya - xa * yt) / (xb * ya - xa * yb)
        if ca >= 0 and cb >= 0 and ca.is_integer() and cb.is_integer():
            best = min(best, (ca * 3 + cb))
        tokens.append(best)
    print(sum(token for token in tokens if token != float("inf")))


calc_tokens(machines=machines)
calc_tokens(machines=machines, distance=10000000000000)
