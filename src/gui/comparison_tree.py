"""
Comparison Tree View Module
Tree view component for displaying comparison results
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Dict, Any
from ..core.directory_scanner import DirectoryComparison

class ComparisonTreeView:
    """Tree view component for displaying comparison results"""
    
    def __init__(self, parent: tk.Widget, file_selected_callback: Optional[Callable] = None):
        """
        Initialize the comparison tree view
        
        Args:
            parent: Parent widget
            file_selected_callback: Callback when a file is selected
        """
        self.parent = parent
        self.file_selected_callback = file_selected_callback
        self.comparison_data: Optional[DirectoryComparison] = None
        self.file_diff_map: Dict[str, Any] = {}  # Store file_diff objects by item_id
        
        self._create_widgets()
        self._setup_styles()
    
    def _create_widgets(self):
        """Create the tree view widgets"""
        # Create frame for tree and scrollbars
        tree_frame = ttk.Frame(self.parent)
        tree_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Create tree view
        self.tree = ttk.Treeview(tree_frame, columns=("status", "size_left", "size_right", "modified"), show="tree headings")
        
        # Configure columns
        self.tree.heading("#0", text="File Path")
        self.tree.heading("status", text="Status")
        self.tree.heading("size_left", text="Left Size")
        self.tree.heading("size_right", text="Right Size")
        self.tree.heading("modified", text="Modified")
        
        self.tree.column("#0", width=300, minwidth=200)
        self.tree.column("status", width=80, minwidth=60)
        self.tree.column("size_left", width=100, minwidth=80)
        self.tree.column("size_right", width=100, minwidth=80)
        self.tree.column("modified", width=120, minwidth=100)
        
        # Create scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Bind events
        self.tree.bind("<<TreeviewSelect>>", self._on_item_selected)
        self.tree.bind("<Double-1>", self._on_item_double_click)
        
        # Context menu
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="Copy Path", command=self._copy_path)
        self.context_menu.add_command(label="Show in File Manager", command=self._show_in_file_manager)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Copy to Right", command=self._copy_to_right)
        self.context_menu.add_command(label="Copy to Left", command=self._copy_to_left)
        
        self.tree.bind("<Button-3>", self._show_context_menu)  # Right click
    
    def _setup_styles(self):
        """Setup tree view styles"""
        style = ttk.Style()
        
        # Configure tags for different file statuses
        self.tree.tag_configure("added", foreground="#008000")  # Green
        self.tree.tag_configure("removed", foreground="#ff0000")  # Red
        self.tree.tag_configure("modified", foreground="#ff8c00")  # Orange
        self.tree.tag_configure("identical", foreground="#808080")  # Gray
    
    def display_comparison(self, comparison: DirectoryComparison):
        """
        Display comparison results in the tree
        
        Args:
            comparison: DirectoryComparison object to display
        """
        self.comparison_data = comparison
        self.clear()
        
        # Create category nodes
        categories = {
            "added": ("Added Files", comparison.added_files),
            "removed": ("Removed Files", comparison.removed_files),
            "modified": ("Modified Files", comparison.modified_files),
            "identical": ("Identical Files", comparison.identical_files)
        }
        
        for status, (category_name, file_list) in categories.items():
            if not file_list:
                continue
            
            # Create category node
            category_id = self.tree.insert("", "end", text=f"{category_name} ({len(file_list)})", 
                                         values=("", "", "", ""), tags=[status])
            
            # Add files to category
            for file_path in sorted(file_list):
                file_diff = comparison.file_differences.get(file_path)
                if file_diff:
                    self._add_file_item(category_id, file_path, file_diff, status)
        
        # Expand all categories
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
    
    def _add_file_item(self, parent_id: str, file_path: str, file_diff, status: str):
        """Add a file item to the tree"""
        # Get file information
        left_size = ""
        right_size = ""
        modified_info = ""
        
        if file_diff.left_info and file_diff.left_info.exists:
            left_size = self._format_size(file_diff.left_info.size)
            modified_info = file_diff.left_info.modified_time.strftime('%Y-%m-%d %H:%M')
        
        if file_diff.right_info and file_diff.right_info.exists:
            right_size = self._format_size(file_diff.right_info.size)
            if not modified_info:  # Use right modified time if left doesn't exist
                modified_info = file_diff.right_info.modified_time.strftime('%Y-%m-%d %H:%M')
        
        # Insert item
        item_id = self.tree.insert(parent_id, "end", 
                                 text=file_path,
                                 values=(status.capitalize(), left_size, right_size, modified_info),
                                 tags=[status])
        
        # Store file difference data in our map
        self.file_diff_map[item_id] = file_diff
    
    def _on_item_selected(self, event):
        """Handle item selection"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        item_id = selected_item[0]
        
        # Check if this is a file item (has file_diff data)
        file_diff = self.file_diff_map.get(item_id)
        if file_diff and self.file_selected_callback:
            file_path = self.tree.item(item_id, "text")
            self.file_selected_callback(file_path, file_diff)
    
    def _on_item_double_click(self, event):
        """Handle item double-click"""
        # Could be used to open files in external editor
        pass
    
    def _show_context_menu(self, event):
        """Show context menu"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def _copy_path(self):
        """Copy selected file path to clipboard"""
        selected_item = self.tree.selection()
        if selected_item:
            file_path = self.tree.item(selected_item[0], "text")
            self.parent.clipboard_clear()
            self.parent.clipboard_append(file_path)
    
    def _show_in_file_manager(self):
        """Show selected file in file manager"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        try:
            file_diff = self.tree.set(selected_item[0], "file_diff")
            if file_diff:
                # Try to open the file location
                import subprocess
                import platform
                
                file_path = None
                if file_diff.left_info and file_diff.left_info.exists:
                    file_path = file_diff.left_info.path
                elif file_diff.right_info and file_diff.right_info.exists:
                    file_path = file_diff.right_info.path
                
                if file_path:
                    if platform.system() == "Darwin":  # macOS
                        subprocess.run(["open", "-R", file_path])
                    elif platform.system() == "Windows":
                        subprocess.run(["explorer", "/select,", file_path])
                    else:  # Linux
                        subprocess.run(["xdg-open", os.path.dirname(file_path)])
        except Exception as e:
            print(f"Error showing file in file manager: {e}")
    
    def _copy_to_right(self):
        """Copy selected file from left to right"""
        # TODO: Implement file copying functionality
        tk.messagebox.showinfo("Info", "Copy to right functionality not yet implemented.")
    
    def _copy_to_left(self):
        """Copy selected file from right to left"""
        # TODO: Implement file copying functionality
        tk.messagebox.showinfo("Info", "Copy to left functionality not yet implemented.")
    
    def clear(self):
        """Clear the tree view"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.comparison_data = None
        self.file_diff_map.clear()  # Clear the file diff map as well
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        size = float(size_bytes)
        
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f} {size_names[i]}"
    
    def get_selected_file(self):
        """Get the currently selected file"""
        selected_item = self.tree.selection()
        if not selected_item:
            return None, None
        
        try:
            file_diff = self.tree.set(selected_item[0], "file_diff")
            if file_diff:
                file_path = self.tree.item(selected_item[0], "text")
                return file_path, file_diff
        except tk.TclError:
            pass
        
        return None, None
