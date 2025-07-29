#!/usr/bin/env python3
"""
Unit tests for the global lock module.

This module tests all aspects of the global lock functionality including:
- UnifiedLock class
- GlobalLockManager
- Decorator usage
- Context manager usage
- Async operations
- Thread safety
- Key-based isolation
"""

import unittest
import asyncio
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from unittest.mock import patch, MagicMock

from jinnang.concurrency.global_lock import (
    UnifiedLock,
    GlobalLockManager,
    with_global_lock,
    global_lock,
    global_alock,
    lock,
    alock,
    global_lock_manager
)


class TestUnifiedLock(unittest.TestCase):
    """Test the UnifiedLock class."""
    
    def setUp(self):
        self.lock = UnifiedLock("test_lock")
    
    def test_lock_initialization(self):
        """Test lock initialization."""
        self.assertEqual(self.lock.name, "test_lock")
        self.assertIsNotNone(self.lock._thread_lock)
        self.assertIsNone(self.lock._async_lock)  # Should be lazy
    
    def test_sync_context_manager(self):
        """Test synchronous context manager usage."""
        with self.lock:
            # Lock should be acquired
            self.assertTrue(self.lock._thread_lock._is_owned())
        # Lock should be released
        self.assertFalse(self.lock._thread_lock._is_owned())
    
    def test_sync_acquire_release(self):
        """Test explicit acquire/release methods."""
        self.lock.acquire()
        self.assertTrue(self.lock._thread_lock._is_owned())
        self.lock.release()
        self.assertFalse(self.lock._thread_lock._is_owned())
    
    def test_sync_nested_locking(self):
        """Test nested synchronous locking (reentrant)."""
        with self.lock:
            with self.lock:
                with self.lock:
                    self.assertTrue(self.lock._thread_lock._is_owned())
        self.assertFalse(self.lock._thread_lock._is_owned())
    
    def test_async_context_manager(self):
        """Test asynchronous context manager usage."""
        async def run_test():
            async with self.lock:
                # Async lock should be created and acquired
                self.assertIsNotNone(self.lock._async_lock)
                self.assertTrue(self.lock._async_lock.locked())
            # Lock should be released
            self.assertFalse(self.lock._async_lock.locked())
        
        asyncio.run(run_test())
    
    def test_decorator_with_mixed_args_and_kwargs(self):
        """Test that decorator works with functions using both args and kwargs."""
        @with_global_lock("mixed_args_test")
        def func_with_mixed_params(key, timeout, data, optional=None):
            """Function with both positional and keyword arguments."""
            return {
                "key": key, 
                "timeout": timeout, 
                "data": data, 
                "optional": optional
            }
        
        # Test with keyword arguments
        result = func_with_mixed_params(
            "test_key", 
            30, 
            "test_data", 
            optional="extra_value"
        )
        expected = {
            "key": "test_key", 
            "timeout": 30, 
            "data": "test_data", 
            "optional": "extra_value"
        }
        self.assertEqual(result, expected)
        
        # Test with positional arguments only
        result2 = func_with_mixed_params("key2", 45, "data2")
        expected2 = {
            "key": "key2", 
            "timeout": 45, 
            "data": "data2", 
            "optional": None
        }
        self.assertEqual(result2, expected2)
    
    def test_async_acquire_release(self):
        """Test explicit async acquire/release methods."""
        async def run_test():
            await self.lock.acquire_async()
            self.assertIsNotNone(self.lock._async_lock)
            self.assertTrue(self.lock._async_lock.locked())
            self.lock.release_async()
            self.assertFalse(self.lock._async_lock.locked())
        
        asyncio.run(run_test())


