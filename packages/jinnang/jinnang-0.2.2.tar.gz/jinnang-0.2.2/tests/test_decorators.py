import unittest
import unittest
import time
from unittest.mock import patch, MagicMock
from jinnang.common.decorators import mock_when, fail_recover, custom_retry
from jinnang.common.exceptions import BadInputException
from jinnang.verbosity.verbosity import Verbosity
import json

class TestDecorators(unittest.TestCase):

    def test_mock_when_condition_true(self):
        # Test case where condition is true, mock_result should be returned
        mock_condition = lambda: True
        mock_result_func = lambda *args, **kwargs: "mocked_value"

        @mock_when(mock_condition, mock_result_func)
        def original_function():
            return "original_value"

        self.assertEqual(original_function(), "mocked_value")

    def test_mock_when_condition_false(self):
        # Test case where condition is false, original function should be called
        mock_condition = lambda: False

        @mock_when(mock_condition, None) # mock_result is not used when condition is false
        def original_function():
            return "original_value"

        self.assertEqual(original_function(), "original_value")

    def test_mock_when_mock_result_raises_exception(self):
        # Test case where mock_result raises an exception, should fall back to original
        mock_condition = lambda: True
        def mock_result_func_raises():
            raise ValueError("Mock error")

        @mock_when(mock_condition, mock_result_func_raises, verbosity=Verbosity.ONCE)
        def original_function():
            return "original_value"

        self.assertEqual(original_function(), "original_value")

    def test_mock_when_mock_result_raises_exception_logging(self):
        # Test case to ensure the info log is triggered when mock_result raises an exception
        mock_condition = lambda: True
        def mock_result_func_raises():
            raise ValueError("Mock error")

        @mock_when(mock_condition, mock_result_func_raises, verbosity=Verbosity.ONCE)
        def original_function():
            return "original_value"

        with self.assertLogs('jinnang.common.decorators', level='INFO') as cm:
            original_function()
            self.assertIn('Cannot find result for', cm.output[0])

    def test_fail_recover_no_exception(self):
        # Test case where no exception occurs
        @fail_recover
        def successful_function():
            return {"status": "success"}

        result = successful_function()
        self.assertEqual(result, {"status": "success"})

    def test_fail_recover_json_decode_error(self):
        # Test case for JSONDecodeError
        @fail_recover
        def json_error_function():
            raise json.JSONDecodeError("Invalid JSON", "doc", 0)

        result = json_error_function()
        self.assertEqual(result['statusCode'], 400)
        self.assertIn("Invalid JSON", result['body'])

    def test_fail_recover_bad_input_exception(self):
        # Test case for BadInputException
        @fail_recover
        def bad_input_function():
            raise BadInputException("Bad input provided")

        result = bad_input_function()
        self.assertEqual(result['statusCode'], 400)
        self.assertIn("Bad input provided", result['body'])

    def test_fail_recover_generic_exception(self):
        # Test case for a generic Exception
        @fail_recover
        def generic_error_function():
            raise ValueError("Something went wrong")

        result = generic_error_function()
        self.assertEqual(result['statusCode'], 500)
        self.assertIn("Something went wrong", result['body'])

    def test_custom_retry_success_first_attempt(self):
        # Test case where function succeeds on the first attempt
        mock_func = MagicMock(return_value="success")
        @custom_retry(max_retries=3, retry_exceptions=ValueError)
        def func():
            return mock_func()

        self.assertEqual(func(), "success")
        mock_func.assert_called_once()

    def test_custom_retry_success_after_retry(self):
        # Test case where function succeeds after one retry
        mock_func = MagicMock(side_effect=[ValueError("fail"), "success"])
        @custom_retry(max_retries=3, retry_exceptions=ValueError, delay=0.01)
        def func():
            return mock_func()

        self.assertEqual(func(), "success")
        self.assertEqual(mock_func.call_count, 2)

    def test_custom_retry_all_retries_fail(self):
        # Test case where function fails after all retries
        mock_func = MagicMock(side_effect=ValueError("fail"))
        @custom_retry(max_retries=3, retry_exceptions=ValueError, delay=0.01, default_output="default")
        def func():
            return mock_func()

        self.assertEqual(func(), "default")
        self.assertEqual(mock_func.call_count, 3)

    def test_custom_retry_no_retries(self):
        # Test case with max_retries = 0
        mock_func = MagicMock(side_effect=ValueError("fail"))
        @custom_retry(max_retries=0, retry_exceptions=ValueError, default_output="no_retry")
        def func():
            return mock_func()

        self.assertEqual(func(), "no_retry")
        mock_func.assert_not_called()

    def test_custom_retry_different_exception(self):
        # Test case where a different exception is raised (should not retry)
        mock_func = MagicMock(side_effect=TypeError("wrong type"))
        @custom_retry(max_retries=3, retry_exceptions=ValueError, default_output="default")
        def func():
            return mock_func()

        with self.assertRaises(TypeError):
            func()
        mock_func.assert_called_once()

    def test_custom_retry_multiple_exceptions(self):
        # Test case with multiple retry exceptions
        mock_func = MagicMock(side_effect=[ValueError("v"), TypeError("t"), "success"])
        @custom_retry(max_retries=3, retry_exceptions=(ValueError, TypeError), delay=0.01)
        def func():
            return mock_func()

        self.assertEqual(func(), "success")
        self.assertEqual(mock_func.call_count, 3)

    def test_custom_retry_delay(self):
        # Test that delay is respected
        mock_func = MagicMock(side_effect=[ValueError("fail"), "success"])
        start_time = time.time()
        @custom_retry(max_retries=2, retry_exceptions=ValueError, delay=0.1)
        def func():
            return mock_func()

        func()
        end_time = time.time()
        self.assertGreaterEqual(end_time - start_time, 0.1)


