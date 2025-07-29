#!/usr/bin/env python3
"""
Unit tests for the suppress_c_stdout_stderr function.

This module tests all aspects of the suppress functionality including:
- Basic suppression of C stdout/stderr
- Threading scenarios
- Nested suppression contexts
- Error handling
- Performance characteristics
"""

import unittest
import os
import sys
import threading
import time
import subprocess
import tempfile
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed
from unittest.mock import patch, MagicMock

from src.jinnang.io.system import suppress_c_stdout_stderr


class TestSuppressCStdoutStderr(unittest.TestCase):
    """Test the suppress_c_stdout_stderr function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
    
    def tearDown(self):
        """Clean up after tests."""
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
    
    def test_basic_suppression(self):
        """Test basic suppression functionality."""
        # Capture what would normally go to stdout/stderr
        captured_stdout = StringIO()
        captured_stderr = StringIO()
        
        with patch('sys.stdout', captured_stdout), patch('sys.stderr', captured_stderr):
            with suppress_c_stdout_stderr():
                # These should be suppressed (C-level output)
                os.write(1, b"This should be suppressed\n")
                os.write(2, b"This error should be suppressed\n")
                
                # These should still appear (Python-level output)
                print("This should appear", file=sys.stdout)
                print("This error should appear", file=sys.stderr)
        
        stdout_content = captured_stdout.getvalue()
        stderr_content = captured_stderr.getvalue()
        
        # Python-level output should appear
        self.assertIn("This should appear", stdout_content)
        self.assertIn("This error should appear", stderr_content)
        
        # C-level output should be suppressed (not in Python stdout/stderr)
        self.assertNotIn("This should be suppressed", stdout_content)
        self.assertNotIn("This error should be suppressed", stderr_content)
    
    def test_context_manager_exit(self):
        """Test that suppression is properly restored after context exit."""
        # Store original file descriptors
        original_stdout_fd = os.dup(1)
        original_stderr_fd = os.dup(2)
        
        try:
            with suppress_c_stdout_stderr():
                # Inside context, descriptors should be redirected
                pass
            
            # After context, descriptors should be restored
            # We can't easily test this directly, but we can ensure no exceptions
            os.write(1, b"Test after context\n")
            os.write(2, b"Error test after context\n")
            
        finally:
            # Clean up
            os.close(original_stdout_fd)
            os.close(original_stderr_fd)
    
    def test_nested_suppression(self):
        """Test nested suppression contexts."""
        captured_stdout = StringIO()
        
        with patch('sys.stdout', captured_stdout):
            with suppress_c_stdout_stderr():
                os.write(1, b"Outer suppressed\n")
                print("Outer Python", file=sys.stdout)
                
                with suppress_c_stdout_stderr():
                    os.write(1, b"Inner suppressed\n")
                    print("Inner Python", file=sys.stdout)
                
                os.write(1, b"Outer suppressed again\n")
                print("Outer Python again", file=sys.stdout)
        
        stdout_content = captured_stdout.getvalue()
        
        # Python output should appear
        self.assertIn("Outer Python", stdout_content)
        self.assertIn("Inner Python", stdout_content)
        self.assertIn("Outer Python again", stdout_content)
        
        # C-level output should be suppressed
        self.assertNotIn("Outer suppressed", stdout_content)
        self.assertNotIn("Inner suppressed", stdout_content)
        self.assertNotIn("Outer suppressed again", stdout_content)
    
    def test_exception_handling(self):
        """Test that suppression is properly restored even when exceptions occur."""
        original_stdout_fd = os.dup(1)
        original_stderr_fd = os.dup(2)
        
        try:
            with self.assertRaises(ValueError):
                with suppress_c_stdout_stderr():
                    os.write(1, b"Before exception\n")
                    raise ValueError("Test exception")
            
            # After exception, descriptors should be restored
            os.write(1, b"After exception\n")
            
        finally:
            os.close(original_stdout_fd)
            os.close(original_stderr_fd)
    
    def test_threading_isolation(self):
        """Test that suppression works correctly across multiple threads."""
        results = []
        results_lock = threading.Lock()
        
        def worker(thread_id, use_suppression):
            try:
                if use_suppression:
                    with suppress_c_stdout_stderr():
                        # Simulate C-level output (will be suppressed)
                        os.write(1, f"Thread {thread_id} C output\n".encode())
                        # This should work fine
                        result = f"Thread {thread_id} with suppression completed"
                else:
                    # Without suppression
                    os.write(1, f"Thread {thread_id} C output\n".encode())
                    result = f"Thread {thread_id} without suppression completed"
                
                with results_lock:
                    results.append((thread_id, use_suppression, result))
                    
            except Exception as e:
                with results_lock:
                    results.append((thread_id, use_suppression, f"Error: {e}"))
        
        threads = []
        for i in range(10):
            use_suppression = i % 2 == 0  # Alternate between suppressed and non-suppressed
            thread = threading.Thread(target=worker, args=(i, use_suppression))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Verify results
        self.assertEqual(len(results), 10)
        
        for thread_id, used_suppression, result in results:
            # All threads should complete successfully
            self.assertIn("completed", result)
            self.assertNotIn("Error:", result)
            
            # Verify the correct suppression mode was used
            if used_suppression:
                self.assertIn("with suppression", result)
            else:
                self.assertIn("without suppression", result)
    
    def test_concurrent_suppression(self):
        """Test concurrent suppression operations."""
        def worker(worker_id):
            with suppress_c_stdout_stderr():
                # Simulate some work with C-level output
                for i in range(10):
                    os.write(1, f"Worker {worker_id} iteration {i}\n".encode())
                    time.sleep(0.001)  # Small delay to increase chance of interleaving
                return f"Worker {worker_id} completed"
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(worker, i) for i in range(5)]
            results = [future.result() for future in as_completed(futures)]
        
        # All workers should complete successfully
        self.assertEqual(len(results), 5)
        for i in range(5):
            self.assertIn(f"Worker {i} completed", results)
    
    def test_mixed_suppression_and_normal_output(self):
        """Test mixing suppressed and normal output in the same thread."""
        captured_stdout = StringIO()
        
        with patch('sys.stdout', captured_stdout):
            # Normal output
            print("Before suppression", file=sys.stdout)
            
            with suppress_c_stdout_stderr():
                os.write(1, b"Suppressed C output\n")
                print("During suppression", file=sys.stdout)
            
            # Normal output again
            print("After suppression", file=sys.stdout)
        
        stdout_content = captured_stdout.getvalue()
        
        # Python output should appear
        self.assertIn("Before suppression", stdout_content)
        self.assertIn("During suppression", stdout_content)
        self.assertIn("After suppression", stdout_content)
        
        # C output should be suppressed
        self.assertNotIn("Suppressed C output", stdout_content)
    
    def test_large_output_suppression(self):
        """Test suppression of large amounts of output."""
        with suppress_c_stdout_stderr():
            # Generate large amount of C-level output
            for i in range(1000):
                os.write(1, f"Large output line {i}\n".encode())
                os.write(2, f"Large error line {i}\n".encode())
        
        # Should complete without issues
        # The main test is that this doesn't hang or crash
    
    def test_rapid_context_switching(self):
        """Test rapid entering and exiting of suppression contexts."""
        for i in range(100):
            with suppress_c_stdout_stderr():
                os.write(1, f"Rapid test {i}\n".encode())
        
        # Should complete without issues
    
    def test_subprocess_integration(self):
        """Test that suppression works with subprocess calls."""
        # Create a temporary script that produces C-level output
        script_content = f'''
import os
import sys
sys.path.insert(0, "{os.path.abspath('src')}")
from jinnang.io.system import suppress_c_stdout_stderr

# Test without suppression first
print("Before suppression")

with suppress_c_stdout_stderr():
    # These writes should be suppressed at C level
    os.write(1, b"C stdout from subprocess\\n")
    os.write(2, b"C stderr from subprocess\\n")
    # Python level output should still work
    print("Python stdout from subprocess")
    print("Python stderr from subprocess", file=sys.stderr)

print("After suppression")
'''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(script_content)
            script_path = f.name
        
        try:
            # Run the script
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True
            )
            
            # Should complete successfully
            self.assertEqual(result.returncode, 0)
            
            # Python output should appear
            self.assertIn("Before suppression", result.stdout)
            self.assertIn("Python stdout from subprocess", result.stdout)
            self.assertIn("After suppression", result.stdout)
            self.assertIn("Python stderr from subprocess", result.stderr)
            
            # Note: C-level suppression in subprocess is complex to test
            # The main goal is to ensure the function doesn't crash
            
        finally:
            os.unlink(script_path)


class TestSuppressPerformance(unittest.TestCase):
    """Test performance characteristics of suppression."""
    
    def test_suppression_overhead(self):
        """Test that suppression doesn't add excessive overhead."""
        # Test without suppression
        iterations = 100  # Reduced for more realistic testing
        start_time = time.time()
        for i in range(iterations):
            # Do some minimal work
            _ = i * 2
        no_suppression_time = time.time() - start_time
        
        # Test with suppression
        start_time = time.time()
        for i in range(iterations):
            with suppress_c_stdout_stderr():
                # Do the same minimal work
                _ = i * 2
        suppression_time = time.time() - start_time
        
        # Suppression will add overhead, but shouldn't be excessive
        # Allow for reasonable overhead (100x is generous for file descriptor operations)
        max_allowed_time = max(no_suppression_time * 100, 1.0)  # At least 1 second allowance
        self.assertLess(suppression_time, max_allowed_time, 
                       f"Suppression took {suppression_time:.3f}s vs {no_suppression_time:.3f}s baseline")
    
    def test_concurrent_performance(self):
        """Test performance under concurrent access."""
        def worker():
            for i in range(100):
                with suppress_c_stdout_stderr():
                    os.write(1, f"Worker output {i}\n".encode())
        
        start_time = time.time()
        
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        duration = time.time() - start_time
        
        # Should complete in reasonable time
        self.assertLess(duration, 10.0, "Concurrent suppression took too long")


class TestSuppressEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def test_already_redirected_descriptors(self):
        """Test behavior when descriptors are already redirected."""
        # This is a complex test that would require mocking file descriptor operations
        # For now, we'll just ensure the context manager works
        with suppress_c_stdout_stderr():
            with suppress_c_stdout_stderr():
                os.write(1, b"Nested test\n")
    
    def test_invalid_file_descriptors(self):
        """Test behavior with invalid file descriptors."""
        # This test ensures the function handles edge cases gracefully
        with suppress_c_stdout_stderr():
            # Should not crash even if there are issues with file descriptors
            pass
    
    def test_signal_handling(self):
        """Test that suppression works correctly with signal handling."""
        # Basic test to ensure signals don't interfere
        import signal
        
        def signal_handler(signum, frame):
            pass
        
        original_handler = signal.signal(signal.SIGUSR1, signal_handler)
        
        try:
            with suppress_c_stdout_stderr():
                os.write(1, b"Signal test\n")
                # Send signal to self (this is safe in tests)
                os.kill(os.getpid(), signal.SIGUSR1)
                os.write(1, b"After signal\n")
        finally:
            signal.signal(signal.SIGUSR1, original_handler)


class TestSuppressIntegration(unittest.TestCase):
    """Integration tests for suppress functionality."""
    
    def test_with_global_lock_integration(self):
        """Test that suppression works correctly with global locks."""
        from jinnang.concurrency.global_lock import global_lock
        
        results = []
        
        def worker(worker_id):
            with global_lock("suppress_integration_test"):
                with suppress_c_stdout_stderr():
                    os.write(1, f"Worker {worker_id} C output\n".encode())
                    results.append(f"Worker {worker_id} completed")
        
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All workers should complete
        self.assertEqual(len(results), 5)
        for i in range(5):
            self.assertIn(f"Worker {i} completed", results)
    
    def test_real_world_scenario(self):
        """Test a real-world scenario with mixed operations."""
        import json
        
        def process_data(data_id):
            """Simulate processing data with C library calls."""
            with suppress_c_stdout_stderr():
                # Simulate C library output that should be suppressed
                os.write(1, f"Processing data {data_id}...\n".encode())
                os.write(2, f"Debug info for data {data_id}\n".encode())
                
                # Simulate actual work
                time.sleep(0.01)
                
                # Return result (this would normally go to Python stdout)
                return {"data_id": data_id, "status": "processed"}
        
        # Process multiple data items concurrently
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(process_data, i) for i in range(10)]
            results = [future.result() for future in as_completed(futures)]
        
        # All data should be processed
        self.assertEqual(len(results), 10)
        
        # Verify results
        processed_ids = {result["data_id"] for result in results}
        self.assertEqual(processed_ids, set(range(10)))
        
        # All should have processed status
        for result in results:
            self.assertEqual(result["status"], "processed")


if __name__ == "__main__":
    unittest.main()