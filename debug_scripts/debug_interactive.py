#!/usr/bin/env python3
"""Interactive test to verify exclusions with user-specified directories"""

import sys
import os
sys.path.append('/Users/aussie/projects/2025/DriveDiff')

from src.utils.yaml_config import YamlConfigManager
from src.core.directory_scanner import DirectoryScanner

def test_user_directories():
    """Test exclusions with user-specified directories"""
    print("🎯 Interactive Directory Exclusion Test")
    print("This will test exclusions with directories you specify")
    
    # Load configuration
    config_manager = YamlConfigManager()
    scanner = DirectoryScanner.from_config(config_manager)
    
    print(f"\n📋 Current exclusion configuration:")
    print(f"   Exclude patterns: {len(scanner.exclude_paths)} patterns loaded")
    
    # Show some key patterns
    config = config_manager.load_config()
    key_patterns = [p for p in config['paths']['exclude_patterns'] if p in ['tmp', 'cache', 'node_modules', '.git', '__pycache__', 'venv']]
    print(f"   Key patterns: {key_patterns}")
    
    # Test with some common project directories
    test_directories = [
        "/Users/aussie/projects",
        "/Users/aussie/projects/2025",
        "/Users/aussie/projects/2025/DriveDiff",
        "/usr/local",
        "/tmp",
        "/var/cache"
    ]
    
    print(f"\n🔍 Testing structure scanning on common directories:")
    
    for test_dir in test_directories:
        if os.path.exists(test_dir) and os.path.isdir(test_dir):
            print(f"\n📁 Testing: {test_dir}")
            
            try:
                # Use the same method as the GUI
                structure = scanner._scan_directory_structure(test_dir)
                
                print(f"   📊 Found {len(structure)} items in structure")
                
                # Show first few items
                for item in sorted(structure)[:5]:
                    print(f"      📂 {item}")
                    
                if len(structure) > 5:
                    print(f"      ... and {len(structure) - 5} more items")
                
                # Check for potentially excluded items
                excluded_patterns = ['tmp', 'cache', 'node_modules', '.git', '__pycache__', 'venv', 'build', 'dist']
                found_excluded = []
                
                for item in structure:
                    for pattern in excluded_patterns:
                        if pattern in item.lower():
                            found_excluded.append(f"{item} (contains '{pattern}')")
                            break
                
                if found_excluded:
                    print(f"      ⚠️  Found potentially excluded items:")
                    for item in found_excluded[:3]:
                        print(f"         🔸 {item}")
                    if len(found_excluded) > 3:
                        print(f"         ... and {len(found_excluded) - 3} more")
                else:
                    print(f"      ✅ No excluded patterns found in structure")
                    
            except PermissionError:
                print(f"      ❌ Permission denied")
            except Exception as e:
                print(f"      ❌ Error: {e}")
        else:
            print(f"📁 {test_dir}: Does not exist or not accessible")

def manual_directory_test():
    """Allow manual testing of specific directories"""
    print(f"\n🔧 Manual Directory Testing")
    print("Enter directory paths to test (one per line, empty line to finish):")
    
    config_manager = YamlConfigManager()
    scanner = DirectoryScanner.from_config(config_manager)
    
    while True:
        try:
            path = input("Directory path (or press Enter to finish): ").strip()
            if not path:
                break
                
            if os.path.exists(path) and os.path.isdir(path):
                print(f"🔍 Scanning structure of: {path}")
                
                structure = scanner._scan_directory_structure(path)
                print(f"   📊 Structure contains {len(structure)} items")
                
                # Show all items if not too many
                if len(structure) <= 20:
                    for item in sorted(structure):
                        print(f"      📂 {item}")
                else:
                    for item in sorted(structure)[:10]:
                        print(f"      📂 {item}")
                    print(f"      ... and {len(structure) - 10} more items")
                    
            else:
                print(f"   ❌ Directory does not exist or is not accessible")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_user_directories()
    manual_directory_test()
