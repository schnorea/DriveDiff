"""
Structure Tree View Module
Specialized tree view for displaying directory structure differences
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Dict, List
import os

from ..core.directory_scanner import StructureComparison

class StructureTreeView:
    """Tree view specialized for directory structure comparison with color coding"""
    
    def __init__(self, parent: tk.Widget, selection_callback: Optional[Callable] = None):
        """
        Initialize the structure tree view
        
        Args:
            parent: Parent widget
            selection_callback: Optional callback for item selection
        """
        self.parent = parent
        self.selection_callback = selection_callback
        self.structure_comparison: Optional[StructureComparison] = None
        
        self._create_widgets()
        self._setup_styles()
        
    def _create_widgets(self):
        """Create the tree view and related widgets"""
        # Main frame
        main_frame = ttk.Frame(self.parent)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Header with legend
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        ttk.Label(header_frame, text="Directory Structure Comparison", font=("TkDefaultFont", 10, "bold")).pack(side="left")
        
        # Legend frame
        legend_frame = ttk.Frame(header_frame)
        legend_frame.pack(side="right")
        
        # Color legend
        ttk.Label(legend_frame, text="Legend:", font=("TkDefaultFont", 8)).pack(side="left", padx=(10, 5))
        
        # Added legend
        added_frame = ttk.Frame(legend_frame)
        added_frame.pack(side="left", padx=2)
        added_label = ttk.Label(added_frame, text="● Added", foreground="#00AA00", font=("TkDefaultFont", 8))
        added_label.pack()
        
        # Removed legend  
        removed_frame = ttk.Frame(legend_frame)
        removed_frame.pack(side="left", padx=2)
        removed_label = ttk.Label(removed_frame, text="● Removed", foreground="#CC0000", font=("TkDefaultFont", 8))
        removed_label.pack()
        
        # Common legend
        common_frame = ttk.Frame(legend_frame)
        common_frame.pack(side="left", padx=2)
        common_label = ttk.Label(common_frame, text="● Common", foreground="#0066CC", font=("TkDefaultFont", 8))
        common_label.pack()
        
        # Tree view with scrollbars
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame, selectmode="browse")
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Configure columns
        self.tree["columns"] = ("status", "type", "path")
        self.tree["show"] = "tree headings"
        
        # Column configuration
        self.tree.heading("#0", text="Directory Structure", anchor="w")
        self.tree.heading("status", text="Status", anchor="center")
        self.tree.heading("type", text="Type", anchor="center")
        self.tree.heading("path", text="Full Path", anchor="w")
        
        self.tree.column("#0", width=400, minwidth=200)
        self.tree.column("status", width=80, minwidth=60)
        self.tree.column("type", width=80, minwidth=60)
        self.tree.column("path", width=300, minwidth=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self._on_item_selected)
        
        # Summary frame
        summary_frame = ttk.Frame(main_frame)
        summary_frame.grid(row=2, column=0, sticky="ew", pady=(5, 0))
        
        self.summary_var = tk.StringVar(value="No comparison data")
        ttk.Label(summary_frame, textvariable=self.summary_var, font=("TkDefaultFont", 9)).pack()
        
    def _setup_styles(self):
        """Setup custom styles for different item types"""
        style = ttk.Style()
        
        # Create custom tags for different status types
        self.tree.tag_configure("added", foreground="#00AA00", font=("TkDefaultFont", 9, "bold"))
        self.tree.tag_configure("removed", foreground="#CC0000", font=("TkDefaultFont", 9, "bold"))
        self.tree.tag_configure("common", foreground="#0066CC", font=("TkDefaultFont", 9))
        
    def display_structure_comparison(self, comparison: StructureComparison, left_base: str, right_base: str):
        """
        Display structure comparison results
        
        Args:
            comparison: StructureComparison object
            left_base: Left directory base path
            right_base: Right directory base path
        """
        self.structure_comparison = comparison
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Build directory tree structure
        directory_tree = self._build_directory_tree(comparison, left_base, right_base)
        
        # Populate tree view
        self._populate_tree(directory_tree)
        
        # Update summary
        total_dirs = len(comparison.added_directories) + len(comparison.removed_directories) + len(comparison.common_directories)
        summary = f"Total directories: {total_dirs} | Added: {len(comparison.added_directories)} | Removed: {len(comparison.removed_directories)} | Common: {len(comparison.common_directories)}"
        self.summary_var.set(summary)
        
    def _build_directory_tree(self, comparison: StructureComparison, left_base: str, right_base: str) -> Dict:
        """
        Build a hierarchical tree structure from flat directory paths
        
        Args:
            comparison: StructureComparison object
            left_base: Left directory base path
            right_base: Right directory base path
            
        Returns:
            Dictionary representing the tree structure
        """
        tree = {}
        
        # Process all directories
        all_directories = []
        
        # Add directories with their status
        for dir_path in comparison.added_directories:
            all_directories.append((dir_path, "added", right_base))
            
        for dir_path in comparison.removed_directories:
            all_directories.append((dir_path, "removed", left_base))
            
        for dir_path in comparison.common_directories:
            all_directories.append((dir_path, "common", left_base))
            
        # Build tree structure
        for dir_path, status, base_path in all_directories:
            parts = dir_path.split(os.sep)
            current = tree
            
            # Build nested structure
            full_path = ""
            for i, part in enumerate(parts):
                if i == 0:
                    full_path = part
                else:
                    full_path = os.path.join(full_path, part)
                    
                if part not in current:
                    current[part] = {
                        "children": {},
                        "status": status,
                        "full_path": full_path,
                        "absolute_path": os.path.join(base_path, full_path)
                    }
                current = current[part]["children"]
                
        return tree
        
    def _populate_tree(self, tree_data: Dict, parent: str = ""):
        """
        Populate the treeview with directory data
        
        Args:
            tree_data: Tree structure dictionary
            parent: Parent item ID
        """
        for name, data in sorted(tree_data.items()):
            status = data["status"]
            full_path = data["full_path"]
            absolute_path = data["absolute_path"]
            
            # Determine status icon
            if status == "added":
                status_text = "+ Added"
                tag = "added"
            elif status == "removed":
                status_text = "- Removed"
                tag = "removed"
            else:
                status_text = "= Common"
                tag = "common"
                
            # Insert item
            item_id = self.tree.insert(
                parent, 
                "end", 
                text=name,
                values=(status_text, "Directory", absolute_path),
                tags=(tag,)
            )
            
            # Recursively add children
            if data["children"]:
                self._populate_tree(data["children"], item_id)
                
        # Expand all items initially
        self._expand_all()
        
    def _expand_all(self):
        """Expand all tree items"""
        def expand_item(item):
            self.tree.item(item, open=True)
            for child in self.tree.get_children(item):
                expand_item(child)
                
        for item in self.tree.get_children():
            expand_item(item)
            
    def _on_item_selected(self, event):
        """Handle item selection"""
        selection = self.tree.selection()
        if selection and self.selection_callback:
            item = selection[0]
            values = self.tree.item(item, "values")
            if len(values) >= 3:
                directory_path = values[2]  # absolute_path
                self.selection_callback(directory_path)
                
    def clear(self):
        """Clear the tree view"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.summary_var.set("No comparison data")
