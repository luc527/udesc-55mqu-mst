import graphviz

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


    lastidx = 0
    for i, c in enumerate(name):
        if c == '/':
            lastidx = i
    name = name[lastidx+1:]

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

    dir = 'images'
    print(f'Rendered graph {name}, see {g.render(directory=dir)}')