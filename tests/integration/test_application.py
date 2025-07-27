#!/usr/bin/env python3
"""Test main application with configuration dialog"""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("🚀 Testing Main Application...")
    
    try:
        # Test importing main components
        from gui.main_window import MainWindow
        from utils.yaml_config import YamlConfigManager
        
        print("   ✅ All imports successful!")
        
        # Test configuration manager
        config_manager = YamlConfigManager()
        config = config_manager.load_config()
        
        print("   ✅ Configuration loaded!")
        print(f"   📊 Config has {len(config)} top-level keys")
        
        # Test dual configurations
        dir_config = config_manager.get_directory_comparison_config()
        struct_config = config_manager.get_structure_comparison_config()
        
        print(f"   📁 Directory comparison: {len(dir_config.exclude_paths)} exclusions")
        print(f"   🌳 Structure comparison: {len(struct_config.exclude_paths)} exclusions")
        
        print("\n🎉 All components are working correctly!")
        print("   ℹ️  You can now run: python main.py")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💥 Application test failed!")
        sys.exit(1)
