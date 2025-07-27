"""
Dialogs Module
Various dialog windows for the application
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any
from ..utils.config import ConfigManager

class SettingsDialog:
    """Settings configuration dialog"""
    
    def __init__(self, parent: tk.Widget, config_manager: ConfigManager):
        """
        Initialize settings dialog
        
        Args:
            parent: Parent widget
            config_manager: Configuration manager instance
        """
        self.parent = parent
        self.config_manager = config_manager
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("500x400")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self._create_widgets()
        self._load_current_settings()
    
    def _create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Notebook for different setting categories
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        # General settings tab
        self._create_general_tab()
        
        # Ignore patterns tab
        self._create_ignore_patterns_tab()
        
        # Appearance tab
        self._create_appearance_tab()
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky="ew")
        
        ttk.Button(button_frame, text="OK", command=self._ok_clicked).pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self._cancel_clicked).pack(side="right")
        ttk.Button(button_frame, text="Apply", command=self._apply_clicked).pack(side="right", padx=(0, 5))
        ttk.Button(button_frame, text="Reset", command=self._reset_clicked).pack(side="left")
    
    def _create_general_tab(self):
        """Create general settings tab"""
        general_frame = ttk.Frame(self.notebook)
        self.notebook.add(general_frame, text="General")
        
        # Remember window position
        self.remember_window_pos = tk.BooleanVar()
        ttk.Checkbutton(general_frame, text="Remember window position and size", 
                       variable=self.remember_window_pos).pack(anchor="w", pady=5)
        
        # Remember last directories
        self.remember_directories = tk.BooleanVar()
        ttk.Checkbutton(general_frame, text="Remember last selected directories", 
                       variable=self.remember_directories).pack(anchor="w", pady=5)
        
        # Auto-refresh
        self.auto_refresh = tk.BooleanVar()
        ttk.Checkbutton(general_frame, text="Auto-refresh when directories change", 
                       variable=self.auto_refresh).pack(anchor="w", pady=5)
        
        # Comparison options
        options_frame = ttk.LabelFrame(general_frame, text="Comparison Options")
        options_frame.pack(fill="x", pady=10)
        
        self.compare_metadata = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Compare file metadata (timestamps, permissions)", 
                       variable=self.compare_metadata).pack(anchor="w", padx=5, pady=2)
        
        self.ignore_case = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Ignore case in file names", 
                       variable=self.ignore_case).pack(anchor="w", padx=5, pady=2)
        
        self.follow_symlinks = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Follow symbolic links", 
                       variable=self.follow_symlinks).pack(anchor="w", padx=5, pady=2)
        
        # Performance settings
        perf_frame = ttk.LabelFrame(general_frame, text="Performance")
        perf_frame.pack(fill="x", pady=10)
        
        ttk.Label(perf_frame, text="Maximum file size for content comparison (MB):").pack(anchor="w", padx=5, pady=2)
        self.max_file_size = tk.StringVar(value="100")
        ttk.Entry(perf_frame, textvariable=self.max_file_size, width=10).pack(anchor="w", padx=5, pady=2)
        
        ttk.Label(perf_frame, text="Thread pool size for comparison:").pack(anchor="w", padx=5, pady=2)
        self.thread_pool_size = tk.StringVar(value="4")
        ttk.Entry(perf_frame, textvariable=self.thread_pool_size, width=10).pack(anchor="w", padx=5, pady=2)
    
    def _create_ignore_patterns_tab(self):
        """Create ignore patterns tab"""
        ignore_frame = ttk.Frame(self.notebook)
        self.notebook.add(ignore_frame, text="Ignore Patterns")
        
        ttk.Label(ignore_frame, text="File patterns to ignore during comparison:").pack(anchor="w", pady=5)
        
        # Listbox with scrollbar
        list_frame = ttk.Frame(ignore_frame)
        list_frame.pack(fill="both", expand=True, pady=5)
        
        self.ignore_listbox = tk.Listbox(list_frame)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.ignore_listbox.yview)
        self.ignore_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.ignore_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Entry and buttons for adding/removing patterns
        entry_frame = ttk.Frame(ignore_frame)
        entry_frame.pack(fill="x", pady=5)
        
        self.new_pattern = tk.StringVar()
        pattern_entry = ttk.Entry(entry_frame, textvariable=self.new_pattern)
        pattern_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        pattern_entry.bind("<Return>", lambda e: self._add_pattern())
        
        ttk.Button(entry_frame, text="Add", command=self._add_pattern).pack(side="right", padx=(0, 5))
        ttk.Button(entry_frame, text="Remove", command=self._remove_pattern).pack(side="right")
        
        # Default patterns
        default_frame = ttk.Frame(ignore_frame)
        default_frame.pack(fill="x", pady=5)
        
        ttk.Label(default_frame, text="Default patterns:").pack(side="left")
        ttk.Button(default_frame, text="Add Common", command=self._add_common_patterns).pack(side="right")
    
    def _create_appearance_tab(self):
        """Create appearance settings tab"""
        appearance_frame = ttk.Frame(self.notebook)
        self.notebook.add(appearance_frame, text="Appearance")
        
        # Font settings
        font_frame = ttk.LabelFrame(appearance_frame, text="Font Settings")
        font_frame.pack(fill="x", pady=5)
        
        ttk.Label(font_frame, text="Font family:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.font_family = tk.StringVar(value="Courier")
        font_combo = ttk.Combobox(font_frame, textvariable=self.font_family, 
                                 values=["Courier", "Monaco", "Consolas", "DejaVu Sans Mono"])
        font_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        
        ttk.Label(font_frame, text="Font size:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.font_size = tk.StringVar(value="10")
        ttk.Entry(font_frame, textvariable=self.font_size, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        font_frame.grid_columnconfigure(1, weight=1)
        
        # Color scheme
        color_frame = ttk.LabelFrame(appearance_frame, text="Color Scheme")
        color_frame.pack(fill="x", pady=5)
        
        self.color_scheme = tk.StringVar(value="default")
        schemes = ["default", "dark", "high_contrast"]
        for scheme in schemes:
            ttk.Radiobutton(color_frame, text=scheme.replace("_", " ").title(), 
                          variable=self.color_scheme, value=scheme).pack(anchor="w", padx=5, pady=2)
        
        # Display options
        display_frame = ttk.LabelFrame(appearance_frame, text="Display Options")
        display_frame.pack(fill="x", pady=5)
        
        self.show_line_numbers = tk.BooleanVar()
        ttk.Checkbutton(display_frame, text="Show line numbers", 
                       variable=self.show_line_numbers).pack(anchor="w", padx=5, pady=2)
        
        self.word_wrap = tk.BooleanVar()
        ttk.Checkbutton(display_frame, text="Word wrap in file viewer", 
                       variable=self.word_wrap).pack(anchor="w", padx=5, pady=2)
        
        self.syntax_highlighting = tk.BooleanVar()
        ttk.Checkbutton(display_frame, text="Syntax highlighting", 
                       variable=self.syntax_highlighting).pack(anchor="w", padx=5, pady=2)
    
    def _load_current_settings(self):
        """Load current settings into the dialog"""
        settings = self.config_manager.load_settings()
        
        # General settings
        self.remember_window_pos.set(settings.get('remember_window_pos', True))
        self.remember_directories.set(settings.get('remember_directories', True))
        self.auto_refresh.set(settings.get('auto_refresh', False))
        self.compare_metadata.set(settings.get('compare_metadata', True))
        self.ignore_case.set(settings.get('ignore_case', False))
        self.follow_symlinks.set(settings.get('follow_symlinks', False))
        self.max_file_size.set(str(settings.get('max_file_size', 100)))
        self.thread_pool_size.set(str(settings.get('thread_pool_size', 4)))
        
        # Ignore patterns
        patterns = settings.get('ignore_patterns', [])
        for pattern in patterns:
            self.ignore_listbox.insert(tk.END, pattern)
        
        # Appearance settings
        self.font_family.set(settings.get('font_family', 'Courier'))
        self.font_size.set(str(settings.get('font_size', 10)))
        self.color_scheme.set(settings.get('color_scheme', 'default'))
        self.show_line_numbers.set(settings.get('show_line_numbers', False))
        self.word_wrap.set(settings.get('word_wrap', False))
        self.syntax_highlighting.set(settings.get('syntax_highlighting', True))
    
    def _add_pattern(self):
        """Add a new ignore pattern"""
        pattern = self.new_pattern.get().strip()
        if pattern and pattern not in self.ignore_listbox.get(0, tk.END):
            self.ignore_listbox.insert(tk.END, pattern)
            self.new_pattern.set("")
    
    def _remove_pattern(self):
        """Remove selected ignore pattern"""
        selection = self.ignore_listbox.curselection()
        if selection:
            self.ignore_listbox.delete(selection[0])
    
    def _add_common_patterns(self):
        """Add common ignore patterns"""
        common_patterns = [
            "*.tmp", "*.bak", "*.swp", "*~", ".DS_Store", "Thumbs.db",
            "*.pyc", "*.pyo", "__pycache__", ".git", ".svn", ".hg",
            "node_modules", "*.log"
        ]
        
        existing = set(self.ignore_listbox.get(0, tk.END))
        for pattern in common_patterns:
            if pattern not in existing:
                self.ignore_listbox.insert(tk.END, pattern)
    
    def _ok_clicked(self):
        """Handle OK button click"""
        if self._apply_settings():
            self.result = "ok"
            self.dialog.destroy()
    
    def _cancel_clicked(self):
        """Handle Cancel button click"""
        self.result = "cancel"
        self.dialog.destroy()
    
    def _apply_clicked(self):
        """Handle Apply button click"""
        self._apply_settings()
    
    def _reset_clicked(self):
        """Handle Reset button click"""
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults?", parent=self.dialog):
            self.config_manager.reset_settings()
            self._load_current_settings()
    
    def _apply_settings(self) -> bool:
        """Apply current settings"""
        try:
            settings = {
                'remember_window_pos': self.remember_window_pos.get(),
                'remember_directories': self.remember_directories.get(),
                'auto_refresh': self.auto_refresh.get(),
                'compare_metadata': self.compare_metadata.get(),
                'ignore_case': self.ignore_case.get(),
                'follow_symlinks': self.follow_symlinks.get(),
                'max_file_size': int(self.max_file_size.get()),
                'thread_pool_size': int(self.thread_pool_size.get()),
                'ignore_patterns': list(self.ignore_listbox.get(0, tk.END)),
                'font_family': self.font_family.get(),
                'font_size': int(self.font_size.get()),
                'color_scheme': self.color_scheme.get(),
                'show_line_numbers': self.show_line_numbers.get(),
                'word_wrap': self.word_wrap.get(),
                'syntax_highlighting': self.syntax_highlighting.get()
            }
            
            self.config_manager.save_settings(settings)
            return True
            
        except ValueError as e:
            messagebox.showerror("Invalid Settings", f"Please check your input values: {str(e)}", parent=self.dialog)
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}", parent=self.dialog)
            return False

class AboutDialog:
    """About dialog"""
    
    def __init__(self, parent: tk.Widget):
        """
        Initialize about dialog
        
        Args:
            parent: Parent widget
        """
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("About SD Card Comparison Tool")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 100))
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Application title
        title_label = ttk.Label(main_frame, text="SD Card Comparison Tool", 
                               font=("TkDefaultFont", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Version
        version_label = ttk.Label(main_frame, text="Version 1.0.0")
        version_label.pack()
        
        # Description
        description_text = """
