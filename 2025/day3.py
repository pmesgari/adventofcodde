with open(0, encoding='utf-8') as f:
    lines = [list(map(int, list(line))) for line in f.read().splitlines()]

def get_idx(val, start, l):
    for i in range(start, len(l)):
        if l[i] == val:
            return i
    return -1


def get_max_joltage(line):
    max_joltage = 0
    for i in range(9, 0, -1):
        a = get_idx(i, 0, line)
        if a >= 0:
            for j in range(9, 0, -1):
                b = get_idx(j, a+1, line)
                if b >= 0:
                    pair = int(f'{line[a]}{line[b]}')
                    if pair > max_joltage:
                        max_joltage = pair

    return max_joltage

# print(get_max_joltage([2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8]))

total = 0
for line in lines:
    total += get_max_joltage(line)

print(total)


def pick_batteries(line, n):
    batteries = []
    start = 0
    end = len(line) - n - 1
    for p in range(n):
        remaining = n - p - 1
        end = len(line) - remaining
        best = max(line[start:end])
        start = line.index(best, start, end) + 1
        batteries.append(str(best))

    return int(''.join(batteries))


# print(pick_batteries([8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1], 2))

total = 0
for line in lines:
    total += pick_batteries(line, 12)

print(total)


