"""
Main Window Module
Main application window and UI coordination
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from typing import Optional

from ..core.directory_scanner import DirectoryScanner, DirectoryComparison, StructureComparison
from ..core.report_generator import ReportGenerator
from ..utils.yaml_config import YamlConfigManager
from .comparison_tree import ComparisonTreeView
from .structure_tree import StructureTreeView
from .file_viewer import FileViewer
from .dialogs import SettingsDialog, AboutDialog
from .config_dialog import ConfigurationDialog
from ..utils.config import ConfigManager

class MainWindow:
    """Main application window"""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the main window
        
        Args:
            root: Root Tkinter window
        """
        self.root = root
        self.config_manager = ConfigManager()
        self.yaml_config_manager = YamlConfigManager()
        self.directory_scanner = DirectoryScanner.from_config(self.yaml_config_manager)
        self.report_generator = ReportGenerator()
        
        self.left_path = tk.StringVar()
        self.right_path = tk.StringVar()
        self.current_comparison: Optional[DirectoryComparison] = None
        self.current_structure_comparison: Optional[StructureComparison] = None
        self.comparison_thread: Optional[threading.Thread] = None
        self.structure_thread: Optional[threading.Thread] = None
        
        self._setup_window()
        self._create_menu()
        self._create_widgets()
        self._load_settings()
    
    def _setup_window(self):
        """Setup the main window properties"""
        self.root.title("SD Card Comparison Tool")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure grid weights for resizing
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_menu(self):
        """Create the application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Comparison...", command=self._save_comparison, accelerator="Ctrl+S")
        file_menu.add_command(label="Load Comparison...", command=self._load_comparison, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Export Report...", command=self._export_report, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_closing, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Application Settings...", command=self._show_settings)
        edit_menu.add_command(label="Scan Configuration...", command=self._show_scan_config)
        edit_menu.add_command(label="Clear Results", command=self._clear_results)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh", command=self._refresh_comparison, accelerator="F5")
        view_menu.add_separator()
        view_menu.add_checkbutton(label="Show Identical Files", command=self._toggle_identical_files)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About...", command=self._show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-s>', lambda e: self._save_comparison())
        self.root.bind('<Control-o>', lambda e: self._load_comparison())
        self.root.bind('<Control-e>', lambda e: self._export_report())
        self.root.bind('<Control-q>', lambda e: self._on_closing())
        self.root.bind('<F5>', lambda e: self._refresh_comparison())
    
    def _create_widgets(self):
        """Create the main widgets with tabbed interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        
        # Path selection frame
        path_frame = ttk.LabelFrame(main_frame, text="Select Directories to Compare")
        path_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        path_frame.grid_columnconfigure(1, weight=1)
        
        # Left path selection
        ttk.Label(path_frame, text="Left Directory:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        left_entry = ttk.Entry(path_frame, textvariable=self.left_path, width=50)
        left_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        ttk.Button(path_frame, text="Browse...", command=self._browse_left_directory).grid(row=0, column=2, padx=5, pady=2)
        
        # Right path selection
        ttk.Label(path_frame, text="Right Directory:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        right_entry = ttk.Entry(path_frame, textvariable=self.right_path, width=50)
        right_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        ttk.Button(path_frame, text="Browse...", command=self._browse_right_directory).grid(row=1, column=2, padx=5, pady=2)
        
        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))
        
        # Progress bar and status
        progress_frame = ttk.Frame(control_frame)
        progress_frame.pack(fill="x", expand=True)
        
        # Progress info
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack(side="left")
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(side="right", fill="x", expand=True, padx=(10, 0))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, sticky="nsew")
        
        # Content Comparison Tab
        self._create_content_tab()
        
        # Structure Comparison Tab
        self._create_structure_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief="sunken")
        status_bar.grid(row=3, column=0, sticky="ew", pady=(5, 0))
    
    def _create_content_tab(self):
        """Create the content comparison tab"""
        # Content tab frame
        content_frame = ttk.Frame(self.notebook)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Control frame for content tab
        content_control_frame = ttk.Frame(content_frame)
        content_control_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Compare button
        self.compare_button = ttk.Button(content_control_frame, text="Compare Directories", command=self._start_comparison)
        self.compare_button.pack(side="left", padx=(0, 5))
        
        # Cancel button
        self.cancel_button = ttk.Button(content_control_frame, text="Cancel", command=self._cancel_comparison, state="disabled")
        self.cancel_button.pack(side="left", padx=(0, 10))
        
        # Results frame (PanedWindow for resizable panes)
        self.paned_window = ttk.PanedWindow(content_frame, orient="horizontal")
        self.paned_window.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Left pane - comparison tree
        tree_frame = ttk.LabelFrame(self.paned_window, text="Comparison Results")
        self.comparison_tree = ComparisonTreeView(tree_frame, self._on_file_selected)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        self.paned_window.add(tree_frame, weight=1)
        
        # Right pane - file viewer
        viewer_frame = ttk.LabelFrame(self.paned_window, text="File Viewer")
        self.file_viewer = FileViewer(viewer_frame, self.config_manager)
        viewer_frame.grid_columnconfigure(0, weight=1)
        viewer_frame.grid_rowconfigure(0, weight=1)
        self.paned_window.add(viewer_frame, weight=2)
        
        # Add tab to notebook
        self.notebook.add(content_frame, text="Content Comparison")
        
    def _create_structure_tab(self):
        """Create the structure comparison tab"""
        # Structure tab frame
        structure_frame = ttk.Frame(self.notebook)
        structure_frame.grid_columnconfigure(0, weight=1)
        structure_frame.grid_rowconfigure(1, weight=1)
        
        # Control frame for structure tab
        structure_control_frame = ttk.LabelFrame(structure_frame, text="Structure Analysis Controls")
        structure_control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # Compare Structure button
        self.structure_button = ttk.Button(structure_control_frame, text="🌳 Compare Structure", command=self._start_structure_comparison)
        self.structure_button.pack(side="left", padx=10, pady=5)
        
        # Cancel Structure button
        self.cancel_structure_button = ttk.Button(structure_control_frame, text="Cancel", command=self._cancel_structure_comparison, state="disabled")
        self.cancel_structure_button.pack(side="left", padx=(5, 10), pady=5)
        
        # Structure tree view
        tree_container = ttk.Frame(structure_frame)
        tree_container.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        tree_container.grid_columnconfigure(0, weight=1)
        tree_container.grid_rowconfigure(0, weight=1)
        
        self.structure_tree = StructureTreeView(tree_container, self._on_directory_selected)
        
        # Add tab to notebook
        self.notebook.add(structure_frame, text="Structure Comparison")
    
    def _browse_left_directory(self):
        """Browse for left directory"""
        directory = filedialog.askdirectory(
            title="Select Left Directory",
            initialdir=self.left_path.get() or os.path.expanduser("~")
        )
        if directory:
            self.left_path.set(directory)
    
    def _browse_right_directory(self):
        """Browse for right directory"""
        directory = filedialog.askdirectory(
            title="Select Right Directory",
            initialdir=self.right_path.get() or os.path.expanduser("~")
        )
        if directory:
            self.right_path.set(directory)
    
    def _on_directory_selected(self, directory_path: str):
        """Handle directory selection in structure tree"""
        # Update status bar to show selected directory
        self.status_var.set(f"Selected: {directory_path}")
        
        # Switch to structure tab if not already there
        self.notebook.select(1)  # Structure tab is index 1
    
    def _cancel_structure_comparison(self):
        """Cancel structure comparison"""
        if self.structure_thread and self.structure_thread.is_alive():
            self.directory_scanner.cancel_comparison()
            self.structure_thread.join(timeout=1.0)
        
        self.cancel_structure_button.config(state="disabled")
        self.structure_button.config(state="normal")
        self.progress_var.set("Cancelled")
        self.progress_bar.config(value=0)
    
    def _start_comparison(self):
        """Start directory comparison"""
        left_path = self.left_path.get().strip()
        right_path = self.right_path.get().strip()
        
        # Validate paths
        if not left_path or not right_path:
            messagebox.showerror("Error", "Please select both directories to compare.")
            return
        
        if not os.path.exists(left_path) or not os.path.isdir(left_path):
            messagebox.showerror("Error", f"Left directory does not exist or is not accessible: {left_path}")
            return
        
        if not os.path.exists(right_path) or not os.path.isdir(right_path):
            messagebox.showerror("Error", f"Right directory does not exist or is not accessible: {right_path}")
            return
        
        if left_path == right_path:
            messagebox.showerror("Error", "Please select different directories to compare.")
            return
        
        # Load scan configuration and apply it
        try:
            scan_config = self.yaml_config_manager.get_scan_configuration()
            
            # Update directory scanner with current configuration
            self.directory_scanner = DirectoryScanner.from_config(self.yaml_config_manager)
            
        except Exception as e:
            messagebox.showwarning("Configuration Warning", 
                                 f"Failed to load scan configuration: {str(e)}\n"
                                 "Using default settings.")
        
        # Clear previous results
        self._clear_results()
        
        # Update UI for comparison
        self.compare_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.progress_bar.config(value=0)
        self.progress_var.set("Starting comparison...")
        self.status_var.set("Comparing directories...")
        
        # Start comparison in a separate thread
        self.comparison_thread = self.directory_scanner.compare_directories_async(
            left_path, right_path,
            progress_callback=self._on_progress_update,
            completion_callback=self._on_comparison_complete
        )
    
    def _cancel_comparison(self):
        """Cancel the current comparison"""
        if self.comparison_thread and self.comparison_thread.is_alive():
            self.directory_scanner.cancel_comparison()
            self.status_var.set("Cancelling comparison...")
        elif self.structure_thread and self.structure_thread.is_alive():
            self.directory_scanner.cancel_comparison()
            self.status_var.set("Cancelling structure comparison...")
    
    def _on_progress_update(self, current: int, total: int, current_file: str):
        """Handle progress updates from comparison"""
        def update_ui():
            if total > 0:
                progress = (current / total) * 100
                self.progress_bar.config(value=progress)
                self.progress_var.set(f"Processing {current}/{total}: {os.path.basename(current_file)}")
        
        # Schedule UI update in main thread
        self.root.after(0, update_ui)
    
    def _on_comparison_complete(self, comparison: Optional[DirectoryComparison]):
        """Handle completion of directory comparison"""
        def update_ui():
            self.compare_button.config(state="normal")
            self.cancel_button.config(state="disabled")
            self.progress_bar.config(value=0)
            
            if comparison:
                self.current_comparison = comparison
                self.comparison_tree.display_comparison(comparison)
                
                # Update status
                summary = f"Comparison complete: {len(comparison.identical_files)} identical, " \
                         f"{len(comparison.modified_files)} modified, " \
                         f"{len(comparison.added_files)} added, " \
                         f"{len(comparison.removed_files)} removed"
                
                self.progress_var.set("Comparison complete")
                self.status_var.set(summary)
            else:
                self.progress_var.set("Comparison failed or cancelled")
                self.status_var.set("Ready")
                messagebox.showerror("Error", "Comparison failed or was cancelled.")
        
        # Schedule UI update in main thread
        self.root.after(0, update_ui)
    
    def _start_structure_comparison(self):
        """Start directory structure comparison"""
        left_path = self.left_path.get().strip()
        right_path = self.right_path.get().strip()
        
        # Validate paths (same validation as full comparison)
        if not left_path or not right_path:
            messagebox.showerror("Error", "Please select both directories to compare.")
            return
        
        if not os.path.exists(left_path) or not os.path.isdir(left_path):
            messagebox.showerror("Error", f"Left directory does not exist or is not accessible: {left_path}")
            return
        
        if not os.path.exists(right_path) or not os.path.isdir(right_path):
            messagebox.showerror("Error", f"Right directory does not exist or is not accessible: {right_path}")
            return
        
        if left_path == right_path:
            messagebox.showerror("Error", "Please select different directories to compare.")
            return
        
        # Load scan configuration and apply it
        try:
            # Use structure-specific configuration
            structure_config = self.yaml_config_manager.get_structure_comparison_config()
            
            # Update directory scanner with structure comparison configuration
            self.directory_scanner = DirectoryScanner.from_config(self.yaml_config_manager, "structure")
            
        except Exception as e:
            messagebox.showwarning("Configuration Warning", 
                                 f"Failed to load structure comparison configuration: {str(e)}\n"
                                 "Using default settings.")
        
        # Switch to structure tab
        self.notebook.select(1)  # Structure tab is index 1
        
        # Clear previous structure results
        self.structure_tree.clear()
        
        # Update UI for structure comparison
        self.compare_button.config(state="disabled")
        self.structure_button.config(state="disabled")
        self.cancel_structure_button.config(state="normal")
        self.progress_bar.config(value=0)
        self.progress_var.set("Starting structure comparison...")
        self.status_var.set("Comparing directory structures...")
        
        # Start structure comparison in a separate thread
        self.structure_thread = self.directory_scanner.compare_structure_async(
            left_path, right_path,
            progress_callback=self._on_structure_progress_update,
            completion_callback=self._on_structure_comparison_complete
        )
    
    def _on_structure_progress_update(self, current: int, total: int, current_path: str):
        """Handle progress updates from structure comparison"""
        def update_ui():
            if total > 0:
                # Comparison phase - show percentage
                progress = (current / total) * 100
                self.progress_bar.config(value=progress)
                self.progress_var.set(f"Analyzing {current}/{total}: {os.path.basename(current_path)}")
            else:
                # Scanning phase - show indeterminate progress
                self.progress_bar.config(mode='indeterminate')
                if not hasattr(self, '_progress_started') or not self._progress_started:
                    self.progress_bar.start(10)  # Start indeterminate animation
                    self._progress_started = True
                self.progress_var.set(current_path)
        
        # Schedule UI update in main thread
        self.root.after(0, update_ui)
    
    def _on_structure_comparison_complete(self, structure_comparison: Optional[StructureComparison]):
        """Handle completion of structure comparison"""
        def update_ui():
            # Stop indeterminate progress and reset
            if hasattr(self, '_progress_started') and self._progress_started:
                self.progress_bar.stop()
                self._progress_started = False
            
            self.progress_bar.config(mode='determinate', value=0)
            self.compare_button.config(state="normal")
            self.structure_button.config(state="normal")
            self.cancel_structure_button.config(state="disabled")
            
            if structure_comparison:
                self.current_structure_comparison = structure_comparison
                
                # Display in the new structure tree
                left_path = self.left_path.get().strip()
                right_path = self.right_path.get().strip()
                self.structure_tree.display_structure_comparison(structure_comparison, left_path, right_path)
                
                # Update status
                summary = f"Structure comparison complete: {len(structure_comparison.common_directories)} common dirs, " \
                         f"{len(structure_comparison.added_directories)} added, " \
                         f"{len(structure_comparison.removed_directories)} removed"
                
                self.progress_var.set("Structure comparison complete")
                self.status_var.set(summary)
            else:
                self.progress_var.set("Structure comparison failed or cancelled")
                self.status_var.set("Ready")
                messagebox.showerror("Error", "Structure comparison failed or was cancelled.")
        
        # Schedule UI update in main thread
        self.root.after(0, update_ui)
    
    def _on_file_selected(self, file_path: str, file_diff):
        """Handle file selection in the comparison tree"""
        if not file_diff:
            return
        
        left_file_path = None
        right_file_path = None
        
        # Construct full file paths using base directories
        left_base = self.left_path.get()
        right_base = self.right_path.get()
        
        if file_diff.left_info and file_diff.left_info.exists and left_base:
            left_file_path = os.path.join(left_base, file_diff.left_info.path)
        
        if file_diff.right_info and file_diff.right_info.exists and right_base:
            right_file_path = os.path.join(right_base, file_diff.right_info.path)
        
        self.file_viewer.display_files(left_file_path, right_file_path, file_diff)
    
    def _clear_results(self):
        """Clear comparison results"""
        self.current_comparison = None
        self.current_structure_comparison = None
        self.comparison_tree.clear()
        self.structure_tree.clear()
        self.file_viewer.clear()
        self.progress_var.set("Ready")
        self.status_var.set("Ready")
    
    def _refresh_comparison(self):
        """Refresh the current comparison"""
        if self.left_path.get() and self.right_path.get():
            self._start_comparison()
    
    def _save_comparison(self):
        """Save comparison results"""
        if not self.current_comparison:
            messagebox.showwarning("Warning", "No comparison results to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Comparison Results",
            defaultextension=".json",
            initialdir=os.path.expanduser("~"),  # Default to user's home directory
            filetypes=[
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Check if user is trying to save to a mounted volume and warn them
                if file_path.startswith('/Volumes/'):
                    response = messagebox.askyesno(
                        "Warning - Mounted Volume Detected",
                        f"You're trying to save to a mounted volume:\n{file_path}\n\n"
                        "Mounted volumes (SD cards, USB drives) are often read-only and may cause the save to fail.\n\n"
                        "Recommended locations:\n"
                        "• Desktop: ~/Desktop/\n"
                        "• Documents: ~/Documents/\n"
                        "• Home directory: ~/\n\n"
                        "Do you want to continue with this location?"
                    )
                    if not response:
                        return
                
                # Get panel names from file viewer
                left_panel_name, right_panel_name = self.file_viewer.get_panel_names()
                
                report_content = self.report_generator.generate_json_report(
                    self.current_comparison,
                    self.left_path.get(),
                    self.right_path.get(),
                    left_panel_name,
                    right_panel_name
                )
                
                if self.report_generator.save_report(report_content, file_path):
                    messagebox.showinfo("Success", f"Comparison results saved to {file_path}")
                else:
                    messagebox.showerror(
                        "Save Failed", 
                        f"Failed to save comparison results to:\n{file_path}\n\n"
                        "If this is a mounted volume (SD card, USB drive), it may be read-only.\n"
                        "Try saving to your Desktop, Documents folder, or home directory instead."
                    )
            except Exception as e:
                error_msg = f"Failed to save comparison results: {str(e)}"
                if "Read-only file system" in str(e):
                    error_msg += "\n\nThe target location is read-only. Please choose a writable location such as your Desktop or Documents folder."
                messagebox.showerror("Error", error_msg)
    
    def _load_comparison(self):
        """Load comparison results"""
        file_path = filedialog.askopenfilename(
            title="Load Comparison Results",
            filetypes=[
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # TODO: Implement loading of comparison results
                messagebox.showinfo("Info", "Loading comparison results is not yet implemented.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load comparison results: {str(e)}")
    
    def _export_report(self):
        """Export comparison report"""
        if not self.current_comparison:
            messagebox.showwarning("Warning", "No comparison results to export.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Report",
            defaultextension=".html",
            initialdir=os.path.expanduser("~"),  # Default to user's home directory
            filetypes=[
                ("HTML files", "*.html"),
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("JSON files", "*.json")
            ]
        )
        
        if file_path:
            try:
                # Check if user is trying to save to a mounted volume and warn them
                if file_path.startswith('/Volumes/'):
                    response = messagebox.askyesno(
                        "Warning - Mounted Volume Detected",
                        f"You're trying to save to a mounted volume:\n{file_path}\n\n"
                        "Mounted volumes (SD cards, USB drives) are often read-only and may cause the save to fail.\n\n"
                        "Recommended locations:\n"
                        "• Desktop: ~/Desktop/\n"
                        "• Documents: ~/Documents/\n"
                        "• Home directory: ~/\n\n"
                        "Do you want to continue with this location?"
                    )
                    if not response:
                        return
                
                # Get panel names from file viewer
                left_panel_name, right_panel_name = self.file_viewer.get_panel_names()
                
                ext = os.path.splitext(file_path)[1].lower()
                
                if ext == '.html':
                    print(f"Generating HTML report...")  # Debug
                    report_content = self.report_generator.generate_html_report(
                        self.current_comparison, self.left_path.get(), self.right_path.get(),
                        left_panel_name, right_panel_name
                    )
                elif ext == '.txt':
                    report_content = self.report_generator.generate_text_report(
                        self.current_comparison, self.left_path.get(), self.right_path.get(),
                        left_panel_name, right_panel_name
                    )
                elif ext == '.csv':
                    report_content = self.report_generator.generate_csv_report(
                        self.current_comparison, self.left_path.get(), self.right_path.get(),
                        left_panel_name, right_panel_name
                    )
                elif ext == '.json':
                    report_content = self.report_generator.generate_json_report(
                        self.current_comparison, self.left_path.get(), self.right_path.get(),
                        left_panel_name, right_panel_name
                    )
                else:
                    report_content = self.report_generator.generate_text_report(
                        self.current_comparison, self.left_path.get(), self.right_path.get(),
                        left_panel_name, right_panel_name
                    )
                
                print(f"Report content generated, length: {len(report_content)}")  # Debug
                print(f"Saving to: {file_path}")  # Debug
                
                if self.report_generator.save_report(report_content, file_path):
                    messagebox.showinfo("Success", f"Report exported to {file_path}")
                else:
                    messagebox.showerror(
                        "Export Failed", 
                        f"Failed to export report to:\n{file_path}\n\n"
                        "If this is a mounted volume (SD card, USB drive), it may be read-only.\n"
                        "Try saving to your Desktop, Documents folder, or home directory instead."
                    )
                    
            except Exception as e:
                error_msg = f"Failed to export report: {str(e)}"
                if "Read-only file system" in str(e):
                    error_msg += "\n\nThe target location is read-only. Please choose a writable location such as your Desktop or Documents folder."
                messagebox.showerror("Error", error_msg)
    
    def _show_scan_config(self):
        """Show scan configuration dialog"""
        dialog = ConfigurationDialog(self.root, self.yaml_config_manager)
        self.root.wait_window(dialog.dialog)
        
        # If configuration was modified, update the scanner with new settings
        if dialog.result == "ok":
            try:
                # Update directory scanner with new configuration
                self.directory_scanner = DirectoryScanner.from_config(self.yaml_config_manager)
                self.status_var.set("Scan configuration updated")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update scan configuration: {str(e)}")
    
    def _show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self.root, self.config_manager)
        self.root.wait_window(dialog.dialog)
    
    def _show_about(self):
        """Show about dialog"""
        dialog = AboutDialog(self.root)
        self.root.wait_window(dialog.dialog)
    
    def _toggle_identical_files(self):
        """Toggle display of identical files"""
        # TODO: Implement filtering in comparison tree
        pass
    
    def _load_settings(self):
        """Load application settings"""
        settings = self.config_manager.load_settings()
        
        # Apply window geometry if saved
        if 'window_geometry' in settings:
            self.root.geometry(settings['window_geometry'])
        
        # Apply other settings - scanner will be created from YAML config, 
        # but keep compatibility with old settings
        self.directory_scanner = DirectoryScanner.from_config(self.yaml_config_manager)
    
    def _save_settings(self):
        """Save application settings"""
        settings = {
            'window_geometry': self.root.geometry(),
            'left_path': self.left_path.get(),
            'right_path': self.right_path.get()
        }
        
        self.config_manager.save_settings(settings)
    
    def _on_closing(self):
        """Handle application closing"""
        # Cancel any running comparison
        if self.comparison_thread and self.comparison_thread.is_alive():
            self.directory_scanner.cancel_comparison()
            # Give it a moment to cancel
            self.comparison_thread.join(timeout=1.0)
        
        # Save settings
        self._save_settings()
        
        # Close the application
        self.root.destroy()
