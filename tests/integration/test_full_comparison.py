#!/usr/bin/env python3
"""
Test full structure comparison with exclusions
"""

import os
import sys
import tempfile
sys.path.insert(0, '/Users/aussie/projects/2025/DriveDiff')

from src.utils.yaml_config import YamlConfigManager
from src.core.directory_scanner import DirectoryScanner

def test_full_structure_comparison():
    print("🔍 Testing Full Structure Comparison with Exclusions")
    
    # Create two test directories with excluded content
    with tempfile.TemporaryDirectory() as temp_dir:
        left_dir = os.path.join(temp_dir, "left")
        right_dir = os.path.join(temp_dir, "right")
        
        # Create directory structure in left
        os.makedirs(os.path.join(left_dir, "src"))
        os.makedirs(os.path.join(left_dir, "tmp", "bad"))  # Should be excluded
        os.makedirs(os.path.join(left_dir, "cache"))       # Should be excluded
        os.makedirs(os.path.join(left_dir, "docs"))
        
        # Create directory structure in right  
        os.makedirs(os.path.join(right_dir, "src"))
        os.makedirs(os.path.join(right_dir, "node_modules", "pkg"))  # Should be excluded
        os.makedirs(os.path.join(right_dir, ".git", "objects"))     # Should be excluded
        os.makedirs(os.path.join(right_dir, "docs"))
        os.makedirs(os.path.join(right_dir, "build"))
        
        print(f"Created test directories:")
        print(f"  Left: {left_dir}")
        print(f"  Right: {right_dir}")
        
        # Load configuration and create scanner
        config_manager = YamlConfigManager()
        scanner = DirectoryScanner.from_config(config_manager)
        
        # Run structure comparison
        print(f"\n🧪 Running structure comparison...")
        structure_comparison = scanner.compare_structure(left_dir, right_dir)
        
        print(f"\nStructure comparison results:")
        print(f"  Common directories: {len(structure_comparison.common_directories)}")
        for d in sorted(structure_comparison.common_directories):
            print(f"    {d}")
        
        print(f"  Added directories (in right only): {len(structure_comparison.added_directories)}")
        for d in sorted(structure_comparison.added_directories):
            print(f"    {d}")
            
        print(f"  Removed directories (in left only): {len(structure_comparison.removed_directories)}")
        for d in sorted(structure_comparison.removed_directories):
            print(f"    {d}")
        
        # Check if any excluded directories appear in results
        all_found_dirs = (structure_comparison.common_directories + 
                         structure_comparison.added_directories + 
                         structure_comparison.removed_directories)
        
        excluded_dirs_found = []
        for d in all_found_dirs:
            if any(excluded in d.lower() for excluded in ['tmp', 'cache', 'node_modules', '.git']):
                excluded_dirs_found.append(d)
        
        if excluded_dirs_found:
            print(f"\n❌ Found excluded directories in results:")
            for d in excluded_dirs_found:
                print(f"    {d}")
        else:
            print(f"\n✅ No excluded directories found in structure comparison results!")
            print(f"✅ Path exclusions are working correctly for structure comparison!")

if __name__ == "__main__":
    test_full_structure_comparison()
