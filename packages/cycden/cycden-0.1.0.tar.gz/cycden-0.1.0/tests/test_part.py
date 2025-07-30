import unittest
from cycden import CycdenGenerator
from cycden.reg.graph_partition_db import get_partition_function

class TestPartitions(unittest.TestCase):
    def setUp(self):
        self.G = CycdenGenerator()(4, 2)

    def test_degree_partition(self):
        degree_partition = get_partition_function("degree")(self.G)
        self.assertIn("Degree", degree_partition.columns)
        self.assertIn("Count", degree_partition.columns)

    def test_reverse_degree_pair(self):
        rev = get_partition_function("reverse_degree_pair")(self.G)
        self.assertIn("Reverse Deg(u)", rev.columns)

if __name__ == "__main__":
    unittest.main()
