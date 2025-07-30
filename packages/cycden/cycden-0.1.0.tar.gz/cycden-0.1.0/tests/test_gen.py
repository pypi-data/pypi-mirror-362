import unittest
from cycden import CycdenGenerator
import networkx as nx

class TestCycdenGenerator(unittest.TestCase):
    def test_graph_creation(self):
        G = CycdenGenerator()(5, 2)
        self.assertIsInstance(G, nx.Graph)
        self.assertGreaterEqual(G.number_of_nodes(), 1)
        self.assertGreaterEqual(G.number_of_edges(), 1)

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            CycdenGenerator()(-1, 0)

if __name__ == "__main__":
    unittest.main()
