import networkx as nx

class CycdenGenerator:
    """
    Generator for Cyclic Dendrimers CD(n, m).

    Parameters:
        n (int): Length of the core cycle (must be ≥ 3).
        m (int): Number of pendant nodes (must be ≥ 1) attached to each cycle vertex.

    Returns:
        networkx.Graph: The constructed cyclic dendrimer graph.
    """
    def __call__(self, n: int, m: int) -> nx.Graph:
        if not isinstance(n, int) or not isinstance(m, int):
            raise TypeError("Both n and m must be integers.")
        if n < 3:
            raise ValueError("Cycle length n must be ≥ 3.")
        if m < 1:
            raise ValueError("Number of pendants m must be ≥ 1.")

        C_n = nx.cycle_graph(n)
        E_m = nx.empty_graph(m)
        G = nx.Graph()

        # Add cycle nodes and edges
        for v in C_n.nodes():
            G.add_node(v)
        for u, v in C_n.edges():
            G.add_edge(u, v)

        # Attach a disjoint E_m to each C_n node
        for v in range(n):
            offset = max(G.nodes()) + 1
            G = nx.disjoint_union(G, E_m)
            for i in range(offset, offset + m):
                G.add_edge(v, i)

        return G
