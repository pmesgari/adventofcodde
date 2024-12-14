"""--- Day 11: Plutonian Pebbles ---"""

from typing import List
from collections import Counter

with open(0, encoding='utf-8') as f:
    stones_input = list(map(int, f.readline().split(' ')))


def apply(stone: int) -> dict:
    """Apply the rules to a given stone"""
    if stone == 0:
        return [1]
    if len(str(stone)) % 2 == 0:
        mid = len(str(stone)) // 2
        left = int(str(stone)[:mid])
        right = int(str(stone)[mid:])
        return [left, right]
    return [stone * 2024]


def blink(stones: List[int], iteration=1) -> List[int]:
    """Blink and apply the rules"""
    counter = Counter(stones)

    for _ in range(iteration):
        c = Counter()
        for stone in counter:
            for change in apply(stone):
                c[change] += counter[stone]
        counter = c

    return counter.total()


print(blink(stones=stones_input, iteration=25))
print(blink(stones=stones_input, iteration=75))
