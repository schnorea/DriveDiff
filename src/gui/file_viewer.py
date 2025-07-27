"""
File Viewer Module
Side-by-side file content viewer with diff highlighting
"""

import tkinter as tk
from tkinter import ttk, font
import os
import difflib
from typing import Optional, List, Tuple
from ..core.file_comparator import FileComparator, FileDifference

class FileViewer:
    """Side-by-side file content viewer"""
    
    def __init__(self, parent: tk.Widget, config_manager=None):
        """
        Initialize the file viewer
        
        Args:
            parent: Parent widget
            config_manager: Optional YAML config manager for loading UI settings
        """
        self.parent = parent
        self.config_manager = config_manager
        self.file_comparator = FileComparator()
        self.current_left_path: Optional[str] = None
        self.current_right_path: Optional[str] = None
        self.current_diff: Optional[FileDifference] = None
        
        # Custom names for left and right panels
        self.left_panel_name = "Left File"
        self.right_panel_name = "Right File"
        
        # Load panel names from config if available
        self._load_ui_settings()
        
        self._create_widgets()
        self._setup_styles()
    
    def _create_widgets(self):
        """Create the file viewer widgets"""
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # File info frame
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        
        # Left file info
        self.left_info_frame = ttk.LabelFrame(info_frame, text=self.left_panel_name)
        self.left_info_frame.grid(row=0, column=0, sticky="ew", padx=(0, 2))
        
        self.left_path_label = ttk.Label(self.left_info_frame, text="No file selected", foreground="gray")
        self.left_path_label.pack(anchor="w", padx=5, pady=2)
        
        self.left_details_label = ttk.Label(self.left_info_frame, text="", font=("TkDefaultFont", 8))
        self.left_details_label.pack(anchor="w", padx=5, pady=2)
        
        # Right file info
        self.right_info_frame = ttk.LabelFrame(info_frame, text=self.right_panel_name)
        self.right_info_frame.grid(row=0, column=1, sticky="ew", padx=(2, 0))
        
        self.right_path_label = ttk.Label(self.right_info_frame, text="No file selected", foreground="gray")
        self.right_path_label.pack(anchor="w", padx=5, pady=2)
        
        self.right_details_label = ttk.Label(self.right_info_frame, text="", font=("TkDefaultFont", 8))
        self.right_details_label.pack(anchor="w", padx=5, pady=2)
        
        # Content viewer (PanedWindow for resizable panes)
        self.content_paned = ttk.PanedWindow(main_frame, orient="horizontal")
        self.content_paned.grid(row=1, column=0, sticky="nsew")
        
        # Left content frame
        left_content_frame = ttk.Frame(self.content_paned)
        self._create_text_widget(left_content_frame, "left")
        self.content_paned.add(left_content_frame, weight=1)
        
        # Right content frame
        right_content_frame = ttk.Frame(self.content_paned)
        self._create_text_widget(right_content_frame, "right")
        self.content_paned.add(right_content_frame, weight=1)
        
        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, sticky="ew", pady=(5, 0))
        
        # View mode selection
        ttk.Label(control_frame, text="View:").pack(side="left", padx=(0, 5))
        
        self.view_mode = tk.StringVar(value="side_by_side")
        view_combo = ttk.Combobox(control_frame, textvariable=self.view_mode, 
                                 values=["side_by_side", "unified_diff", "hex_view"],
                                 state="readonly", width=15)
        view_combo.pack(side="left", padx=(0, 10))
        view_combo.bind("<<ComboboxSelected>>", self._on_view_mode_changed)
        
        # Sync scrolling checkbox
        self.sync_scrolling = tk.BooleanVar(value=True)
        sync_check = ttk.Checkbutton(control_frame, text="Sync Scrolling", 
                                   variable=self.sync_scrolling, 
                                   command=self._toggle_sync_scrolling)
        sync_check.pack(side="left", padx=(0, 10))
        
        # Font size controls
        ttk.Label(control_frame, text="Font Size:").pack(side="left", padx=(10, 5))
        font_frame = ttk.Frame(control_frame)
        font_frame.pack(side="left")
        
        ttk.Button(font_frame, text="-", width=3, command=self._decrease_font_size).pack(side="left")
        self.font_size_var = tk.StringVar(value="10")
        font_size_label = ttk.Label(font_frame, textvariable=self.font_size_var, width=3)
        font_size_label.pack(side="left", padx=5)
        ttk.Button(font_frame, text="+", width=3, command=self._increase_font_size).pack(side="left")
        
        # Panel names button
        ttk.Button(control_frame, text="Panel Names...", 
                  command=self._show_panel_names_dialog).pack(side="left", padx=(10, 0))
        
        # Apply initial settings from config
        self._apply_initial_settings()
    
    def _apply_initial_settings(self):
        """Apply initial settings loaded from config"""
        if hasattr(self, '_initial_sync_setting'):
            self.sync_scrolling.set(self._initial_sync_setting)
        if hasattr(self, '_initial_font_size'):
            self.font_size_var.set(str(self._initial_font_size))
            self._set_font_size(self._initial_font_size)
        if hasattr(self, '_initial_view_mode'):
            self.view_mode.set(self._initial_view_mode)
    
    def _create_text_widget(self, parent: tk.Widget, side: str):
        """Create a text widget with scrollbars"""
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        
        # Create text widget
        text_widget = tk.Text(frame, wrap="none", font=("Courier", 10), 
                            state="disabled", cursor="arrow")
        text_widget.grid(row=0, column=0, sticky="nsew")
        
        # Create scrollbars
        v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
        h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=text_widget.xview)
        
        text_widget.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Store reference
        if side == "left":
            self.left_text = text_widget
            self.left_v_scroll = v_scrollbar
            self.left_h_scroll = h_scrollbar
        else:
            self.right_text = text_widget
            self.right_v_scroll = v_scrollbar
            self.right_h_scroll = h_scrollbar
        
        # Bind scrolling events for synchronization
        text_widget.bind("<MouseWheel>", lambda e: self._on_mousewheel(e, side))
        text_widget.bind("<Button-4>", lambda e: self._on_mousewheel(e, side))
        text_widget.bind("<Button-5>", lambda e: self._on_mousewheel(e, side))
        
        # Bind scrollbar events for synchronization
        if side == "left":
            v_scrollbar.configure(command=lambda *args: self._on_v_scroll("left", *args))
            h_scrollbar.configure(command=lambda *args: self._on_h_scroll("left", *args))
        else:
            v_scrollbar.configure(command=lambda *args: self._on_v_scroll("right", *args))
            h_scrollbar.configure(command=lambda *args: self._on_h_scroll("right", *args))
    
    def _setup_styles(self):
        """Setup text widget styles and tags"""
        # Configure tags for syntax highlighting and diff visualization
        for text_widget in [self.left_text, self.right_text]:
            # Diff highlighting tags
            text_widget.tag_configure("added", background="#d4edd6", foreground="#155724")
            text_widget.tag_configure("removed", background="#f8d7da", foreground="#721c24")
            text_widget.tag_configure("modified", background="#fff3cd", foreground="#856404")
            text_widget.tag_configure("empty", background="#f8f9fa", foreground="#6c757d")
            text_widget.tag_configure("line_number", foreground="#6c757d", font=("Courier", 8))
            
            # Syntax highlighting tags (basic)
            text_widget.tag_configure("keyword", foreground="#0000ff")
            text_widget.tag_configure("string", foreground="#008000")
            text_widget.tag_configure("comment", foreground="#808080")
    
    def display_files(self, left_path: Optional[str], right_path: Optional[str], file_diff: Optional[FileDifference]):
        """
        Display files for comparison
        
        Args:
            left_path: Path to left file
            right_path: Path to right file
            file_diff: FileDifference object
        """
        self.current_left_path = left_path
        self.current_right_path = right_path
        self.current_diff = file_diff
        
        # Update file info
        self._update_file_info()
        
        # Display content based on view mode
        view_mode = self.view_mode.get()
        if view_mode == "side_by_side":
            self._display_side_by_side()
        elif view_mode == "unified_diff":
            self._display_unified_diff()
        elif view_mode == "hex_view":
            self._display_hex_view()
    
    def _update_file_info(self):
        """Update file information labels"""
        # Left file info
        if self.current_left_path and os.path.exists(self.current_left_path):
            self.left_path_label.config(text=os.path.basename(self.current_left_path), foreground="black")
            
            if self.current_diff and self.current_diff.left_info:
                info = self.current_diff.left_info
                size_str = self._format_size(info.size)
                modified_str = info.modified_time.strftime('%Y-%m-%d %H:%M:%S')
                details = f"Size: {size_str} | Modified: {modified_str} | Permissions: {info.permissions}"
                self.left_details_label.config(text=details)
            else:
                self.left_details_label.config(text="")
        else:
            self.left_path_label.config(text="File not found", foreground="red")
            self.left_details_label.config(text="")
        
        # Right file info
        if self.current_right_path and os.path.exists(self.current_right_path):
            self.right_path_label.config(text=os.path.basename(self.current_right_path), foreground="black")
            
            if self.current_diff and self.current_diff.right_info:
                info = self.current_diff.right_info
                size_str = self._format_size(info.size)
                modified_str = info.modified_time.strftime('%Y-%m-%d %H:%M:%S')
                details = f"Size: {size_str} | Modified: {modified_str} | Permissions: {info.permissions}"
                self.right_details_label.config(text=details)
            else:
                self.right_details_label.config(text="")
        else:
            self.right_path_label.config(text="File not found", foreground="red")
            self.right_details_label.config(text="")
    
    def _display_side_by_side(self):
        """Display files side by side with diff highlighting"""
        # Clear existing content
        self._clear_text_widgets()
        
        left_lines = []
        right_lines = []
        
        # Load file contents
        if self.current_left_path and os.path.exists(self.current_left_path):
            left_content = self._load_file_content(self.current_left_path)
            if left_content is not None:
                left_lines = left_content.splitlines()
        
        if self.current_right_path and os.path.exists(self.current_right_path):
            right_content = self._load_file_content(self.current_right_path)
            if right_content is not None:
                right_lines = right_content.splitlines()
        
        # If both files exist and are text, perform line-by-line comparison
        if (left_lines and right_lines and 
            self.current_left_path and self.current_right_path and
            self.file_comparator._is_text_file(self.current_left_path) and
            self.file_comparator._is_text_file(self.current_right_path)):
            
            self._display_side_by_side_with_diff(left_lines, right_lines)
        else:
            # Display files without diff highlighting
            if left_lines:
                self._set_text_content(self.left_text, '\n'.join(left_lines))
            if right_lines:
                self._set_text_content(self.right_text, '\n'.join(right_lines))
    
    def _display_side_by_side_with_diff(self, left_lines: List[str], right_lines: List[str]):
        """Display files side by side with line-by-line diff highlighting"""
        # Create a sequence matcher for line-by-line comparison
        matcher = difflib.SequenceMatcher(None, left_lines, right_lines)
        
        # Prepare aligned content for both sides
        left_display_lines = []
        right_display_lines = []
        left_line_tags = []
        right_line_tags = []
        
        for opcode in matcher.get_opcodes():
            tag, i1, i2, j1, j2 = opcode
            
            if tag == 'equal':
                # Lines are identical
                for i in range(i1, i2):
                    left_display_lines.append(left_lines[i])
                    left_line_tags.append('equal')
                    right_display_lines.append(right_lines[j1 + (i - i1)])
                    right_line_tags.append('equal')
            
            elif tag == 'delete':
                # Lines only in left file
                for i in range(i1, i2):
                    left_display_lines.append(left_lines[i])
                    left_line_tags.append('removed')
                    right_display_lines.append("")  # Empty line on right
                    right_line_tags.append('empty')
            
            elif tag == 'insert':
                # Lines only in right file
                for j in range(j1, j2):
                    left_display_lines.append("")  # Empty line on left
                    left_line_tags.append('empty')
                    right_display_lines.append(right_lines[j])
                    right_line_tags.append('added')
            
            elif tag == 'replace':
                # Lines are different
                left_count = i2 - i1
                right_count = j2 - j1
                max_count = max(left_count, right_count)
                
                for k in range(max_count):
                    if k < left_count:
                        left_display_lines.append(left_lines[i1 + k])
                        left_line_tags.append('modified')
                    else:
                        left_display_lines.append("")
                        left_line_tags.append('empty')
                    
                    if k < right_count:
                        right_display_lines.append(right_lines[j1 + k])
                        right_line_tags.append('modified')
                    else:
                        right_display_lines.append("")
                        right_line_tags.append('empty')
        
        # Display content with highlighting
        self._set_text_content_with_tags(self.left_text, left_display_lines, left_line_tags)
        self._set_text_content_with_tags(self.right_text, right_display_lines, right_line_tags)
    
    def _display_unified_diff(self):
        """Display unified diff view"""
        self._clear_text_widgets()
        
        if not (self.current_left_path and self.current_right_path):
            return
        
        # Generate diff
        diff_lines = self.file_comparator.get_text_diff(self.current_left_path, self.current_right_path)
        
        if diff_lines:
            diff_content = "".join(diff_lines)
            
            # Display diff in left pane, hide right pane
            self._set_text_content(self.left_text, diff_content)
            self._apply_diff_line_highlighting(self.left_text, diff_lines)
            
            # Hide right pane for unified view
            self.content_paned.forget(1)
        else:
            self._set_text_content(self.left_text, "Files are identical or not text files")
    
    def _display_hex_view(self):
        """Display hex view of files"""
        self._clear_text_widgets()
        
        # Load and display left file as hex
        if self.current_left_path and os.path.exists(self.current_left_path):
            hex_content = self._load_file_as_hex(self.current_left_path)
            self._set_text_content(self.left_text, hex_content)
        
        # Load and display right file as hex
        if self.current_right_path and os.path.exists(self.current_right_path):
            hex_content = self._load_file_as_hex(self.current_right_path)
            self._set_text_content(self.right_text, hex_content)
    
    def _load_file_content(self, file_path: str) -> Optional[str]:
        """Load file content as text"""
        try:
            if not os.path.exists(file_path):
                return f"File not found: {file_path}"
            
            if self.file_comparator._is_text_file(file_path):
                return self.file_comparator._read_text_file(file_path)
            else:
                return f"Binary file: {os.path.basename(file_path)}\nSize: {self._format_size(os.path.getsize(file_path))}"
        except PermissionError as e:
            return f"Permission denied: Cannot read {os.path.basename(file_path)}\n\nThis file requires elevated permissions to access.\nTry running the application with appropriate permissions."
        except Exception as e:
            return f"Error loading file: {str(e)}"
    
    def _load_file_as_hex(self, file_path: str, max_bytes: int = 1024 * 1024) -> str:
        """Load file content as hex dump"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read(max_bytes)
            
            hex_lines = []
            for i in range(0, len(data), 16):
                chunk = data[i:i+16]
                hex_part = ' '.join(f'{b:02x}' for b in chunk)
                ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
                hex_lines.append(f'{i:08x}  {hex_part:<48} |{ascii_part}|')
            
            result = '\n'.join(hex_lines)
            if len(data) == max_bytes:
                result += f"\n\n[Truncated at {max_bytes} bytes]"
            
            return result
            
        except Exception as e:
            return f"Error loading file as hex: {str(e)}"
    
    def _set_text_content(self, text_widget: tk.Text, content: str):
        """Set content in a text widget"""
        text_widget.config(state="normal")
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, content)
        text_widget.config(state="disabled")
    
    def _set_text_content_with_tags(self, text_widget: tk.Text, lines: List[str], line_tags: List[str]):
        """Set text content with line-by-line tags for diff highlighting"""
        text_widget.config(state="normal")
        text_widget.delete(1.0, tk.END)
        
        for i, (line, tag) in enumerate(zip(lines, line_tags)):
            line_num = i + 1
            start_pos = f"{line_num}.0"
            
            # Insert line content
            text_widget.insert(tk.END, line + "\n")
            
            # Apply tag to the entire line if it's not 'equal'
            if tag != 'equal':
                end_pos = f"{line_num}.end"
                text_widget.tag_add(tag, start_pos, end_pos)
        
        text_widget.config(state="disabled")
    
    def _clear_text_widgets(self):
        """Clear both text widgets"""
        self.left_text.config(state="normal")
        self.right_text.config(state="normal")
        
        self.left_text.delete(1.0, tk.END)
        self.right_text.delete(1.0, tk.END)
        
        self.left_text.config(state="disabled")
        self.right_text.config(state="disabled")
        
        # Restore right pane if it was hidden
        if len(self.content_paned.panes()) == 1:
            right_content_frame = self.right_text.master.master
            self.content_paned.add(right_content_frame, weight=1)
    
    def _apply_diff_highlighting(self):
        """Apply diff highlighting to text widgets"""
        # This is a simplified implementation
        # In a full implementation, you would parse the diff and apply appropriate tags
        pass
    
    def _apply_diff_line_highlighting(self, text_widget: tk.Text, diff_lines: List[str]):
        """Apply highlighting to diff lines"""
        text_widget.config(state="normal")
        
        for i, line in enumerate(diff_lines, 1):
            line_start = f"{i}.0"
            line_end = f"{i}.end"
            
            if line.startswith('+'):
                text_widget.tag_add("added", line_start, line_end)
            elif line.startswith('-'):
                text_widget.tag_add("removed", line_start, line_end)
            elif line.startswith('@@'):
                text_widget.tag_add("modified", line_start, line_end)
        
        text_widget.config(state="disabled")
    
    def _on_view_mode_changed(self, event=None):
        """Handle view mode change"""
        if self.current_left_path or self.current_right_path:
            self.display_files(self.current_left_path, self.current_right_path, self.current_diff)
    
    def _toggle_sync_scrolling(self):
        """Toggle synchronized scrolling"""
        if self.sync_scrolling.get():
            # Sync current scroll positions when enabled
            self._sync_scroll_positions()
    
    def _on_mousewheel(self, event, side: str):
        """Handle mouse wheel scrolling"""
        if self.sync_scrolling.get():
            # Calculate scroll amount
            delta = 0
            if event.num == 4 or event.delta > 0:
                delta = -1
            elif event.num == 5 or event.delta < 0:
                delta = 1
            
            # Scroll both widgets synchronously
            for widget in [self.left_text, self.right_text]:
                widget.yview_scroll(delta, "units")
            
            return "break"  # Prevent default scrolling
        else:
            # Allow normal scrolling for the current widget only
            current_widget = self.left_text if side == "left" else self.right_text
            delta = 0
            if event.num == 4 or event.delta > 0:
                delta = -1
            elif event.num == 5 or event.delta < 0:
                delta = 1
            
            current_widget.yview_scroll(delta, "units")
            return "break"
    
    def _on_v_scroll(self, side: str, *args):
        """Handle vertical scrollbar scrolling"""
        if side == "left":
            self.left_text.yview(*args)
        else:
            self.right_text.yview(*args)
        
        # Sync scrolling if enabled
        if self.sync_scrolling.get():
            if side == "left":
                self.right_text.yview_moveto(self.left_text.yview()[0])
            else:
                self.left_text.yview_moveto(self.right_text.yview()[0])
    
    def _on_h_scroll(self, side: str, *args):
        """Handle horizontal scrollbar scrolling"""
        if side == "left":
            self.left_text.xview(*args)
        else:
            self.right_text.xview(*args)
        
        # Sync horizontal scrolling if enabled
        if self.sync_scrolling.get():
            if side == "left":
                self.right_text.xview_moveto(self.left_text.xview()[0])
            else:
                self.left_text.xview_moveto(self.right_text.xview()[0])
    
    def _sync_scroll_positions(self):
        """Synchronize scroll positions between text widgets"""
        if hasattr(self, 'left_text') and hasattr(self, 'right_text'):
            # Sync to the left widget's position
            left_v_pos = self.left_text.yview()[0]
            left_h_pos = self.left_text.xview()[0]
            
            self.right_text.yview_moveto(left_v_pos)
            self.right_text.xview_moveto(left_h_pos)
    
    def _increase_font_size(self):
        """Increase font size"""
        current_size = int(self.font_size_var.get())
        new_size = min(current_size + 1, 20)
        self._set_font_size(new_size)
    
    def _decrease_font_size(self):
        """Decrease font size"""
        current_size = int(self.font_size_var.get())
        new_size = max(current_size - 1, 6)
        self._set_font_size(new_size)
    
    def _set_font_size(self, size: int):
        """Set font size for both text widgets"""
        self.font_size_var.set(str(size))
        new_font = ("Courier", size)
        
        self.left_text.config(font=new_font)
        self.right_text.config(font=new_font)
    
    def clear(self):
        """Clear the file viewer"""
        self.current_left_path = None
        self.current_right_path = None
        self.current_diff = None
        
        self._clear_text_widgets()
        
        self.left_path_label.config(text="No file selected", foreground="gray")
        self.left_details_label.config(text="")
        self.right_path_label.config(text="No file selected", foreground="gray")
        self.right_details_label.config(text="")
    
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
    
    def set_panel_names(self, left_name: str, right_name: str):
        """
        Set custom names for the left and right panels
        
        Args:
            left_name: Custom name for the left panel
            right_name: Custom name for the right panel
        """
        self.left_panel_name = left_name
        self.right_panel_name = right_name
        
        # Update the LabelFrame text
        self.left_info_frame.config(text=left_name)
        self.right_info_frame.config(text=right_name)
    
    def get_panel_names(self) -> Tuple[str, str]:
        """
        Get the current panel names
        
        Returns:
            Tuple containing (left_name, right_name)
        """
        return (self.left_panel_name, self.right_panel_name)
    
    def reset_panel_names(self):
        """Reset panel names to default values"""
        self.set_panel_names("Left File", "Right File")
    
    def _show_panel_names_dialog(self):
        """Show dialog to set custom panel names"""
        try:
            print("Creating panel names dialog...")  # Debug
            
            # Get the root window
            root = self.parent.winfo_toplevel()
            
            dialog = tk.Toplevel(root)
            dialog.title("Set Panel Names")
            dialog.resizable(False, False)
            
            # Set proper dialog properties
            dialog.transient(root)
            dialog.grab_set()
            
            print("Dialog window created...")  # Debug
            
            # Center the dialog using the same approach as other working dialogs
            dialog.geometry("+%d+%d" % (root.winfo_rootx() + 50, root.winfo_rooty() + 50))
            
            # Main frame with padding
            main_frame = ttk.Frame(dialog, padding="20")
            main_frame.pack(fill="both", expand=True)
            
            # Title
            title_label = ttk.Label(main_frame, text="Customize Panel Names", 
                                   font=("TkDefaultFont", 12, "bold"))
            title_label.pack(pady=(0, 20))
            
            # Input section
            input_frame = ttk.Frame(main_frame)
            input_frame.pack(fill="x", pady=(0, 15))
            
            # Left panel name
            left_frame = ttk.Frame(input_frame)
            left_frame.pack(fill="x", pady=5)
            ttk.Label(left_frame, text="Left Panel Name:", width=16).pack(side="left")
            left_var = tk.StringVar(value=self.left_panel_name)
            left_entry = ttk.Entry(left_frame, textvariable=left_var, width=30)
            left_entry.pack(side="left", padx=(10, 0), fill="x", expand=True)
            
            # Right panel name  
            right_frame = ttk.Frame(input_frame)
            right_frame.pack(fill="x", pady=5)
            ttk.Label(right_frame, text="Right Panel Name:", width=16).pack(side="left")
            right_var = tk.StringVar(value=self.right_panel_name)
            right_entry = ttk.Entry(right_frame, textvariable=right_var, width=30)
            right_entry.pack(side="left", padx=(10, 0), fill="x", expand=True)
            
            print("Entry fields created...")  # Debug
            
            # Preset section
            preset_frame = ttk.LabelFrame(main_frame, text="Quick Presets", padding="10")
            preset_frame.pack(fill="x", pady=(0, 15))
            
            def apply_preset(left_name, right_name):
                print(f"Applying preset: {left_name}, {right_name}")  # Debug
                left_var.set(left_name)
                right_var.set(right_name)
            
            # First row of presets
            preset_row1 = ttk.Frame(preset_frame)
            preset_row1.pack(fill="x", pady=2)
            
            ttk.Button(preset_row1, text="Original / Modified", width=18,
                      command=lambda: apply_preset("Original", "Modified")).pack(side="left", padx=2)
            ttk.Button(preset_row1, text="Source / Target", width=18,
                      command=lambda: apply_preset("Source", "Target")).pack(side="left", padx=2)
            
            # Second row of presets
            preset_row2 = ttk.Frame(preset_frame)
            preset_row2.pack(fill="x", pady=2)
            
            ttk.Button(preset_row2, text="Before / After", width=18,
                      command=lambda: apply_preset("Before", "After")).pack(side="left", padx=2)
            ttk.Button(preset_row2, text="Local / Remote", width=18,
                      command=lambda: apply_preset("Local", "Remote")).pack(side="left", padx=2)
            
            # Third row of presets
            preset_row3 = ttk.Frame(preset_frame)
            preset_row3.pack(fill="x", pady=2)
            
            ttk.Button(preset_row3, text="Old / New", width=18,
                      command=lambda: apply_preset("Old", "New")).pack(side="left", padx=2)
            ttk.Button(preset_row3, text="Reset to Default", width=18,
                      command=lambda: apply_preset("Left File", "Right File")).pack(side="left", padx=2)
            
            print("Preset buttons created...")  # Debug
            
            # Button frame
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill="x", pady=(15, 0))
            
            def apply_names():
                print("Apply button clicked...")  # Debug
                left_name = left_var.get().strip()
                right_name = right_var.get().strip()
                
                if not left_name:
                    left_name = "Left File"
                if not right_name:
                    right_name = "Right File"
                    
                print(f"Setting panel names: {left_name}, {right_name}")  # Debug
                self.set_panel_names(left_name, right_name)
                self.save_ui_settings()
                dialog.grab_release()
                dialog.destroy()
            
            def cancel():
                print("Cancel button clicked...")  # Debug
                dialog.grab_release()
                dialog.destroy()
            
            # Buttons
            ttk.Button(button_frame, text="Cancel", command=cancel).pack(side="right", padx=(5, 0))
            ttk.Button(button_frame, text="Apply", command=apply_names).pack(side="right")
            
            # Set up close protocol
            def on_closing():
                print("Dialog closing via window manager...")  # Debug
                dialog.grab_release()
                dialog.destroy()
            
            dialog.protocol("WM_DELETE_WINDOW", on_closing)
            
            # Focus and selection
            left_entry.focus_set()
            left_entry.select_range(0, tk.END)
            
            print("Dialog setup complete and should be visible")  # Debug
            
        except Exception as e:
            print(f"Error creating dialog: {e}")
            import traceback
            traceback.print_exc()
    
    def _load_ui_settings(self):
        """Load UI settings from config manager"""
        if self.config_manager and hasattr(self.config_manager, 'config'):
            try:
                ui_config = self.config_manager.config.get('ui', {})
                panel_names = ui_config.get('panel_names', {})
                
                self.left_panel_name = panel_names.get('left', 'Left File')
                self.right_panel_name = panel_names.get('right', 'Right File')
                
                # Store other settings for later application
                file_viewer_config = ui_config.get('file_viewer', {})
                self._initial_sync_setting = file_viewer_config.get('sync_scrolling', True)
                self._initial_font_size = file_viewer_config.get('font_size', 10)
                self._initial_view_mode = file_viewer_config.get('default_view', 'side_by_side')
                    
            except Exception as e:
                print(f"Warning: Could not load UI settings: {e}")
                # Set defaults
                self._initial_sync_setting = True
                self._initial_font_size = 10
                self._initial_view_mode = 'side_by_side'
        else:
            # Set defaults
            self._initial_sync_setting = True
            self._initial_font_size = 10
            self._initial_view_mode = 'side_by_side'
    
    def save_ui_settings(self):
        """Save current UI settings to config manager"""
        if self.config_manager:
            try:
                if not hasattr(self.config_manager, 'config'):
                    self.config_manager.config = {}
                
                if 'ui' not in self.config_manager.config:
                    self.config_manager.config['ui'] = {}
                
                # Save panel names
                self.config_manager.config['ui']['panel_names'] = {
                    'left': self.left_panel_name,
                    'right': self.right_panel_name
                }
                
                # Save other UI settings
                file_viewer_settings = {}
                if hasattr(self, 'sync_scrolling'):
                    file_viewer_settings['sync_scrolling'] = self.sync_scrolling.get()
                if hasattr(self, 'font_size_var'):
                    file_viewer_settings['font_size'] = int(self.font_size_var.get())
                if hasattr(self, 'view_mode'):
                    file_viewer_settings['default_view'] = self.view_mode.get()
                
                self.config_manager.config['ui']['file_viewer'] = file_viewer_settings
                
                # Save to file
                self.config_manager.save_config()
                
            except Exception as e:
                print(f"Warning: Could not save UI settings: {e}")
