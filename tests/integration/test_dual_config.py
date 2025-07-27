#!/usr/bin/env python3
"""Test the new dual configuration system"""

import sys
import os
sys.path.append('/Users/aussie/projects/2025/DriveDiff')

from src.utils.yaml_config import YamlConfigManager
from src.core.directory_scanner import DirectoryScanner

def test_dual_configuration():
    """Test the new dual configuration system"""
    print("🎯 Testing Dual Configuration System")
    
    config_manager = YamlConfigManager()
    
    # Test configuration loading
    print("\n1️⃣ Testing configuration loading...")
    config = config_manager.load_config()
    
    print(f"   ✅ Configuration loaded successfully")
    print(f"   Has directory_comparison: {'directory_comparison' in config}")
    print(f"   Has structure_comparison: {'structure_comparison' in config}")
    
    # Test directory comparison configuration
    print("\n2️⃣ Testing directory comparison configuration...")
    dir_config = config_manager.get_directory_comparison_config()
    
    print(f"   Scan paths: {len(dir_config.scan_paths)}")
    print(f"   Exclude paths: {len(dir_config.exclude_paths)}")
    print(f"   Include patterns: {len(dir_config.include_patterns)}")
    print(f"   Exclude patterns: {len(dir_config.exclude_patterns)}")
    
    # Test structure comparison configuration
    print("\n3️⃣ Testing structure comparison configuration...")
    struct_config = config_manager.get_structure_comparison_config()
    
    print(f"   Scan paths: {len(struct_config.scan_paths)}")
    print(f"   Exclude paths: {len(struct_config.exclude_paths)}")
    print(f"   Include patterns: {len(struct_config.include_patterns)}")
    print(f"   Exclude patterns: {len(struct_config.exclude_patterns)}")
    
    # Test DirectoryScanner creation for both types
    print("\n4️⃣ Testing DirectoryScanner creation...")
    
    # Directory comparison scanner
    dir_scanner = DirectoryScanner.from_config(config_manager, "directory")
    print(f"   Directory scanner - exclude paths: {len(dir_scanner.exclude_paths)}")
    print(f"   Directory scanner - include patterns: {len(dir_scanner.include_patterns)}")
    
    # Structure comparison scanner
    struct_scanner = DirectoryScanner.from_config(config_manager, "structure")
    print(f"   Structure scanner - exclude paths: {len(struct_scanner.exclude_paths)}")
    print(f"   Structure scanner - include patterns: {len(struct_scanner.include_patterns)}")
    
    # Test exclusion differences
    print("\n5️⃣ Testing exclusion behavior differences...")
    
    test_paths = [
        "/Volumes/rootfs/usr/share",
        "/Volumes/rootfs/var/log",
        "/project/test.conf"
    ]
    
    print(f"{'Path':<30} {'Dir Excluded':<12} {'Struct Excluded':<15}")
    print("-" * 60)
    
    for path in test_paths:
        dir_excluded = dir_scanner._should_exclude_path(path)
        struct_excluded = struct_scanner._should_exclude_path(path)
        
        dir_status = "✅ YES" if dir_excluded else "❌ NO"
        struct_status = "✅ YES" if struct_excluded else "❌ NO"
        
        print(f"{path:<30} {dir_status:<12} {struct_status:<15}")
    
    # Test file filtering differences  
    print("\n6️⃣ Testing file filtering differences...")
    
    test_files = [
        "config.conf",
        "data.txt", 
        "binary.bin",
        "script.py"
    ]
    
    print(f"{'File':<15} {'Dir Included':<12} {'Struct Included':<15}")
    print("-" * 45)
    
    for filename in test_files:
        dir_included = dir_scanner._should_include_file("/test/" + filename)
        struct_included = struct_scanner._should_include_file("/test/" + filename)
        
        dir_status = "✅ YES" if dir_included else "❌ NO"
        struct_status = "✅ YES" if struct_included else "❌ NO"
        
        print(f"{filename:<15} {dir_status:<12} {struct_status:<15}")
    
    print(f"\n🎉 Dual configuration system test complete!")
    print(f"   Directory and structure comparisons now have separate configurations")
    print(f"   This allows different exclusion rules for different comparison types")

if __name__ == "__main__":
    test_dual_configuration()
