"""--- Day 22: Monkey Market ---"""

from collections import deque, Counter

with open(0) as f:
    initial_secret_data = list(map(int, [l.strip() for l in f.readlines()]))


def generate(start, n):
    """Generate the nth secret number starting with start value"""
    res = 0
    def mix(secret, val):
        return secret ^ val
    def prune(val):
        return val % 16777216
    res = start
    for _ in range(n):
        res = prune(mix(res, res * 64))
        res = prune(mix(res, res // 32))
        res = prune(mix(res, res * 2048))

    return res

def calc_prices(start, n):
    prices = {}
    deltas = deque(maxlen=4)
    price = start % 10
    for _ in range(n):
        start = generate(start, 1)
        previous_price = price
        price = start % 10
        deltas.append(price - previous_price)
        D = tuple(deltas)
        if len(D) == 4 and D not in prices:
            prices[D] = price
    
    return prices


def calc_max_bananas(secrets, n):
    total = Counter()
    for secret in secrets:
        for delta, price in calc_prices(secret, n).items():
            total[delta] += price

    return total


print(sum((generate(val, 2000) for val in initial_secret_data), 0))
print(max(calc_max_bananas(initial_secret_data, 2000).values()))