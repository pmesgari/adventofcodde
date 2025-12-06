from typing import Tuple, List

Range = Tuple[int, int]

with open(0, encoding='utf-8') as f:
    ranges: List[Range] = []
    ingredients = []

    for line in f:
        if line == '\n':
            break
        a, b = line.split('-')
        ranges.append((int(a), int(b)))
    
    for line in f:
        ingredients.append(int(line))

def part1():
    count = 0
    for id in ingredients:
        for a, b in ranges:
            if id >= a and id <= b:
                count += 1
                break

    print(count)


def merge_ranges(ranges: List[Range]):
    """Sort ranges, then merge all overlapping ranges"""
    
    ranges.sort(key=lambda r: r[0])

    current_range = ranges[0]

    merged_ranges = []
    i = 1
    while i < len(ranges):
        a1, b1 = current_range
        a2, b2 = ranges[i]

        # overlap
        if (a2 <= b1 and b2 >= a1):
            current_range = (min(a1, a2), max(b1, b2))
        # disjoint
        else:
            merged_ranges.append(current_range)
            current_range = (a2, b2)
        i += 1

    merged_ranges.append(current_range)
    return merged_ranges


def test_merge_ranges():
    # 1. Basic Overlap
    # Ranges overlap significantly
    assert merge_ranges([(1, 5), (4, 8)]) == [(1, 8)]

    # 2. Touching Ranges
    # Ranges touch exactly at 5 (inclusive ranges usually merge here)
    assert merge_ranges([(1, 5), (5, 10)]) == [(1, 10)]

    # 3. Subset / Nested Ranges
    # (3, 6) is completely inside (1, 10)
    assert merge_ranges([(1, 10), (3, 6)]) == [(1, 10)]

    # 4. Subset with matching start
    assert merge_ranges([(1, 10), (1, 5)]) == [(1, 10)]

    # 5. Subset with matching end
    assert merge_ranges([(1, 10), (5, 10)]) == [(1, 10)]

    # 6. Disjoint Ranges
    # A gap exists between 5 and 7
    assert merge_ranges([(1, 5), (7, 10)]) == [(1, 5), (7, 10)]

    # 7. Unsorted Inputs
    # The function should handle inputs that aren't pre-sorted
    unsorted_input = [(10, 12), (1, 5), (8, 15)]
    # Logic: (1, 5) is first. (8, 15) swallows (10, 12).
    assert merge_ranges(unsorted_input) == [(1, 5), (8, 15)]

    # 8. Chain Merge
    # A chain reaction: (1,3) touches (2,4) which touches (3,6)
    chain_input = [(1, 3), (2, 4), (3, 6)]
    assert merge_ranges(chain_input) == [(1, 6)]

    # 9. Duplicate Ranges
    assert merge_ranges([(1, 5), (1, 5)]) == [(1, 5)]

    # 10. Single Range
    assert merge_ranges([(1, 5)]) == [(1, 5)]

    # 11. Complex Mix
    # Combines overlaps, subsets, and gaps
    complex_input = [
        (1, 4),   # Merges with (2, 5) -> (1, 5)
        (8, 10),  # Merges with (9, 11) -> (8, 11)
        (2, 5), 
        (15, 20), # Consumes (16, 18) -> (15, 20)
        (16, 18), 
        (9, 11)
    ]
    expected_complex = [(1, 5), (8, 11), (15, 20)]
    assert merge_ranges(complex_input) == expected_complex


def part2():
    count = 0
    merged_ranges = merge_ranges(ranges)
    for a1, b1 in merged_ranges:
        count += (b1 - a1 + 1)

    print(count)


part1()
part2()
