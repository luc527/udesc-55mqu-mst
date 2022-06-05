from heapq import heappop, heappush
import graphviz
import sys
from pyomo.environ import *
from itertools import chain, combinations

# M = float('inf')        # solver doesn't even run with this
# M = sys.float_info.max  # solver gives incorrect solution with this (took me WAY to long to find out)
M = 100000

"""
Generates a n-by-n matrix with all cells set to x
"""
def square_matrix(n, x):
    m = [[] for _ in range(n)]
    for i in range(n):
        m[i] = [x for _ in range(n)]
    return m

"""
Prints a matrix, separating rows by \n and cols by \t
"""
def print_matrix(m):
    for i in range(0, len(m)):
        for j in range(0, len(m[i])):
            print(m[i][j] if m[i][j] != M else 'INF', end='\t')
        print()

"""
Parses a file describing a weighted undirected graph and returns the graph
represented as an adjacency matrix adj, where adj[i][j] is the weight of the
edge from i to j (equal to adj[j][i]), or M (global) if there's no edge connecting
i and j.
"""
def parse_instance(filename):
    with open(filename, 'r') as fp:
        lines = fp.readlines()

    lines = filter(lambda l: l[0] != '#', lines)  #remove comments
    lines = map(lambda l: l[:-1], lines)  #remove '\n'

    verts = int(next(lines))
    edges = int(next(lines))

    weights = square_matrix(verts, M)

    for line in lines:
        toks = line.split(' ')
        a, b, w = int(toks[0]), int(toks[1]), float(toks[2])
        weights[a][b] = w
        weights[b][a] = w

    return weights

"""
Outputs a graph along with its minimum spanning tree as an image.
The image will be named f'{name}.gv.pdf'.
The graph (adj) is expected to be a float[][], and the minimum spanning
tree (mst) a boolean[][].
"""
def output_image(name, adj, mst):
    verts = len(adj)
    g = graphviz.Graph(name, engine='neato')
    g.attr('node', {'shape': 'point'})
    g.attr('edge', {'fontsize': '8'})
    for a in range(verts):
        g.node(str(a))
    for b in range(verts):
        for a in range(b):
            if adj[a][b] == M:
                continue
            attr = {'weight': str( int(1000 - 1000*adj[a][b]) )}
            if mst[a][b]:
                attr['color'] = 'red'
                attr['penwidth'] = '3'
            label = ''
            if verts < 50:
                label = str(adj[a][b])
            g.edge(str(a), str(b), label, attr)
    print(f'Rendered graph {name}, see {g.render()}')

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

"""
Solves the minimum spanning tree problem using integer linear programming.
Expects the graph (adj) to be represented as a float[][].
Returns { mst, edges, weight } just like lazy_prim()
"""
def int_prog(adj):
    v = len(adj)

    model = ConcreteModel()

    # Decision variable: x[i][j] = whether the edge i-j is part of thre MST (1) or not (0)
    model.x = Var(range(v), range(v), domain=Boolean)

    # Objective: minimize tree weight
    model.obj = Objective( \
        sense=minimize, \
        expr=sum(adj[i][j] * model.x[i,j] for i in range(v) for j in range(i+1, v)) \
    )

    model.con = ConstraintList()

    # The tree subgraph needs to be undirected
    for i in range(v):
        for j in range(i+1, v):
            model.con.add(expr=model.x[i,j] == model.x[j,i])

    # Has to be a spanning tree

    # - Has exactly v-1 edges
    model.con.add(expr=sum(model.x[i,j] for i in range(v) for j in range(i+1, v)) == v - 1)

    # - Has no cycles
    # Or, equivalently, every subset S of vertices has no more than |S|-1 edges in it
    # (e.g. connect any three of {0,1,2,3} and try adding another edge without creating a cycle)
    vs = list(range(v))
    subsets = chain.from_iterable(combinations(vs, r) for r in range(1, len(vs)))
    for s in subsets:
        model.con.add(expr=sum(model.x[i,j] for i in s for j in s if i <= j) <= len(s) - 1)

    opt = SolverFactory('glpk')
    opt.solve(model)

    edges = []
    mst = square_matrix(v, False)
    for j in range(v):
        for i in range(j):
            if model.x[i,j]() == 1:
                edges.append((adj[i][j], i, j))
                mst[i][j] = True
                mst[j][i] = True
    weight = model.obj()

    return { \
        'mst': mst, \
        'edges': edges, \
        'weight': weight \
    }

print('Parsing instance...')
adj = parse_instance(sys.argv[1])

if (len(sys.argv) > 2 and sys.argv[2] == 'prim'):
    print('Finding MST by Prim\'s algorithm...')
    result = lazy_prim(adj)
else:
    print('Finding MST by solving an integer programming model...')
    result = int_prog(adj)

print('edges', result['edges'], 'weight', result['weight'])
print('Outputting image...')
output_image(sys.argv[1], adj, result['mst'])
