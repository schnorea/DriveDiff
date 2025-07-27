#!/usr/bin/env python3
"""Test configuration loading without GUI"""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.yaml_config import YamlConfigManager

def main():
    print("🔧 Testing Configuration Loading...")
    
    try:
        # Initialize configuration manager
        config_manager = YamlConfigManager()
        
        print("   📋 Loading configuration...")
        config = config_manager.load_config()
        
        print("   ✅ Configuration loaded successfully!")
        print(f"   📊 Config keys: {list(config.keys())}")
        
        # Test dual configurations
        print("   🔄 Testing dual configurations...")
        dir_config = config_manager.get_directory_comparison_config()
        struct_config = config_manager.get_structure_comparison_config()
        
        print(f"   📁 Directory config paths: {len(dir_config.exclude_paths)} exclude paths")
        print(f"   🌳 Structure config paths: {len(struct_config.exclude_paths)} exclude paths")
        
        print("\n🎉 Configuration system is working correctly!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💥 Configuration test failed!")
        sys.exit(1)
