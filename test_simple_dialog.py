#!/usr/bin/env python3
"""
Simple test to debug the dialog issue
"""

import sys
import os
sys.path.append('/Users/aussie/projects/2025/DriveDiff')

import tkinter as tk
from tkinter import ttk

def test_simple_dialog():
    """Test a simple dialog to see if the issue is with basic dialog creation"""
    
    root = tk.Tk()
    root.title("Dialog Test")
    root.geometry("300x200")
    
    def show_simple_dialog():
        print("Creating dialog...")
        
        dialog = tk.Toplevel(root)
        dialog.title("Test Dialog")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        
        print("Dialog created, setting up...")
        
        # Try without transient/grab first
        # dialog.transient(root)
        # dialog.grab_set()
        
        # Add some content
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="This is a test dialog").pack(pady=10)
        
        def close_dialog():
            print("Closing dialog...")
            dialog.destroy()
        
        ttk.Button(frame, text="Close", command=close_dialog).pack(pady=10)
        
        print("Dialog setup complete")
        
        # Try to keep it alive
        try:
            dialog.wait_window()
        except Exception as e:
            print(f"Error with wait_window: {e}")
    
    ttk.Button(root, text="Show Dialog", command=show_simple_dialog).pack(pady=50)
    
    print("Starting main loop...")
    root.mainloop()

if __name__ == "__main__":
    test_simple_dialog()
