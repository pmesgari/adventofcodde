import re
import z3


def solve_z3(buttons, targets, mode):
    """
    Generic solver using Z3.
    mode: 'toggle' (Part 1, mod 2) or 'add' (Part 2, integer)
    """
    opt = z3.Optimize()

    # Create variables
    # For 'toggle', we only care about 0 or 1 press.
    # For 'add', we can press multiple times (>= 0).
    x_vars = [z3.Int(f"x_{i}") for i in range(len(buttons))]

    for x in x_vars:
        opt.add(x >= 0)
        if mode == "toggle":
            opt.add(x <= 1)

    # Constraints
    for row_idx, target_val in enumerate(targets):
        row_sum = 0
        for btn_idx, affected_rows in enumerate(buttons):
            if row_idx in affected_rows:
                row_sum += x_vars[btn_idx]

        if mode == "toggle":
            # In toggle mode, the sum of presses modulo 2 must match the target (0 or 1)
            opt.add(row_sum % 2 == target_val)
        else:
            # In add mode, the sum must exactly match the integer target
            opt.add(row_sum == target_val)

    # Objective: Minimize total button presses
    total_presses = z3.Sum(x_vars)
    opt.minimize(total_presses)

    if opt.check() == z3.sat:
        return opt.model().eval(total_presses).as_long()
    return 0


def parse_line(line):
    """Parses a single line into button definitions and targets for both parts."""
    # Parse Buttons: (1,3) (2) ...
    # Each tuple represents indices affected by that button
    btn_matches = re.findall(r"\(([0-9,]+)\)", line)
    buttons = [list(map(int, m.split(","))) for m in btn_matches]

    # Parse Part 1 Target: [.##.] -> [0, 1, 1, 0]
    p1_match = re.search(r"\[(.*?)\]", line)
    targets_p1 = []
    if p1_match:
        targets_p1 = [1 if c == "#" else 0 for c in p1_match.group(1)]

    # Parse Part 2 Target: {3,5,4,7} -> [3, 5, 4, 7]
    p2_match = re.search(r"\{([0-9,-]+)\}", line)
    targets_p2 = []
    if p2_match:
        targets_p2 = list(map(int, p2_match.group(1).split(",")))

    return buttons, targets_p1, targets_p2


def main():
    with open(0) as f:
        lines = [line.strip() for line in f if line.strip()]

    total_p1 = 0
    total_p2 = 0

    for line in lines:
        buttons, t1, t2 = parse_line(line)

        if t1:
            total_p1 += solve_z3(buttons, t1, mode="toggle")

        if t2:
            total_p2 += solve_z3(buttons, t2, mode="add")

    print(f"Part 1: {total_p1}")
    print(f"Part 2: {total_p2}")


if __name__ == "__main__":
    main()
