"""
File Utilities Module
Various file system utility functions
"""

import os
import shutil
import stat
import platform
import subprocess
from typing import Optional, List, Dict, Any
from datetime import datetime

def get_file_size_human(size_bytes: int) -> str:
    """
    Convert file size to human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"

def get_file_permissions_string(file_path: str) -> str:
    """
    Get file permissions as a string
    
    Args:
        file_path: Path to the file
        
    Returns:
        Permission string (e.g., "rwxr-xr-x")
    """
    try:
        mode = os.stat(file_path).st_mode
        perms = []
        
        # Owner permissions
        perms.append('r' if mode & stat.S_IRUSR else '-')
        perms.append('w' if mode & stat.S_IWUSR else '-')
        perms.append('x' if mode & stat.S_IXUSR else '-')
        
        # Group permissions
        perms.append('r' if mode & stat.S_IRGRP else '-')
        perms.append('w' if mode & stat.S_IWGRP else '-')
        perms.append('x' if mode & stat.S_IXGRP else '-')
        
        # Other permissions
        perms.append('r' if mode & stat.S_IROTH else '-')
        perms.append('w' if mode & stat.S_IWOTH else '-')
        perms.append('x' if mode & stat.S_IXOTH else '-')
        
        return ''.join(perms)
        
    except (OSError, IOError):
        return "unknown"

def is_binary_file(file_path: str, chunk_size: int = 1024) -> bool:
    """
    Check if a file is binary
    
    Args:
        file_path: Path to the file
        chunk_size: Size of chunk to read for detection
        
    Returns:
        True if file is binary, False if text
    """
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(chunk_size)
            if not chunk:
                return False  # Empty file is considered text
            
            # Check for null bytes (common in binary files)
            if b'\x00' in chunk:
                return True
            
            # Check for a high percentage of non-printable characters
            text_chars = bytearray(range(32, 127)) + b'\n\r\t\b'
            non_text_chars = len([byte for byte in chunk if byte not in text_chars])
            
            # If more than 30% are non-text characters, consider it binary
            return (non_text_chars / len(chunk)) > 0.3
            
    except (OSError, IOError):
        return True  # Assume binary if we can't read it

def safe_copy_file(src_path: str, dst_path: str, preserve_metadata: bool = True) -> bool:
    """
    Safely copy a file from source to destination
    
    Args:
        src_path: Source file path
        dst_path: Destination file path
        preserve_metadata: Whether to preserve file metadata
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        
        # Copy the file
        if preserve_metadata:
            shutil.copy2(src_path, dst_path)
        else:
            shutil.copy(src_path, dst_path)
        
        return True
        
    except Exception as e:
        print(f"Error copying file from {src_path} to {dst_path}: {e}")
        return False

def safe_move_file(src_path: str, dst_path: str) -> bool:
    """
    Safely move a file from source to destination
    
    Args:
        src_path: Source file path
        dst_path: Destination file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        
        # Move the file
        shutil.move(src_path, dst_path)
        return True
        
    except Exception as e:
        print(f"Error moving file from {src_path} to {dst_path}: {e}")
        return False

def safe_delete_file(file_path: str, use_trash: bool = True) -> bool:
    """
    Safely delete a file
    
    Args:
        file_path: Path to the file to delete
        use_trash: Whether to move to trash instead of permanent deletion
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if use_trash:
            try:
                import send2trash
                send2trash.send2trash(file_path)
                return True
            except ImportError:
                pass  # Fall back to permanent deletion
        
        os.remove(file_path)
        return True
        
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False

def get_file_type_description(file_path: str) -> str:
    """
    Get a description of the file type
    
    Args:
        file_path: Path to the file
        
    Returns:
        File type description
    """
    if not os.path.exists(file_path):
        return "File not found"
    
    if os.path.isdir(file_path):
        return "Directory"
    
    if os.path.islink(file_path):
        return "Symbolic link"
    
    # Check by extension
    _, ext = os.path.splitext(file_path.lower())
    
    type_mapping = {
        '.txt': 'Text file',
        '.py': 'Python script',
        '.js': 'JavaScript file',
        '.html': 'HTML document',
        '.css': 'CSS stylesheet',
        '.json': 'JSON data',
        '.xml': 'XML document',
        '.yaml': 'YAML file',
        '.yml': 'YAML file',
        '.md': 'Markdown document',
        '.rst': 'reStructuredText document',
        '.cfg': 'Configuration file',
        '.ini': 'Configuration file',
        '.conf': 'Configuration file',
        '.log': 'Log file',
        '.sql': 'SQL script',
        '.sh': 'Shell script',
        '.bat': 'Batch script',
        '.exe': 'Executable file',
        '.dll': 'Dynamic link library',
        '.so': 'Shared object',
        '.pdf': 'PDF document',
        '.doc': 'Word document',
        '.docx': 'Word document',
        '.xls': 'Excel spreadsheet',
        '.xlsx': 'Excel spreadsheet',
        '.jpg': 'JPEG image',
        '.jpeg': 'JPEG image',
        '.png': 'PNG image',
        '.gif': 'GIF image',
        '.bmp': 'Bitmap image',
        '.mp3': 'MP3 audio',
        '.wav': 'WAV audio',
        '.mp4': 'MP4 video',
        '.avi': 'AVI video',
        '.zip': 'ZIP archive',
        '.tar': 'TAR archive',
        '.gz': 'GZIP archive',
        '.rar': 'RAR archive'
    }
    
    if ext in type_mapping:
        return type_mapping[ext]
    
    # Check if it's a binary file
    if is_binary_file(file_path):
        return "Binary file"
    else:
        return "Text file"

