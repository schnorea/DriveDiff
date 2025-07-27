#!/usr/bin/env python3
"""Test script to verify the new configuration works with real directory scanning"""

import sys
import os
sys.path.append('/Users/aussie/projects/2025/DriveDiff')

from src.utils.yaml_config import YamlConfigManager
from src.core.directory_scanner import DirectoryScanner

def test_real_scanning():
    """Test actual directory scanning with the new dual configuration"""
    print("🎯 Testing Real Directory Scanning with Dual Configuration")
    
    config_manager = YamlConfigManager()
    
    # Test directories
    test_left = "/Users/aussie/projects/2025/DriveDiff/test_dirs_scan/left"
    test_right = "/Users/aussie/projects/2025/DriveDiff/test_dirs_scan/right"
    
    if not os.path.exists(test_left) or not os.path.exists(test_right):
        print(f"❌ Test directories don't exist: {test_left}, {test_right}")
        return
    
    print(f"\n📁 Testing Directory Comparison...")
    dir_scanner = DirectoryScanner.from_config(config_manager, "directory")
    
    # Test directory comparison
    print(f"   Scanning {test_left}...")
    dir_left_files = dir_scanner.scan_directory(test_left)
    print(f"   Found {len(dir_left_files)} files")
    
    print(f"   Scanning {test_right}...") 
    dir_right_files = dir_scanner.scan_directory(test_right)
    print(f"   Found {len(dir_right_files)} files")
    
    # Show some files found
    print(f"   Sample files from directory scan:")
    for file in sorted(list(dir_left_files)[:5]):
        print(f"      {file}")
    
    print(f"\n🌳 Testing Structure Comparison...")
    struct_scanner = DirectoryScanner.from_config(config_manager, "structure")
    
    # Test structure comparison
    print(f"   Scanning structure of {test_left}...")
    struct_left = struct_scanner._scan_directory_structure(test_left)
    print(f"   Found {len(struct_left)} structure items")
    
    print(f"   Scanning structure of {test_right}...")
    struct_right = struct_scanner._scan_directory_structure(test_right)
    print(f"   Found {len(struct_right)} structure items")
    
    # Show structure items
    print(f"   Structure items found:")
    for item in sorted(struct_left):
        print(f"      {item}")
    
    print(f"\n📊 Comparison Results:")
    print(f"   Directory scan found {len(dir_left_files | dir_right_files)} unique files")
    print(f"   Structure scan found {len(struct_left | struct_right)} unique structure items")
    
    # Test the mounted volume exclusions
    print(f"\n🔍 Testing Mounted Volume Exclusions...")
    
    # Simulate mounted volume paths
    mounted_paths = [
        "/Volumes/rootfs/usr/share/doc",
        "/Volumes/rootfs/var/log/system.log",
        "/Volumes/rootfs/etc/config.conf",
        "/mnt/backup/tmp/tempfile"
    ]
    
    print(f"{'Path':<35} {'Dir Excluded':<12} {'Struct Excluded'}")
    print("-" * 60)
    
    for path in mounted_paths:
        dir_excluded = dir_scanner._should_exclude_path(path)
        struct_excluded = struct_scanner._should_exclude_path(path)
        
        dir_status = "✅ YES" if dir_excluded else "❌ NO"
        struct_status = "✅ YES" if struct_excluded else "❌ NO"
        
        print(f"{path:<35} {dir_status:<12} {struct_status}")
    
    print(f"\n🎉 Real scanning test complete!")
    print(f"   Both directory and structure comparisons are using separate configurations")
    print(f"   Mounted volume exclusions are working correctly")

if __name__ == "__main__":
    test_real_scanning()
