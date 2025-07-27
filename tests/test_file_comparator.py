"""
Test cases for FileComparator class
"""

import unittest
import tempfile
import os
from datetime import datetime
from src.core.file_comparator import FileComparator, FileInfo, FileDifference

class TestFileComparator(unittest.TestCase):
    """Test cases for FileComparator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.comparator = FileComparator()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test files
        self.test_file1 = os.path.join(self.temp_dir, "test1.txt")
        self.test_file2 = os.path.join(self.temp_dir, "test2.txt")
        self.test_file3 = os.path.join(self.temp_dir, "test3.txt")
        
        with open(self.test_file1, 'w') as f:
            f.write("Hello, world!\nThis is a test file.\n")
        
        with open(self.test_file2, 'w') as f:
            f.write("Hello, world!\nThis is a test file.\n")  # Identical to file1
        
        with open(self.test_file3, 'w') as f:
            f.write("Hello, world!\nThis is a different test file.\n")
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_get_file_info_existing_file(self):
        """Test getting file info for existing file"""
        file_info = self.comparator.get_file_info(self.test_file1)
        
        self.assertIsNotNone(file_info)
        self.assertEqual(file_info.path, self.test_file1)
        self.assertTrue(file_info.exists)
        self.assertGreater(file_info.size, 0)
        self.assertIsInstance(file_info.modified_time, datetime)
    
    def test_get_file_info_nonexistent_file(self):
        """Test getting file info for non-existent file"""
        nonexistent_file = os.path.join(self.temp_dir, "nonexistent.txt")
        file_info = self.comparator.get_file_info(nonexistent_file)
        
        self.assertIsNotNone(file_info)
        self.assertFalse(file_info.exists)
    
    def test_compare_identical_files(self):
        """Test comparing identical files"""
        diff = self.comparator.compare_files(self.test_file1, self.test_file2)
        
        self.assertEqual(diff.status, 'identical')
        self.assertIsNotNone(diff.left_info)
        self.assertIsNotNone(diff.right_info)
    
    def test_compare_different_files(self):
        """Test comparing different files"""
        diff = self.comparator.compare_files(self.test_file1, self.test_file3)
        
        self.assertEqual(diff.status, 'modified')
        self.assertIsNotNone(diff.left_info)
        self.assertIsNotNone(diff.right_info)
    
    def test_compare_with_missing_left_file(self):
        """Test comparing when left file is missing"""
        nonexistent_file = os.path.join(self.temp_dir, "missing.txt")
        diff = self.comparator.compare_files(nonexistent_file, self.test_file1)
        
        self.assertEqual(diff.status, 'added')
    
    def test_compare_with_missing_right_file(self):
        """Test comparing when right file is missing"""
        nonexistent_file = os.path.join(self.temp_dir, "missing.txt")
        diff = self.comparator.compare_files(self.test_file1, nonexistent_file)
        
        self.assertEqual(diff.status, 'removed')
    
    def test_is_text_file(self):
        """Test text file detection"""
        self.assertTrue(self.comparator._is_text_file(self.test_file1))
        
        # Create a binary file with more binary content
        binary_file = os.path.join(self.temp_dir, "binary.bin")
        with open(binary_file, 'wb') as f:
            # Write enough binary data to be detected as binary
            binary_data = bytes(range(256)) * 10  # 2560 bytes of binary data
            f.write(binary_data)
        
        self.assertFalse(self.comparator._is_text_file(binary_file))
    
    def test_get_text_diff(self):
        """Test text diff generation"""
        diff_lines = self.comparator.get_text_diff(self.test_file1, self.test_file3)
        
        self.assertIsNotNone(diff_lines)
        self.assertGreater(len(diff_lines), 0)
    
    def test_ignore_patterns(self):
        """Test ignore pattern functionality"""
        comparator = FileComparator(ignore_patterns=['*.tmp', '*.bak'])
        
        self.assertTrue(comparator.should_ignore_file('test.tmp'))
        self.assertTrue(comparator.should_ignore_file('backup.bak'))
        self.assertFalse(comparator.should_ignore_file('test.txt'))

if __name__ == '__main__':
    unittest.main()
