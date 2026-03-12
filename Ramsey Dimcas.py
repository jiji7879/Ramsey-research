import itertools

def write_ramsey_cnf(k, n, num_vertices, filename):
    # 1. Generate all possible edges in Kv
    vertices = list(range(1, num_vertices + 1))
    edges = list(itertools.combinations(vertices, 2))
    edge_to_var = {edge: i + 1 for i, edge in enumerate(edges)}
    
    clauses = []

    # 2. Add constraints: No Red clique of size k
    for clique in itertools.combinations(vertices, k):
        clique_edges = list(itertools.combinations(clique, 2))
        clause = " ".join([f"-{edge_to_var[tuple(e)]}" for e in clique_edges])
        clauses.append(f"{clause} 0")

    # 3. Add constraints: No Blue clique of size n
    for clique in itertools.combinations(vertices, n):
        clique_edges = list(itertools.combinations(clique, 2))
        clause = " ".join([f"{edge_to_var[tuple(e)]}" for e in clique_edges])
        clauses.append(f"{clause} 0")

    # 4. Write to the file
    with open(filename, 'w') as f:
        f.write(f"c CNF file proving R({k},{n}) boundary on {num_vertices} vertices\n")
        f.write(f"p cnf {len(edges)} {len(clauses)}\n")
        for c in clauses:
            f.write(f"{c}\n")
    
    print(f"File '{filename}' generated successfully.")
    print(f"Variables (Edges): {len(edges)}")
    print(f"Clauses (Cliques): {len(clauses)}")

if __name__ == "__main__":
    # Example: Generating the proof that R(4, 3) <= 9
    # This will create a file that a SAT solver will find UNSATISFIABLE.
    write_ramsey_cnf(k=3, n=3, num_vertices=6, filename="r33_6.cnf")