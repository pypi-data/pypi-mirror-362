import unittest
from bruneus import random_table_name


class TestNaming(unittest.TestCase):
    def test_uniqueness(self):
        names = [random_table_name("uniq-test") for x in range(0, 100)]
        self.assertEqual(len(names), len(set(names)))


if __name__ == "__main__":
    unittest.main()
