import itertools

def generate_ramsey_cnf(n):
    edges = list(itertools.combinations(range(1, n + 1), 2))
    edge_to_var = {edge: i + 1 for i, edge in enumerate(edges)}
    clauses = []

    # 1. Forbid Red C4
    for nodes in itertools.combinations(range(1, n + 1), 4):
        # 3 possible C4s on these 4 nodes
        p = list(nodes)
        for cycle in [(p[0],p[1],p[2],p[3]), (p[0],p[2],p[1],p[3]), (p[0],p[1],p[3],p[2])]:
            c_edges = [(min(cycle[i], cycle[(i+1)%4]), max(cycle[i], cycle[(i+1)%4])) for i in range(4)]
            print([-edge_to_var[e] for e in c_edges])
            clauses.append([-edge_to_var[e] for e in c_edges])

    # 2. Forbid Blue W5
    for nodes in itertools.combinations(range(1, n + 1), 5):
        for h in nodes:
            rim = [v for v in nodes if v != h]
            # Rim can form 3 different C4s in the complement
            for r_cycle in [(rim[0],rim[1],rim[2],rim[3]), (rim[0],rim[2],rim[1],rim[3]), (rim[0],rim[1],rim[3],rim[2])]:
                rim_edges = [(min(r_cycle[i], r_cycle[(i+1)%4]), max(r_cycle[i], r_cycle[(i+1)%4])) for i in range(4)]
                hub_edges = [(min(h, r), max(h, r)) for r in rim]
                # Clause: at least one edge must be Red to break the Blue W5
                clauses.append([edge_to_var[e] for e in (rim_edges + hub_edges)])

    return clauses, len(edges)

# Example for n=7
clauses, var_count = generate_ramsey_cnf(7)
print(f"p cnf {var_count} {len(clauses)}")