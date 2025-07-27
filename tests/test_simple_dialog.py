#!/usr/bin/env python3
"""Test the configuration dialog to see what's broken"""

import sys
import os
import tkinter as tk
sys.path.append('/Users/aussie/projects/2025/DriveDiff')

def test_config_dialog():
    """Test the configuration dialog"""
    print("🧪 Testing Configuration Dialog")
    
    try:
        from src.utils.yaml_config import YamlConfigManager
        print("   ✅ YamlConfigManager imported")
        
        from src.gui.config_dialog import ConfigurationDialog
        print("   ✅ ConfigurationDialog imported")
        
        # Create root window
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        print("   ✅ Root window created")
        
        # Create config manager
        config_manager = YamlConfigManager()
        print("   ✅ Config manager created")
        
        # Try to create dialog
        print("   🔧 Creating configuration dialog...")
        dialog = ConfigurationDialog(root, config_manager)
        print("   ✅ Configuration dialog created successfully!")
        
        # Clean up
        root.destroy()
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating dialog: {e}")
        import traceback
        traceback.print_exc()
        
        # Clean up
        try:
            root.destroy()
        except:
            pass
        return False

if __name__ == "__main__":
    success = test_config_dialog()
    print(f"\nDialog test {'✅ PASSED' if success else '❌ FAILED'}")
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    test_simple_dialog()
