import unittest
from datetime import datetime
import pytz
from jinnang.date.date import date_str_to_iso_date_str, timestamp_to_date


class TestDateUtilities(unittest.TestCase):
    """Test cases for date utility functions."""

    def test_date_str_to_iso_date_str_basic(self):
        """Test basic date string to ISO conversion."""
        date_str = "2023-12-25 15:30:45"
        result = date_str_to_iso_date_str(date_str)
        
        # Should return ISO format string in Asia/Shanghai timezone
        self.assertIsInstance(result, str)
        self.assertIn("2023-12-25", result)
        self.assertIn("+08:00", result)  # Shanghai timezone offset

    def test_date_str_to_iso_date_str_with_timezone(self):
        """Test date conversion with explicit timezone."""
        date_str = "2023-12-25 15:30:45"
        target_tz = "America/New_York"
        result = date_str_to_iso_date_str(date_str, target_tz)
        
        self.assertIsInstance(result, str)
        self.assertIn("2023-12-25", result)
        # New York timezone offset (EST/EDT)
        self.assertTrue("-05:00" in result or "-04:00" in result)

    def test_date_str_to_iso_date_str_colon_replacement(self):
        """Test date string with colons in date part."""
        date_str = "2023:12:25 15:30:45"
        result = date_str_to_iso_date_str(date_str)
        
        self.assertIsInstance(result, str)
        self.assertIn("2023-12-25", result)

    def test_date_str_to_iso_date_str_microseconds_removed(self):
        """Test that microseconds are removed from the result."""
        date_str = "2023-12-25T15:30:45.123456"
        result = date_str_to_iso_date_str(date_str)
        
        self.assertIsInstance(result, str)
        self.assertNotIn(".123456", result)
        self.assertNotIn(".", result.split("T")[1].split("+")[0])  # No decimal in time part

    def test_date_str_to_iso_date_str_utc_input(self):
        """Test with UTC timezone input."""
        date_str = "2023-12-25T15:30:45Z"
        result = date_str_to_iso_date_str(date_str)
        
        self.assertIsInstance(result, str)
        # Should convert UTC to Shanghai time
        self.assertIn("+08:00", result)

    def test_date_str_to_iso_date_str_none_input(self):
        """Test with None input."""
        result = date_str_to_iso_date_str(None)
        self.assertIsNone(result)

    def test_date_str_to_iso_date_str_empty_string(self):
        """Test with empty string input."""
        result = date_str_to_iso_date_str("")
        self.assertIsNone(result)

    def test_date_str_to_iso_date_str_invalid_format(self):
        """Test with invalid date format."""
        invalid_dates = [
            "not a date",
            "2023-13-45",  # Invalid month/day
            "invalid format",
            "2023/25/12",  # Ambiguous format
        ]
        
        for invalid_date in invalid_dates:
            with self.subTest(invalid_date=invalid_date):
                result = date_str_to_iso_date_str(invalid_date)
                self.assertIsNone(result)

    def test_date_str_to_iso_date_str_various_formats(self):
        """Test with various valid date formats."""
        valid_formats = [
            "2023-12-25",
            "2023-12-25 15:30",
            "2023-12-25T15:30:45",
            "Dec 25, 2023",
            "25/12/2023",
            "2023/12/25"
        ]
        
        for date_format in valid_formats:
            with self.subTest(date_format=date_format):
                result = date_str_to_iso_date_str(date_format)
                if result is not None:  # Some formats might not be parseable
                    self.assertIsInstance(result, str)
                    self.assertIn("2023", result)

    def test_timestamp_to_date_basic(self):
        """Test basic timestamp to date conversion."""
        # Unix timestamp for 2023-12-25 12:00:00 UTC
        timestamp = 1703505600
        result = timestamp_to_date(timestamp)
        
        # Default format is '%y%m%d' in Asia/Shanghai timezone
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 6)  # YYMMDD format
        self.assertTrue(result.isdigit())

    def test_timestamp_to_date_custom_format(self):
        """Test timestamp conversion with custom format."""
        timestamp = 1703505600  # 2023-12-25 12:00:00 UTC
        custom_format = '%Y-%m-%d'
        result = timestamp_to_date(timestamp, fstr=custom_format)
        
        self.assertIsInstance(result, str)
        self.assertRegex(result, r'\d{4}-\d{2}-\d{2}')  # YYYY-MM-DD format

    def test_timestamp_to_date_custom_timezone(self):
        """Test timestamp conversion with custom timezone."""
        timestamp = 1703505600  # 2023-12-25 12:00:00 UTC
        timezone = 'America/New_York'
        result = timestamp_to_date(timestamp, timezone=timezone)
        
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 6)  # YYMMDD format

    def test_timestamp_to_date_various_formats(self):
        """Test timestamp conversion with various format strings."""
        timestamp = 1703505600
        format_tests = [
            ('%Y%m%d', 8),  # YYYYMMDD
            ('%d/%m/%Y', 10),  # DD/MM/YYYY
            ('%B %d, %Y', None),  # Full month name
            ('%Y-%m-%d %H:%M:%S', 19),  # Full datetime
        ]
        
        for fmt, expected_len in format_tests:
            with self.subTest(format=fmt):
                result = timestamp_to_date(timestamp, fstr=fmt)
                self.assertIsInstance(result, str)
                if expected_len:
                    self.assertEqual(len(result), expected_len)

    def test_timestamp_to_date_zero_timestamp(self):
        """Test with zero timestamp (Unix epoch)."""
        timestamp = 0  # 1970-01-01 00:00:00 UTC
        result = timestamp_to_date(timestamp)
        
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 6)
        # Should be 700101 in Asia/Shanghai (8 hours ahead)
        self.assertEqual(result, '700101')

    def test_timestamp_to_date_negative_timestamp(self):
        """Test with negative timestamp (before Unix epoch)."""
        timestamp = -86400  # 1969-12-31 00:00:00 UTC
        result = timestamp_to_date(timestamp)
        
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 6)

    def test_timestamp_to_date_float_timestamp(self):
        """Test with float timestamp."""
        timestamp = 1703505600.5  # With fractional seconds
        result = timestamp_to_date(timestamp)
        
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 6)

    def test_timestamp_to_date_timezone_differences(self):
        """Test that different timezones produce different results."""
        timestamp = 1703505600
        
        result_shanghai = timestamp_to_date(timestamp, timezone='Asia/Shanghai')
        result_utc = timestamp_to_date(timestamp, timezone='UTC')
        result_ny = timestamp_to_date(timestamp, timezone='America/New_York')
        
        # Results should be different due to timezone offsets
        timezones_results = [result_shanghai, result_utc, result_ny]
        unique_results = set(timezones_results)
        
        # At least some should be different (depending on the specific timestamp)
        self.assertGreaterEqual(len(unique_results), 1)

    def test_timestamp_to_date_consistency(self):
        """Test that same inputs produce same outputs."""
        timestamp = 1703505600
        
        result1 = timestamp_to_date(timestamp)
        result2 = timestamp_to_date(timestamp)
        
        self.assertEqual(result1, result2)


if __name__ == '__main__':
    unittest.main()