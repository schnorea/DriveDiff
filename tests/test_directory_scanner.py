"""
Test cases for DirectoryScanner class
"""

import unittest
import tempfile
import os
import shutil
from src.core.directory_scanner import DirectoryScanner, DirectoryComparison

class TestDirectoryScanner(unittest.TestCase):
    """Test cases for DirectoryScanner"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.scanner = DirectoryScanner()
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test directory structure
        self.left_dir = os.path.join(self.temp_dir, "left")
        self.right_dir = os.path.join(self.temp_dir, "right")
        
        os.makedirs(self.left_dir)
        os.makedirs(self.right_dir)
        
        # Create some test files
        # Common files
        with open(os.path.join(self.left_dir, "common.txt"), 'w') as f:
            f.write("Common file content")
        with open(os.path.join(self.right_dir, "common.txt"), 'w') as f:
            f.write("Common file content")
        
        # Modified file
        with open(os.path.join(self.left_dir, "modified.txt"), 'w') as f:
            f.write("Original content")
        with open(os.path.join(self.right_dir, "modified.txt"), 'w') as f:
            f.write("Modified content")
        
        # File only in left
        with open(os.path.join(self.left_dir, "only_left.txt"), 'w') as f:
            f.write("Only in left")
        
        # File only in right
        with open(os.path.join(self.right_dir, "only_right.txt"), 'w') as f:
            f.write("Only in right")
    
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_scan_directory(self):
        """Test directory scanning"""
        files = self.scanner.scan_directory(self.left_dir)
        
        self.assertIn("common.txt", files)
        self.assertIn("modified.txt", files)
        self.assertIn("only_left.txt", files)
        self.assertNotIn("only_right.txt", files)
    
    def test_scan_nonexistent_directory(self):
        """Test scanning non-existent directory"""
        nonexistent_dir = os.path.join(self.temp_dir, "nonexistent")
        files = self.scanner.scan_directory(nonexistent_dir)
        
        self.assertEqual(len(files), 0)
    
    def test_compare_directories(self):
        """Test directory comparison"""
        comparison = self.scanner.compare_directories(self.left_dir, self.right_dir)
        
        self.assertIsInstance(comparison, DirectoryComparison)
        self.assertIn("common.txt", comparison.identical_files)
        self.assertIn("modified.txt", comparison.modified_files)
        self.assertIn("only_left.txt", comparison.removed_files)
        self.assertIn("only_right.txt", comparison.added_files)
    
    def test_get_directory_summary(self):
        """Test directory summary"""
        summary = self.scanner.get_directory_summary(self.left_dir)
        
        self.assertTrue(summary['accessible'])
        self.assertEqual(summary['file_count'], 3)  # common.txt, modified.txt, only_left.txt
        self.assertGreater(summary['total_size'], 0)
    
    def test_cancel_comparison(self):
        """Test comparison cancellation"""
        self.scanner.cancel_comparison()
        self.assertTrue(self.scanner._cancel_requested)

if __name__ == '__main__':
    unittest.main()
