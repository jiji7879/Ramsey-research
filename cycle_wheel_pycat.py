from pysat.solvers import Glucose42
import itertools
import time

def solve_ramsey(r, b, n, assumptions=[]):
    vertices = list(range(1, n + 1))
    edges = list(itertools.combinations(vertices, 2))
    edge_to_var = {e: i + 1 for i, e in enumerate(edges)}
    clauses = []
    
    solver = Glucose42()

    # Forbid Red Cr
    for subset in itertools.combinations(vertices, r):
        for cycle_edges in get_edges_for_cycle(list(subset)):
            clauses.append([-edge_to_var[e] for e in cycle_edges])
    
    # 3. Forbid Blue W5
    for subset in itertools.combinations(vertices, b):
        subset = list(subset)
        for i in range(len(subset)):
            hub = subset[i]
            rim = subset[:i] + subset[i+1:]
            for rim_cycle_edges in get_edges_for_cycle(rim):
                hub_edges = [tuple(sorted((hub, r))) for r in rim]
                # Clause: At least one of these rim/hub edges must be RED
                clauses.append([edge_to_var[e] for e in (rim_cycle_edges + hub_edges)])
    
    for c in clauses:
        solver.add_clause(c)
    
    # 4. Solve
    print("Solving the SAT problem...")
    if solver.solve(assumptions=assumptions):
        print(f"R(C{r}, W{b}) > {n}. SATISFIABLE (A valid coloring exists)")
        model = solver.get_model()
        # Separate edges by color based on the SAT model
        red_edges = [edges[i] for i in range(len(edges)) if model[i] > 0]
        red_is = [edge_to_var[edges[i]] for i in range(len(edges)) if model[i] > 0]
        blue_edges = [edges[i] for i in range(len(edges)) if model[i] < 0]
        print(solver.accum_stats())
        #print(red_edges, red_is)
        return red_edges
    else:
        print(f"R(C{r}, W{b}) <= {n}. UNSATISFIABLE (No such coloring exists)")
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

def get_edges_for_cycle(nodes):
    """Generates all unique cycles of length len(nodes) for a set of nodes."""
    # Fix first node to avoid rotations, then permute the rest
    first = nodes[0]
    rest = nodes[1:]
    unique_cycles = []
    for p in itertools.permutations(rest):
        path = (first,) + p
        # To avoid reflections (e.g., 1-2-3 and 1-3-2), we can check ordering
        if p[0] < p[-1]: 
            edges = []
            for i in range(len(path)):
                u, v = path[i], path[(i+1)%len(path)]
                edges.append(tuple(sorted((u, v))))
            unique_cycles.append(edges)
    return unique_cycles

start = time.time()
n = solve_ramsey(8, 5, 14)
end = time.time()
print(f"Time elapsed: {end - start:.2f} seconds")