#!/usr/bin/env python3
"""
Simple test script to debug structure scanning exclusions
"""

import os
import sys
sys.path.insert(0, '/Users/aussie/projects/2025/DriveDiff')

from src.utils.yaml_config import YamlConfigManager
from src.core.directory_scanner import DirectoryScanner

def test_exclusions():
    print("Testing structure scanning exclusions...")
    
    # Load configuration
    config_manager = YamlConfigManager()
    scanner = DirectoryScanner.from_config(config_manager)
    
    print(f"Exclude patterns: {scanner.ignore_patterns}")
    print(f"Exclude paths: {scanner.exclude_paths}")
    
    # Test specific paths
    test_cases = [
        "tmp",
        "tmp/should_be_excluded", 
        "normal_dir",
        "left/subdir"
    ]
    
    print("\nTesting individual path exclusions:")
    for test_path in test_cases:
        full_path = os.path.join("test_dirs", test_path)
        path_excluded = scanner._should_exclude_path(full_path, "test_dirs")
        pattern_excluded = scanner._should_ignore_file(test_path)
        print(f"  {test_path}: path_excluded={path_excluded}, pattern_excluded={pattern_excluded}")
    
    # Test structure scanning
    print(f"\nScanning test_dirs structure...")
    structure = scanner._scan_directory_structure("test_dirs")
    print(f"Found {len(structure)} directories:")
    for d in sorted(structure):
        print(f"  {d}")
    
    # Check if any should have been excluded
    print(f"\nChecking results against exclusion rules:")
    for d in sorted(structure):
        full_path = os.path.join("test_dirs", d)
        path_excluded = scanner._should_exclude_path(full_path, "test_dirs") 
        pattern_excluded = scanner._should_ignore_file(d)
        if path_excluded or pattern_excluded:
            print(f"  ❌ {d} should have been excluded!")
        else:
            print(f"  ✅ {d} correctly included")

if __name__ == "__main__":
    test_exclusions()