class TestGlobalLockManager(unittest.TestCase):
    """Test the GlobalLockManager class."""
    
    def setUp(self):
        self.manager = GlobalLockManager()
    
    def test_get_or_create_lock(self):
        """Test lock creation and retrieval."""
        lock1 = self.manager._get_or_create_lock("test_key")
        lock2 = self.manager._get_or_create_lock("test_key")
        
        # Should return the same lock instance
        self.assertIs(lock1, lock2)
        self.assertEqual(lock1.name, "test_key")
    
    def test_different_keys_different_locks(self):
        """Test that different keys create different locks."""
        lock1 = self.manager._get_or_create_lock("key1")
        lock2 = self.manager._get_or_create_lock("key2")
        
        self.assertIsNot(lock1, lock2)
        self.assertEqual(lock1.name, "key1")
        self.assertEqual(lock2.name, "key2")
    
    def test_sync_context_manager(self):
        """Test synchronous context manager."""
        with self.manager.lock("test_key"):
            # Lock should be created and acquired
            self.assertIn("test_key", self.manager._locks)
    
    def test_execute_sync(self):
        """Test synchronous function execution."""
        def test_func(x, y):
            return x + y
        
        result = self.manager.execute_sync(
            lock_key="test_key", 
            func=test_func, 
            func_args=(2, 3)
        )
        self.assertEqual(result, 5)
    
    def test_async_context_manager(self):
        """Test asynchronous context manager."""
        async def run_test():
            async with self.manager.alock("test_key"):
                # Lock should be created and acquired
                self.assertIn("test_key", self.manager._locks)
        
        asyncio.run(run_test())
    
    def test_execute_async(self):
        """Test asynchronous function execution."""
        async def run_test():
            async def test_func(x, y):
                await asyncio.sleep(0.01)
                return x * y
            
            result = await self.manager.execute_async(
                lock_key="test_key", 
                func=test_func, 
                func_args=(3, 4)
            )
            self.assertEqual(result, 12)
        
        asyncio.run(run_test())
    
    def test_list_keys(self):
        """Test listing active lock keys."""
        self.manager._get_or_create_lock("key1")
        self.manager._get_or_create_lock("key2")
        
        keys = self.manager.list_keys()
        self.assertIn("key1", keys)
        self.assertIn("key2", keys)
    
    def test_cleanup_unused_locks(self):
        """Test cleanup of unused locks."""
        # Create some locks
        self.manager._get_or_create_lock("key1")
        self.manager._get_or_create_lock("key2")
        
        # Cleanup should remove unused locks
        self.manager.cleanup_unused_locks()
        
        # Keys should be removed (since locks aren't held)
        keys = self.manager.list_keys()
        self.assertEqual(len(keys), 0)
    
    def test_get_lock(self):
        """Test getting a lock instance."""
        lock = self.manager.get_lock("test_key")
        self.assertIsInstance(lock, UnifiedLock)
        self.assertEqual(lock.name, "test_key")


