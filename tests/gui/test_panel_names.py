#!/usr/bin/env python3
"""
Test script to demonstrate the panel names feature
"""

import sys
import os
sys.path.append('/Users/aussie/projects/2025/DriveDiff')

import tkinter as tk
from src.gui.file_viewer import FileViewer
from src.utils.yaml_config import YamlConfigManager

def test_panel_names():
    """Test the panel names functionality"""
    
    # Create a simple test window
    root = tk.Tk()
    root.title("Panel Names Test")
    root.geometry("800x600")
    
    # Create config manager
    config_manager = YamlConfigManager()
    config_manager.load_config()
    
    # Create file viewer with config
    file_viewer = FileViewer(root, config_manager)
    
    # Test setting different panel names
    print("Testing panel name functionality...")
    
    # Test 1: Default names
    print(f"Default names: {file_viewer.get_panel_names()}")
    
    # Test 2: Custom names
    file_viewer.set_panel_names("Original Version", "Modified Version")
    print(f"Custom names: {file_viewer.get_panel_names()}")
    
    # Test 3: Preset names
    presets = [
        ("Source", "Target"),
        ("Before", "After"), 
        ("Local", "Remote"),
        ("Old", "New")
    ]
    
    for left_name, right_name in presets:
        file_viewer.set_panel_names(left_name, right_name)
        print(f"Preset '{left_name} / {right_name}': {file_viewer.get_panel_names()}")
    
    # Reset to defaults
    file_viewer.reset_panel_names()
    print(f"Reset to defaults: {file_viewer.get_panel_names()}")
    
    print("\nPanel names feature test completed!")
    print("You can now:")
    print("1. Click 'Panel Names...' button to open the customization dialog")
    print("2. Try different presets (Original/Modified, Source/Target, etc.)")
    print("3. Enter custom names for your specific use case")
    print("4. Settings will be saved to your YAML config file")
    
    # Run the GUI
    root.mainloop()

if __name__ == "__main__":
    test_panel_names()
