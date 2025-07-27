#!/usr/bin/env python3
"""Enhanced test to debug YAML loading"""

import os
import sys
import tkinter as tk
import shutil

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.config_dialog import ConfigurationDialog
from utils.yaml_config import YamlConfigManager

def main():
    print("🔧 Enhanced Configuration Loading Debug...")
    
    try:
        # Create root window but don't show it
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        # Initialize configuration manager
        config_manager = YamlConfigManager()
        
        print("   📋 Creating configuration dialog...")
        dialog = ConfigurationDialog(root, config_manager)
        
        print("   ✅ Configuration dialog created successfully!")
        
        # Get initial states
        print("   🔍 Examining initial state...")
        initial_config = dialog.current_config.copy()
        initial_yaml = dialog.yaml_editor.get(1.0, tk.END)
        print(f"   📄 Initial config keys: {list(initial_config.keys())}")
        print(f"   📄 Initial YAML length: {len(initial_yaml)} characters")
        
        # Test importing NEW_CONFIG.yml
        print("   📂 Testing import of NEW_CONFIG.yml...")
        if os.path.exists("NEW_CONFIG.yml"):
            # Load the file manually to compare
            with open("NEW_CONFIG.yml", 'r') as f:
                file_content = f.read()
            print(f"   📄 File content length: {len(file_content)} characters")
            
            # Import via config manager
            imported_config = config_manager.import_config("NEW_CONFIG.yml")
            
            if imported_config:
                print("   ✅ NEW_CONFIG.yml imported successfully!")
                print(f"   📄 Imported config keys: {list(imported_config.keys())}")
                
                # Update dialog state
                old_config = dialog.current_config.copy()
                dialog.current_config = imported_config
                
                print("   🔄 Calling _load_configuration()...")
                dialog._load_configuration()
                
                # Check the YAML editor content after loading
                loaded_yaml = dialog.yaml_editor.get(1.0, tk.END)
                print(f"   📄 Loaded YAML length: {len(loaded_yaml)} characters")
                
                # Compare configs
                print("   🔍 Comparing configurations...")
                config_changed = old_config != imported_config
                yaml_changed = loaded_yaml != initial_yaml
                
                print(f"   📊 Config changed: {config_changed}")
                print(f"   📊 YAML changed: {yaml_changed}")
                
                # Show differences if any
                if config_changed:
                    print("   📝 Configuration differences found")
                    old_keys = set(old_config.keys())
                    new_keys = set(imported_config.keys())
                    print(f"   🔑 Old keys: {old_keys}")
                    print(f"   🔑 New keys: {new_keys}")
                
                if yaml_changed:
                    print("   📝 YAML content changed successfully!")
                    # Show first few lines of each
                    print("   📄 First few lines of initial YAML:")
                    for i, line in enumerate(initial_yaml.strip().split('\n')[:3]):
                        print(f"      {i+1}: {line}")
                    print("   📄 First few lines of loaded YAML:")
                    for i, line in enumerate(loaded_yaml.strip().split('\n')[:3]):
                        print(f"      {i+1}: {line}")
                else:
                    print("   ⚠️  YAML editor content identical")
                    # Check if the yaml formatter is working
                    print("   🔍 Testing yaml formatter directly...")
                    test_yaml = config_manager._format_yaml_for_display(imported_config)
                    print(f"   📄 Formatter output length: {len(test_yaml)} characters")
                    
                    # Compare with initial
                    formatter_different = test_yaml != initial_yaml
                    print(f"   📊 Formatter output different: {formatter_different}")
                    
            else:
                print("   ❌ Failed to import NEW_CONFIG.yml")
        else:
            print("   ⚠️  NEW_CONFIG.yml not found, skipping import test")
        
        # Clean up
        root.destroy()
        
        print("\n🎉 Enhanced debug test completed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💥 Enhanced debug test failed!")
        sys.exit(1)
