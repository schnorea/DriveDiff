#!/usr/bin/env python3
"""Comprehensive test of the enhanced exclusion system"""

import sys
import os
sys.path.append('/Users/aussie/projects/2025/DriveDiff')

from src.utils.yaml_config import YamlConfigManager
from src.core.directory_scanner import DirectoryScanner

def test_exclusion_comprehensive():
    """Test the enhanced exclusion system comprehensively"""
    print("🎯 Comprehensive Exclusion Test")
    
    config_manager = YamlConfigManager()
    scanner = DirectoryScanner.from_config(config_manager)
    
    # Test cases that should be excluded
    should_be_excluded = [
        # Standard system paths
        "/usr/share",
        "/usr/share/doc",
        "/usr/share/doc/package",
        "/tmp",
        "/tmp/file.txt",
        "/var/cache",
        "/var/cache/data.db",
        
        # Mounted volume system paths  
        "/Volumes/rootfs/usr/share",
        "/Volumes/rootfs/usr/share/doc",
        "/Volumes/rootfs/usr/share/doc/package",
        "/Volumes/rootfs/tmp",
        "/Volumes/rootfs/tmp/file.txt",
        "/Volumes/rootfs/var/cache",
        "/Volumes/rootfs/var/cache/data.db",
        
        # Other mount points
        "/mnt/backup/usr/share",
        "/mnt/backup/var/cache",
        "/media/disk/tmp",
        
        # Pattern-based exclusions
        "/some/path/node_modules",
        "/project/node_modules/package",
        "/app/.git",
        "/app/.git/config",
        "/code/__pycache__",
        "/code/__pycache__/file.pyc",
    ]
    
    # Test cases that should NOT be excluded
    should_not_be_excluded = [
        "/usr/bin",
        "/usr/local/bin",
        "/home/user",
        "/etc/config.conf",
        "/var/log/app.log",
        "/Volumes/rootfs/etc",
        "/Volumes/rootfs/usr/bin",
        "/mnt/backup/home",
        "/project/src",
        "/app/main.py",
    ]
    
    print("\n✅ Testing paths that SHOULD be excluded:")
    excluded_correctly = 0
    for path in should_be_excluded:
        excluded = scanner._should_exclude_path(path)
        status = "✅" if excluded else "❌"
        print(f"   {status} {path}")
        if excluded:
            excluded_correctly += 1
    
    print(f"\n📊 Exclusion Results: {excluded_correctly}/{len(should_be_excluded)} correctly excluded")
    
    print("\n✅ Testing paths that should NOT be excluded:")
    not_excluded_correctly = 0
    for path in should_not_be_excluded:
        excluded = scanner._should_exclude_path(path)
        status = "✅" if not excluded else "❌" 
        print(f"   {status} {path}")
        if not excluded:
            not_excluded_correctly += 1
    
    print(f"\n📊 Inclusion Results: {not_excluded_correctly}/{len(should_not_be_excluded)} correctly included")
    
    total_correct = excluded_correctly + not_excluded_correctly
    total_tests = len(should_be_excluded) + len(should_not_be_excluded)
    
    print(f"\n🎯 Overall Results: {total_correct}/{total_tests} tests passed ({total_correct/total_tests*100:.1f}%)")
    
    if total_correct == total_tests:
        print("🎉 All exclusion tests passed! The mounted volume issue should be resolved.")
    else:
        print("⚠️  Some tests failed. The exclusion logic may need further refinement.")

if __name__ == "__main__":
    test_exclusion_comprehensive()
