#!/usr/bin/env python3
"""
Debug structure comparison exclusions
"""

import os
import sys
sys.path.insert(0, '/Users/aussie/projects/2025/DriveDiff')

from src.utils.yaml_config import YamlConfigManager
from src.core.directory_scanner import DirectoryScanner

def debug_structure_exclusions():
    print("🔍 Debugging Structure Comparison Exclusions")
    
    # Load configuration
    config_manager = YamlConfigManager()
    scanner = DirectoryScanner.from_config(config_manager)
    
    print(f"Configuration loaded:")
    print(f"  exclude_paths: {scanner.exclude_paths}")
    print(f"  ignore_patterns: {scanner.ignore_patterns}")
    print(f"  scan_paths: {scanner.scan_paths}")
    
    # Create test directory structure with excluded items
    test_dir = "test_dirs"
    print(f"\nCurrent structure in {test_dir}:")
    for root, dirs, files in os.walk(test_dir):
        level = root.replace(test_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
    
    # Test structure scanning
    print(f"\n🧪 Testing structure scanning on {test_dir}...")
    structure = scanner._scan_directory_structure(test_dir)
    print(f"Structure scan found {len(structure)} directories:")
    for d in sorted(structure):
        print(f"  {d}")
    
    # Test if directories should be excluded
    print(f"\n🔍 Checking exclusion logic for each found directory:")
    for d in sorted(structure):
        full_path = os.path.join(test_dir, d)
        
        # Test path exclusion
        path_excluded = scanner._should_exclude_path(full_path, test_dir)
        
        # Test pattern exclusion
        pattern_excluded = scanner._should_ignore_file(d)
        
        # Test directory name exclusion
        dir_excluded = scanner._should_ignore_directory(os.path.basename(d))
        
        status = "✅ included"
        if path_excluded:
            status = "❌ EXCLUDED BY PATH"
        elif pattern_excluded:
            status = "❌ EXCLUDED BY PATTERN"
        elif dir_excluded:
            status = "❌ EXCLUDED BY DIRECTORY"
        
        print(f"  {d}: {status}")
        if path_excluded or pattern_excluded or dir_excluded:
            print(f"    path_excluded={path_excluded}, pattern_excluded={pattern_excluded}, dir_excluded={dir_excluded}")

if __name__ == "__main__":
    debug_structure_exclusions()