def open_file_in_system(file_path: str) -> bool:
    """
    Open a file with the system's default application
    
    Args:
        file_path: Path to the file to open
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", file_path], check=True)
        elif platform.system() == "Windows":
            os.startfile(file_path)
        else:  # Linux and others
            subprocess.run(["xdg-open", file_path], check=True)
        
        return True
        
    except Exception as e:
        print(f"Error opening file {file_path}: {e}")
        return False

def show_file_in_explorer(file_path: str) -> bool:
    """
    Show a file in the system file explorer/finder
    
    Args:
        file_path: Path to the file to show
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", "-R", file_path], check=True)
        elif platform.system() == "Windows":
            subprocess.run(["explorer", "/select,", file_path], check=True)
        else:  # Linux
            # Open the directory containing the file
            directory = os.path.dirname(file_path)
            subprocess.run(["xdg-open", directory], check=True)
        
        return True
        
    except Exception as e:
        print(f"Error showing file {file_path} in explorer: {e}")
        return False

def validate_directory_path(path: str) -> Dict[str, Any]:
    """
    Validate a directory path and return information about it
    
    Args:
        path: Directory path to validate
        
    Returns:
        Dictionary with validation results
    """
    result = {
        'valid': False,
        'exists': False,
        'is_directory': False,
        'readable': False,
        'writable': False,
        'error': None
    }
    
    try:
        if not path:
            result['error'] = "Path is empty"
            return result
        
        path = os.path.expanduser(path)  # Expand ~ if present
        
        result['exists'] = os.path.exists(path)
        
        if not result['exists']:
            result['error'] = "Path does not exist"
            return result
        
        result['is_directory'] = os.path.isdir(path)
        
        if not result['is_directory']:
            result['error'] = "Path is not a directory"
            return result
        
        result['readable'] = os.access(path, os.R_OK)
        result['writable'] = os.access(path, os.W_OK)
        
        if not result['readable']:
            result['error'] = "Directory is not readable"
            return result
        
        result['valid'] = True
        
    except Exception as e:
        result['error'] = str(e)
    
    return result

def get_directory_info(directory_path: str) -> Dict[str, Any]:
    """
    Get detailed information about a directory
    
    Args:
        directory_path: Path to the directory
        
    Returns:
        Dictionary with directory information
    """
    info = {
        'path': directory_path,
        'exists': False,
        'file_count': 0,
        'directory_count': 0,
        'total_size': 0,
        'last_modified': None,
        'permissions': None,
        'error': None
    }
    
    try:
        if not os.path.exists(directory_path):
            info['error'] = "Directory does not exist"
            return info
        
        if not os.path.isdir(directory_path):
            info['error'] = "Path is not a directory"
            return info
        
        info['exists'] = True
        
        # Get basic directory info
        stat_result = os.stat(directory_path)
        info['last_modified'] = datetime.fromtimestamp(stat_result.st_mtime)
        info['permissions'] = get_file_permissions_string(directory_path)
        
        # Count files and calculate total size
        file_count = 0
        directory_count = 0
        total_size = 0
        
        for root, dirs, files in os.walk(directory_path):
            directory_count += len(dirs)
            file_count += len(files)
            
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
                except (OSError, IOError):
                    pass  # Skip files we can't access
        
        info['file_count'] = file_count
        info['directory_count'] = directory_count
        info['total_size'] = total_size
        
    except Exception as e:
        info['error'] = str(e)
    
    return info

def create_backup_filename(original_path: str) -> str:
    """
    Create a backup filename for a given file
    
    Args:
        original_path: Original file path
        
    Returns:
        Backup filename
    """
    directory = os.path.dirname(original_path)
    filename = os.path.basename(original_path)
    name, ext = os.path.splitext(filename)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{name}_backup_{timestamp}{ext}"
    
    return os.path.join(directory, backup_filename)

def cleanup_temp_files(temp_dir: str, max_age_hours: int = 24) -> int:
    """
    Clean up temporary files older than specified age
    
    Args:
        temp_dir: Temporary directory path
        max_age_hours: Maximum age in hours for temp files
        
    Returns:
        Number of files cleaned up
    """
    if not os.path.exists(temp_dir):
        return 0
    
    cleanup_count = 0
    max_age_seconds = max_age_hours * 3600
    current_time = datetime.now().timestamp()
    
    try:
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                
                if file_age > max_age_seconds:
                    try:
                        os.remove(file_path)
                        cleanup_count += 1
                    except OSError:
                        pass  # Skip files we can't delete
    
    except OSError:
        pass  # Skip if we can't access the directory
    
    return cleanup_count
