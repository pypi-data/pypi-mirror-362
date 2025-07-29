import unittest
import os
import tempfile
import time
from unittest.mock import patch, MagicMock
from datetime import datetime
import pytz

from jinnang.path.path import MyPath, ensure_unique_path, get_file_timestamp


class TestPathUtilities(unittest.TestCase):
    """Test cases for path utility functions."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.temp_dir, "test_file.txt")
        
        # Create a test file
        with open(self.test_file_path, "w") as f:
            f.write("Test content")
        
    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        os.rmdir(self.temp_dir)

    def test_my_path_basename(self):
        """Test MyPath basename property."""
        path = MyPath("/path/to/file.txt")
        self.assertEqual(path.basename, "file")
        
        path = MyPath("/path/to/file")
        self.assertEqual(path.basename, "file")
        
        path = MyPath("/path/to/file.name.with.dots.txt")
        self.assertEqual(path.basename, "file.name.with.dots")

    def test_my_path_extension(self):
        """Test MyPath extension property."""
        path = MyPath("/path/to/file.txt")
        self.assertEqual(path.extension, "txt")
        
        path = MyPath("/path/to/file")
        self.assertEqual(path.extension, "")
        
        path = MyPath("/path/to/file.name.with.dots.txt")
        self.assertEqual(path.extension, "txt")

    def test_my_path_abspath(self):
        """Test MyPath abspath property."""
        # Test with relative path
        rel_path = "relative/path/file.txt"
        path = MyPath(rel_path)
        self.assertTrue(os.path.isabs(path.abspath))
        self.assertTrue(path.abspath.endswith(rel_path))
        
        # Test with absolute path
        abs_path = "/absolute/path/file.txt"
        path = MyPath(abs_path)
        self.assertEqual(path.abspath, abs_path)
        
        # Test with tilde expansion
        path = MyPath("~/file.txt")
        self.assertNotIn("~", path.abspath)
        self.assertTrue(os.path.isabs(path.abspath))

    def test_my_path_hash(self):
        """Test MyPath hash property."""
        path = MyPath(self.test_file_path)
        hash_value = path.hash
        self.assertIsInstance(hash_value, str)
        self.assertEqual(len(hash_value), 32)  # MD5 hash length

    def test_my_path_timezone(self):
        """Test MyPath timezone property."""
        path = MyPath(self.test_file_path)
        timezone = path.timezone
        self.assertEqual(str(timezone), "Asia/Shanghai")

    def test_my_path_timestamp(self):
        """Test MyPath timestamp property."""
        path = MyPath(self.test_file_path)
        timestamp = path.timestamp
        self.assertIsInstance(timestamp, (int, float))
        self.assertGreater(timestamp, 0)

    def test_my_path_timestr(self):
        """Test MyPath timestr property."""
        path = MyPath(self.test_file_path)
        timestr = path.timestr
        self.assertIsInstance(timestr, str)
        # Check format: YYYY-MM-DD HH:MM:SS
        self.assertRegex(timestr, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')

    def test_my_path_date(self):
        """Test MyPath date property."""
        path = MyPath(self.test_file_path)
        date = path.date
        self.assertIsInstance(date, str)
        self.assertEqual(len(date), 6)  # YYMMDD format
        self.assertTrue(date.isdigit())

    def test_my_path_time_of_a_day(self):
        """Test MyPath time_of_a_day property."""
        # Test different time periods with fixed timestamps
        # Based on the actual implementation in src/jinnang/path/path.py
        test_cases = [
            (0, 'Midnight'),
            (4, 'Midnight'),
            (5, 'Morning'),
            (11, 'Morning'),
            (12, 'Noon'),
            (13, 'Afternoon'),
            (16, 'Afternoon'),
            (17, 'Evening'),
            (20, 'Evening'),
            (21, 'Night'),
            (23, 'Night'),
        ]
        
        for hour, expected_period in test_cases:
            get_file_timestamp.cache_clear()
            fresh_path = MyPath(self.test_file_path)
            shanghai_tz = pytz.timezone('Asia/Shanghai')
            naive_dt = datetime(2023, 1, 1, hour, 0, 0)
            test_time = shanghai_tz.localize(naive_dt)
            with patch('jinnang.path.path.get_file_timestamp', return_value=test_time.timestamp()):
                MyPath.time_of_a_day.fget.cache_clear()
                returned_period = fresh_path.time_of_a_day
                self.assertEqual(returned_period, expected_period, 
                               f"Hour {hour} should return '{expected_period}' but got '{returned_period}'")

    def test_get_file_timestamp(self):
        """Test get_file_timestamp function."""
        timestamp = get_file_timestamp(self.test_file_path)
        self.assertIsInstance(timestamp, (int, float))
        self.assertGreater(timestamp, 0)
        
        # Test with non-existent file
        non_existent_path = "/path/that/does/not/exist.txt"
        timestamp = get_file_timestamp(non_existent_path)
        self.assertIsInstance(timestamp, (int, float))  # Should return current time



    def test_ensure_unique_path_decorator(self):
        """Test ensure_unique_path decorator."""
        # Create a function that returns a path
        @ensure_unique_path
        def get_path():
            return self.test_file_path
        
        # First call should return a modified path since the original exists
        unique_path = get_path()
        self.assertNotEqual(unique_path, self.test_file_path)
        self.assertTrue(unique_path.startswith(os.path.splitext(self.test_file_path)[0]))
        self.assertTrue(unique_path.endswith(os.path.splitext(self.test_file_path)[1]))
        self.assertIn("-1", unique_path)  # Should append -1 to make it unique
        
        # Create the file returned by the first call
        with open(unique_path, "w") as f:
            f.write("Another test file")
            
        try:
            # Second call should return a different path
            second_unique_path = get_path()
            self.assertNotEqual(second_unique_path, self.test_file_path)
            self.assertNotEqual(second_unique_path, unique_path)
            self.assertIn("-2", second_unique_path)  # Should append -2
        finally:
            # Clean up the additional file
            if os.path.exists(unique_path):
                os.remove(unique_path)

    def test_ensure_unique_path_with_none(self):
        """Test ensure_unique_path decorator with None return value."""
        @ensure_unique_path
        def get_none_path():
            return None
        
        result = get_none_path()
        self.assertIsNone(result)  # Should still return None


if __name__ == '__main__':
    unittest.main()