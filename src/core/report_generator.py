"""
Report Generator Module
Handles generation of comparison reports in various formats
"""

import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional
from .directory_scanner import DirectoryComparison
from .file_comparator import FileDifference

class ReportGenerator:
    """Handles generation of comparison reports"""
    
    def __init__(self):
        """Initialize report generator"""
        pass
    
    def generate_text_report(self, comparison: DirectoryComparison, 
                           left_path: str, right_path: str,
                           left_panel_name: str = "Left", right_panel_name: str = "Right") -> str:
        """
        Generate a text report of the comparison
        
        Args:
            comparison: DirectoryComparison object
            left_path: Path to the left directory
            right_path: Path to the right directory
            left_panel_name: Custom name for the left panel
            right_panel_name: Custom name for the right panel
            
        Returns:
            Text report as string
        """
        report_lines = []
        report_lines.append("SD Card Comparison Report")
        report_lines.append("=" * 50)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        report_lines.append(f"{left_panel_name} directory:  {left_path}")
        report_lines.append(f"{right_panel_name} directory: {right_path}")
        report_lines.append("")
        
        # Summary
        report_lines.append("Summary:")
        report_lines.append(f"  Total files processed: {comparison.processed_files}")
        report_lines.append(f"  Identical files: {len(comparison.identical_files)}")
        report_lines.append(f"  Modified files: {len(comparison.modified_files)}")
        report_lines.append(f"  Added files: {len(comparison.added_files)}")
        report_lines.append(f"  Removed files: {len(comparison.removed_files)}")
        report_lines.append("")
        
        # Added files
        if comparison.added_files:
            report_lines.append(f"Added Files (present in {right_panel_name}, missing in {left_panel_name}):")
            report_lines.append("-" * 50)
            for file_path in sorted(comparison.added_files):
                file_diff = comparison.file_differences.get(file_path)
                if file_diff and file_diff.right_info:
                    size = self._format_size(file_diff.right_info.size)
                    modified = file_diff.right_info.modified_time.strftime('%Y-%m-%d %H:%M:%S')
                    report_lines.append(f"  + {file_path} ({size}, {modified})")
                else:
                    report_lines.append(f"  + {file_path}")
            report_lines.append("")
        
        # Removed files
        if comparison.removed_files:
            report_lines.append(f"Removed Files (present in {left_panel_name}, missing in {right_panel_name}):")
            report_lines.append("-" * 50)
            for file_path in sorted(comparison.removed_files):
                file_diff = comparison.file_differences.get(file_path)
                if file_diff and file_diff.left_info:
                    size = self._format_size(file_diff.left_info.size)
                    modified = file_diff.left_info.modified_time.strftime('%Y-%m-%d %H:%M:%S')
                    report_lines.append(f"  - {file_path} ({size}, {modified})")
                else:
                    report_lines.append(f"  - {file_path}")
            report_lines.append("")
        
        # Modified files
        if comparison.modified_files:
            report_lines.append("Modified Files:")
            report_lines.append("-" * 50)
            for file_path in sorted(comparison.modified_files):
                file_diff = comparison.file_differences.get(file_path)
                if file_diff and file_diff.left_info and file_diff.right_info:
                    left_size = self._format_size(file_diff.left_info.size)
                    right_size = self._format_size(file_diff.right_info.size)
                    left_modified = file_diff.left_info.modified_time.strftime('%Y-%m-%d %H:%M:%S')
                    right_modified = file_diff.right_info.modified_time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    report_lines.append(f"  ~ {file_path}")
                    report_lines.append(f"    {left_panel_name}:  {left_size}, {left_modified}")
                    report_lines.append(f"    {right_panel_name}: {right_size}, {right_modified}")
                else:
                    report_lines.append(f"  ~ {file_path}")
            report_lines.append("")
        
        return "\n".join(report_lines)
    
    def generate_html_report(self, comparison: DirectoryComparison,
                           left_path: str, right_path: str,
                           left_panel_name: str = "Left", right_panel_name: str = "Right") -> str:
        """
        Generate an HTML report of the comparison
        
        Args:
            comparison: DirectoryComparison object
            left_path: Path to the left directory
            right_path: Path to the right directory
            left_panel_name: Custom name for the left panel
            right_panel_name: Custom name for the right panel
            
        Returns:
            HTML report as string
        """
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>SD Card Comparison Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; }}
        .summary {{ background-color: #e8f4fd; padding: 10px; margin: 10px 0; border-radius: 5px; }}
        .section {{ margin: 20px 0; }}
        .file-list {{ margin-left: 20px; }}
        .added {{ color: #008000; }}
        .removed {{ color: #ff0000; }}
        .modified {{ color: #ff8c00; }}
        .identical {{ color: #808080; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>SD Card Comparison Report</h1>
        <p>Generated: {timestamp}</p>
        <p>{left_panel_name} directory: <code>{left_path}</code></p>
        <p>{right_panel_name} directory: <code>{right_path}</code></p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <table>
            <tr><th>Category</th><th>Count</th></tr>
            <tr><td>Total files processed</td><td>{total_files}</td></tr>
            <tr><td class="identical">Identical files</td><td>{identical_count}</td></tr>
            <tr><td class="modified">Modified files</td><td>{modified_count}</td></tr>
            <tr><td class="added">Added files</td><td>{added_count}</td></tr>
            <tr><td class="removed">Removed files</td><td>{removed_count}</td></tr>
        </table>
    </div>
    
    {sections}
</body>
</html>
        """
        
        sections = []
        
        # Added files section
        if comparison.added_files:
            sections.append('<div class="section">')
            sections.append(f'<h2 class="added">Added Files (present in {right_panel_name}, missing in {left_panel_name})</h2>')
            sections.append('<div class="file-list">')
            for file_path in sorted(comparison.added_files):
                file_diff = comparison.file_differences.get(file_path)
                if file_diff and file_diff.right_info:
                    size = self._format_size(file_diff.right_info.size)
                    modified = file_diff.right_info.modified_time.strftime('%Y-%m-%d %H:%M:%S')
                    sections.append(f'<p class="added">+ {file_path} ({size}, {modified})</p>')
                else:
                    sections.append(f'<p class="added">+ {file_path}</p>')
            sections.append('</div></div>')
        
        # Removed files section
        if comparison.removed_files:
            sections.append('<div class="section">')
            sections.append(f'<h2 class="removed">Removed Files (present in {left_panel_name}, missing in {right_panel_name})</h2>')
            sections.append('<div class="file-list">')
            for file_path in sorted(comparison.removed_files):
                file_diff = comparison.file_differences.get(file_path)
                if file_diff and file_diff.left_info:
                    size = self._format_size(file_diff.left_info.size)
                    modified = file_diff.left_info.modified_time.strftime('%Y-%m-%d %H:%M:%S')
                    sections.append(f'<p class="removed">- {file_path} ({size}, {modified})</p>')
                else:
                    sections.append(f'<p class="removed">- {file_path}</p>')
            sections.append('</div></div>')
        
        # Modified files section
        if comparison.modified_files:
            sections.append('<div class="section">')
            sections.append('<h2 class="modified">Modified Files</h2>')
            sections.append('<div class="file-list">')
            for file_path in sorted(comparison.modified_files):
                file_diff = comparison.file_differences.get(file_path)
                if file_diff and file_diff.left_info and file_diff.right_info:
                    left_size = self._format_size(file_diff.left_info.size)
                    right_size = self._format_size(file_diff.right_info.size)
                    left_modified = file_diff.left_info.modified_time.strftime('%Y-%m-%d %H:%M:%S')
                    right_modified = file_diff.right_info.modified_time.strftime('%Y-%m-%d %H:%M:%S')
                    
                    sections.append(f'<p class="modified">~ {file_path}</p>')
                    sections.append('<div style="margin-left: 20px;">')
                    sections.append(f'<p>{left_panel_name}: {left_size}, {left_modified}</p>')
                    sections.append(f'<p>{right_panel_name}: {right_size}, {right_modified}</p>')
                    sections.append('</div>')
                else:
                    sections.append(f'<p class="modified">~ {file_path}</p>')
            sections.append('</div></div>')
        
        return html_template.format(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            left_path=left_path,
            right_path=right_path,
            left_panel_name=left_panel_name,
            right_panel_name=right_panel_name,
            total_files=comparison.processed_files,
            identical_count=len(comparison.identical_files),
            modified_count=len(comparison.modified_files),
            added_count=len(comparison.added_files),
            removed_count=len(comparison.removed_files),
            sections='\n'.join(sections)
        )
    
    def generate_csv_report(self, comparison: DirectoryComparison,
                          left_path: str, right_path: str,
                          left_panel_name: str = "Left", right_panel_name: str = "Right") -> str:
        """
        Generate a CSV report of the comparison
        
        Args:
            comparison: DirectoryComparison object
            left_path: Path to the left directory
            right_path: Path to the right directory
            left_panel_name: Custom name for the left panel
            right_panel_name: Custom name for the right panel
            
        Returns:
            CSV report as string
        """
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'File Path', 'Status', f'{left_panel_name} Size', f'{right_panel_name} Size',
            f'{left_panel_name} Modified', f'{right_panel_name} Modified', 
            f'{left_panel_name} Permissions', f'{right_panel_name} Permissions'
        ])
        
        # Process all files
        for file_path, file_diff in comparison.file_differences.items():
            left_size = file_diff.left_info.size if file_diff.left_info and file_diff.left_info.exists else ""
            right_size = file_diff.right_info.size if file_diff.right_info and file_diff.right_info.exists else ""
            left_modified = file_diff.left_info.modified_time.strftime('%Y-%m-%d %H:%M:%S') if file_diff.left_info and file_diff.left_info.exists else ""
            right_modified = file_diff.right_info.modified_time.strftime('%Y-%m-%d %H:%M:%S') if file_diff.right_info and file_diff.right_info.exists else ""
            left_permissions = file_diff.left_info.permissions if file_diff.left_info and file_diff.left_info.exists else ""
            right_permissions = file_diff.right_info.permissions if file_diff.right_info and file_diff.right_info.exists else ""
            
            writer.writerow([
                file_path, file_diff.status, left_size, right_size,
                left_modified, right_modified, left_permissions, right_permissions
            ])
        
        return output.getvalue()
    
    def generate_json_report(self, comparison: DirectoryComparison,
                           left_path: str, right_path: str,
                           left_panel_name: str = "Left", right_panel_name: str = "Right") -> str:
        """
        Generate a JSON report of the comparison
        
        Args:
            comparison: DirectoryComparison object
            left_path: Path to the left directory
            right_path: Path to the right directory
            left_panel_name: Custom name for the left panel
            right_panel_name: Custom name for the right panel
            
        Returns:
            JSON report as string
        """
        report_data = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'left_path': left_path,
                'right_path': right_path,
                'left_panel_name': left_panel_name,
                'right_panel_name': right_panel_name,
                'total_files': comparison.processed_files
            },
            'summary': {
                'identical_files': len(comparison.identical_files),
                'modified_files': len(comparison.modified_files),
                'added_files': len(comparison.added_files),
                'removed_files': len(comparison.removed_files)
            },
            'files': {}
        }
        
        # Convert file differences to JSON-serializable format
        for file_path, file_diff in comparison.file_differences.items():
            file_data = {
                'status': file_diff.status
            }
            
            if file_diff.left_info and file_diff.left_info.exists:
                file_data['left'] = {
                    'size': file_diff.left_info.size,
                    'modified_time': file_diff.left_info.modified_time.isoformat(),
                    'permissions': file_diff.left_info.permissions,
                    'hash_sha256': file_diff.left_info.hash_sha256
                }
            
            if file_diff.right_info and file_diff.right_info.exists:
                file_data['right'] = {
                    'size': file_diff.right_info.size,
                    'modified_time': file_diff.right_info.modified_time.isoformat(),
                    'permissions': file_diff.right_info.permissions,
                    'hash_sha256': file_diff.right_info.hash_sha256
                }
            
            report_data['files'][file_path] = file_data
        
        return json.dumps(report_data, indent=2)
    
    def save_report(self, report_content: str, file_path: str) -> bool:
        """
        Save report content to a file
        
        Args:
            report_content: Content of the report
            file_path: Path where to save the report
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if trying to write to a mounted volume (common read-only issue)
            if file_path.startswith('/Volumes/'):
                print(f"WARNING: Attempting to save to mounted volume: {file_path}")
                print("Mounted volumes are often read-only. Consider saving to your home directory or Desktop instead.")
            
            # Ensure directory exists (only if there's a directory part)
            dir_path = os.path.dirname(file_path)
            if dir_path:  # Only create directories if there's a directory component
                os.makedirs(dir_path, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            return True
            
        except OSError as e:
            if e.errno == 30:  # Read-only file system
                print(f"ERROR: Cannot save to read-only file system: {file_path}")
                print("The target location is read-only (likely a mounted SD card or USB drive).")
                print("Please choose a writable location such as:")
                print("  - Your Desktop: ~/Desktop/")
                print("  - Your Documents folder: ~/Documents/")
                print("  - Your home directory: ~/")
                return False
            else:
                print(f"OS Error saving report to {file_path}: {e}")
                import traceback
                traceback.print_exc()
                return False
        except Exception as e:
            print(f"Error saving report to {file_path}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
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
