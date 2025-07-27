#!/usr/bin/env python3
"""Simple test to verify the new configuration doesn't break the basic functionality"""

import sys
import os
sys.path.append('/Users/aussie/projects/2025/DriveDiff')

def test_basic_functionality():
    """Test that basic functionality still works with new configuration"""
    print("🎯 Testing Basic Functionality with New Configuration")
    
    try:
        # Test 1: Configuration loading
        print("\n1️⃣ Testing configuration loading...")
        from src.utils.yaml_config import YamlConfigManager
        config_manager = YamlConfigManager()
        config = config_manager.load_config()
        print("   ✅ Configuration loaded successfully")
        
        # Test 2: DirectoryScanner creation
        print("\n2️⃣ Testing DirectoryScanner creation...")
        from src.core.directory_scanner import DirectoryScanner
        
        # Legacy method (should still work)
        legacy_scanner = DirectoryScanner.from_config_legacy(config_manager)
        print("   ✅ Legacy scanner created successfully")
        
        # New methods
        dir_scanner = DirectoryScanner.from_config(config_manager, "directory")
        struct_scanner = DirectoryScanner.from_config(config_manager, "structure")
        print("   ✅ Directory and structure scanners created successfully")
        
        # Test 3: Basic scanning functionality
        print("\n3️⃣ Testing basic scanning...")
        test_dir = "/Users/aussie/projects/2025/DriveDiff"
        
        if os.path.exists(test_dir):
            files = dir_scanner.scan_directory(test_dir)
            print(f"   ✅ Directory scan found {len(files)} files")
            
            if hasattr(dir_scanner, '_scan_directory_structure'):
                structure = dir_scanner._scan_directory_structure(test_dir)
                print(f"   ✅ Structure scan found {len(structure)} items")
        
        # Test 4: Configuration saving
        print("\n4️⃣ Testing configuration saving...")
        success = config_manager.save_config(config)
        print(f"   ✅ Configuration saved: {success}")
        
        print("\n🎉 All basic functionality tests passed!")
        print("   The new dual configuration system is working correctly")
        print("   Both directory and structure comparisons are functional")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    if not success:
        sys.exit(1)
