"""--- Day 7: Bridge Repair ---"""
from typing import List


with open(0, encoding='utf-8') as f:
    equations_input = [l.strip() for l in f.readlines()]
    test_values = []
    numbers = []
    for eq in equations_input:
        test_val, nums = eq.split(': ')
        test_values.append(int(test_val))
        numbers.append(list(map(int, nums.split(' '))))


def calc_calibration_result(test_val: int, equation: List[int], concat: bool=False) -> int:
    """Given an equation calculate the calibration result
    T[0] = [equation[0]]
    T[i] = [
        T[i-1][j] + equation[i],
        T[i-1][j] * equation[i]
    ]
    1 <= i < len(equation)
    1 <= j < len(T[i-1])

    return test_val if any T[-1] == test_val otherwise 0

    To include the concat operation we change the recurrence relation to

    T[i] = [
        T[i-1][j] + equation[i],
        T[i-1][j] * equation[i],
        equation[i-1] || equation[i], if i == 1
        T[i-1][j] || equation[i], if i >= 2
    ]
    1 <= i < len(equation)
    1 <= j < len(T[i-1])

    292
        11
            11
        11 6
            11 * 6
            11 + 6
        11 6 16
            11 * 6 + 16
            11 + 6 + 16
            11 * 6 * 16
            11 + 6 * 16
        11 6 16 20
            11 * 6 + 16 + 20
            11 + 6 + 16 + 20
            11 * 6 * 16 + 20
            11 + 6 * 16 + 20
            11 * 6 + 16 * 20
            11 + 6 + 16 * 20
            11 * 6 * 16 * 20
            11 + 6 * 16 * 20
    7290    6 8 6 15
        6
            6
        6 8
            6 + 8
            6 * 8
            6 || 8
        6 8 6
            6 + 8 + 6
            6 * 8 + 6
            6 || 8 + 6
            6 + 8 * 6
            6 * 8 * 6
            6 || 8 * 6
            6 + 8 || 6
            6 * 8 || 6
            6 || 8 || 6

    """
    if len(equation) == 1 and equation[0] == test_val:
        return test_val
    elif len(equation) == 1 and equation[0] != test_val:
        return 0
    T = [[]] * len(equation)
    T[0] = [equation[0]]

    for i in range(1, len(equation)):
        t = []
        for j in range(len(T[i-1])):
            t.append(T[i-1][j] * equation[i])
            t.append(T[i-1][j] + equation[i])
            if concat:
                if i == 1:
                    t.append(int(f'{equation[i-1]}{equation[i]}'))
                else:
                    prev = T[i-1][j]
                    t.append(int(f'{prev}{equation[i]}'))

        T[i] = t
    for val in T[-1]:
        if val == test_val:
            return test_val
    return 0

# print(calc_calibration_result(190, [10, 19]))
# print(calc_calibration_result(3267, [81, 40, 27]))
# print(calc_calibration_result(292, [11, 6, 16, 20]))


def calc_total_calibration_result() -> int:
    """Calculate the total calibration result"""
    total = 0
    for idx, val in enumerate(test_values):
        result = calc_calibration_result(val, numbers[idx])
        if result == 0:
            result = calc_calibration_result(val, numbers[idx], concat=True)
        total += result

    return total

print(calc_total_calibration_result())
