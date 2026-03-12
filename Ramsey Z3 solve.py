import itertools
from pysat.solvers import Cadical195

def solve_with_manual_symmetry(v, k, n):
    # 1. Setup Mapping
    vertices = list(range(1, v + 1))
    edges = list(itertools.combinations(vertices, 2))
    edge_to_var = {tuple(sorted(e)): i + 1 for i, e in enumerate(edges)}
    var_to_edge = {i + 1: tuple(sorted(e)) for i, e in enumerate(edges)}
    
    solver = Cadical195()
    

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

    
    solver.conf_budget(2)
    print("Solving the SAT problem...")
    status = solver.solve_limited()
    print(status)
    if status is not None and status:
        print(f"R({k},{n}) > {v}: SATISFIABLE (A valid coloring exists)")
        model = solver.get_model()
        # Separate edges by color based on the SAT model
        red_edges = [edges[i] for i in range(len(edges)) if model[i] > 0]
        red_is = [edge_to_var[edges[i]] for i in range(len(edges)) if model[i] > 0]
        blue_edges = [edges[i] for i in range(len(edges)) if model[i] < 0]
        print(solver.accum_stats())
        print(red_edges, red_is)
        return red_edges
    elif status is not None and not status:
        print(f"R({k},{n}) <= {v}: UNSATISFIABLE (No such coloring exists)")
        print(solver.accum_stats())
        print(solver.get_core())
        return None
    else:
        print(solver.status)
        print(solver.accu_time)
        print(solver.accum_stats())
        print(solver.cadical)
        print(solver.call_time)
        print(solver.pengine)
        print(solver.reset_observed)
        print("Something")
        
solve_with_manual_symmetry(8, 3, 4)