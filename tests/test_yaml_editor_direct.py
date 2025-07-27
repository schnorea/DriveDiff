#!/usr/bin/env python3
"""Test the _refresh_yaml_editor method directly"""

import os
import sys
import tkinter as tk

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.config_dialog import ConfigurationDialog
from utils.yaml_config import YamlConfigManager

def main():
    print("🔧 Testing _refresh_yaml_editor method directly...")
    
    try:
        # Create root window but don't show it
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        # Initialize configuration manager
        config_manager = YamlConfigManager()
        
        print("   📋 Creating configuration dialog...")
        dialog = ConfigurationDialog(root, config_manager)
        
        print("   ✅ Configuration dialog created successfully!")
        
        # Get initial YAML content
        initial_yaml = dialog.yaml_editor.get(1.0, tk.END)
        print(f"   📄 Initial YAML length: {len(initial_yaml)}")
        
        # Load NEW_CONFIG.yml
        if os.path.exists("NEW_CONFIG.yml"):
            imported_config = config_manager.import_config("NEW_CONFIG.yml")
            if imported_config:
                dialog.current_config = imported_config
                print(f"   ✅ Config updated, calling _refresh_yaml_editor()...")
                
                # Test the method directly with debug
                try:
                    yaml_content = dialog.config_manager._format_yaml_for_display(dialog.current_config)
                    print(f"   📄 Generated YAML length: {len(yaml_content)}")
                    
                    print("   🔄 Clearing editor...")
                    dialog.yaml_editor.delete(1.0, tk.END)
                    
                    print("   📝 Inserting new content...")
                    dialog.yaml_editor.insert(1.0, yaml_content)
                    
                    # Check the result
                    result_yaml = dialog.yaml_editor.get(1.0, tk.END)
                    print(f"   📄 Result YAML length: {len(result_yaml)}")
                    
                    if result_yaml != initial_yaml:
                        print("   ✅ YAML editor updated successfully!")
                    else:
                        print("   ❌ YAML editor content unchanged")
                        
                except Exception as e:
                    print(f"   ❌ Error in _refresh_yaml_editor: {e}")
                    import traceback
                    traceback.print_exc()
                    
        # Clean up
        root.destroy()
        
        print("\n🎉 Direct method test completed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💥 Direct method test failed!")
        sys.exit(1)
