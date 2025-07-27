#!/usr/bin/env python3
"""Test the configuration dialog GUI"""

import os
import sys
import tkinter as tk

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import using absolute imports
import gui.config_dialog as config_dialog_module
import utils.yaml_config as yaml_config_module

def main():
    print("🔧 Testing Configuration Dialog...")
    
    # Create root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    try:
        # Initialize configuration manager
        config_manager = yaml_config_module.YamlConfigManager()
        
        print("   📋 Creating configuration dialog...")
        dialog = config_dialog_module.ConfigurationDialog(root, config_manager)
        
        print("   ✅ Configuration dialog created successfully!")
        print("   🎯 Dialog should be visible now...")
        
        # Run the dialog
        root.mainloop()
        
    except Exception as e:
        print(f"   ❌ Error creating configuration dialog: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Configuration dialog test completed!")
    else:
        print("\n💥 Configuration dialog test failed!")