if __name__ == '__main__':
    unittest.main()

    def test_mock_when_condition_true(self):
        """Test mock_when decorator when condition is True."""
        mock_result_func = lambda *args, **kwargs: "mocked_result"
        condition = lambda: True
        
        @mock_when(condition)
        def test_function():
            return "real_result"
        
        # Need to set mock_result in the decorator's scope
        # This is a limitation of the current implementation
        # For testing, we'll modify the approach
        pass

    def test_mock_when_condition_false(self):
        """Test mock_when decorator when condition is False."""
        condition = lambda: False
        
        @mock_when(condition)
        def test_function():
            return "real_result"
        
        result = test_function()
        self.assertEqual(result, "real_result")

    def test_fail_recover_success(self):
        """Test fail_recover decorator with successful function execution."""
        @fail_recover
        def successful_function():
            return {"success": True, "data": "test"}
        
        result = successful_function()
        self.assertEqual(result, {"success": True, "data": "test"})

    def test_fail_recover_json_decode_error(self):
        """Test fail_recover decorator with JSONDecodeError."""
        @fail_recover
        def function_with_json_error():
            raise json.JSONDecodeError("Invalid JSON", "doc", 0)
        
        result = function_with_json_error()
        
        self.assertEqual(result['statusCode'], 400)
        body = json.loads(result['body'])
        self.assertEqual(body['code'], 400)
        self.assertIn("Invalid JSON", body['msg'])

    def test_fail_recover_bad_input_exception(self):
        """Test fail_recover decorator with BadInputException."""
        @fail_recover
        def function_with_bad_input():
            raise BadInputException("Bad input provided")
        
        result = function_with_bad_input()
        
        self.assertEqual(result['statusCode'], 400)
        body = json.loads(result['body'])
        self.assertEqual(body['code'], 400)
        self.assertIn("Bad input provided", body['msg'])

    def test_fail_recover_generic_exception(self):
        """Test fail_recover decorator with generic exception."""
        @fail_recover
        def function_with_generic_error():
            raise ValueError("Something went wrong")
        
        result = function_with_generic_error()
        
        self.assertEqual(result['statusCode'], 500)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        body = json.loads(result['body'])
        self.assertEqual(body['code'], 500)
        self.assertIn("Something went wrong", body['msg'])

    def test_fail_recover_preserves_function_metadata(self):
        """Test that fail_recover preserves original function metadata."""
        @fail_recover
        def documented_function():
            """This function has documentation."""
            return "result"
        
        self.assertEqual(documented_function.__name__, "documented_function")
        self.assertEqual(documented_function.__doc__, "This function has documentation.")

    def test_custom_retry_success_first_attempt(self):
        """Test custom_retry decorator with successful first attempt."""
        @custom_retry(max_retries=3, retry_exceptions=ValueError)
        def successful_function():
            return "success"
        
        result = successful_function()
        self.assertEqual(result, "success")

    def test_custom_retry_success_after_retries(self):
        """Test custom_retry decorator with success after some retries."""
        call_count = 0
        
        @custom_retry(max_retries=3, retry_exceptions=ValueError)
        def function_with_retries():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Temporary failure")
            return "success"
        
        result = function_with_retries()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)

    def test_custom_retry_max_retries_exceeded(self):
        """Test custom_retry decorator when max retries are exceeded."""
        call_count = 0
        
        @custom_retry(max_retries=2, retry_exceptions=ValueError, default_output="failed")
        def always_failing_function():
            nonlocal call_count
            call_count += 1
            raise ValueError("Always fails")
        
        result = always_failing_function()
        self.assertEqual(result, "failed")
        self.assertEqual(call_count, 2)

    def test_custom_retry_non_retry_exception(self):
        """Test custom_retry decorator with non-retry exception."""
        @custom_retry(max_retries=3, retry_exceptions=ValueError)
        def function_with_non_retry_exception():
            raise TypeError("This should not be retried")
        
        with self.assertRaises(TypeError):
            function_with_non_retry_exception()

    def test_custom_retry_multiple_exception_types(self):
        """Test custom_retry decorator with multiple exception types."""
        call_count = 0
        
        @custom_retry(max_retries=3, retry_exceptions=(ValueError, TypeError))
        def function_with_multiple_exceptions():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("First failure")
            elif call_count == 2:
                raise TypeError("Second failure")
            return "success"
        
        result = function_with_multiple_exceptions()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)

    def test_custom_retry_with_delay(self):
        """Test custom_retry decorator with delay between retries."""
        call_count = 0
        start_time = time.time()
        
        @custom_retry(max_retries=2, retry_exceptions=ValueError, delay=0.1)
        def function_with_delay():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Temporary failure")
            return "success"
        
        result = function_with_delay()
        end_time = time.time()
        
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 2)
        # Should have taken at least 0.1 seconds due to delay
        self.assertGreaterEqual(end_time - start_time, 0.1)

    def test_custom_retry_preserves_function_metadata(self):
        """Test that custom_retry preserves original function metadata."""
        @custom_retry(max_retries=3, retry_exceptions=ValueError)
        def documented_function():
            """This function has documentation."""
            return "result"
        
        self.assertEqual(documented_function.__name__, "documented_function")
        self.assertEqual(documented_function.__doc__, "This function has documentation.")

    def test_custom_retry_with_args_and_kwargs(self):
        """Test custom_retry decorator preserves function arguments."""
        call_count = 0
        
        @custom_retry(max_retries=2, retry_exceptions=ValueError)
        def function_with_args(arg1, arg2, kwarg1=None):
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Temporary failure")
            return f"{arg1}-{arg2}-{kwarg1}"
        
        result = function_with_args("test1", "test2", kwarg1="test3")
        self.assertEqual(result, "test1-test2-test3")
        self.assertEqual(call_count, 2)

    def test_custom_retry_default_output_none(self):
        """Test custom_retry decorator with default None output."""
        @custom_retry(max_retries=1, retry_exceptions=ValueError)
        def always_failing_function():
            raise ValueError("Always fails")
        
        result = always_failing_function()
        self.assertIsNone(result)

    def test_custom_retry_zero_retries(self):
        """Test custom_retry decorator with zero retries."""
        call_count = 0
        
        @custom_retry(max_retries=0, retry_exceptions=ValueError, default_output="no_retries")
        def function_no_retries():
            nonlocal call_count
            call_count += 1
            raise ValueError("Immediate failure")
        
        result = function_no_retries()
        self.assertEqual(result, "no_retries")
        self.assertEqual(call_count, 0)  # Should not be called at all

    @patch('jinnang.common.decorators.logger')
    def test_custom_retry_logging(self, mock_logger):
        """Test that custom_retry logs retry attempts."""
        call_count = 0
        
        @custom_retry(max_retries=2, retry_exceptions=ValueError)
        def function_with_logging():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Logged failure")
            return "success"
        
        result = function_with_logging()
        self.assertEqual(result, "success")
        
        # Verify that debug logging was called
        mock_logger.debug.assert_called()
        debug_call_args = mock_logger.debug.call_args[0][0]
        self.assertIn("Retry", debug_call_args)
        self.assertIn("Logged failure", debug_call_args)


if __name__ == '__main__':
    unittest.main()