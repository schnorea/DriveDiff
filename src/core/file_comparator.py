"""
File Comparator Module
Handles file-by-file comparison operations
"""

import os
import hashlib
import difflib
import chardet
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class FileInfo:
    """Information about a file"""
    path: str
    size: int
    modified_time: datetime
    permissions: str
    hash_sha256: Optional[str] = None
    exists: bool = True

@dataclass
class FileDifference:
    """Represents a difference between two files"""
    file_path: str
    status: str  # 'added', 'removed', 'modified', 'identical'
    left_info: Optional[FileInfo] = None
    right_info: Optional[FileInfo] = None
    content_diff: Optional[List[str]] = None

class FileComparator:
    """Handles file comparison operations"""
    
    def __init__(self, ignore_patterns: List[str] = None):
        """
        Initialize file comparator
        
        Args:
            ignore_patterns: List of file patterns to ignore during comparison
        """
        self.ignore_patterns = ignore_patterns or []
        self.supported_text_extensions = {
            '.txt', '.py', '.js', '.html', '.css', '.json', '.xml', '.yaml', '.yml',
            '.md', '.rst', '.cfg', '.ini', '.conf', '.log', '.sql', '.sh', '.bat',
            '.c', '.cpp', '.h', '.hpp', '.java', '.cs', '.php', '.rb', '.go', '.rs'
        }
    
    def get_file_info(self, file_path: str) -> Optional[FileInfo]:
        """
        Get file information
        
        Args:
            file_path: Path to the file
            
        Returns:
            FileInfo object or None if file doesn't exist or is binary
        """
        try:
            if not os.path.exists(file_path):
                return FileInfo(
                    path=file_path,
                    size=0,
                    modified_time=datetime.min,
                    permissions="",
                    exists=False
                )
            
            # Skip binary files
            if not self._is_text_file(file_path):
                return None
            
            stat = os.stat(file_path)
            return FileInfo(
                path=file_path,
                size=stat.st_size,
                modified_time=datetime.fromtimestamp(stat.st_mtime),
                permissions=oct(stat.st_mode)[-3:],
                hash_sha256=self._calculate_sha256(file_path) if stat.st_size < 100 * 1024 * 1024 else None  # Only hash files < 100MB
            )
        except (OSError, IOError) as e:
            print(f"Error getting file info for {file_path}: {e}")
            return None
    
    def _calculate_sha256(self, file_path: str) -> str:
        """Calculate SHA256 hash of a file"""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except (OSError, IOError):
            return ""
    
    def compare_files(self, left_path: str, right_path: str) -> Optional[FileDifference]:
        """
        Compare two files
        
        Args:
            left_path: Path to the left file
            right_path: Path to the right file
            
        Returns:
            FileDifference object or None if both files are binary/should be skipped
        """
        left_info = self.get_file_info(left_path)
        right_info = self.get_file_info(right_path)
        
        # Skip if both files are binary or don't exist
        if not left_info and not right_info:
            return None
        
        # Handle cases where one or both files don't exist or are binary
        left_exists = left_info and left_info.exists
        right_exists = right_info and right_info.exists
        
        if not left_exists and right_exists:
            # Right file exists as text, left doesn't exist or is binary
            status = 'added'
            rel_path = os.path.basename(right_path)
        elif left_exists and not right_exists:
            # Left file exists as text, right doesn't exist or is binary
            status = 'removed'
            rel_path = os.path.basename(left_path)
        elif left_exists and right_exists:
            # Both files exist and are text
            rel_path = os.path.basename(left_path)
            if self._files_identical(left_info, right_info):
                status = 'identical'
            else:
                status = 'modified'
        else:
            # Both files don't exist or are binary - shouldn't happen
            return None
        
        return FileDifference(
            file_path=rel_path,
            status=status,
            left_info=left_info,
            right_info=right_info
        )
    
    def _files_identical(self, left_info: FileInfo, right_info: FileInfo) -> bool:
        """Check if two files are identical using SHA256 hash comparison only"""
        # First check size for quick elimination
        if left_info.size != right_info.size:
            return False
        
        # Use SHA256 hash comparison - this is the primary method
        if left_info.hash_sha256 and right_info.hash_sha256:
            return left_info.hash_sha256 == right_info.hash_sha256
        
        # If we don't have hashes (e.g., for very large files), do byte-by-byte comparison
        try:
            with open(left_info.path, 'rb') as f1, open(right_info.path, 'rb') as f2:
                while True:
                    chunk1 = f1.read(4096)
                    chunk2 = f2.read(4096)
                    if chunk1 != chunk2:
                        return False
                    if not chunk1:  # End of file
                        return True
        except (OSError, IOError):
            return False
    
    def get_text_diff(self, left_path: str, right_path: str) -> Optional[List[str]]:
        """
        Get text difference between two files
        
        Args:
            left_path: Path to the left file
            right_path: Path to the right file
            
        Returns:
            List of diff lines or None if files are not text or error occurred
        """
        if not self._is_text_file(left_path) or not self._is_text_file(right_path):
            return None
        
        try:
            left_content = self._read_text_file(left_path)
            right_content = self._read_text_file(right_path)
            
            if left_content is None or right_content is None:
                return None
            
            diff = list(difflib.unified_diff(
                left_content.splitlines(keepends=True),
                right_content.splitlines(keepends=True),
                fromfile=f"a/{os.path.basename(left_path)}",
                tofile=f"b/{os.path.basename(right_path)}",
                lineterm=""
            ))
            
            return diff
            
        except Exception as e:
            print(f"Error generating diff for {left_path} and {right_path}: {e}")
            return None
    
    def _is_text_file(self, file_path: str) -> bool:
        """Check if a file is a text file"""
        if not os.path.exists(file_path):
            return False
            
        # Check by extension first
        _, ext = os.path.splitext(file_path.lower())
        if ext in self.supported_text_extensions:
            return True
        
        # Check by content
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if not chunk:
                    return True  # Empty file is considered text
                
                # Check for null bytes (common in binary files)
                if b'\x00' in chunk:
                    return False
                
                # Use chardet to detect encoding
                result = chardet.detect(chunk)
                if result['encoding'] is None:
                    return False
                
                # Try to decode as text
                try:
                    chunk.decode(result['encoding'])
                    return True
                except (UnicodeDecodeError, LookupError):
                    return False
                    
        except (OSError, IOError):
            return False
    
    def _read_text_file(self, file_path: str) -> Optional[str]:
        """Read text file with encoding detection"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
            
            # Detect encoding
            result = chardet.detect(raw_data)
            encoding = result['encoding'] or 'utf-8'
            
            return raw_data.decode(encoding, errors='replace')
            
        except Exception as e:
            print(f"Error reading text file {file_path}: {e}")
            return None
    
    def should_ignore_file(self, file_path: str) -> bool:
        """Check if a file should be ignored based on patterns"""
        file_name = os.path.basename(file_path)
        
        for pattern in self.ignore_patterns:
            if self._match_pattern(file_name, pattern):
                return True
        
        return False
    
    def _match_pattern(self, filename: str, pattern: str) -> bool:
        """Simple pattern matching (supports * wildcard)"""
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)
