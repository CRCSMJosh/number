"""
Comprehensive unit tests for the random number generator module.

This test suite covers the generate_random_number function with various
scenarios including happy paths, edge cases, and failure conditions.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Import the module under test
# Since the file is named 'random' without .py extension, we need to import it carefully
import importlib.util
spec = importlib.util.spec_from_file_location("random_module", "random")
random_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(random_module)


class TestGenerateRandomNumber(unittest.TestCase):
    """Test suite for the generate_random_number function."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.generate_random_number = random_module.generate_random_number

    def tearDown(self):
        """Clean up after each test method."""
        pass

    @patch('random.randint')
    def test_generate_random_number_basic_range(self, mock_randint):
        """Test that function returns value from mocked random.randint."""
        mock_randint.return_value = 5
        result = self.generate_random_number(1, 10)
        self.assertEqual(result, 5)
        mock_randint.assert_called_once_with(1, 10)

    @patch('random.randint')
    def test_generate_random_number_calls_randint_with_correct_params(self, mock_randint):
        """Test that random.randint is called with the correct parameters."""
        mock_randint.return_value = 50
        self.generate_random_number(10, 100)
        mock_randint.assert_called_once_with(10, 100)

    @patch('random.randint')
    def test_generate_random_number_with_equal_min_max(self, mock_randint):
        """Test when min and max values are equal."""
        mock_randint.return_value = 42
        result = self.generate_random_number(42, 42)
        self.assertEqual(result, 42)
        mock_randint.assert_called_once_with(42, 42)

    @patch('random.randint')
    def test_generate_random_number_with_negative_range(self, mock_randint):
        """Test with negative number range."""
        mock_randint.return_value = -5
        result = self.generate_random_number(-10, -1)
        self.assertEqual(result, -5)
        mock_randint.assert_called_once_with(-10, -1)

    @patch('random.randint')
    def test_generate_random_number_with_negative_to_positive_range(self, mock_randint):
        """Test with range spanning negative to positive."""
        mock_randint.return_value = 0
        result = self.generate_random_number(-50, 50)
        self.assertEqual(result, 0)
        mock_randint.assert_called_once_with(-50, 50)

    @patch('random.randint')
    def test_generate_random_number_with_zero_bounds(self, mock_randint):
        """Test with zero as one or both bounds."""
        mock_randint.return_value = 0
        result = self.generate_random_number(0, 0)
        self.assertEqual(result, 0)
        mock_randint.assert_called_once_with(0, 0)

    @patch('random.randint')
    def test_generate_random_number_with_zero_as_min(self, mock_randint):
        """Test with zero as minimum value."""
        mock_randint.return_value = 5
        result = self.generate_random_number(0, 10)
        self.assertEqual(result, 5)
        mock_randint.assert_called_once_with(0, 10)

    @patch('random.randint')
    def test_generate_random_number_with_zero_as_max(self, mock_randint):
        """Test with zero as maximum value."""
        mock_randint.return_value = -5
        result = self.generate_random_number(-10, 0)
        self.assertEqual(result, -5)
        mock_randint.assert_called_once_with(-10, 0)

    @patch('random.randint')
    def test_generate_random_number_with_large_numbers(self, mock_randint):
        """Test with very large number range."""
        mock_randint.return_value = 500000
        result = self.generate_random_number(1, 1000000)
        self.assertEqual(result, 500000)
        mock_randint.assert_called_once_with(1, 1000000)

    @patch('random.randint')
    def test_generate_random_number_returns_integer(self, mock_randint):
        """Test that the function returns an integer type."""
        mock_randint.return_value = 7
        result = self.generate_random_number(1, 10)
        self.assertIsInstance(result, int)

    @patch('random.randint')
    def test_generate_random_number_multiple_calls_independence(self, mock_randint):
        """Test that multiple calls are independent."""
        mock_randint.side_effect = [3, 7, 2]

        result1 = self.generate_random_number(1, 10)
        result2 = self.generate_random_number(1, 10)
        result3 = self.generate_random_number(1, 10)

        self.assertEqual(result1, 3)
        self.assertEqual(result2, 7)
        self.assertEqual(result3, 2)
        self.assertEqual(mock_randint.call_count, 3)

    def test_generate_random_number_with_invalid_range_raises_error(self):
        """Test that providing min > max raises ValueError (from random.randint)."""
        with self.assertRaises(ValueError):
            self.generate_random_number(10, 1)

    @patch('random.randint')
    def test_generate_random_number_with_very_large_range(self, mock_randint):
        """Test with extremely large range."""
        mock_randint.return_value = 0
        result = self.generate_random_number(-1000000, 1000000)
        self.assertEqual(result, 0)
        mock_randint.assert_called_once_with(-1000000, 1000000)

    def test_generate_random_number_actual_randomness(self):
        """Integration test: verify actual random behavior without mocking."""
        # Run multiple times and check all values are within range
        min_val, max_val = 1, 100
        results = set()

        for _ in range(50):
            result = self.generate_random_number(min_val, max_val)
            self.assertGreaterEqual(result, min_val)
            self.assertLessEqual(result, max_val)
            self.assertIsInstance(result, int)
            results.add(result)

        # With 50 iterations on range 1-100, we should get multiple different values
        # This tests actual randomness (though not guaranteed, very likely)
        self.assertGreater(len(results), 1,
                          "Expected multiple different random values")

    def test_generate_random_number_boundary_values(self):
        """Integration test: verify boundary values are included in possible results."""
        min_val, max_val = 1, 3
        results = set()

        # Run many times to likely hit all values in small range
        for _ in range(100):
            result = self.generate_random_number(min_val, max_val)
            results.add(result)

        # Should eventually hit boundaries (1 and 3) in small range
        self.assertIn(min_val, results, "Minimum value should be possible")
        self.assertIn(max_val, results, "Maximum value should be possible")

    @patch('random.randint')
    def test_generate_random_number_preserves_parameter_types(self, mock_randint):
        """Test that integer parameters are passed correctly to randint."""
        mock_randint.return_value = 5

        # Test with explicit integers
        result = self.generate_random_number(1, 10)
        self.assertEqual(result, 5)

        # Verify the call was made with the expected values
        args, _kwargs = mock_randint.call_args
        self.assertEqual(args, (1, 10))

    def test_generate_random_number_docstring_exists(self):
        """Test that the function has a docstring."""
        self.assertIsNotNone(self.generate_random_number.__doc__)
        self.assertIn("random", self.generate_random_number.__doc__.lower())

    @patch('random.randint')
    def test_generate_random_number_with_single_value_range(self, mock_randint):
        """Test edge case with range of size 1."""
        mock_randint.return_value = 5
        result = self.generate_random_number(5, 5)
        self.assertEqual(result, 5)

    @patch('random.randint')
    def test_generate_random_number_handles_randint_exceptions(self, mock_randint):
        """Test that exceptions from random.randint propagate correctly."""
        mock_randint.side_effect = ValueError("Invalid range")

        with self.assertRaises(ValueError) as context:
            self.generate_random_number(10, 1)

        self.assertIn("Invalid range", str(context.exception))


