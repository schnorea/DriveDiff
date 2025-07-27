#!/usr/bin/env python3
"""Test exclusions with realistic mounted volume scenario"""

import sys
import os
sys.path.append('/Users/aussie/projects/2025/DriveDiff')

from src.utils.yaml_config import YamlConfigManager
from src.core.directory_scanner import DirectoryScanner

def test_mounted_volume_scenario():
    """Test the exact scenario described by the user"""
    print("🎯 Testing Mounted Volume Scenario")
    print("Simulating comparison of /Volumes/rootfs vs /Volumes/backup")
    print("with exclusions like /usr/share configured")
    
    config_manager = YamlConfigManager()
    scanner = DirectoryScanner.from_config(config_manager)
    
    # Create a realistic test scenario
    left_base = "/Volumes/rootfs"
    right_base = "/Volumes/backup"
    
    # Test paths that would be found during structure scanning
    test_structure_paths = [
        # Paths that should be excluded
        (f"{left_base}/usr/share", True, "System directory"),
        (f"{left_base}/usr/share/doc", True, "System subdirectory"),  
        (f"{left_base}/tmp", True, "Temp directory"),
        (f"{left_base}/tmp/cache", True, "Temp subdirectory"),
        (f"{left_base}/var/cache", True, "Cache directory"),
        (f"{left_base}/var/cache/apt", True, "Cache subdirectory"),
        (f"{left_base}/proc", True, "Process directory"),
        (f"{left_base}/sys", True, "System directory"),
        (f"{left_base}/dev", True, "Device directory"),
        
        # Paths that should NOT be excluded
        (f"{left_base}/etc", False, "Config directory"),
        (f"{left_base}/usr/bin", False, "Binary directory"),
        (f"{left_base}/usr/local", False, "Local directory"),
        (f"{left_base}/home", False, "Home directory"),
        (f"{left_base}/opt", False, "Optional software"),
        
        # Right side (same logic should apply)
        (f"{right_base}/usr/share", True, "System directory"),
        (f"{right_base}/tmp", True, "Temp directory"),
        (f"{right_base}/var/cache", True, "Cache directory"),
        (f"{right_base}/etc", False, "Config directory"),
        (f"{right_base}/usr/bin", False, "Binary directory"),
    ]
    
    print(f"\n📋 Current exclusion configuration:")
    print(f"   Path exclusions: {len(scanner.exclude_paths)}")
    for path in scanner.exclude_paths[:5]:
        print(f"      {path}")
    if len(scanner.exclude_paths) > 5:
        print(f"      ... and {len(scanner.exclude_paths) - 5} more")
    
    print(f"\n🧪 Testing structure scanning exclusions:")
    print(f"{'Path':<50} {'Expected':<10} {'Actual':<10} {'Result':<8} {'Description'}")
    print("-" * 90)
    
    correct = 0
    total = 0
    
    for path, should_exclude, description in test_structure_paths:
        excluded = scanner._should_exclude_path(path)
        expected = "EXCLUDE" if should_exclude else "INCLUDE"
        actual = "EXCLUDE" if excluded else "INCLUDE"
        result = "✅ PASS" if (excluded == should_exclude) else "❌ FAIL"
        
        print(f"{path:<50} {expected:<10} {actual:<10} {result:<8} {description}")
        
        if excluded == should_exclude:
            correct += 1
        total += 1
    
    print(f"\n📊 Results: {correct}/{total} tests passed ({correct/total*100:.1f}%)")
    
    if correct == total:
        print("\n🎉 Perfect! Your mounted volume exclusion issue is resolved!")
        print("   The exclusions will now work correctly when comparing:")
        print("   • /Volumes/rootfs vs /Volumes/backup")
        print("   • /mnt/disk1 vs /mnt/disk2") 
        print("   • Any mounted volumes containing system directories")
        print("\n✨ Key improvements:")
        print("   • Patterns like /usr/share now match /Volumes/rootfs/usr/share")
        print("   • Subdirectories are properly excluded")
        print("   • Both path and pattern exclusions work together")
    else:
        print(f"\n⚠️  Still some issues to resolve")

if __name__ == "__main__":
    test_mounted_volume_scenario()
