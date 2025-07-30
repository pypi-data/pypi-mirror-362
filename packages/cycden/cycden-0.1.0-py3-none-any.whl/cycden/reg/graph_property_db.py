# reg/graph_property_db.py

import networkx as nx
from statistics import mean

GRAPH_PROPERTY_FUNCS = {}

def register(name):
    def decorator(fn):
        GRAPH_PROPERTY_FUNCS[name.lower()] = fn
        return fn
    return decorator

@register("nodes")
def nodes(G): return G.number_of_nodes()

@register("edges")
def edges(G): return G.number_of_edges()

@register("components")
def components(G): return nx.number_connected_components(G)

@register("density")
def density(G): return nx.density(G)

@register("max_degree")
def max_degree(G): return max(dict(G.degree()).values())

@register("min_degree")
def min_degree(G): return min(dict(G.degree()).values())

@register("clustering_avg")
def clustering_avg(G): return nx.average_clustering(G)

@register("transitivity")
def transitivity(G): return nx.transitivity(G)

@register("assortativity_degree")
def assortativity(G): return nx.degree_assortativity_coefficient(G)

@register("diameter")
def diameter(G): return nx.diameter(G) if nx.is_connected(G) else None

@register("radius")
def radius(G): return nx.radius(G) if nx.is_connected(G) else None

@register("avg_path_length")
def avg_path_length(G): return nx.average_shortest_path_length(G) if nx.is_connected(G) else None


@register("girth")
def girth(G):
    cycles = nx.cycle_basis(G)
    return min((len(c) for c in cycles), default=None)

@register("cyclomatic_number")
def cyclomatic_number(G):
    return G.number_of_edges() - G.number_of_nodes() + nx.number_connected_components(G)
