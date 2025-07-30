# reg/graph_matrices_db.py

import networkx as nx
import numpy as np

MATRIX_REGISTRY = {}

def register_matrix(name):
    def decorator(fn):
        MATRIX_REGISTRY[name.lower()] = fn
        return fn
    return decorator

def get_matrix_function(name):
    name = name.lower()
    if name not in MATRIX_REGISTRY:
        raise KeyError(f"Matrix type '{name}' not found.")
    return MATRIX_REGISTRY[name]

@register_matrix("adjacency")
def adjacency_matrix(G, **kwargs):
    return nx.adjacency_matrix(G).toarray()

@register_matrix("incidence")
def incidence_matrix(G, **kwargs):
    oriented = kwargs.get("oriented", False)
    return nx.incidence_matrix(G, oriented=oriented).toarray()

@register_matrix("distance")
def distance_matrix(G, **kwargs):
    dist = nx.floyd_warshall_numpy(G)     # returns float64 by default
    return dist.astype(int, copy=False)   # enforce integers without extra copy

@register_matrix("degree")
def degree_matrix(G, **kwargs):
    degrees = np.array([d for _, d in G.degree()])
    return np.diag(degrees)


