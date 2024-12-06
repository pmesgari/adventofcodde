"""--- Day 5: Print Queue ---"""

from typing import List, Tuple

RulesType = List[Tuple[int, int]]

with open(0) as f:
    rules = []
    pages = []
    for line in f:
        if line == '\n':
            break
        x, y = map(int, line.strip().split('|'))
        rules.append((x, y))

    for line in f:
        pages.append(list(map(int, line.strip().split(','))))


def is_valid_order(rules: RulesType, page: List[int]):
    """Check if a page follows the given rules"""
    for x, y in rules:
        if x in page and y in page:
            if page.index(x) > page.index(y):
                return False
    return True


def apply(rules: RulesType, page: List[int]):
    """Apply the rules to the page
    If all the rules succeed return the middle page number
    """
    return page[len(page) // 2] if is_valid_order(rules, page) else 0


def sum_middle_pages(rules: RulesType, pages: List[int]):
    """Sum the middle pages of all valid page orderings"""
    return sum(apply(rules, page) for page in pages)


def fix(rules: RulesType, page: List[int]):
    """Keep applying the rules until the page order is correct"""
    changing = True
    
    while changing:
        changing = False
        for x, y in rules:
            if x in page and y in page:
                x_idx = page.index(x)
                y_idx = page.index(y)
                if x_idx > y_idx:
                    page[x_idx] = y
                    page[y_idx] = x
                    changing = True
                    continue

    return page


def sum_fixed_middle_pages(rules: RulesType, pages: List[int]):
    """Sum the middle pages of all fixed pages"""
    total = 0
    for page in pages:
        if not is_valid_order(rules, page):
            fixed_page = fix(rules, page)
            total += fixed_page[len(fixed_page) // 2]
    
    return total

print(sum_middle_pages(rules, pages))
print(sum_fixed_middle_pages(rules, pages))