class TestDecorators(unittest.TestCase):
    """Test decorator functionality."""
    
    def test_sync_decorator(self):
        """Test synchronous decorator."""
        call_count = 0
        
        @with_global_lock("sync_test")
        def test_func():
            nonlocal call_count
            call_count += 1
            time.sleep(0.01)
            return call_count
        
        # Test single call
        result = test_func()
        self.assertEqual(result, 1)
        
        # Test multiple calls
        results = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(test_func) for _ in range(5)]
            for future in as_completed(futures):
                results.append(future.result())
        
        # All calls should have completed sequentially
        self.assertEqual(sorted(results), [2, 3, 4, 5, 6])
    
    def test_async_decorator(self):
        """Test asynchronous decorator."""
        async def run_test():
            call_count = 0
            
            @with_global_lock("async_test")
            async def test_func():
                nonlocal call_count
                call_count += 1
                await asyncio.sleep(0.01)
                return call_count
            
            # Test single call
            result = await test_func()
            self.assertEqual(result, 1)
            
            # Test multiple concurrent calls
            tasks = [test_func() for _ in range(5)]
            results = await asyncio.gather(*tasks)
            
            # All calls should have completed sequentially
            self.assertEqual(sorted(results), [2, 3, 4, 5, 6])
        
        asyncio.run(run_test())
    
    def test_decorator_with_timeout(self):
        """Test decorator with timeout."""
        @with_global_lock("timeout_test", timeout=0.1)
        def slow_func():
            time.sleep(0.2)
            return "completed"
        
        # First call should succeed
        result = slow_func()
        self.assertEqual(result, "completed")
    
    def test_decorator_preserves_function_metadata(self):
        """Test that decorator preserves function metadata."""
        @with_global_lock("metadata_test")
        def test_func():
            """Test function docstring."""
            return "result"
        
        self.assertEqual(test_func.__name__, "test_func")
        self.assertEqual(test_func.__doc__, "Test function docstring.")
    
    def test_decorator_with_key_parameter(self):
        """Test that decorator works with functions that have 'key' parameter."""
        @with_global_lock("key_param_test")
        def func_with_key_param(key, value):
            """Function that has a 'key' parameter."""
            return f"{key}:{value}"
        
        # This should not raise "multiple values for argument 'key'" error
        result = func_with_key_param("test_key", "test_value")
        self.assertEqual(result, "test_key:test_value")
    
    def test_decorator_with_timeout_parameter(self):
        """Test that decorator works with functions that have 'timeout' parameter."""
        @with_global_lock("timeout_param_test")
        def func_with_timeout_param(timeout, operation):
            """Function that has a 'timeout' parameter."""
            return f"timeout={timeout}, operation={operation}"
        
        # This should not raise "multiple values for argument 'timeout'" error
        result = func_with_timeout_param(30, "database_query")
        self.assertEqual(result, "timeout=30, operation=database_query")
    
    def test_decorator_with_both_key_and_timeout_parameters(self):
        """Test that decorator works with functions that have both 'key' and 'timeout' parameters."""
        @with_global_lock("both_params_test")
        def func_with_both_params(key, timeout, data):
            """Function that has both 'key' and 'timeout' parameters."""
            return {"key": key, "timeout": timeout, "data": data}
        
        # This should not raise any parameter conflict errors
        result = func_with_both_params("cache_key", 60, "some_data")
        expected = {"key": "cache_key", "timeout": 60, "data": "some_data"}
        self.assertEqual(result, expected)
    
    def test_async_decorator_with_key_parameter(self):
        """Test that async decorator works with functions that have 'key' parameter."""
        async def run_test():
            @with_global_lock("async_key_param_test")
            async def async_func_with_key_param(key, value):
                """Async function that has a 'key' parameter."""
                await asyncio.sleep(0.001)  # Small delay
                return f"async_{key}:{value}"
            
            # This should not raise "multiple values for argument 'key'" error
            result = await async_func_with_key_param("async_test_key", "async_test_value")
            self.assertEqual(result, "async_async_test_key:async_test_value")
        
        asyncio.run(run_test())
    
    def test_async_decorator_with_timeout_parameter(self):
        """Test that async decorator works with functions that have 'timeout' parameter."""
        async def run_test():
            @with_global_lock("async_timeout_param_test")
            async def async_func_with_timeout_param(timeout, operation):
                """Async function that has a 'timeout' parameter."""
                await asyncio.sleep(0.001)  # Small delay
                return f"async_timeout={timeout}, operation={operation}"
            
            # This should not raise "multiple values for argument 'timeout'" error
            result = await async_func_with_timeout_param(45, "async_database_query")
            self.assertEqual(result, "async_timeout=45, operation=async_database_query")
        
        asyncio.run(run_test())
    
    def test_decorator_with_mixed_args_and_kwargs(self):
        """Test that decorator works with functions using both positional and keyword arguments."""
        @with_global_lock("mixed_args_test")
        def func_with_mixed_params(key, timeout, *args, **kwargs):
            """Function that has both 'key' and 'timeout' parameters plus varargs."""
            return {
                "key": key,
                "timeout": timeout,
                "args": args,
                "kwargs": kwargs
            }
        
        # Test with both positional and keyword arguments
        result = func_with_mixed_params("test_key", 30, "extra_arg", data="test_data")
        expected = {
            "key": "test_key",
            "timeout": 30,
            "args": ("extra_arg",),
            "kwargs": {"data": "test_data"}
        }
        self.assertEqual(result, expected)


class TestContextManagers(unittest.TestCase):
    """Test context manager functionality."""
    
    def test_global_lock_context_manager(self):
        """Test global_lock context manager."""
        with global_lock("context_test"):
            # Should be able to access the lock
            self.assertIn("context_test", global_lock_manager.list_keys())
    
    def test_lock_alias(self):
        """Test lock alias."""
        with lock("alias_test"):
            self.assertIn("alias_test", global_lock_manager.list_keys())
    
    def test_async_context_manager(self):
        """Test async context managers."""
        async def run_test():
            async with global_alock("async_context_test"):
                self.assertIn("async_context_test", global_lock_manager.list_keys())
            
            async with alock("async_alias_test"):
                self.assertIn("async_alias_test", global_lock_manager.list_keys())
        
        asyncio.run(run_test())
    
    def test_nested_context_managers(self):
        """Test nested context managers with same key."""
        with global_lock("nested_test"):
            with global_lock("nested_test"):
                with global_lock("nested_test"):
                    # Should work due to reentrant locks
                    self.assertIn("nested_test", global_lock_manager.list_keys())


