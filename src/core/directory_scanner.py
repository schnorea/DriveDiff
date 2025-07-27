"""
Directory Scanner Module
Handles directory traversal and comparison operations
"""

import os
import fnmatch
import threading
from typing import Dict, List, Set, Callable, Optional, Tuple
from dataclasses import dataclass
from .file_comparator import FileComparator, FileDifference
from ..utils.yaml_config import YamlConfigManager

@dataclass
class DirectoryComparison:
    """Results of a directory comparison"""
    added_files: List[str]
    removed_files: List[str]
    modified_files: List[str]
    identical_files: List[str]
    file_differences: Dict[str, FileDifference]
    total_files: int
    processed_files: int

class DirectoryScanner:
    """Handles directory scanning and comparison operations"""
    
    def __init__(self, ignore_patterns: List[str] = None, include_patterns: List[str] = None, scan_paths: List[str] = None):
        """
        Initialize directory scanner
        
        Args:
            ignore_patterns: List of file patterns to ignore
            include_patterns: List of file patterns to include (if specified, only these will be included)
            scan_paths: List of relative paths within directories to scan (if specified, only these subdirectories will be scanned)
        """
        self.file_comparator = FileComparator(ignore_patterns)
        self.ignore_patterns = ignore_patterns or []
        self.include_patterns = include_patterns or []
        self.scan_paths = scan_paths or []
        self._cancel_requested = False
    
    @classmethod
    def from_config(cls, config_manager: YamlConfigManager):
        """
        Create DirectoryScanner from YAML configuration
        
        Args:
            config_manager: YAML configuration manager
            
        Returns:
            DirectoryScanner instance configured according to YAML settings
        """
        config = config_manager.load_config()
        
        # Extract patterns from configuration
        ignore_patterns = []
        include_patterns = []
        scan_paths = []
        
        # Get scan paths from configuration
        if 'paths' in config:
            paths_config = config['paths']
            scan_paths = paths_config.get('scan', [])
        
        if 'patterns' in config:
            patterns_config = config['patterns']
            
            # Get exclude patterns
            if 'exclude' in patterns_config:
                exclude_config = patterns_config['exclude']
                ignore_patterns.extend(exclude_config.get('files', []))
                ignore_patterns.extend(exclude_config.get('directories', []))
                ignore_patterns.extend(exclude_config.get('extensions', []))
            
            # Get include patterns  
            if 'include' in patterns_config:
                include_config = patterns_config['include']
                include_patterns.extend(include_config.get('files', []))
                include_patterns.extend(include_config.get('extensions', []))
        
        return cls(ignore_patterns=ignore_patterns, include_patterns=include_patterns, scan_paths=scan_paths)
    
    def scan_directory(self, directory_path: str) -> Set[str]:
        """
        Scan a directory and return set of relative file paths
        
        Args:
            directory_path: Path to the directory to scan
            
        Returns:
            Set of relative file paths
        """
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            return set()
        
        file_set = set()
        
        try:
            # If scan_paths are specified, only scan those subdirectories
            if self.scan_paths:
                for scan_path in self.scan_paths:
                    # Treat scan paths as relative to the base directory, even if they start with "/"
                    # Remove leading "/" to make them relative
                    relative_scan_path = scan_path.lstrip('/')
                    full_scan_path = os.path.join(directory_path, relative_scan_path)
                    
                    if os.path.exists(full_scan_path):
                        if os.path.isdir(full_scan_path):
                            # Scan the specified subdirectory
                            self._scan_path(full_scan_path, directory_path, file_set)
                        elif os.path.isfile(full_scan_path):
                            # Add the specific file if it matches patterns
                            relative_path = os.path.relpath(full_scan_path, directory_path)
                            if self._should_include_file(full_scan_path):
                                file_set.add(relative_path)
            else:
                # Scan the entire directory (original behavior)
                self._scan_path(directory_path, directory_path, file_set)
                    
        except (OSError, IOError) as e:
            print(f"Error scanning directory {directory_path}: {e}")
        
        return file_set
    
    def _scan_path(self, scan_root: str, base_directory: str, file_set: Set[str]):
        """
        Helper method to scan a specific path
        
        Args:
            scan_root: The root path to scan
            base_directory: The base directory for relative path calculation
            file_set: Set to add found files to
        """
        for root, dirs, files in os.walk(scan_root):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if not self._should_ignore_directory(d)]
            
            for file in files:
                if self._cancel_requested:
                    break
                    
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, base_directory)
                
                if self._should_include_file(file_path):
                    file_set.add(relative_path)
            
            if self._cancel_requested:
                break
    
    def compare_directories(self, 
                           left_path: str, 
                           right_path: str,
                           progress_callback: Optional[Callable[[int, int, str], None]] = None) -> DirectoryComparison:
        """
        Compare two directories
        
        Args:
            left_path: Path to the left directory
            right_path: Path to the right directory
            progress_callback: Optional callback for progress updates (current, total, current_file)
            
        Returns:
            DirectoryComparison object
        """
        self._cancel_requested = False
        
        # Scan both directories
        if progress_callback:
            progress_callback(0, 1, "Scanning directories...")
        
        left_files = self.scan_directory(left_path)
        right_files = self.scan_directory(right_path)
        
        # Find differences
        all_files = left_files | right_files
        total_files = len(all_files)
        
        added_files = []
        removed_files = []
        modified_files = []
        identical_files = []
        file_differences = {}
        
        processed = 0
        
        for relative_path in sorted(all_files):
            if self._cancel_requested:
                break
                
            processed += 1
            
            if progress_callback:
                progress_callback(processed, total_files, relative_path)
            
            left_file_path = os.path.join(left_path, relative_path)
            right_file_path = os.path.join(right_path, relative_path)
            
            # Compare the files
            file_diff = self.file_comparator.compare_files(left_file_path, right_file_path)
            
            # Skip if file comparison returned None (both files are binary)
            if file_diff is None:
                continue
            
            # Update the FileInfo objects to use relative paths for consistency
            if file_diff.left_info:
                file_diff.left_info.path = relative_path
            if file_diff.right_info:
                file_diff.right_info.path = relative_path
            
            file_differences[relative_path] = file_diff
            
            # Categorize the difference
            if file_diff.status == 'added':
                added_files.append(relative_path)
            elif file_diff.status == 'removed':
                removed_files.append(relative_path)
            elif file_diff.status == 'modified':
                modified_files.append(relative_path)
            elif file_diff.status == 'identical':
                identical_files.append(relative_path)
        
        return DirectoryComparison(
            added_files=added_files,
            removed_files=removed_files,
            modified_files=modified_files,
            identical_files=identical_files,
            file_differences=file_differences,
            total_files=total_files,
            processed_files=processed
        )
    
    def compare_directories_async(self,
                                 left_path: str,
                                 right_path: str,
                                 progress_callback: Optional[Callable[[int, int, str], None]] = None,
                                 completion_callback: Optional[Callable[[DirectoryComparison], None]] = None):
        """
        Compare directories asynchronously
        
        Args:
            left_path: Path to the left directory
            right_path: Path to the right directory
            progress_callback: Optional callback for progress updates
            completion_callback: Optional callback when comparison is complete
        """
        def run_comparison():
            try:
                result = self.compare_directories(left_path, right_path, progress_callback)
                if completion_callback:
                    completion_callback(result)
            except Exception as e:
                print(f"Error during directory comparison: {e}")
                if completion_callback:
                    completion_callback(None)
        
        thread = threading.Thread(target=run_comparison, daemon=True)
        thread.start()
        return thread
    
    def cancel_comparison(self):
        """Cancel the current comparison operation"""
        self._cancel_requested = True
    
    def get_directory_summary(self, directory_path: str) -> Dict[str, int]:
        """
        Get summary statistics for a directory
        
        Args:
            directory_path: Path to the directory
            
        Returns:
            Dictionary with file count, total size, etc.
        """
        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            return {
                'file_count': 0,
                'directory_count': 0,
                'total_size': 0,
                'accessible': False
            }
        
        file_count = 0
        directory_count = 0
        total_size = 0
        
        try:
            # If scan_paths are specified, only count files in those paths
            if self.scan_paths:
                for scan_path in self.scan_paths:
                    # Treat scan paths as relative to the base directory, even if they start with "/"
                    relative_scan_path = scan_path.lstrip('/')
                    full_scan_path = os.path.join(directory_path, relative_scan_path)
                    if os.path.exists(full_scan_path):
                        if os.path.isdir(full_scan_path):
                            # Count files in the specified subdirectory
                            sub_file_count, sub_dir_count, sub_total_size = self._count_files_in_path(full_scan_path, directory_path)
                            file_count += sub_file_count
                            directory_count += sub_dir_count
                            total_size += sub_total_size
                        elif os.path.isfile(full_scan_path):
                            # Count the specific file if it matches patterns
                            relative_path = os.path.relpath(full_scan_path, directory_path)
                            if self._should_include_file(full_scan_path):
                                file_count += 1
                                try:
                                    total_size += os.path.getsize(full_scan_path)
                                except (OSError, IOError):
                                    pass  # Skip files we can't access
            else:
                # Count all files in the directory (original behavior)
                file_count, directory_count, total_size = self._count_files_in_path(directory_path, directory_path)
            
            return {
                'file_count': file_count,
                'directory_count': directory_count,
                'total_size': total_size,
                'accessible': True
            }
            
        except (OSError, IOError) as e:
            print(f"Error getting directory summary for {directory_path}: {e}")
            return {
                'file_count': 0,
                'directory_count': 0,
                'total_size': 0,
                'accessible': False
            }
    
    def _count_files_in_path(self, scan_root: str, base_directory: str) -> tuple:
        """
        Helper method to count files in a specific path
        
        Args:
            scan_root: The root path to scan
            base_directory: The base directory for relative path calculation
            
        Returns:
            Tuple of (file_count, directory_count, total_size)
        """
        file_count = 0
        directory_count = 0
        total_size = 0
        
        for root, dirs, files in os.walk(scan_root):
            directory_count += len(dirs)
            
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, base_directory)
                
                if self._should_include_file(file_path):
                    file_count += 1
                    try:
                        total_size += os.path.getsize(file_path)
                    except (OSError, IOError):
                        pass  # Skip files we can't access
        
        return file_count, directory_count, total_size
    
    def _should_ignore_directory(self, directory_name: str) -> bool:
        """Check if a directory should be ignored"""
        ignored_dirs = {'.git', '.svn', '.hg', '__pycache__', '.DS_Store', 'node_modules'}
        
        if directory_name in ignored_dirs:
            return True
        
        # Check against ignore patterns
        for pattern in self.ignore_patterns:
            if self.file_comparator._match_pattern(directory_name, pattern):
                return True
        
        return False
    
    def _should_include_file(self, file_path: str) -> bool:
        """
        Check if a file should be included based on patterns and whether it's text
        
        Args:
            file_path: Absolute path to check
            
        Returns:
            True if file should be included
        """
        file_name = os.path.basename(file_path)
        
        # Check include patterns first - if specified, only include matching files
        if self.include_patterns:
            included = False
            for pattern in self.include_patterns:
                if fnmatch.fnmatch(file_name, pattern) or fnmatch.fnmatch(file_path, pattern):
                    included = True
                    break
            if not included:
                return False
        
        # Check ignore patterns
        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(file_name, pattern) or fnmatch.fnmatch(file_path, pattern):
                return False
        
        # Skip binary files - only include text files
        if not self.file_comparator._is_text_file(file_path):
            return False
                
        return True
