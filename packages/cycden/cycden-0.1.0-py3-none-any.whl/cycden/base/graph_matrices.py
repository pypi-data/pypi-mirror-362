from cycden.reg.graph_matrices_db import get_matrix_function
from cycden import CycdenGenerator  # your direct cycden generator
import sympy
import numpy as np
import networkx as nx
import re

class GraphMatrices:
    def __init__(self, G):
        self.G = G
        self._cache = {}

    def get(self, matrix_type, **kwargs):
        if matrix_type not in self._cache:
            fn = get_matrix_function(matrix_type)
            self._cache[matrix_type] = fn(self.G, **kwargs)
        return self._cache[matrix_type]


class GraphMatricesBatch:
    def __init__(self, graph_string, matrix_string):
        self.graph_specs = [s.strip() for s in graph_string.split(";")]
        self.matrix_specs = [s.strip() for s in matrix_string.split(",")]

    def compute_all(self):
        result = {}
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

                matrices = {}
                for matrix_spec in self.matrix_specs:
                    name, *args = [s.strip() for s in matrix_spec.split(";")]
                    kwargs = {}
                    if args:
                        for arg in args:
                            if "=" in arg:
                                k, v = arg.split("=")
                                kwargs[k.strip()] = eval(v.strip())
                    func = get_matrix_function(name)
                    matrices[name] = func(G, **kwargs)
                result[graph_input] = matrices

            except Exception as e:
                result[graph_input] = {"error": str(e)}
        return result

    def display_all_latex(self):
        from IPython.display import display, Math

        result = self.compute_all()
        for graph_input, matrices in result.items():
            display(Math(f"\\text{{Graph: }} \\boxed{{{graph_input}}}"))
            if "error" in matrices:
                display(Math(f"\\text{{Error: }} {matrices['error']}"))
                continue
            for name, matrix in matrices.items():
                try:
                    sym_matrix = sympy.Matrix(matrix)
                    latex_code = sympy.latex(sym_matrix)
                    display(Math(f"\\text{{Matrix: }} {name} = {latex_code}"))
                except Exception as e:
                    display(Math(f"\\text{{Matrix: }} {name} = \\text{{[Error rendering: {e}]}}"))

__all__ = ["GraphMatrices", "GraphMatricesBatch"]
