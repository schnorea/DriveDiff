#!/usr/bin/env python3
"""
SD Card Comparison Tool
Main entry point for the application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.gui.main_window import MainWindow
import tkinter as tk
from tkinter import messagebox

def main():
    """Main entry point for the SD Card Comparison Tool"""
    try:
        # Create the main window
        root = tk.Tk()
        app = MainWindow(root)
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
