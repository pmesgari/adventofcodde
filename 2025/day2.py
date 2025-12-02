with open(0, encoding='utf-8') as f:
    line = f.readline().strip().split(',')
    ranges = [list(map(int, item.split('-'))) for item in line if item]


def chunk(s, n):
    return [s[i:i+n] for i in range(0, len(s), n)]

invalid_ids = 0
for start, end in ranges:
    # print(start, end)
    while start <= end:
        mid = len(str(start)) // 2
        if str(start)[:mid] == str(start)[mid:]:
            invalid_ids += start
            # print('\t' + str(start))
        start += 1

# print(invalid_ids)

total = 0
seen = set()
for start, end in ranges:
    while start <= end:
        for n in range(1, len(str(start)) // 2 + 1):
            chunks = chunk(str(start), n)
            if all(c == chunks[0] for c in chunks) and start not in seen:
                total += start
                seen.add(start)
                # print(start, chunks)
        start += 1

print(total)