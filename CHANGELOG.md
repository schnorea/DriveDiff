# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-27

### Added
- Initial release of DriveDiff SD Card Comparison Tool
- GUI-based directory comparison with tkinter interface
- SHA256 hash-based file comparison for content verification
- Binary file detection and exclusion from text comparison
- Side-by-side file viewer with synchronized scrolling
- Color-coded diff highlighting for text files
- Custom panel names feature for personalizing left/right labels
- YAML configuration system for scan paths and file patterns
- Selective directory scanning with configurable paths
- Multiple export formats: HTML, CSV, JSON, and Text reports
- Save and load comparison results functionality
- Progress tracking for large directory comparisons
- File filtering with ignore patterns
- Read-only file system protection with helpful warnings
- Cross-platform compatibility (macOS, Windows, Linux)

### Features
- **Core Comparison Engine**
  - Directory tree scanning and comparison
  - File-by-file SHA256 hash verification
  - Detection of identical, modified, added, and removed files
  - Binary file exclusion for focused text analysis

- **User Interface**
  - Professional tkinter-based GUI with ttk styling
  - Tree view navigation by file status categories
  - Modal dialogs with proper positioning
  - Real-time progress indication
  - Intuitive file browser integration

- **File Viewer**
  - Side-by-side text file comparison
  - Synchronized scrolling between panels
  - Diff highlighting with color coding
  - Custom panel naming (e.g., "Production SD", "Backup SD")
  - File information display (size, modification time, permissions)

- **Configuration Management**
  - YAML-based configuration files
  - Scan path selection for targeted analysis
  - File pattern ignore lists
  - Persistent UI settings
  - Configuration dialog interface

- **Export and Reporting**
  - HTML reports with embedded CSS styling
  - CSV format for spreadsheet analysis
  - JSON format for programmatic access
  - Plain text reports for simple sharing
  - Panel names included in all report metadata

- **Error Handling and Robustness**
  - Comprehensive error handling with user-friendly messages
  - Read-only file system detection and warnings
  - Mount volume path validation
  - Graceful handling of permission errors
  - File encoding detection for text files

### Technical Details
- **Dependencies**: Python 3.7+, tkinter, PyYAML, chardet
- **Architecture**: Modular design with separation of concerns
- **Testing**: Comprehensive test suite with pytest
- **Documentation**: Detailed README with usage examples
- **Packaging**: Virtual environment support with requirements.txt

### Security
- SHA256 cryptographic hashing for file integrity verification
- No external network dependencies
- Local file system access only
- Safe file handling with proper encoding detection