class TestThreadSafety(unittest.TestCase):
    """Test thread safety and concurrency."""
    
    def test_concurrent_access_different_keys(self):
        """Test concurrent access with different keys."""
        results = []
        
        def worker(key, value):
            with global_lock(key):
                time.sleep(0.01)
                results.append(value)
        
        threads = []
        for i in range(10):
            thread = threading.Thread(target=worker, args=(f"key_{i}", i))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All workers should complete
        self.assertEqual(len(results), 10)
        self.assertEqual(sorted(results), list(range(10)))
    
    def test_concurrent_access_same_key(self):
        """Test concurrent access with same key."""
        results = []
        
        def worker(value):
            with global_lock("shared_key"):
                current_len = len(results)
                time.sleep(0.01)  # Simulate work
                results.append(value)
                # Verify no race condition
                self.assertEqual(len(results), current_len + 1)
        
        threads = []
        for i in range(10):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All workers should complete sequentially
        self.assertEqual(len(results), 10)
    
    def test_mixed_sync_async_operations(self):
        """Test mixed synchronous and asynchronous operations."""
        results = []
        
        def sync_worker(value):
            with global_lock("mixed_key"):
                time.sleep(0.01)
                results.append(f"sync_{value}")
        
        async def async_worker(value):
            async with global_alock("mixed_key"):
                await asyncio.sleep(0.01)
                results.append(f"async_{value}")
        
        async def run_mixed_test():
            # Start sync operations in threads
            with ThreadPoolExecutor(max_workers=3) as executor:
                sync_futures = [executor.submit(sync_worker, i) for i in range(3)]
                
                # Run async operations
                async_tasks = [async_worker(i) for i in range(3)]
                await asyncio.gather(*async_tasks)
                
                # Wait for sync operations
                for future in sync_futures:
                    future.result()
        
        asyncio.run(run_mixed_test())
        
        # All operations should complete
        self.assertEqual(len(results), 6)
        sync_results = [r for r in results if r.startswith("sync_")]
        async_results = [r for r in results if r.startswith("async_")]
        self.assertEqual(len(sync_results), 3)
        self.assertEqual(len(async_results), 3)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""
    
    def test_exception_in_context_manager(self):
        """Test that locks are released even when exceptions occur."""
        try:
            with global_lock("exception_test"):
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        # Lock should be released
        lock = global_lock_manager.get_lock("exception_test")
        self.assertFalse(lock._thread_lock._is_owned())
    
    def test_exception_in_async_context_manager(self):
        """Test that async locks are released even when exceptions occur."""
        async def run_test():
            try:
                async with global_alock("async_exception_test"):
                    raise ValueError("Test async exception")
            except ValueError:
                pass
            
            # Lock should be released
            lock = global_lock_manager.get_lock("async_exception_test")
            if lock._async_lock:
                self.assertFalse(lock._async_lock.locked())
        
        asyncio.run(run_test())
    
    def test_exception_in_decorated_function(self):
        """Test that locks are released when decorated functions raise exceptions."""
        @with_global_lock("decorator_exception_test")
        def failing_func():
            raise RuntimeError("Decorator test exception")
        
        with self.assertRaises(RuntimeError):
            failing_func()
        
        # Lock should be released
        lock = global_lock_manager.get_lock("decorator_exception_test")
        self.assertFalse(lock._thread_lock._is_owned())
    
    def test_empty_key(self):
        """Test behavior with empty key."""
        with global_lock(""):
            self.assertIn("", global_lock_manager.list_keys())
    
    def test_none_key_handling(self):
        """Test behavior with None key (should be converted to string)."""
        with global_lock(None):
            keys = global_lock_manager.list_keys()
            # None should be converted to string
            self.assertTrue(any("None" in str(key) for key in keys))


class TestPerformance(unittest.TestCase):
    """Test performance characteristics."""
    
    def test_lock_creation_performance(self):
        """Test that lock creation is reasonably fast."""
        start_time = time.time()
        
        for i in range(1000):
            global_lock_manager._get_or_create_lock(f"perf_key_{i}")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in reasonable time (adjust threshold as needed)
        self.assertLess(duration, 1.0, "Lock creation took too long")
    
    def test_concurrent_lock_access_performance(self):
        """Test performance under concurrent access."""
        def worker():
            for i in range(100):
                with global_lock("perf_shared_key"):
                    # Minimal work
                    pass
        
        start_time = time.time()
        
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete in reasonable time
        self.assertLess(duration, 5.0, "Concurrent access took too long")


if __name__ == "__main__":
    unittest.main()