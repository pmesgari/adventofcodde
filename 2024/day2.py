"""--- Day 2: Red-Nosed Reports ---"""

from typing import List

with open(0, encoding='utf-8') as f:
    reports = [list(map(int, l.strip().split())) for l in f.readlines()]


def is_safe(levels: List[int], dampen=False):
    """Determine if levels are safe or not"""
    def _is_safe(levels: List[int]):
        # a[i] < a[i+1] -> a[i+1] - a[i] > 0
        increasing = all([levels[i+1] - levels[i] in range(1, 4) for i in range(len(levels)-1)])
        # a[i] > a[i+1] -> a[i] - a[i+1] > 0
        decreasing = all([levels[i] - levels[i+1] in range(1, 4) for i in range(len(levels)-1)])

        return increasing or decreasing

    if dampen:
        if _is_safe(levels):
            return True
        for i in range(len(levels)):
            # try removing each level and check if it becomes safe
            if _is_safe(levels[:i] + levels[i+1:]):
                return True
    return _is_safe(levels)


total_safe_reports = sum(1 for report in reports if is_safe(report))
print(total_safe_reports)

total_safe_reports_with_dampen = sum(1 for report in reports if is_safe(report, dampen=True))
print(total_safe_reports_with_dampen)
