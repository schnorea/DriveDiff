"""
Configuration Dialog Module
Popup interface for modifying YAML configuration
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from typing import Dict, Any, List, Optional
from ..utils.yaml_config import YamlConfigManager

class ConfigurationDialog:
    """Configuration dialog for YAML settings"""
    
    def __init__(self, parent: tk.Widget, config_manager: YamlConfigManager = None):
        """
        Initialize configuration dialog
        
        Args:
            parent: Parent widget
            config_manager: YAML configuration manager
        """
        self.parent = parent
        self.config_manager = config_manager or YamlConfigManager()
        self.result = None
        self.current_config = {}
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Scan Configuration")
        self.dialog.geometry("800x700")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Handle dialog closing
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)
        
        self._create_widgets()
        self._load_configuration()
    
    def _create_widgets(self):
        """Create dialog widgets"""
        # Main frame with padding
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Create notebook for different sections
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        # Create tabs
        self._create_paths_tab()
        self._create_patterns_tab()
        self._create_performance_tab()
        self._create_advanced_tab()
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, sticky="ew")
        
        # Left side buttons
        ttk.Button(button_frame, text="Load Config...", command=self._load_from_file).pack(side="left")
        ttk.Button(button_frame, text="Save Config...", command=self._save_to_file).pack(side="left", padx=(5, 0))
        ttk.Button(button_frame, text="Reset to Defaults", command=self._reset_to_defaults).pack(side="left", padx=(5, 0))
        
        # Right side buttons
        ttk.Button(button_frame, text="Cancel", command=self._on_cancel).pack(side="right")
        ttk.Button(button_frame, text="Apply", command=self._on_apply).pack(side="right", padx=(0, 5))
        ttk.Button(button_frame, text="OK", command=self._on_ok).pack(side="right", padx=(0, 5))
    
    def _create_paths_tab(self):
        """Create paths configuration tab"""
        paths_frame = ttk.Frame(self.notebook)
        self.notebook.add(paths_frame, text="Paths")
        
        # Main container with scrollbar
        canvas = tk.Canvas(paths_frame)
        scrollbar = ttk.Scrollbar(paths_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Logging level
        logging_frame = ttk.LabelFrame(scrollable_frame, text="Logging Configuration")
        logging_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(logging_frame, text="Log Level:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.log_level_var = tk.StringVar()
        log_level_combo = ttk.Combobox(logging_frame, textvariable=self.log_level_var,
                                      values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                                      state="readonly", width=15)
        log_level_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        logging_frame.grid_columnconfigure(1, weight=1)
        
        # Scan paths
        scan_frame = ttk.LabelFrame(scrollable_frame, text="Scan Paths")
        scan_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Label(scan_frame, text="Directories to scan:").pack(anchor="w", padx=5, pady=(5, 0))
        
        # Scan paths listbox with scrollbar
        scan_list_frame = ttk.Frame(scan_frame)
        scan_list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.scan_paths_listbox = tk.Listbox(scan_list_frame, height=6)
        scan_scrollbar = ttk.Scrollbar(scan_list_frame, orient="vertical", command=self.scan_paths_listbox.yview)
        self.scan_paths_listbox.configure(yscrollcommand=scan_scrollbar.set)
        
        self.scan_paths_listbox.pack(side="left", fill="both", expand=True)
        scan_scrollbar.pack(side="right", fill="y")
        
        # Scan paths buttons
        scan_btn_frame = ttk.Frame(scan_frame)
        scan_btn_frame.pack(fill="x", padx=5, pady=(0, 5))
        
        self.scan_path_var = tk.StringVar()
        scan_entry = ttk.Entry(scan_btn_frame, textvariable=self.scan_path_var)
        scan_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        scan_entry.bind("<Return>", lambda e: self._add_scan_path())
        
        ttk.Button(scan_btn_frame, text="Browse...", command=self._browse_scan_path).pack(side="right", padx=(0, 5))
        ttk.Button(scan_btn_frame, text="Add", command=self._add_scan_path).pack(side="right", padx=(0, 5))
        ttk.Button(scan_btn_frame, text="Remove", command=self._remove_scan_path).pack(side="right")
        
        # Exclude paths
        exclude_frame = ttk.LabelFrame(scrollable_frame, text="Exclude Paths")
        exclude_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Label(exclude_frame, text="Directories to exclude:").pack(anchor="w", padx=5, pady=(5, 0))
        
        # Exclude paths listbox with scrollbar
        exclude_list_frame = ttk.Frame(exclude_frame)
        exclude_list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.exclude_paths_listbox = tk.Listbox(exclude_list_frame, height=6)
        exclude_scrollbar = ttk.Scrollbar(exclude_list_frame, orient="vertical", command=self.exclude_paths_listbox.yview)
        self.exclude_paths_listbox.configure(yscrollcommand=exclude_scrollbar.set)
        
        self.exclude_paths_listbox.pack(side="left", fill="both", expand=True)
        exclude_scrollbar.pack(side="right", fill="y")
        
        # Exclude paths buttons
        exclude_btn_frame = ttk.Frame(exclude_frame)
        exclude_btn_frame.pack(fill="x", padx=5, pady=(0, 5))
        
        self.exclude_path_var = tk.StringVar()
        exclude_entry = ttk.Entry(exclude_btn_frame, textvariable=self.exclude_path_var)
        exclude_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        exclude_entry.bind("<Return>", lambda e: self._add_exclude_path())
        
        ttk.Button(exclude_btn_frame, text="Browse...", command=self._browse_exclude_path).pack(side="right", padx=(0, 5))
        ttk.Button(exclude_btn_frame, text="Add", command=self._add_exclude_path).pack(side="right", padx=(0, 5))
        ttk.Button(exclude_btn_frame, text="Remove", command=self._remove_exclude_path).pack(side="right")
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_patterns_tab(self):
        """Create patterns configuration tab"""
        patterns_frame = ttk.Frame(self.notebook)
        self.notebook.add(patterns_frame, text="Patterns")
        
        # Include patterns
        include_frame = ttk.LabelFrame(patterns_frame, text="Include Patterns")
        include_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Label(include_frame, text="File patterns to include (glob patterns):").pack(anchor="w", padx=5, pady=(5, 0))
        
        # Include patterns listbox
        include_list_frame = ttk.Frame(include_frame)
        include_list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.include_patterns_listbox = tk.Listbox(include_list_frame)
        include_scrollbar = ttk.Scrollbar(include_list_frame, orient="vertical", command=self.include_patterns_listbox.yview)
        self.include_patterns_listbox.configure(yscrollcommand=include_scrollbar.set)
        
        self.include_patterns_listbox.pack(side="left", fill="both", expand=True)
        include_scrollbar.pack(side="right", fill="y")
        
        # Include patterns buttons
        include_btn_frame = ttk.Frame(include_frame)
        include_btn_frame.pack(fill="x", padx=5, pady=(0, 5))
        
        self.include_pattern_var = tk.StringVar()
        include_entry = ttk.Entry(include_btn_frame, textvariable=self.include_pattern_var)
        include_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        include_entry.bind("<Return>", lambda e: self._add_include_pattern())
        
        ttk.Button(include_btn_frame, text="Add", command=self._add_include_pattern).pack(side="right", padx=(0, 5))
        ttk.Button(include_btn_frame, text="Remove", command=self._remove_include_pattern).pack(side="right")
        
        # Exclude patterns
        exclude_patterns_frame = ttk.LabelFrame(patterns_frame, text="Exclude Patterns")
        exclude_patterns_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Label(exclude_patterns_frame, text="File patterns to exclude (glob patterns):").pack(anchor="w", padx=5, pady=(5, 0))
        
        # Exclude patterns listbox
        exclude_patterns_list_frame = ttk.Frame(exclude_patterns_frame)
        exclude_patterns_list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.exclude_patterns_listbox = tk.Listbox(exclude_patterns_list_frame)
        exclude_patterns_scrollbar = ttk.Scrollbar(exclude_patterns_list_frame, orient="vertical", command=self.exclude_patterns_listbox.yview)
        self.exclude_patterns_listbox.configure(yscrollcommand=exclude_patterns_scrollbar.set)
        
        self.exclude_patterns_listbox.pack(side="left", fill="both", expand=True)
        exclude_patterns_scrollbar.pack(side="right", fill="y")
        
        # Exclude patterns buttons
        exclude_patterns_btn_frame = ttk.Frame(exclude_patterns_frame)
        exclude_patterns_btn_frame.pack(fill="x", padx=5, pady=(0, 5))
        
        self.exclude_pattern_var = tk.StringVar()
        exclude_patterns_entry = ttk.Entry(exclude_patterns_btn_frame, textvariable=self.exclude_pattern_var)
        exclude_patterns_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        exclude_patterns_entry.bind("<Return>", lambda e: self._add_exclude_pattern())
        
        ttk.Button(exclude_patterns_btn_frame, text="Add", command=self._add_exclude_pattern).pack(side="right", padx=(0, 5))
        ttk.Button(exclude_patterns_btn_frame, text="Remove", command=self._remove_exclude_pattern).pack(side="right")
        
        # Common patterns buttons
        common_frame = ttk.Frame(patterns_frame)
        common_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(common_frame, text="Quick Add:").pack(side="left")
        ttk.Button(common_frame, text="Common Include", command=self._add_common_include_patterns).pack(side="left", padx=(10, 5))
        ttk.Button(common_frame, text="Common Exclude", command=self._add_common_exclude_patterns).pack(side="left")
    
    def _create_performance_tab(self):
        """Create performance configuration tab"""
        perf_frame = ttk.Frame(self.notebook)
        self.notebook.add(perf_frame, text="Performance")
        
        # Performance settings
        settings_frame = ttk.LabelFrame(perf_frame, text="Performance Settings")
        settings_frame.pack(fill="x", padx=5, pady=5)
        
        # Worker threads
        ttk.Label(settings_frame, text="Worker Threads:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.worker_threads_var = tk.StringVar()
        worker_threads_spin = ttk.Spinbox(settings_frame, from_=1, to=32, textvariable=self.worker_threads_var, width=10)
        worker_threads_spin.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(settings_frame, text="(1-32 threads for parallel processing)").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        
        # Hash chunk size
        ttk.Label(settings_frame, text="Hash Chunk Size:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.hash_chunk_var = tk.StringVar()
        hash_chunk_spin = ttk.Spinbox(settings_frame, from_=1024, to=1048576, increment=1024, textvariable=self.hash_chunk_var, width=10)
        hash_chunk_spin.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(settings_frame, text="(bytes, larger = faster but more memory)").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        
        # Max files
        ttk.Label(settings_frame, text="Max Files to Process:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.max_files_var = tk.StringVar()
        max_files_spin = ttk.Spinbox(settings_frame, from_=0, to=1000000, textvariable=self.max_files_var, width=10)
        max_files_spin.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(settings_frame, text="(0 = unlimited)").grid(row=2, column=2, sticky="w", padx=5, pady=5)
        
        settings_frame.grid_columnconfigure(2, weight=1)
        
        # Performance tips
        tips_frame = ttk.LabelFrame(perf_frame, text="Performance Tips")
        tips_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        tips_text = """
