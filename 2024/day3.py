"""--- Day 3: Mull It Over ---"""

import re

with open(0, encoding='utf-8') as f:
    content = f.read()


total = 0
match = re.findall(r"mul\((\d+),(\d+)\)", content)
for item in match:
    x, y = item
    total += int(x) * int(y)

print(total)

total = 0
match = re.findall(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))", content)
enable = True
# we either match a mul(x,y), a do(), or a don't()
for item in match:
    # remember the most recent do or don't
    if 'do()' in item:
        enable = True
    elif 'don\'t()' in item:
        enable = False
    else:
        x, y = item[:2]
        total += int(x) * int(y) * enable

print(total)
