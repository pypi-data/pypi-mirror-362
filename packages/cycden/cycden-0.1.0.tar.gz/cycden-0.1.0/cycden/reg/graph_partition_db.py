#reg/graph_partition_db.py

import networkx as nx
import numpy as np
import pandas as pd
from collections import Counter, defaultdict

PARTITION_REGISTRY = {}

def register_partition(name):
    def decorator(fn):
        PARTITION_REGISTRY[name.lower()] = fn
        return fn
    return decorator

def get_partition_function(name):
    name = name.lower()
    if name not in PARTITION_REGISTRY:
        raise KeyError(f"Partition type '{name}' not found.")
    return PARTITION_REGISTRY[name]

@register_partition("degree")
def degree_partition(G, **kwargs):
    degree_counts = Counter(dict(G.degree()).values())
    df = pd.DataFrame(sorted(degree_counts.items()), columns=["Degree", "Count"])
    return df

@register_partition("distance")
def distance_partition(G, **kwargs):
    nodes = list(G.nodes)
    lengths = dict(nx.floyd_warshall(G))
    dist_counter = defaultdict(int)
    for i, u in enumerate(nodes):
        for v in nodes[i + 1:]:
            d = lengths[u][v]
            if d != float('inf'):
                dist_counter[d] += 1
    df = pd.DataFrame(sorted(dist_counter.items()), columns=["Distance", "Count"])
    return df

@register_partition("degree_pair")
def degree_pair_partition(G, **kwargs):
    edges = G.edges()
    deg = dict(G.degree())
    degree_pairs = defaultdict(int)
    for u, v in edges:
        i, j = sorted((deg[u], deg[v]))
        degree_pairs[(i, j)] += 1
    df = pd.DataFrame(
        sorted(((i, j, c) for (i, j), c in degree_pairs.items())),
        columns=["deg(u)", "deg(v)", "Count"]
    )
    return df

@register_partition("distance_degpair")
def distance_degpair_partition(G, **kwargs):
    deg = dict(G.degree())
    lengths = dict(nx.all_pairs_shortest_path_length(G))
    pair_counter = defaultdict(int)

    nodes = list(G.nodes)
    for i, u in enumerate(nodes):
        for v in nodes[i + 1:]:
            d = lengths[u][v]
            du, dv = deg[u], deg[v]
            i_, j_ = sorted((du, dv))
            pair_counter[(i_, j_, d)] += 1

    df = pd.DataFrame(
        sorted(((i_, j_, d, c) for (i_, j_, d), c in pair_counter.items())),
        columns=["Deg(u)", "Deg(v)", "Distance", "Count"]
    )
    return df

@register_partition("reverse_degree")
def reverse_degree_partition(G, **kwargs):
    degrees = dict(G.degree())
    max_deg = max(degrees.values())
    
    reverse_deg_counts = defaultdict(int)
    for node, deg in degrees.items():
        reverse_deg = max_deg - deg + 1
        reverse_deg_counts[reverse_deg] += 1
    
    df = pd.DataFrame(sorted(reverse_deg_counts.items()), columns=["Reverse Degree", "Count"])
    return df 

@register_partition("reverse_degree_pair")
def reverse_degree_pair_partition(G, **kwargs):
    edges = G.edges()
    degrees = dict(G.degree())
    max_deg = max(degrees.values())
    
    reverse_deg_pairs = defaultdict(int)
    for u, v in edges:
        i, j = sorted((max_deg - degrees[u] + 1, max_deg - degrees[v] + 1))
        reverse_deg_pairs[(i, j)] += 1
    
    df = pd.DataFrame(
        sorted(((i, j, c) for (i, j), c in reverse_deg_pairs.items())),
        columns=["Reverse Deg(u)", "Reverse Deg(v)", "Count"]
    )
    return df
