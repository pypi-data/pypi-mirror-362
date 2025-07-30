# graph_properties.py

import pandas as pd
from IPython.display import display, Markdown
from cycden.reg.graph_property_db import GRAPH_PROPERTY_FUNCS  # Adjust import path
import networkx as nx

class GraphSummary:
    def __init__(self, G, name="Graph", metrics=None):
        self.G = G
        self.name = name
        self.metrics = metrics or list(GRAPH_PROPERTY_FUNCS.keys())
        self.results = self._compute()

    def _compute(self):
        props = {}
        for key in self.metrics:
            func = GRAPH_PROPERTY_FUNCS.get(key.lower())
            if not func:
                props[key] = "❌ Unknown metric"
                continue
            try:
                props[key] = func(self.G)
            except Exception as e:
                props[key] = f"⚠️ {e}"
        return props

    def summary(self):
        return self.results

    def display(self, decimals: int = 4):
        data = {
            k: round(v, decimals) if isinstance(v, float) else v
            for k, v in self.results.items()
        }
        df = pd.DataFrame(data.items(), columns=["Property", "Value"])
        display(Markdown(f"### 📊 Graph Summary — **{self.name}**"))
        display(df.style.hide(axis="index"))
        
    def __repr__(self):
        return f"<GraphSummary {self.name}: nodes={self.results.get('nodes')} edges={self.results.get('edges')}>"
