# SD Card Comparison Tool Configuration

# This file contains default configuration settings for the SD Card Comparison Tool.
# The application will create a user-specific configuration file at runtime with
# settings that can be modified through the Settings dialog.

# File patterns to ignore by default (can be modified in Settings)
DEFAULT_IGNORE_PATTERNS = [
    "*.tmp",
    "*.bak", 
    "*.swp",
    "*~",
    ".DS_Store",
    "Thumbs.db",
    "*.pyc",
    "*.pyo",
    "__pycache__",
    ".git",
    ".svn",
    ".hg",
    "node_modules",
    "*.log"
]

# Maximum file size for content comparison (MB)
DEFAULT_MAX_FILE_SIZE = 100

# Default window size
DEFAULT_WINDOW_SIZE = "1200x800"

# Default font settings
DEFAULT_FONT_FAMILY = "Courier"
DEFAULT_FONT_SIZE = 10

# Performance settings
DEFAULT_THREAD_POOL_SIZE = 4
DEFAULT_MAX_RECENT_PATHS = 10
