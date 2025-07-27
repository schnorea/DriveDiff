# SD Card Comparison Tool - Project Overview

## 🎯 Project Summary

The SD Card Comparison Tool is a comprehensive GUI-based Python application designed to compare contents between two SD card mount points or any directories. It provides detailed file and directory comparison capabilities with an intuitive user interface.

## ✨ Key Features

### Core Functionality
- **Directory Comparison**: Compare two directories with detailed file-by-file analysis
- **Selective Path Scanning**: Configure specific subdirectories to scan within selected directories via YAML configuration
- **File Content Viewing**: Side-by-side file content comparison with diff highlighting
- **Multiple View Modes**: Side-by-side, unified diff, and hex view options
- **Progress Tracking**: Real-time progress indication for large directory comparisons
- **File Filtering**: Customizable ignore patterns for files and directories

### Comparison Capabilities
- **File Status Detection**: Identifies added, removed, modified, and identical files
- **Metadata Comparison**: Compares file sizes, modification times, and permissions
- **Binary/Text Detection**: Automatic detection of file types with appropriate handling
- **Syntax Highlighting**: Basic syntax highlighting for code files

### Export and Reporting
- **Multiple Export Formats**: HTML, CSV, JSON, and plain text reports
- **Detailed Reports**: Comprehensive comparison results with file metadata
- **Save/Load Results**: Save comparison results for later review

### User Experience
- **Intuitive GUI**: Clean, professional interface built with tkinter
- **Customizable Settings**: Extensive configuration options through settings dialog
- **Recent Paths**: Remember frequently used directory paths
- **Keyboard Shortcuts**: Standard keyboard shortcuts for common operations

## 🏗️ Architecture

### Project Structure
```
DriveDiff/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── config.py                   # Default configuration
├── run.sh / run.bat            # Cross-platform launch scripts
├── README.md                   # Project documentation
├── requirements.md             # Original requirements document
├── src/
│   ├── __init__.py
│   ├── core/                   # Core business logic
│   │   ├── file_comparator.py     # File comparison algorithms
│   │   ├── directory_scanner.py   # Directory traversal and comparison
│   │   └── report_generator.py    # Report generation in multiple formats
│   ├── gui/                    # User interface components
│   │   ├── main_window.py          # Main application window
│   │   ├── comparison_tree.py      # Tree view for comparison results
│   │   ├── file_viewer.py          # File content viewer with diff
│   │   ├── config_dialog.py        # YAML configuration dialog
│   │   └── dialogs.py              # Settings and other dialogs
│   └── utils/                  # Utility modules
│       ├── file_utils.py           # File system utilities
│       ├── config.py               # Configuration management
│       └── yaml_config.py          # YAML configuration manager
└── tests/                      # Unit tests
    ├── test_file_comparator.py
    ├── test_directory_scanner.py
    └── test_file_utils.py
```

### Key Components

#### Core Module (`src/core/`)
- **FileComparator**: Handles individual file comparisons, hash calculations, and diff generation
- **DirectoryScanner**: Manages directory traversal, comparison orchestration, and progress tracking
- **ReportGenerator**: Creates reports in various formats (HTML, CSV, JSON, text)

#### GUI Module (`src/gui/`)
- **MainWindow**: Central application coordinator with menu bar and main layout
- **ComparisonTreeView**: Displays comparison results in a hierarchical tree view
- **FileViewer**: Side-by-side file content viewer with diff highlighting
- **Dialogs**: Settings configuration and about dialogs

#### Utils Module (`src/utils/`)
- **FileUtils**: File system operations, validation, and utility functions
- **Config**: Configuration management with user settings persistence
- **YamlConfigManager**: YAML configuration management with validation and selective path scanning

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)
- Required packages: `chardet`, `Pillow`, `send2trash`

### Installation
1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
- **macOS/Linux**: `./run.sh`
- **Windows**: `run.bat`
- **Direct Python**: `python main.py`

### Basic Usage
1. **Select Directories**: Use the browse buttons to select left and right directories
2. **Start Comparison**: Click "Compare Directories" to begin analysis
3. **Review Results**: Browse the comparison tree to see file differences
4. **View Files**: Select files to see side-by-side content comparison
5. **Export Results**: Use File menu to export reports in various formats

## 🔧 Configuration

### YAML Configuration System
Access via Edit → Scan Configuration to configure:
- **Scan Paths**: Specify which subdirectories to scan within selected directories
- **Include/Exclude Patterns**: File patterns to include or exclude from comparison  
- **Performance Settings**: Worker threads, hash chunk size, file limits
- **Logging**: Set logging levels for debugging

### Settings Dialog
Access via Edit → Settings to configure:
- **General**: Window behavior, comparison options, performance settings
- **Ignore Patterns**: File patterns to exclude from comparison
- **Appearance**: Font settings, color schemes, display options

### Configuration Storage
- **macOS**: `~/Library/Application Support/SDCardComparison/`
- **Linux**: `~/.config/sdcardcomparison/`
- **Windows**: `%APPDATA%\SDCardComparison\`

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

Test coverage includes:
- File comparison algorithms
- Directory scanning logic
- Utility functions
- Error handling scenarios

## 📋 Requirements Compliance

The application fulfills all requirements from the original specification:

✅ **Mount Point Selection**: GUI browse buttons for directory selection  
✅ **Directory Comparison**: Complete file and directory analysis  
✅ **File Comparison**: Side-by-side content viewing with diff highlighting  
✅ **Data Management**: Save/load results, export reports  
✅ **Performance**: Efficient handling of large directories with progress indication  
✅ **Usability**: Intuitive interface with clear error handling  
✅ **File System Support**: Works with various file systems including Paragon extfs  
✅ **Cross-platform**: Compatible with macOS, Linux, and Windows  

## 🔮 Future Enhancements

Potential improvements identified:
- Advanced search and filtering capabilities
- Batch file operations (copy, move, delete)
- Network drive support
- Plugin architecture for custom comparison rules
- Enhanced syntax highlighting
- Integration with version control systems
- Command-line interface for automation

## 🛠️ Development Notes

### Design Decisions
- **tkinter**: Chosen for cross-platform compatibility and no additional dependencies
- **Modular Architecture**: Separation of concerns with clear interfaces between components
- **Threading**: Async operations for UI responsiveness during long operations
- **Configuration Management**: Persistent settings with sensible defaults

### Performance Considerations
- **Lazy Loading**: Files loaded only when needed for viewing
- **Progress Feedback**: Real-time updates during long operations
- **Memory Management**: Efficient handling of large files and directories
- **Cancellation Support**: Ability to cancel long-running operations

## 📝 License

This project is released under the MIT License, allowing for both personal and commercial use.

---

The SD Card Comparison Tool provides a robust, user-friendly solution for comparing directory contents with professional-grade features and cross-platform compatibility.
