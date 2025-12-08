import math
from collections import Counter


with open(0, encoding='utf-8') as f:
    points = []
    for line in f:
        points.append(list(map(int, line.strip().split(','))))


distances = []
for i in range(len(points)):
    x1, y1, z1 = points[i]
    for j in range(i + 1, len(points)):
        x2, y2, z2 = points[j]
        dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
        distances.append((dist, i, j))

sorted_distances = sorted(distances, key=lambda x: x[0])


class UF:
    def __init__(self, N):
        self.ids = [i for i in range(N)]
        self.count = N

    def find(self, p):
        return self.ids[p]
    
    def connected(self, p, q):
        return self.find(p) == self.find(q)
    
    def union(self, p, q):
        pid = self.find(p)
        qid = self.find(q)

        if pid == qid:
            return
        
        for i in range(len(self.ids)):
            if self.ids[i] == pid:
                self.ids[i] = qid
        
        self.count -= 1

    def main(self, distances, limit=None):
        subset = distances[:limit] if limit else distances

        for _, p, q in subset:
            if self.connected(p, q):
                continue
            self.union(p, q)

        return p, q


def part1():
    uf = UF(len(points))
    uf.main(sorted_distances, 1000)

    ids = uf.ids
    counter = Counter(ids)
    total = 1
    for _, c in counter.most_common(3):
        total *= c
    
    print(total)


def part2():
    uf = UF(len(points))

    round = 1
    while not all([id == uf.ids[0] for id in uf.ids]):
        p, q = uf.main(sorted_distances, round)
        round += 1

    print(points[p][0] * points[q][0])

    
part1()
part2()
