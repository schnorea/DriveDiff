#!/usr/bin/env python3

import sys
import os

# Add src to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Change working directory to src for relative imports
original_cwd = os.getcwd()
os.chdir(src_path)

try:
    from core.directory_scanner import DirectoryScanner
    from core.file_comparator import FileComparator
finally:
    # Restore working directory
    os.chdir(original_cwd)

def test_structure_comparison():
    print("Testing structure comparison...")
    
    # Create scanner
    file_comparator = FileComparator()
    scanner = DirectoryScanner(file_comparator)
    
    # Test directories
    left_dir = os.path.join(os.path.dirname(__file__), 'test_dirs/left')
    right_dir = os.path.join(os.path.dirname(__file__), 'test_dirs/right')
    
    print(f"Left dir: {left_dir}")
    print(f"Right dir: {right_dir}")
    print(f"Left exists: {os.path.exists(left_dir)}")
    print(f"Right exists: {os.path.exists(right_dir)}")
    
    # Run structure comparison
    result = scanner.compare_structure(left_dir, right_dir)
    
    print(f"\nResults:")
    print(f"Added paths: {result.added_paths}")
    print(f"Removed paths: {result.removed_paths}")
    print(f"Common files: {result.common_files}")
    print(f"Common directories: {result.common_directories}")
    print(f"Total paths: {result.total_paths}")

if __name__ == "__main__":
    test_structure_comparison()
