#!/usr/bin/env python3
"""Test configuration dialog and verify it saves exclusions properly"""

import sys
import os
sys.path.append('/Users/aussie/projects/2025/DriveDiff')

from src.utils.yaml_config import YamlConfigManager
from src.core.directory_scanner import DirectoryScanner

def test_config_persistence():
    """Test if configuration changes are properly saved and loaded"""
    print("🔧 Testing Configuration Persistence")
    
    config_manager = YamlConfigManager()
    
    # Load current config
    print("\n1️⃣ Loading current configuration...")
    config = config_manager.load_config()
    
    original_patterns = config['paths']['exclude_patterns'].copy()
    original_paths = config['paths']['exclude'].copy()
    
    print(f"   Current exclude patterns: {len(original_patterns)}")
    print(f"   Current exclude paths: {len(original_paths)}")
    
    # Add a test pattern
    test_pattern = "TEST_EXCLUSION_PATTERN_UNIQUE_12345"
    
    print(f"\n2️⃣ Adding test pattern: {test_pattern}")
    config['paths']['exclude_patterns'].append(test_pattern)
    
    # Save config
    print("\n3️⃣ Saving configuration...")
    config_manager.save_config(config)
    
    # Reload config to verify persistence
    print("\n4️⃣ Reloading configuration...")
    config_manager = YamlConfigManager()  # Fresh instance
    reloaded_config = config_manager.load_config()
    
    # Check if test pattern persisted
    if test_pattern in reloaded_config['paths']['exclude_patterns']:
        print(f"   ✅ Test pattern persisted in configuration")
    else:
        print(f"   ❌ Test pattern NOT found in reloaded configuration")
        print(f"   Current patterns: {reloaded_config['paths']['exclude_patterns']}")
    
    # Test DirectoryScanner creation
    print("\n5️⃣ Testing DirectoryScanner creation...")
    scanner = DirectoryScanner.from_config(config_manager)
    
    # Test exclusion
    test_excluded = scanner._should_ignore_file(test_pattern)
    if test_excluded:
        print(f"   ✅ DirectoryScanner correctly excludes test pattern")
    else:
        print(f"   ❌ DirectoryScanner does NOT exclude test pattern")
    
    # Clean up - restore original configuration
    print("\n6️⃣ Restoring original configuration...")
    config['paths']['exclude_patterns'] = original_patterns
    config['paths']['exclude'] = original_paths
    config_manager.save_config(config)
    
    print("✅ Configuration persistence test complete")

def check_actual_directories():
    """Check what directories exist in the user's actual scan targets"""
    print("\n🔍 Checking Actual Directories")
    
    config_manager = YamlConfigManager()
    config = config_manager.load_config()
    
    # Check if user has set scan paths
    scan_paths = config.get('paths', {}).get('scan_paths', [])
    
    if scan_paths:
        print(f"Found {len(scan_paths)} scan paths in configuration:")
        for path in scan_paths:
            print(f"   {path}")
            
            if os.path.exists(path):
                print(f"   📁 Checking contents of {path}:")
                
                try:
                    # List immediate subdirectories
                    items = []
                    for item in os.listdir(path):
                        item_path = os.path.join(path, item)
                        if os.path.isdir(item_path):
                            items.append(item)
                    
                    # Show first 10 directories
                    for item in sorted(items)[:10]:
                        print(f"      📂 {item}")
                    
                    if len(items) > 10:
                        print(f"      ... and {len(items) - 10} more directories")
                        
                    # Check for common excludable patterns
                    excludable = ['tmp', 'cache', 'node_modules', '.git', '__pycache__', 'venv', 'build', 'dist']
                    found_excludable = [item for item in items if item in excludable or any(exc in item.lower() for exc in excludable)]
                    
                    if found_excludable:
                        print(f"      🎯 Found excludable directories: {found_excludable}")
                    else:
                        print(f"      ✅ No obvious excludable directories found")
                        
                except PermissionError:
                    print(f"      ❌ Permission denied accessing {path}")
                except Exception as e:
                    print(f"      ❌ Error accessing {path}: {e}")
            else:
                print(f"   ❌ Path does not exist: {path}")
    else:
        print("No scan paths configured - this might be why exclusions seem to not work")
        print("If no scan paths are set, the directory comparison uses the paths you select in the GUI")

if __name__ == "__main__":
    test_config_persistence()
    check_actual_directories()
