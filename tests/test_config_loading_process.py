#!/usr/bin/env python3
"""Test configuration loading specifically"""

import os
import sys
import tkinter as tk
import shutil

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.config_dialog import ConfigurationDialog
from utils.yaml_config import YamlConfigManager

def main():
    print("🔧 Testing Configuration Loading Process...")
    
    try:
        # Create root window but don't show it
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        # Initialize configuration manager
        config_manager = YamlConfigManager()
        
        print("   📋 Creating configuration dialog...")
        dialog = ConfigurationDialog(root, config_manager)
        
        print("   ✅ Configuration dialog created successfully!")
        
        # Test initial YAML loading
        print("   🔄 Testing initial YAML editor content...")
        initial_yaml = dialog.yaml_editor.get(1.0, tk.END)
        print(f"   📄 Initial YAML length: {len(initial_yaml)} characters")
        
        # Test importing NEW_CONFIG.yml
        print("   📂 Testing import of NEW_CONFIG.yml...")
        if os.path.exists("NEW_CONFIG.yml"):
            # Simulate the import process that happens in _load_from_file
            imported_config = config_manager.import_config("NEW_CONFIG.yml")
            
            if imported_config:
                print("   ✅ NEW_CONFIG.yml imported successfully!")
                
                # Simulate the configuration loading process
                dialog.current_config = imported_config
                dialog._load_configuration()
                
                # Check the YAML editor content after loading
                loaded_yaml = dialog.yaml_editor.get(1.0, tk.END)
                print(f"   📄 Loaded YAML length: {len(loaded_yaml)} characters")
                
                # Check if the content actually changed
                if loaded_yaml != initial_yaml:
                    print("   ✅ YAML editor content updated successfully!")
                    
                    # Show a snippet of the loaded YAML
                    lines = loaded_yaml.strip().split('\n')
                    print("   📝 First few lines of loaded YAML:")
                    for i, line in enumerate(lines[:5]):
                        print(f"      {i+1}: {line}")
                else:
                    print("   ⚠️  YAML editor content didn't change")
                    
            else:
                print("   ❌ Failed to import NEW_CONFIG.yml")
        else:
            print("   ⚠️  NEW_CONFIG.yml not found, skipping import test")
        
        # Clean up
        root.destroy()
        
        print("\n🎉 Configuration loading test completed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💥 Configuration loading test failed!")
        sys.exit(1)
