"""
Test cases for file utility functions
"""

import unittest
import tempfile
import os
import shutil
from src.utils.file_utils import (
    get_file_size_human, is_binary_file, get_file_type_description,
    validate_directory_path, get_directory_info, safe_copy_file
)

class TestFileUtils(unittest.TestCase):
    """Test cases for file utilities"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test files
        self.text_file = os.path.join(self.temp_dir, "test.txt")
        with open(self.text_file, 'w') as f:
            f.write("This is a text file")
        
        self.binary_file = os.path.join(self.temp_dir, "test.bin")
        with open(self.binary_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03\x04\x05')
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_get_file_size_human(self):
        """Test human-readable file size formatting"""
        self.assertEqual(get_file_size_human(0), "0 B")
        self.assertEqual(get_file_size_human(1023), "1023.0 B")
        self.assertEqual(get_file_size_human(1024), "1.0 KB")
        self.assertEqual(get_file_size_human(1048576), "1.0 MB")
    
    def test_is_binary_file(self):
        """Test binary file detection"""
        self.assertFalse(is_binary_file(self.text_file))
        self.assertTrue(is_binary_file(self.binary_file))
    
    def test_get_file_type_description(self):
        """Test file type description"""
        self.assertEqual(get_file_type_description(self.text_file), "Text file")
        self.assertEqual(get_file_type_description(self.binary_file), "Binary file")
        
        # Test non-existent file
        nonexistent = os.path.join(self.temp_dir, "nonexistent.txt")
        self.assertEqual(get_file_type_description(nonexistent), "File not found")
        
        # Test directory
        self.assertEqual(get_file_type_description(self.temp_dir), "Directory")
    
    def test_validate_directory_path(self):
        """Test directory path validation"""
        # Valid directory
        result = validate_directory_path(self.temp_dir)
        self.assertTrue(result['valid'])
        self.assertTrue(result['exists'])
        self.assertTrue(result['is_directory'])
        self.assertTrue(result['readable'])
        
        # Non-existent directory
        nonexistent = os.path.join(self.temp_dir, "nonexistent")
        result = validate_directory_path(nonexistent)
        self.assertFalse(result['valid'])
        self.assertFalse(result['exists'])
        
        # File instead of directory
        result = validate_directory_path(self.text_file)
        self.assertFalse(result['valid'])
        self.assertTrue(result['exists'])
        self.assertFalse(result['is_directory'])
        
        # Empty path
        result = validate_directory_path("")
        self.assertFalse(result['valid'])
    
    def test_get_directory_info(self):
        """Test directory information gathering"""
        info = get_directory_info(self.temp_dir)
        
        self.assertTrue(info['exists'])
        self.assertGreaterEqual(info['file_count'], 2)  # At least our test files
        self.assertGreater(info['total_size'], 0)
        self.assertIsNotNone(info['last_modified'])
        self.assertIsNotNone(info['permissions'])
    
    def test_safe_copy_file(self):
        """Test safe file copying"""
        dest_file = os.path.join(self.temp_dir, "copy.txt")
        
        result = safe_copy_file(self.text_file, dest_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(dest_file))
        
        # Read and compare content
        with open(self.text_file, 'r') as f1, open(dest_file, 'r') as f2:
            self.assertEqual(f1.read(), f2.read())

if __name__ == '__main__':
    unittest.main()