A GUI-based application for comparing contents between two SD card mount points, 
providing detailed file and directory comparison capabilities.

Features:
• Side-by-side directory comparison
• File content viewing and comparison
• Multiple export formats (HTML, CSV, JSON, Text)
• Customizable ignore patterns
• Cross-platform compatibility
        """
        
        description_label = ttk.Label(main_frame, text=description_text.strip(), 
                                    justify="left", wraplength=350)
        description_label.pack(pady=10)
        
        # Copyright
        copyright_label = ttk.Label(main_frame, text="© 2025 SD Card Comparison Tool Team")
        copyright_label.pack(pady=(20, 0))
        
        # OK button
        ttk.Button(main_frame, text="OK", command=self.dialog.destroy).pack(pady=(20, 0))

class ProgressDialog:
    """Progress dialog for long-running operations"""
    
    def __init__(self, parent: tk.Widget, title: str = "Progress", cancelable: bool = True):
        """
        Initialize progress dialog
        
        Args:
            parent: Parent widget
            title: Dialog title
            cancelable: Whether the operation can be cancelled
        """
        self.parent = parent
        self.cancelled = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 100))
        
        # Prevent closing with window manager
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_close if cancelable else lambda: None)
        
        self._create_widgets(cancelable)
    
    def _create_widgets(self, cancelable: bool):
        """Create dialog widgets"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Status label
        self.status_var = tk.StringVar(value="Processing...")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.pack(pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                          maximum=100, mode='determinate')
        self.progress_bar.pack(fill="x", pady=(0, 10))
        
        # Detail label
        self.detail_var = tk.StringVar(value="")
        detail_label = ttk.Label(main_frame, textvariable=self.detail_var, 
                               font=("TkDefaultFont", 8))
        detail_label.pack()
        
        # Cancel button
        if cancelable:
            ttk.Button(main_frame, text="Cancel", command=self._on_close).pack(pady=(20, 0))
    
    def update_progress(self, progress: float, status: str = None, detail: str = None):
        """Update progress"""
        self.progress_var.set(progress)
        
        if status:
            self.status_var.set(status)
        
        if detail:
            self.detail_var.set(detail)
        
        self.dialog.update()
    
    def _on_close(self):
        """Handle dialog close"""
        self.cancelled = True
        self.dialog.destroy()
    
    def is_cancelled(self) -> bool:
        """Check if operation was cancelled"""
        return self.cancelled
