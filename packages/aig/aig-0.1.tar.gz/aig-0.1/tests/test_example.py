import unittest
from aig.example import add_one, multiply_by_two


class TestExample(unittest.TestCase):
    """Test cases for example module."""
    
    def test_add_one(self):
        """Test add_one function."""
        self.assertEqual(add_one(5), 6)
        self.assertEqual(add_one(0), 1)
        self.assertEqual(add_one(-1), 0)
        self.assertEqual(add_one(10.5), 11.5)
    
    def test_multiply_by_two(self):
        """Test multiply_by_two function."""
        self.assertEqual(multiply_by_two(5), 10)
        self.assertEqual(multiply_by_two(0), 0)
        self.assertEqual(multiply_by_two(-3), -6)
        self.assertEqual(multiply_by_two(2.5), 5.0)


if __name__ == '__main__':
    unittest.main()