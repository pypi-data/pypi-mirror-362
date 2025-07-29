"""Decorator utilities for function behavior modification.

This module provides reusable decorators that can be applied to functions
to modify their behavior, such as adding retry logic, mocking, and error handling.
"""

import time
import functools
import json
import traceback
from typing import Callable, Any, Type, Union, Tuple
import logging
from ..verbosity.verbosity import Verbosity
from .exceptions import BadInputException
from ..string import truncate

logger = logging.getLogger(__name__)


def mock_when(condition: Callable[..., bool],
              mock_result: Callable[..., Any],
              verbosity: Verbosity = Verbosity.SILENT,
              max_output_length: int = 100):
    """
    Decorator that returns mock result when condition is True,
    otherwise calls the original function.

    This is useful for testing and development environments where
    you want to bypass actual function execution under certain conditions.

    Args:
        condition: Callable that returns boolean to determine if mock should be used
        mock_result: The value to return when condition is True
        verbosity: Verbosity level. Defaults to Verbosity.SILENT.
        max_output_length: Maximum length of logged output values. Defaults to 100.

    Returns:
        The decorated function

    Example:
        ```python
        @mock_when(lambda: os.getenv('ENV') == 'test', lambda: {'test': 'data'})
        def get_real_data():
            # Complex implementation
            return actual_data
        ```
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            def _log_info(msg_template, res=None):
                if verbosity <= Verbosity.SILENT:
                    return

                args_truncated = truncate(json.dumps(args, ensure_ascii=False), max_output_length)
                kwargs_truncated = truncate(json.dumps(kwargs, ensure_ascii=False), max_output_length)

                format_args = {"args": args_truncated, "kwargs": kwargs_truncated}
                if res is not None:
                    format_args["res"] = truncate(json.dumps(res, ensure_ascii=False), max_output_length)

                logger.info(msg_template.format(**format_args))

            if condition():
                try:
                    res = mock_result(*args, **kwargs) if callable(mock_result) else mock_result
                    _log_info('Matching key={args} & {kwargs}. we got res={res}', res)
                    return res
                except Exception:
                    _log_info('Cannot find result for {args} and {kwargs}. Fallable back to normal function calling.')
            return func(*args, **kwargs)
        return wrapper
    return decorator


def fail_recover(func):
    """
    Decorator that catches exceptions and returns a standardized error response.

    This is particularly useful for API handlers where you want to ensure
    a consistent error response format even when exceptions occur.

    Args:
        func: The function to decorate

    Returns:
        A wrapped function that catches exceptions and returns formatted error responses

    Example:
        ```python
        @fail_recover
        def api_handler(event, context):
            # Implementation that might raise exceptions
            return result
        ```
    """
    def _create_error_body(code, msg):
        return json.dumps({
            "code": code,
            "data": {},
            "msg": msg,
        }, ensure_ascii=False)

    @functools.wraps(func)
    def wrapped(*args, **kw):
        try:
            return func(*args, **kw)
        except (json.JSONDecodeError, BadInputException) as e:
            return {
                'statusCode': 400,
                'body': _create_error_body(400, str(e))
            }
        except Exception as e:
            logger.error(traceback.format_exc())
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': _create_error_body(500, str(e))
            }
    return wrapped


def custom_retry(max_retries: int, retry_exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]], 
                delay: float = 0, default_output: Any = None):
    """
    Decorator that retries a function when specific exceptions occur.
    
    This is useful for operations that might fail temporarily due to
    network issues, race conditions, or other transient problems.

    Args:
        max_retries (int): Maximum number of retry attempts
        retry_exceptions (Exception or tuple): Exception(s) that trigger a retry
        delay (float): Delay between retries in seconds (default: 0)
        default_output (Any): Value to return if all retries fail (default: None)
        
    Returns:
        The decorated function that will retry on specified exceptions
        
    Example:
        ```python
        @custom_retry(max_retries=3, retry_exceptions=(ConnectionError, TimeoutError), delay=1)
        def fetch_data():
            # Implementation that might fail temporarily
            return data
        ```
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if max_retries == 0:
                return default_output

            retries = 0
            while retries < max_retries:
                try:
                    res = func(*args, **kwargs)
                    return res
                except retry_exceptions as e:
                    retries += 1
                    if retries >= max_retries:
                        return default_output
                    if delay > 0:
                        time.sleep(delay)
                    logger.debug(f"Retry {retries}/{max_retries} after exception: {e}")
        return wrapper
    return decorator