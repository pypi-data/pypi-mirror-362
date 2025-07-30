from IPython.display import display, Markdown
from cycden.reg.graph_partition_db import get_partition_function, PARTITION_REGISTRY
from cycden import CycdenGenerator
import re

class GraphPartition:
    def __init__(self, G):
        self.G = G

    def __getattr__(self, name):
        if name.endswith('_partition'):
            part_key = name.removesuffix('_partition').lower()
            if part_key in PARTITION_REGISTRY:
                def wrapper(**kwargs):
                    return get_partition_function(part_key)(self.G, **kwargs)
                return wrapper
        raise AttributeError(f"'GraphPartition' object has no attribute '{name}'")


class GraphPartitionBatch:
    def __init__(self, graph_str, partition_str):
        self.graph_specs = [s.strip() for s in graph_str.split("|")]
        self.partitions = [p.strip().lower() for p in partition_str.split(",")]
        self.results = {}

        for graph_input in self.graph_specs:
            try:
                graph_input = graph_input.strip()

                if graph_input.startswith("cycden"):
                    match = re.search(r"cycden\s*,?\s*\(?\s*(\d+)\s*,\s*(\d+)\s*\)?", graph_input)
                    if not match:
                        raise ValueError(f"Invalid format for cycden: {graph_input}")
                    n, m = int(match.group(1)), int(match.group(2))
                    G = CycdenGenerator()(n, m)

                else:
                    raise ValueError(f"Unsupported graph input: {graph_input}")

                self.results[graph_input] = {}
                for part in self.partitions:
                    try:
                        func = get_partition_function(part)
                        self.results[graph_input][part] = func(G)
                    except KeyError as e:
                        self.results[graph_input][part] = f"Partition key error: {e}"

            except Exception as e:
                self.results[graph_input] = f"Error: {e}"

    def display_all_latex(self):
        for graph_input, parts in self.results.items():
            if isinstance(parts, str):
                display(Markdown(f"### `{graph_input}` – *{parts}*"))
                continue

            display(Markdown(f"## **Graph: `{graph_input}`**"))
            for pname, result in parts.items():
                display(Markdown(f"### Partition: `{pname}`"))
                if isinstance(result, str):
                    display(Markdown(f"*{result}*"))
                else:
                    display(result.style.hide(axis='index'))
            display(Markdown("---"))