class TestModuleStructure(unittest.TestCase):
    """Test suite for module-level structure and properties."""

    def test_module_has_generate_random_number_function(self):
        """Test that the module exports the generate_random_number function."""
        self.assertTrue(hasattr(random_module, 'generate_random_number'))
        self.assertTrue(callable(random_module.generate_random_number))

    def test_function_accepts_two_parameters(self):
        """Test that generate_random_number accepts exactly 2 parameters."""
        import inspect
        sig = inspect.signature(random_module.generate_random_number)
        params = list(sig.parameters.keys())
        self.assertEqual(len(params), 2)
        self.assertIn('min_value', params)
        self.assertIn('max_value', params)

    def test_module_imports_random(self):
        """Test that the module properly imports the random module."""
        # This is implicitly tested by the function working, but we can verify
        import random as random_std
        # The function should work, which means random is imported
        result = random_module.generate_random_number(1, 1)
        self.assertIsInstance(result, int)


class TestEdgeCasesAndErrorHandling(unittest.TestCase):
    """Test suite for edge cases and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.generate_random_number = random_module.generate_random_number

    def test_max_int_values(self):
        """Test with maximum possible integer values."""
        # Test with large integers (within reasonable range)
        max_int_test = 10**9
        result = self.generate_random_number(0, max_int_test)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, max_int_test)

    def test_min_int_values(self):
        """Test with minimum (very negative) integer values."""
        min_int_test = -10**9
        result = self.generate_random_number(min_int_test, 0)
        self.assertGreaterEqual(result, min_int_test)
        self.assertLessEqual(result, 0)

    @patch('random.randint')
    def test_consistent_return_value_type(self, mock_randint):
        """Test that return type is always int regardless of input."""
        mock_randint.return_value = 42

        # Test with various input ranges
        test_cases = [
            (1, 10),
            (-5, 5),
            (0, 0),
            (100, 1000),
            (-1000, -100)
        ]

        for min_val, max_val in test_cases:
            with self.subTest(min=min_val, max=max_val):
                result = self.generate_random_number(min_val, max_val)
                self.assertIsInstance(result, int)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)