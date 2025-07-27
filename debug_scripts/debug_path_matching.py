#!/usr/bin/env python3
"""Test path exclusion matching with mounted volumes and different root paths"""

import sys
import os
sys.path.append('/Users/aussie/projects/2025/DriveDiff')

from src.utils.yaml_config import YamlConfigManager
from src.core.directory_scanner import DirectoryScanner

def test_path_matching_issue():
    """Test the path matching issue with mounted volumes"""
    print("🔍 Testing Path Exclusion Matching Issue")
    
    # Load current configuration
    config_manager = YamlConfigManager()
    scanner = DirectoryScanner.from_config(config_manager)
    
    print(f"\n📋 Current path exclusions:")
    for path in scanner.exclude_paths:
        print(f"   {path}")
    
    # Test different path scenarios
    test_cases = [
        # Standard root paths (what exclusions expect)
        "/usr/share",
        "/usr/share/doc", 
        "/tmp",
        "/var/cache",
        
        # Mounted volume paths (what you're actually comparing)
        "/Volumes/rootfs/usr/share",
        "/Volumes/rootfs/usr/share/doc",
        "/Volumes/rootfs/tmp", 
        "/Volumes/rootfs/var/cache",
        
        # Other common mounted scenarios
        "/mnt/disk1/usr/share",
        "/media/backup/var/cache",
        
        # Relative paths within comparison
        "usr/share",
        "var/cache",
        "tmp"
    ]
    
    print(f"\n🧪 Testing path exclusion matching:")
    print(f"{'Path':<40} {'Excluded?':<10} {'Reason'}")
    print("-" * 70)
    
    for test_path in test_cases:
        excluded = scanner._should_exclude_path(test_path)
        
        # Find which exclusion rule matched (if any)
        reason = "Enhanced exclusion logic"
        status = "✅ YES" if excluded else "❌ NO"
        print(f"{test_path:<40} {status:<10} {reason}")
    
    print(f"\n💡 Analysis:")
    print(f"   The issue is that path exclusions like '/usr/share' only match")
    print(f"   exact paths or paths that start with '/usr/share/'.")
    print(f"   ")
    print(f"   When comparing '/Volumes/rootfs/usr/share', it doesn't match")
    print(f"   because the full path is '/Volumes/rootfs/usr/share', not '/usr/share'.")

def test_pattern_vs_path_exclusions():
    """Test how patterns work vs path exclusions"""
    print(f"\n🎯 Testing Pattern vs Path Exclusions")
    
    config_manager = YamlConfigManager()
    config = config_manager.load_config()
    
    # Test with current configuration
    scanner = DirectoryScanner.from_config(config_manager)
    
    test_paths = [
        "/Volumes/rootfs/usr/share/doc/package",
        "/Volumes/rootfs/tmp/tempfile",
        "/mnt/backup/var/cache/data"
    ]
    
    print(f"\n🔍 Current behavior:")
    for path in test_paths:
        excluded_by_path = False
        excluded_by_pattern = False
        
        # Check path exclusions
        for exclude_path in scanner.exclude_paths:
            if path == exclude_path or path.startswith(exclude_path + "/"):
                excluded_by_path = True
                break
        
        # Test pattern exclusions  
        excluded_by_pattern = scanner._should_exclude_path(path)
        
        overall_excluded = scanner._should_exclude_path(path)
        
        print(f"   {path}")
        print(f"      Path exclusion:    {'✅' if excluded_by_path else '❌'}")
        print(f"      Pattern exclusion: {'✅' if excluded_by_pattern else '❌'}")
        print(f"      Overall excluded:  {'✅' if overall_excluded else '❌'}")

if __name__ == "__main__":
    test_path_matching_issue()
    test_pattern_vs_path_exclusions()
