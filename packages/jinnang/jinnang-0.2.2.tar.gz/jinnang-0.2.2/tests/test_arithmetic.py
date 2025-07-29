import unittest
from jinnang.arithmetic.arithmetic import get_mode


class TestArithmeticUtilities(unittest.TestCase):
    """Test cases for arithmetic utility functions."""

    def test_get_mode_single_mode(self):
        """Test get_mode with data having a single mode."""
        data = [1, 2, 2, 3, 4]
        result = get_mode(data)
        self.assertEqual(result, 2)

    def test_get_mode_multiple_modes_returns_smallest(self):
        """Test get_mode returns smallest when multiple modes exist."""
        data = [1, 1, 2, 2, 3, 3]
        result = get_mode(data)
        self.assertEqual(result, 1)  # Should return the smallest mode

    def test_get_mode_all_same_frequency(self):
        """Test get_mode when all elements have same frequency."""
        data = [5, 3, 1, 4, 2]
        result = get_mode(data)
        self.assertEqual(result, 1)  # Should return the smallest element

    def test_get_mode_single_element(self):
        """Test get_mode with single element."""
        data = [42]
        result = get_mode(data)
        self.assertEqual(result, 42)

    def test_get_mode_strings(self):
        """Test get_mode with string data."""
        data = ['apple', 'banana', 'apple', 'cherry']
        result = get_mode(data)
        self.assertEqual(result, 'apple')

    def test_get_mode_strings_multiple_modes(self):
        """Test get_mode with strings having multiple modes."""
        data = ['zebra', 'apple', 'zebra', 'apple', 'banana']
        result = get_mode(data)
        self.assertEqual(result, 'apple')  # Lexicographically smallest

    def test_get_mode_mixed_types(self):
        """Test get_mode with mixed data types."""
        # Note: This might not be practical in real use, but tests the function's behavior
        data = [1, '1', 1, 2]
        result = get_mode(data)
        self.assertEqual(result, 1)  # Integer 1 appears twice

    def test_get_mode_negative_numbers(self):
        """Test get_mode with negative numbers."""
        data = [-3, -1, -3, -2, -1, -1]
        result = get_mode(data)
        self.assertEqual(result, -1)  # -1 appears most frequently

    def test_get_mode_floats(self):
        """Test get_mode with floating point numbers."""
        data = [1.5, 2.7, 1.5, 3.8, 1.5]
        result = get_mode(data)
        self.assertEqual(result, 1.5)

    def test_get_mode_large_dataset(self):
        """Test get_mode with larger dataset."""
        data = [1] * 100 + [2] * 50 + [3] * 75 + [4] * 100
        result = get_mode(data)
        # Both 1 and 4 appear 100 times, should return smaller (1)
        self.assertEqual(result, 1)

    def test_get_mode_tuples(self):
        """Test get_mode with tuple data."""
        data = [(1, 2), (3, 4), (1, 2), (5, 6)]
        result = get_mode(data)
        self.assertEqual(result, (1, 2))

    def test_get_mode_empty_list_raises_error(self):
        """Test get_mode raises ValueError for empty list."""
        with self.assertRaises(ValueError) as context:
            get_mode([])
        self.assertIn("empty", str(context.exception).lower())

    def test_get_mode_none_values(self):
        """Test get_mode with None values."""
        data = [None, 1, None, 2]
        result = get_mode(data)
        self.assertIsNone(result)  # None appears most frequently

    def test_get_mode_boolean_values(self):
        """Test get_mode with boolean values."""
        data = [True, False, True, True, False]
        result = get_mode(data)
        self.assertEqual(result, True)  # True appears 3 times

    def test_get_mode_performance_consistency(self):
        """Test that get_mode returns consistent results."""
        data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        result1 = get_mode(data)
        result2 = get_mode(data)
        self.assertEqual(result1, result2)
        self.assertEqual(result1, 5)  # 5 appears most frequently


if __name__ == '__main__':
    unittest.main()