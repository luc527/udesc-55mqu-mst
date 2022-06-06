from common import *
from heapq import heappop, heappush
import sys

"""
Solves the minimum spanning tree problem with a lazy implementaton of Prim's
algorithm. Based on https://algs4.cs.princeton.edu/43mst/.
Expects the graph (adj) to be represented as a float[][].
Returns {
    mst: bool[][] (adjacency matrix representation of the minimum spanning tree)
    edges: (weight, a, b)[] (adjacency list representation of the minimum spanning tree)
    weight: total weight of the minimum spanning tree (sum of the weight of each edge in the tree)
}
"""
def lazy_prim(adj):
    verts = len(adj)

    marked = [False for _ in range(verts)]
    pq     = []

    mst    = square_matrix(verts, False)
    edges  = []
    weight = 0.0

    def visit(a):
        marked[a] = True
        for b in range(verts):
            if adj[a][b] == M:
                continue
            if marked[b]:
                continue
            heappush(pq, (adj[a][b], a, b))

    visit(0)
    while pq:
        (w, a, b) = heappop(pq)
        if marked[a] and marked[b]:
            continue
        weight += w

        edges.append((w, min(a,b), max(a,b)))
        mst[a][b] = True
        mst[b][a] = True

        if not marked[a]:
            visit(a)
        if not marked[b]:
            visit(b)

    return { \
        'mst': mst, \
        'edges': edges, \
        'weight': weight \
    }

print('Parsing instance...')
adj = parse_instance(sys.argv[1])

print('Finding MST by Prim\'s algorithm...')
result = lazy_prim(adj)

print('edges', result['edges'], 'weight', result['weight'])
print('Outputting image...')
output_image(sys.argv[1], adj, result['mst'])