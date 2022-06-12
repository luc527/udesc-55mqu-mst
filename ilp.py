from common import *
import sys
from pyomo.environ import *
from itertools import chain, combinations
from time import time

"""
Solves the minimum spanning tree problem using integer linear programming
(or gives up if it takes too much time -- more than time_limit seconds, if time_limit > 0).
Expects the graph (adj) to be represented as a float[][].
Returns {
    mst: bool[][] (adjacency matrix representation of the minimum spanning tree)
    edges: (weight, a, b)[] (adjacency list representation of the minimum spanning tree)
    weight: total weight of the minimum spanning tree (sum of the weight of each edge in the tree)
    elapsed: Time it took for the solver to solve the model
}
"""
def int_prog(adj):
    v = len(adj)

    model = ConcreteModel()

    # Decision variable: x[i][j] = whether the edge i-j is part of thre MST (1) or not (0)
    model.x = Var(range(v), range(v), domain=Boolean)

    # Objective: minimize tree weight
    model.obj = Objective( \
        sense=minimize, \
        expr=sum(adj[i][j] * model.x[i,j] for i in range(v) for j in range(i, v)) \
    )

    model.con = ConstraintList()

    # Has to be a spanning tree

    # - Has exactly v-1 edges
    model.con.add(expr=sum(model.x[i,j] for i in range(v) for j in range(i, v)) == v - 1)

    # - Has no cycles
    # Or, equivalently, every subset S of vertices has no more than |S|-1 edges in it
    # (e.g. connect any three of {0,1,2,3} and try adding another edge without creating a cycle)
    vs = list(range(v))
    subsets = chain.from_iterable(combinations(vs, r) for r in range(1, len(vs)))
    for s in subsets:
        model.con.add(expr=sum(model.x[i,j] for i in s for j in s if i <= j) <= len(s) - 1)

    solver = SolverFactory('glpk')
    results = solver.solve(model)
    elapsed = results.solver._list[0]['Time']  # couldn't find the documentation for this

    edges = []
    mst = square_matrix(v, False)
    for i in range(v):
        for j in range(i, v):
            if model.x[i,j]() == 1:
                edges.append((adj[i][j], i, j))
                mst[i][j] = True
                mst[j][i] = True
    weight = model.obj()

    return { \
        'mst': mst, \
        'edges': edges, \
        'weight': weight, \
        'elapsed': elapsed \
    }

print('Parsing instance...')
with open(sys.argv[1], 'r') as fp:
    adj = parse_instance(fp)

print('Finding MST by solving an integer linear programming model...')
result = int_prog(adj)

print('edges', result['edges'])
print('weight', result['weight'])
print('elapsed', result['elapsed'])

if '--visual' in sys.argv:
    print('Outputting image...')
    output_image(sys.argv[1], adj, result['mst'])