Performance Tips:

• Worker Threads: Use 2-4x your CPU cores for I/O bound tasks
• Hash Chunk Size: 64KB (65536) is usually optimal for most systems
• Max Files: Set a limit if you want to test with a subset of files
• Exclude Patterns: Add more specific patterns to skip unnecessary files
• Scan Paths: Be selective about which directories to scan

Memory Usage:
• Each worker thread may use up to Hash Chunk Size in memory
• Total memory ≈ Worker Threads × Hash Chunk Size
• Monitor system resources during large scans
        """
        
        tips_label = tk.Label(tips_frame, text=tips_text.strip(), justify="left", anchor="nw")
        tips_label.pack(fill="both", expand=True, padx=5, pady=5)
    
    def _create_advanced_tab(self):
        """Create advanced configuration tab"""
        advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(advanced_frame, text="Advanced")
        
        # Raw YAML editor
        editor_frame = ttk.LabelFrame(advanced_frame, text="Raw YAML Configuration")
        editor_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Text editor with scrollbar
        editor_container = ttk.Frame(editor_frame)
        editor_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.yaml_editor = scrolledtext.ScrolledText(editor_container, wrap=tk.NONE, font=("Courier", 10))
        self.yaml_editor.pack(fill="both", expand=True)
        
        # Editor buttons
        editor_btn_frame = ttk.Frame(editor_frame)
        editor_btn_frame.pack(fill="x", padx=5, pady=(0, 5))
        
        ttk.Button(editor_btn_frame, text="Refresh from Form", command=self._refresh_yaml_from_form).pack(side="left")
        ttk.Button(editor_btn_frame, text="Apply to Form", command=self._apply_yaml_to_form).pack(side="left", padx=(5, 0))
        ttk.Button(editor_btn_frame, text="Validate", command=self._validate_yaml).pack(side="left", padx=(5, 0))
        
        # Validation frame
        validation_frame = ttk.LabelFrame(advanced_frame, text="Validation")
        validation_frame.pack(fill="x", padx=5, pady=5)
        
        self.validation_text = tk.Text(validation_frame, height=4, state="disabled")
        validation_scrollbar = ttk.Scrollbar(validation_frame, orient="vertical", command=self.validation_text.yview)
        self.validation_text.configure(yscrollcommand=validation_scrollbar.set)
        
        self.validation_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        validation_scrollbar.pack(side="right", fill="y", pady=5)
    
    def _load_configuration(self):
        """Load configuration into the dialog"""
        try:
            self.current_config = self.config_manager.load_config()
            
            # Load logging settings
            logging_config = self.current_config.get('logging', {})
            self.log_level_var.set(logging_config.get('level', 'INFO'))
            
            # Load paths
            paths_config = self.current_config.get('paths', {})
            
            # Scan paths
            self.scan_paths_listbox.delete(0, tk.END)
            for path in paths_config.get('scan', []):
                self.scan_paths_listbox.insert(tk.END, path)
            
            # Exclude paths
            self.exclude_paths_listbox.delete(0, tk.END)
            for path in paths_config.get('exclude', []):
                self.exclude_paths_listbox.insert(tk.END, path)
            
            # Include patterns
            self.include_patterns_listbox.delete(0, tk.END)
            for pattern in paths_config.get('include', []):
                self.include_patterns_listbox.insert(tk.END, pattern)
            
            # Exclude patterns
            self.exclude_patterns_listbox.delete(0, tk.END)
            for pattern in paths_config.get('exclude_patterns', []):
                self.exclude_patterns_listbox.insert(tk.END, pattern)
            
            # Load performance settings
            perf_config = self.current_config.get('performance', {})
            self.worker_threads_var.set(str(perf_config.get('worker_threads', 4)))
            self.hash_chunk_var.set(str(perf_config.get('hash_chunk_size', 65536)))
            self.max_files_var.set(str(perf_config.get('max_files', 0)))
            
            # Load YAML editor
            self._refresh_yaml_from_form()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {str(e)}", parent=self.dialog)
    
    def _refresh_yaml_from_form(self):
        """Refresh YAML editor from form data"""
        try:
            config = self._build_config_from_form()
            yaml_content = self.config_manager._format_yaml_for_display(config)
            
            self.yaml_editor.delete(1.0, tk.END)
            self.yaml_editor.insert(1.0, yaml_content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh YAML: {str(e)}", parent=self.dialog)
    
    def _apply_yaml_to_form(self):
        """Apply YAML editor content to form"""
        try:
            import yaml
            yaml_content = self.yaml_editor.get(1.0, tk.END)
            config = yaml.safe_load(yaml_content)
            
            if config:
                self.current_config = config
                self._load_configuration()
                messagebox.showinfo("Success", "YAML applied to form successfully.", parent=self.dialog)
            else:
                messagebox.showwarning("Warning", "YAML content is empty or invalid.", parent=self.dialog)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply YAML: {str(e)}", parent=self.dialog)
    
    def _validate_yaml(self):
        """Validate YAML content"""
        try:
            import yaml
            yaml_content = self.yaml_editor.get(1.0, tk.END)
            config = yaml.safe_load(yaml_content)
            
            if config:
                errors = self.config_manager.validate_config(config)
                
                self.validation_text.config(state="normal")
                self.validation_text.delete(1.0, tk.END)
                
                if errors:
                    self.validation_text.insert(tk.END, "Validation Errors:\n")
                    for error in errors:
                        self.validation_text.insert(tk.END, f"• {error}\n")
                else:
                    self.validation_text.insert(tk.END, "✓ Configuration is valid!")
                
                self.validation_text.config(state="disabled")
            else:
                self.validation_text.config(state="normal")
                self.validation_text.delete(1.0, tk.END)
                self.validation_text.insert(tk.END, "Error: YAML content is empty or invalid")
                self.validation_text.config(state="disabled")
                
        except Exception as e:
            self.validation_text.config(state="normal")
            self.validation_text.delete(1.0, tk.END)
            self.validation_text.insert(tk.END, f"YAML Syntax Error: {str(e)}")
            self.validation_text.config(state="disabled")
    
    def _build_config_from_form(self) -> Dict[str, Any]:
        """Build configuration dictionary from form data"""
        config = {
            'logging': {
                'level': self.log_level_var.get()
            },
            'paths': {
                'scan': list(self.scan_paths_listbox.get(0, tk.END)),
                'exclude': list(self.exclude_paths_listbox.get(0, tk.END)),
                'include': list(self.include_patterns_listbox.get(0, tk.END)),
                'exclude_patterns': list(self.exclude_patterns_listbox.get(0, tk.END))
            },
            'performance': {
                'worker_threads': int(self.worker_threads_var.get() or 4),
                'hash_chunk_size': int(self.hash_chunk_var.get() or 65536),
                'max_files': int(self.max_files_var.get() or 0)
            }
        }
        return config
    
    # Path management methods
    def _browse_scan_path(self):
        """Browse for scan path"""
        path = filedialog.askdirectory(title="Select Directory to Scan", parent=self.dialog)
        if path:
            self.scan_path_var.set(path)
    
    def _add_scan_path(self):
        """Add scan path to list"""
        path = self.scan_path_var.get().strip()
        if path and path not in self.scan_paths_listbox.get(0, tk.END):
            self.scan_paths_listbox.insert(tk.END, path)
            self.scan_path_var.set("")
    
    def _remove_scan_path(self):
        """Remove selected scan path"""
        selection = self.scan_paths_listbox.curselection()
        if selection:
            self.scan_paths_listbox.delete(selection[0])
    
    def _browse_exclude_path(self):
        """Browse for exclude path"""
        path = filedialog.askdirectory(title="Select Directory to Exclude", parent=self.dialog)
        if path:
            self.exclude_path_var.set(path)
    
    def _add_exclude_path(self):
        """Add exclude path to list"""
        path = self.exclude_path_var.get().strip()
        if path and path not in self.exclude_paths_listbox.get(0, tk.END):
            self.exclude_paths_listbox.insert(tk.END, path)
            self.exclude_path_var.set("")
    
    def _remove_exclude_path(self):
        """Remove selected exclude path"""
        selection = self.exclude_paths_listbox.curselection()
        if selection:
            self.exclude_paths_listbox.delete(selection[0])
    
    # Pattern management methods
    def _add_include_pattern(self):
        """Add include pattern to list"""
        pattern = self.include_pattern_var.get().strip()
        if pattern and pattern not in self.include_patterns_listbox.get(0, tk.END):
            self.include_patterns_listbox.insert(tk.END, pattern)
            self.include_pattern_var.set("")
    
    def _remove_include_pattern(self):
        """Remove selected include pattern"""
        selection = self.include_patterns_listbox.curselection()
        if selection:
            self.include_patterns_listbox.delete(selection[0])
    
    def _add_exclude_pattern(self):
        """Add exclude pattern to list"""
        pattern = self.exclude_pattern_var.get().strip()
        if pattern and pattern not in self.exclude_patterns_listbox.get(0, tk.END):
            self.exclude_patterns_listbox.insert(tk.END, pattern)
            self.exclude_pattern_var.set("")
    
    def _remove_exclude_pattern(self):
        """Remove selected exclude pattern"""
        selection = self.exclude_patterns_listbox.curselection()
        if selection:
            self.exclude_patterns_listbox.delete(selection[0])
    
    def _add_common_include_patterns(self):
        """Add common include patterns"""
        common_patterns = [
            "*.conf", "*.config", "*.cfg", "*.ini", "*.json", "*.yaml", "*.yml",
            "*.xml", "*.properties", "*.log", "*.txt", "*.sh", "*.py", "*.js"
        ]
        
        existing = set(self.include_patterns_listbox.get(0, tk.END))
        for pattern in common_patterns:
            if pattern not in existing:
                self.include_patterns_listbox.insert(tk.END, pattern)
    
    def _add_common_exclude_patterns(self):
        """Add common exclude patterns"""
        common_patterns = [
            "*/tmp/*", "*/temp/*", "*/.git/*", "*/node_modules/*", "*/__pycache__/*",
            "*.pyc", "*.pyo", "*.class", "*.o", "*.so", "*.dll", "*/cache/*", "*/logs/*.log.*"
        ]
        
        existing = set(self.exclude_patterns_listbox.get(0, tk.END))
        for pattern in common_patterns:
            if pattern not in existing:
                self.exclude_patterns_listbox.insert(tk.END, pattern)
    
    # File operations
    def _load_from_file(self):
        """Load configuration from file"""
        file_path = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")],
            parent=self.dialog
        )
        
        if file_path:
            config = self.config_manager.import_config(file_path)
            if config:
                self.current_config = config
                self._load_configuration()
                messagebox.showinfo("Success", f"Configuration loaded from {file_path}", parent=self.dialog)
            else:
                messagebox.showerror("Error", "Failed to load configuration file", parent=self.dialog)
    
    def _save_to_file(self):
        """Save configuration to file"""
        file_path = filedialog.asksaveasfilename(
            title="Save Configuration",
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml *.yml"), ("All files", "*.*")],
            parent=self.dialog
        )
        
        if file_path:
            try:
                config = self._build_config_from_form()
                if self.config_manager.export_config(config, file_path):
                    messagebox.showinfo("Success", f"Configuration saved to {file_path}", parent=self.dialog)
                else:
                    messagebox.showerror("Error", "Failed to save configuration", parent=self.dialog)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save configuration: {str(e)}", parent=self.dialog)
    
    def _reset_to_defaults(self):
        """Reset configuration to defaults"""
        if messagebox.askyesno("Reset Configuration", 
                              "Reset all settings to default values?\nThis cannot be undone.", 
                              parent=self.dialog):
            self.current_config = self.config_manager.default_config.copy()
            self._load_configuration()
    
    # Dialog event handlers
    def _on_ok(self):
        """Handle OK button"""
        if self._validate_and_apply():
            self.result = "ok"
            self.dialog.destroy()
    
    def _on_apply(self):
        """Handle Apply button"""
        self._validate_and_apply()
    
    def _on_cancel(self):
        """Handle Cancel button"""
        self.result = "cancel"
        self.dialog.destroy()
    
    def _validate_and_apply(self) -> bool:
        """Validate and apply configuration"""
        try:
            config = self._build_config_from_form()
            errors = self.config_manager.validate_config(config)
            
            if errors:
                error_msg = "Configuration validation failed:\n\n" + "\n".join(f"• {error}" for error in errors)
                messagebox.showerror("Validation Error", error_msg, parent=self.dialog)
                return False
            
            # Save configuration
            if self.config_manager.save_config(config):
                self.current_config = config
                messagebox.showinfo("Success", "Configuration applied successfully!", parent=self.dialog)
                return True
            else:
                messagebox.showerror("Error", "Failed to save configuration", parent=self.dialog)
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply configuration: {str(e)}", parent=self.dialog)
            return False
    
    def get_configuration(self) -> Optional[Dict[str, Any]]:
        """Get the current configuration"""
        return self.current_config if self.result == "ok" else None
