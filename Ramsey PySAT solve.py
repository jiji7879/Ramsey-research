from pysat.solvers import Glucose42
import itertools
import time

def solve_ramsey(k, n, v, assumptions=[]):
    # 1. Map edges to variable IDs
    print("Mapping edges to variables...")
    vertices = list(range(1, v + 1))
    edges = list(itertools.combinations(vertices, 2))
    edge_to_var = {edge: i + 1 for i, edge in enumerate(edges)}
    print("Easy!")
    
    solver = Glucose42()

    # 2. Constraint: No Red clique of size k
    print(f"Adding constraints for Red cliques...")
    for clique in itertools.combinations(vertices, k):
        clique_edges = [edge_to_var[tuple(e)] for e in itertools.combinations(clique, 2)]
        # Clause: At least one edge must be Blue (negative)
        solver.add_clause([-e for e in clique_edges])

    # 3. Constraint: No Blue clique of size n
    print("Adding constraints for Blue cliques...")
    for clique in itertools.combinations(vertices, n):
        clique_edges = [edge_to_var[tuple(e)] for e in itertools.combinations(clique, 2)]
        # Clause: At least one edge must be Red (positive)
        solver.add_clause([e for e in clique_edges])

    # 4. Solve
    print("Solving the SAT problem...")
    if solver.solve(assumptions=assumptions):
        print(f"R({k},{n}) > {v}: SATISFIABLE (A valid coloring exists)")
        model = solver.get_model()
        # Separate edges by color based on the SAT model
        red_edges = [edges[i] for i in range(len(edges)) if model[i] > 0]
        red_is = [edge_to_var[edges[i]] for i in range(len(edges)) if model[i] > 0]
        blue_edges = [edges[i] for i in range(len(edges)) if model[i] < 0]
        print(solver.accum_stats())
        print(red_edges, red_is)
        return red_edges
    else:
        print(f"R({k},{n}) <= {v}: UNSATISFIABLE (No such coloring exists)")
        print(solver.accum_stats())
        return None

def map_to_edge(v, list_of_coordinates):
    vertices = list(range(1, v + 1))
    edges = list(itertools.combinations(vertices, 2))
    edge_to_var = {edge: i + 1 for i, edge in enumerate(edges)}
    new_list = []

    for i in list_of_coordinates:
        new_list.append(edge_to_var[i])
    
    return new_list

# To prove R(3,3) = 6:
start = time.time()
n = solve_ramsey(3, 3, 7)
end = time.time()
print(f"Time elapsed: {end - start:.2f} seconds")