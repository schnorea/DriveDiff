#!/usr/bin/env python3
"""Debug script to mimic exactly what the GUI does for structure comparison"""

import sys
import os
sys.path.append('/Users/aussie/projects/2025/DriveDiff')

from src.utils.yaml_config import YamlConfigManager
from src.core.directory_scanner import DirectoryScanner

def test_gui_structure_comparison():
    """Test the exact sequence that the GUI uses for structure comparison"""
    print("🎯 Testing GUI Structure Comparison Sequence")
    
    # Step 1: Load configuration (like ConfigDialog does)
    print("\n1️⃣ Loading configuration...")
    config_manager = YamlConfigManager()
    config = config_manager.load_config()
    
    print(f"   ✅ Loaded {len(config['paths']['exclude_patterns'])} exclude patterns")
    print(f"   ✅ Loaded {len(config['paths']['exclude'])} exclude paths")
    
    # Step 2: Create DirectoryScanner from config (like main_window does on line 392)
    print("\n2️⃣ Creating DirectoryScanner from config...")
    scanner = DirectoryScanner.from_config(config_manager)
    
    # Verify exclusions are loaded
    print(f"   ✅ Scanner has {len(scanner.exclude_paths)} exclude paths")
    print(f"   ✅ First few patterns: {list(scanner.exclude_paths)[:3]}")
    
    # Step 3: Set paths (like the GUI does)
    test_left = "/Users/aussie/projects/2025/DriveDiff/test_dirs_scan/left"
    test_right = "/Users/aussie/projects/2025/DriveDiff/test_dirs_scan/right"
    
    if not os.path.exists(test_left) or not os.path.exists(test_right):
        print(f"❌ Test directories don't exist: {test_left}, {test_right}")
        return
    
    print(f"\n3️⃣ Setting comparison paths...")
    print(f"   Left:  {test_left}")
    print(f"   Right: {test_right}")
    
    # Step 4: Run structure comparison (like _compare_structure does)
    print("\n4️⃣ Running structure comparison...")
    
    try:
        # This is the exact call from main_window.py line 394
        left_structure = scanner._scan_directory_structure(test_left)
        right_structure = scanner._scan_directory_structure(test_right)
        
        print(f"\n📊 Structure Comparison Results:")
        print(f"   Left structure:  {len(left_structure)} items")
        print(f"   Right structure: {len(right_structure)} items")
        
        print(f"\n📁 Left structure contents:")
        for item in sorted(left_structure):
            print(f"   {item}")
            
        print(f"\n📁 Right structure contents:")
        for item in sorted(right_structure):
            print(f"   {item}")
            
        # Test specific exclusion cases
        print(f"\n🔍 Checking for excluded items:")
        
        # Check if any excluded patterns are present
        excluded_found = []
        all_items = set(left_structure) | set(right_structure)
        
        test_patterns = ['tmp', 'cache', 'node_modules', '.git', '__pycache__']
        for pattern in test_patterns:
            found_items = [item for item in all_items if pattern in item.lower()]
            if found_items:
                excluded_found.extend(found_items)
                print(f"   ❌ Found {pattern}: {found_items}")
            else:
                print(f"   ✅ {pattern}: correctly excluded")
        
        if excluded_found:
            print(f"\n❌ PROBLEM: Found {len(excluded_found)} items that should be excluded!")
            print("   This means exclusions are NOT working in structure comparison")
        else:
            print(f"\n✅ SUCCESS: No excluded items found in structure comparison")
            print("   Exclusions are working correctly")
            
    except Exception as e:
        print(f"❌ Error during structure comparison: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gui_structure_comparison()
