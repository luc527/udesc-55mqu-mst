from heapq import heappop, heappush
import graphviz
import sys

def square_matrix(n, x):
    m = [[] for _ in range(n)]
    for i in range(n):
        m[i] = [x for _ in range(n)]
    return m

def print_matrix(m):
    for i in range(0, len(m)):
        for j in range(0, len(m[i])):
            print(m[i][j], end='\t')
        print()

def parse_instance(filename):
    with open(filename, 'r') as fp:
        lines = fp.readlines()

    lines = filter(lambda l: l[0] != '#', lines)  #remove comments
    lines = map(lambda l: l[:-1], lines)  #remove '\n'

    verts = int(next(lines))
    edges = int(next(lines))

    weights = square_matrix(verts, float('inf'))

    for line in lines:
        toks = line.split(' ')
        a, b, w = int(toks[0]), int(toks[1]), float(toks[2])
        weights[a][b] = w
        weights[b][a] = w

    return weights

def output_image(name, adj, mst):
    verts = len(adj)
    g = graphviz.Graph(name, engine='neato')
    g.attr('node', {'shape': 'point'})
    g.attr(None, {'splines': 'true'})
    g.attr('edge', {'fontsize': '8'})
    for a in range(verts):
        g.node(str(a))
    for b in range(verts):
        for a in range(b):
            if adj[a][b] == float('inf'):
                continue
            attr = {'weight': str( int(1000 - 1000*adj[a][b]) )}
            if mst[a][b]:
                attr['penwidth'] = '3'
            label = ''
            if verts < 50:
                label = str(adj[a][b])
            g.edge(str(a), str(b), label, attr)
    print(f'Rendered graph {name}, see {g.render()}')

def lazy_prim(adj):
    verts = len(adj)

    marked  = [False for _ in range(verts)]
    weight  = 0.0
    pq      = []

    # Return both adjacency matrix and adjacency list representation
    mst     = square_matrix(verts, False)
    edges   = []

    def visit(a):
        marked[a] = True
        for b in range(verts):
            if adj[a][b] == float('inf'):
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
