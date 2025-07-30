# Cyclic Dendrimer Graph Analysis Package

This package provides tools for generating, analyzing, and computing topological invariants of cyclic dendrimer graph $CD(m,n)$. It includes graph generation, partitioning, index computation, graph summaries, and matrix-based statistics. The system is modular and registry-dependent.

---

## Package Structure

```
cycden/
│
├── cycden.py                       # Generator for cyclic dendrimer graphs
├── base/                           # Folder containing base functions
│   ├── graph_properties.py         # Summary statistics for each graph
│   ├── graph_topoindices.py        # Computes topological indices in batch
│   ├── graph_partition.py          # Computes structural partitions in batch
│   └── graph_matrices              # Generates the matrices involved in each CD$(m,n)$
├── reg/                            # Registry modules for partitioned logic
│   ├── graph_partition_db.py       # Registered graph partitions
│   ├── graph_property_db.py        # Registered graph-level metrics
│   ├── graph_matrices_db.py        # Registered matrix generators
│   └── graph_matrices              # Registered topological computation formulas from partitions
└── cycdem.ipynb                    # Jupyter Notebook for demonstration

```

---
## Dependencies: 
This package requires `numpy`, `pandas`, `networkx` and must be run through an active kernel of a Jupyter notebook. 

Run the following command in the corresponding environment to install these dependencies: 

```python 
    pip install numpy pandas networkx jupyterlab
```
then we can run `jupyter notebook` in the terminal. 

## Getting Started

### Graph Generation
The generator in `cycden.py` supports instantiating a dendrimer via:

```python
from cycden import CycdenGenerator
G = CycdenGenerator()(n, m)  

```
where $n$ is the cycle order and $m$ is the order for $K_{1,m}$

---
##  Topological Index Computation

Use the batch interface to compute one or more indices across several graphs.

```python
from topo_index_batch import TopoIndexBatch

# Example: Compute first and second Zagreb indices
batch = TopoIndexBatch("cycden(5,2), cycden(6,3)", "first_zagreb, second_zagreb")
batch.display()
```

Available indices are registered in `topo_formulas_db.py`. To view the registry:

```python
from topo_index_batch import TOPO_INDEX_REGISTRY

print(list(TOPO_INDEX_REGISTRY))  # Shows all available indices
```

---

## Graph Summary

To retrieve global structural properties of a dendrimer graph:

```python
from cycden import CycdenGenerator
from graph_properties import GraphSummary

G = CycdenGenerator()(6, 3)
summary = GraphSummary(G, name="CycDen(6,3)")
summary.display()
```

Supported metrics include:
- Node/edge count, density
- Degree stats: max/min/avg degree
- Path metrics: diameter, radius, avg path length
- Clustering, transitivity, assortativity
- Connectivity, ring count, cyclomatic number

You can see all registered metrics:

```python
from reg.graph_property_db import GRAPH_PROPERTY_FUNCS
print(list(GRAPH_PROPERTY_FUNCS))
```

---

## Graph Partitions

You can compute structural partitions (e.g., degree, distance, reverse degree pair):

```python
from graph_partition import GraphPartitionBatch

batch = GraphPartitionBatch("cycden(6,2)", "degree, distance, reverse_degree_pair")
batch.display_all_latex()
```

To access a partition manually:
```python
from reg.graph_partition_db import get_partition_function
partition_func = get_partition_function("reverse_degree_pair")
df = partition_func(G)
print(df)
```

To list all registered partitions:
```python
from reg.graph_partition_db import PARTITION_REGISTRY
print(list(PARTITION_REGISTRY))
```

---

## ➕ Adding New Metrics or Partitions

### New Graph Property
```python
@register("my_property")
def my_property(G):
    return some_metric_of(G)
```

### New Partition
```python
@register_partition("my_partition")
def my_partition(G, **kwargs):
    return pd.DataFrame({...})
```

### New Topological Index
```python
@register_topo_index("my_index", "degree", "distance")
def my_index(degree_df, distance_df):
    return compute_from_partitions(degree_df, distance_df)
```

---

## Testing

You can test each component individually using:

```python
G = CycdenGenerator()(4,2)
partition = get_partition_function("degree")(G)
index_val = get_topo_index_function("first_zagreb")[1](partition)
print(index_val)
```

---

## 📎 Notes

- All graphs are undirected.
- Distance matrices used are integer-valued.
- Hybrid indices can take multiple partitions.
- All interfaces handle batch inputs via string specifications.

---
