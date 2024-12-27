"""--- Day 19: Linen Layout ---"""

from typing import List

with open(0) as f:
    lines = [line.strip() for line in f.readlines()]
    pattern_data = [patt.strip() for patt in lines[0].split(",")]
    design_data = lines[2:]


def count_designs(patterns: str, designs: List[str]) -> int:
    """Count number of possible designs and the number of design alternatives"""
    cache = {}
    def can_make(design: str):
        if design in cache:
            return cache[design]
        if not design:
            cache[design] = True
            return 1
        total = 0
        for patt in patterns:
            if design.startswith(patt):
                total += can_make(design[len(patt):])
        cache[design] = total
        return total

    possible = sum((can_make(design) > 0 for design in designs), 0)
    ways = sum((can_make(design) for design in designs), 0)
    return possible, ways


print(count_designs(pattern_data, design_data))
