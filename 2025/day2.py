with open(0, encoding='utf-8') as f:
    line = f.readline().strip().split(',')
    ranges = [list(map(int, item.split('-'))) for item in line if item]


max_val = 0
for r1, r2 in ranges:
    if r1 > max_val:
        max_val = r1
    if r2 > max_val:
        max_val = r2

max_length = len(str(max_val))

def generate_ids(seed, max_val):
    ids = []
    s_seed = str(seed)
    
    current_s = s_seed * 2
    
    while int(current_s) <= max_val:
        ids.append(int(current_s))
        current_s += s_seed
        
    return ids


def is_composed(seed):
    s_seed = str(seed)
    n = len(s_seed)
    for l in range(1, n // 2 + 1):
        if n % l == 0 and s_seed[:l] * (n // l) == s_seed:
            return True
    
    return False


def find_fake_ids(ranges):
    total = 0
    for i in range(1, 10 ** (max_length // 2)):
        if is_composed(i):
            continue
        ids = generate_ids(i, max_val)
        for next_id in ids:
            for r1, r2 in ranges:
                if next_id >= r1 and next_id <= r2:
                    total += next_id
    return total


print(find_fake_ids(ranges))