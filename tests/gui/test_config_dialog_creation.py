#!/usr/bin/env python3
"""Test configuration dialog creation without showing GUI"""

import os
import sys
import tkinter as tk

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gui.config_dialog import ConfigurationDialog
from utils.yaml_config import YamlConfigManager

def main():
    print("🔧 Testing Configuration Dialog Creation...")
    
    try:
        # Create root window but don't show it
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        # Initialize configuration manager
        config_manager = YamlConfigManager()
        
        print("   📋 Creating configuration dialog...")
        dialog = ConfigurationDialog(root, config_manager)
        
        print("   ✅ Configuration dialog created successfully!")
        
        # Test loading configuration
        print("   🔄 Testing configuration loading...")
        dialog._load_configuration()
        
        print("   ✅ Configuration loaded successfully!")
        
        # Test building configuration from form
        print("   🏗️ Testing configuration building...")
        config = dialog._build_config_from_form()
        
        print("   ✅ Configuration built successfully!")
        print(f"   📊 Built config keys: {list(config.keys())}")
        
        # Clean up
        root.destroy()
        
        print("\n🎉 Configuration dialog test completed successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💥 Configuration dialog test failed!")
        sys.exit(1)
