import unittest
from jinnang.string.string import get_numeric, safe_format, remove_special_chars


class TestStringUtilities(unittest.TestCase):
    """Test cases for string utility functions."""

    def test_get_numeric_valid_numbers(self):
        """Test get_numeric with valid numeric inputs."""
        test_cases = [
            ("42", 42.0),
            ("3.14", 3.14),
            ("-10", -10.0),
            ("0", 0.0),
            ("1.5e2", 150.0),
            (42, 42.0),
            (3.14, 3.14),
            (-10, -10.0)
        ]
        
        for input_val, expected in test_cases:
            with self.subTest(input_val=input_val):
                result = get_numeric(input_val)
                self.assertEqual(result, expected)
                self.assertIsInstance(result, float)

    def test_get_numeric_invalid_inputs(self):
        """Test get_numeric with invalid inputs."""
        invalid_inputs = [
            "abc",
            "12abc",
            "abc12",
            "",
            "not a number",
            "12.34.56",
            [1, 2, 3],
            {"key": "value"}
        ]
        
        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                result = get_numeric(invalid_input)
                self.assertIsNone(result)

    def test_get_numeric_none_input(self):
        """Test get_numeric with None input."""
        result = get_numeric(None)
        self.assertIsNone(result)

    def test_safe_format_basic(self):
        """Test basic safe_format functionality."""
        template = "Hello {name}, you are {age} years old"
        data = {"name": "Alice", "age": 30, "extra": "ignored"}
        
        result = safe_format(template, data)
        expected = "Hello Alice, you are 30 years old"
        self.assertEqual(result, expected)

    def test_safe_format_missing_keys(self):
        """Test safe_format with missing keys in data."""
        template = "Hello {name}, you are {age} years old"
        data = {"name": "Alice"}  # missing 'age'
        
        with self.assertRaises(KeyError):
            safe_format(template, data)

    def test_safe_format_extra_keys(self):
        """Test safe_format ignores extra keys in data."""
        template = "Hello {name}"
        data = {
            "name": "Alice", 
            "age": 30, 
            "city": "New York", 
            "unused": "data"
        }
        
        result = safe_format(template, data)
        expected = "Hello Alice"
        self.assertEqual(result, expected)

    def test_safe_format_no_placeholders(self):
        """Test safe_format with template containing no placeholders."""
        template = "This is a plain string"
        data = {"name": "Alice", "age": 30}
        
        result = safe_format(template, data)
        self.assertEqual(result, template)

    def test_safe_format_empty_template(self):
        """Test safe_format with empty template."""
        template = ""
        data = {"name": "Alice"}
        
        result = safe_format(template, data)
        self.assertEqual(result, "")

    def test_safe_format_empty_data(self):
        """Test safe_format with empty data dict."""
        template = "No placeholders here"
        data = {}
        
        result = safe_format(template, data)
        self.assertEqual(result, template)

    def test_safe_format_complex_placeholders(self):
        """Test safe_format with complex placeholder scenarios."""
        template = "Item: {item}, Price: ${price:.2f}, Quantity: {qty}"
        data = {"item": "Widget", "price": 19.99, "qty": 5}
        
        result = safe_format(template, data)
        expected = "Item: Widget, Price: $19.99, Quantity: 5"
        self.assertEqual(result, expected)

    def test_remove_special_chars_basic(self):
        """Test remove_special_chars with basic special characters."""
        # Test with various Unicode categories So, Cn, Co
        test_text = "Hello World! 123 αβγ"
        result = remove_special_chars(test_text)
        # Should keep normal text, numbers, and Greek letters
        self.assertEqual(result, "Hello World! 123 αβγ")

    def test_remove_special_chars_symbols(self):
        """Test remove_special_chars with symbol characters."""
        # Include some So (Symbol, other) characters
        test_text = "Text with symbols: ♠♣♥♦ and more"
        result = remove_special_chars(test_text)
        # Symbols should be removed
        expected = "Text with symbols:  and more"
        self.assertEqual(result, expected)

    def test_remove_special_chars_empty_string(self):
        """Test remove_special_chars with empty string."""
        result = remove_special_chars("")
        self.assertEqual(result, "")

    def test_remove_special_chars_only_special(self):
        """Test remove_special_chars with string containing only special chars."""
        # String with only So category characters
        test_text = "♠♣♥♦"
        result = remove_special_chars(test_text)
        self.assertEqual(result, "")

    def test_remove_special_chars_mixed_content(self):
        """Test remove_special_chars with mixed content."""
        test_text = "Normal text ♠ with symbols ♣ mixed in ♥"
        result = remove_special_chars(test_text)
        expected = "Normal text  with symbols  mixed in "
        self.assertEqual(result, expected)

    def test_remove_special_chars_unicode_preservation(self):
        """Test that remove_special_chars preserves valid Unicode characters."""
        # Test with various Unicode characters that should be preserved
        test_text = "English, 中文, العربية, русский, 日本語"
        result = remove_special_chars(test_text)
        # All these should be preserved as they're not So, Cn, or Co
        self.assertEqual(result, test_text)

    def test_remove_special_chars_numbers_and_punctuation(self):
        """Test that numbers and common punctuation are preserved."""
        test_text = "Test 123 with punctuation: .,;:!?()-_"
        result = remove_special_chars(test_text)
        # Common punctuation should be preserved
        self.assertEqual(result, test_text)


if __name__ == '__main__':
    unittest.main()