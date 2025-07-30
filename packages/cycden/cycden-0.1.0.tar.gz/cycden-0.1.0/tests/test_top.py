import unittest
from cycden import CycdenGenerator

class TestCycdenGenerator(unittest.TestCase):

    def test_graph_creation(self):
        G = CycdenGenerator()(5, 2)
        self.assertEqual(len(G), 5 + 5*2)  
        self.assertEqual(G.number_of_edges(), 5 + 5*2)

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            CycdenGenerator()(-1, 0)

        with self.assertRaises(TypeError):
            CycdenGenerator()("a", 2)