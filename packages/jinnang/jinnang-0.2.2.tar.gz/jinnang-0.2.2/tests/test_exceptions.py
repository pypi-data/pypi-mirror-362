import unittest

from jinnang.common.exceptions import BadInputException


class TestExceptions(unittest.TestCase):
    def test_bad_input_exception(self):
        # Test that BadInputException can be raised
        with self.assertRaises(BadInputException):
            raise BadInputException("Bad input provided")
        
        # Test that BadInputException is an instance of Exception
        exception = BadInputException("Test message")
        self.assertIsInstance(exception, Exception)
        
        # Test exception message
        exception = BadInputException("Test message")
        self.assertEqual(str(exception), "Test message")
        
        # Test empty exception message
        exception = BadInputException()
        self.assertEqual(str(exception), "")
        
        # Test with multiple arguments
        exception = BadInputException("Error", "Additional info", 123)
        self.assertEqual(exception.args, ("Error", "Additional info", 123))


if __name__ == "__main__":
    unittest.main()