"""--- Day 23: LAN Party ---"""

from collections import defaultdict
import networkx as nx


with open(0) as f:
    connection_data = [l.strip().split('-') for l in f.readlines()]


E = defaultdict(set)

for c1, c2 in connection_data:
    E[c1].add(c2)
    E[c2].add(c1)


triples = set()
for u, e in E.items():
    for v in e:
        for w, e in E.items():
            if w == u or w == v:
                continue
            if u in e and v in e:
                triples.add(tuple(sorted((u, v, w))))

count = 0
for triple in triples:
    if any((conn.startswith('t') for conn in triple)):
        count += 1

print(count)

G = nx.Graph()
G.add_edges_from(connection_data)
largest_clique = max(nx.find_cliques(G), key=len)
print(','.join(sorted(largest_clique)))