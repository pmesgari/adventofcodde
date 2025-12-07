import re
import math


def part1():
    with open(0, encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
        numbers = [re.split(r'\s+', line) for line in lines[:len(lines) - 1]]
        numbers = [list(map(int, line)) for line in numbers]
        ops = re.split(r'\s+', lines[-1])
    max_row = len(numbers)
    max_col = len(numbers[0])
    solutions = []
    for col in range(max_col):
        problem = []
        for row in range(max_row):
            problem.append(numbers[row][col])
        if ops[col] == '*':
            solutions.append(math.prod(problem))
        else:
            solutions.append(sum(problem))
    # print(solutions)
    print(sum(solutions))


def solve(nums, op):
    values = [int(''.join(val)) for val in nums]

    if op == '*':
        return math.prod(values)
    return sum(values)


def part2():
    with open(0, encoding='utf-8') as f:
        lines = [line.strip('\n') for line in f.readlines()]
        ops = re.split(r'\s+', lines[-1].strip())

    max_length = len(lines[0])
    total = 0
    ops_idx = 0
    nums = []
    for i in range(max_length):
        v_slice = []
        for j in range(len(lines) - 1):
            v_slice.append(lines[j][i])
        if all([val == ' ' for val in v_slice]):
            total += solve(nums, ops[ops_idx])
            ops_idx += 1
            nums = []
        else:
            nums.append(v_slice)

    total += solve(nums, ops[ops_idx])
    print(total)


# part1()
part2()