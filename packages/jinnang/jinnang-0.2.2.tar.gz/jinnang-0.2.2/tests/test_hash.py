import unittest
import tempfile
import os
from jinnang.common.hash import stable_hash, md5, partial_file_hash


class TestHashFunctions(unittest.TestCase):
    """Test cases for hash utility functions."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file_path = os.path.join(self.temp_dir, "test_file.txt")
        
    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        os.rmdir(self.temp_dir)

    def test_stable_hash_consistency(self):
        """Test that stable_hash produces consistent results for the same input."""
        test_obj = {"key": "value", "number": 42}
        hash1 = stable_hash(test_obj)
        hash2 = stable_hash(test_obj)
        self.assertEqual(hash1, hash2)
        self.assertIsInstance(hash1, str)
        self.assertEqual(len(hash1), 32)  # MD5 hash length
        
    def test_stable_hash_different_inputs(self):
        """Test that different inputs produce different hashes."""
        obj1 = {"key": "value"}
        obj2 = {"key": "different_value"}
        obj3 = {"different_key": "value"}
        
        hash1 = stable_hash(obj1)
        hash2 = stable_hash(obj2)
        hash3 = stable_hash(obj3)
        
        self.assertNotEqual(hash1, hash2)
        self.assertNotEqual(hash1, hash3)
        self.assertNotEqual(hash2, hash3)
        
    def test_stable_hash_various_types(self):
        """Test stable_hash with various data types."""
        test_cases = [
            "string",
            42,
            [1, 2, 3],
            ("tuple", "data"),
            {"nested": {"dict": "value"}},
            None
        ]
        
        hashes = []
        for case in test_cases:
            hash_result = stable_hash(case)
            self.assertIsInstance(hash_result, str)
            self.assertEqual(len(hash_result), 32)
            hashes.append(hash_result)
            
        # All hashes should be unique
        self.assertEqual(len(hashes), len(set(hashes)))
        
    def test_md5_file_hash(self):
        """Test MD5 hash calculation for files."""
        # Create a test file with known content
        test_content = b"Hello, World!"
        with open(self.test_file_path, "wb") as f:
            f.write(test_content)
            
        # Calculate hash
        file_hash = md5(self.test_file_path)
        
        # Known MD5 hash for "Hello, World!"
        expected_hash = "65a8e27d8879283831b664bd8b7f0ad4"
        self.assertEqual(file_hash, expected_hash)
        
    def test_md5_empty_file(self):
        """Test MD5 hash for empty file."""
        # Create empty file
        with open(self.test_file_path, "wb") as f:
            pass
            
        file_hash = md5(self.test_file_path)
        # MD5 hash of empty file
        expected_hash = "d41d8cd98f00b204e9800998ecf8427e"
        self.assertEqual(file_hash, expected_hash)
        
    def test_md5_large_file(self):
        """Test MD5 hash for larger file."""
        # Create a larger test file
        test_content = b"A" * 10000  # 10KB of 'A's
        with open(self.test_file_path, "wb") as f:
            f.write(test_content)
            
        file_hash = md5(self.test_file_path)
        self.assertIsInstance(file_hash, str)
        self.assertEqual(len(file_hash), 32)
        
    def test_partial_file_hash_small_file(self):
        """Test partial hash for small files (should read entire file)."""
        test_content = b"Small file content"
        with open(self.test_file_path, "wb") as f:
            f.write(test_content)
            
        partial_hash = partial_file_hash(self.test_file_path)
        full_hash = md5(self.test_file_path)
        
        # For small files, partial hash should equal full hash
        self.assertEqual(partial_hash, full_hash)
        
    def test_partial_file_hash_large_file(self):
        """Test partial hash for large files."""
        # Create a large file (>12KB to trigger partial reading)
        test_content = b"A" * 5000 + b"B" * 5000 + b"C" * 5000  # 15KB
        with open(self.test_file_path, "wb") as f:
            f.write(test_content)
            
        partial_hash = partial_file_hash(self.test_file_path)
        full_hash = md5(self.test_file_path)
        
        # Partial hash should be different from full hash for large files
        self.assertNotEqual(partial_hash, full_hash)
        self.assertIsInstance(partial_hash, str)
        self.assertEqual(len(partial_hash), 32)
        
    def test_partial_file_hash_custom_chunk_size(self):
        """Test partial hash with custom chunk size."""
        test_content = b"Custom chunk size test content" * 1000
        with open(self.test_file_path, "wb") as f:
            f.write(test_content)
            
        hash1 = partial_file_hash(self.test_file_path, chunk_size=1024)
        hash2 = partial_file_hash(self.test_file_path, chunk_size=2048)
        
        # Different chunk sizes should produce different hashes
        self.assertNotEqual(hash1, hash2)
        
    def test_file_not_found_error(self):
        """Test that functions raise appropriate errors for non-existent files."""
        non_existent_path = "/path/that/does/not/exist.txt"
        
        with self.assertRaises(FileNotFoundError):
            md5(non_existent_path)
            
        with self.assertRaises(FileNotFoundError):
            partial_file_hash(non_existent_path)


if __name__ == '__main__':
    unittest.main()