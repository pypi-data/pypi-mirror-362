from cycden.reg.graph_partition_db import get_partition_function
from cycden.reg.topo_formulas_db import get_topo_index_function
from cycden import CycdenGenerator
from IPython.display import display, Markdown
import pandas as pd
import re

class TopoIndexBatch:
    def __init__(self, graph_str, index_str):
        self.graph_specs = [s.strip() for s in graph_str.split("|")]
        self.indices = [i.strip().lower() for i in index_str.split(",")]
        self.results = {}
        self._compute_all()

    def _compute_all(self):
        for graph_input in self.graph_specs:
            try:
                graph_input = graph_input.strip()

                # Parse cycden(n, m)
                if graph_input.startswith("cycden"):
                    match = re.search(r"cycden\s*,?\s*\(?\s*(\d+)\s*,\s*(\d+)\s*\)?", graph_input)
                    if not match:
                        raise ValueError(f"Invalid format for cycden: {graph_input}")
                    n, m = int(match.group(1)), int(match.group(2))
                    G = CycdenGenerator()(n, m)
                else:
                    raise ValueError(f"Unsupported graph input: {graph_input}")

                row = {}
                for index in self.indices:
                    try:
                        partition_keys, fn = get_topo_index_function(index)
                        partitions = []
                        for key in partition_keys:
                            part_func = get_partition_function(key)
                            partitions.append(part_func(G))
                        row[index] = fn(*partitions)
                    except Exception as e:
                        row[index] = f"⚠️ {e}"

                self.results[graph_input] = row

            except Exception as e:
                self.results[graph_input] = {"error": str(e)}

    def display(self):
        for graph_input, result in self.results.items():
            df = pd.DataFrame([result])
            display(df.style.hide(axis="index").set_caption(f"Topological Indices for `{graph_input}`"))

    def to_df(self):
        return pd.DataFrame.from_dict(self.results, orient="index")
