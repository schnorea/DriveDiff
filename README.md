# DriveDiff - SD Card Comparison Tool

A powerful GUI-based application for comparing contents between two directories or SD cards, providing detailed file-by-file analysis with SHA256 hash verification.

## 🚀 Features

### Core Comparison
- **Directory Comparison**: Compare any two directories or mounted SD cards
- **SHA256 Hash Verification**: Content-based comparison using cryptographic hashes
- **Binary File Detection**: Automatically excludes binary files from text comparison
- **Smart File Analysis**: Detects identical, modified, added, and removed files

### User Interface
- **Intuitive GUI**: Clean tkinter-based interface with professional styling
- **Side-by-Side File Viewer**: Compare file contents with synchronized scrolling
- **Diff Highlighting**: Color-coded differences in text files
- **Custom Panel Names**: Personalize left/right panel labels (e.g., "Production SD", "Backup SD")
- **Tree View Navigation**: Browse comparison results by category
- **Progress Tracking**: Real-time progress indication for large comparisons

### Configuration & Flexibility
- **YAML Configuration**: Configurable scan paths and file patterns
- **Selective Scanning**: Choose which subdirectories to include/exclude
- **File Filtering**: Built-in patterns for common file types to ignore
- **Binary File Exclusion**: Skip binary files to focus on text content

### Export & Reporting
- **Multiple Export Formats**: HTML, CSV, JSON, and Text reports
- **Detailed Reports**: Include file sizes, modification times, and panel names
- **Save/Load Comparisons**: Persist comparison results for later analysis
- **Read-Only Protection**: Smart warnings when saving to mounted volumes

## 📋 Requirements

- **Python**: 3.7 or higher
- **Operating System**: macOS, Windows, or Linux
- **GUI Framework**: tkinter (usually included with Python)
- **Dependencies**: See `requirements.txt`

## 🛠️ Installation

### Option 1: Clone Repository
```bash
git clone https://github.com/yourusername/DriveDiff.git
cd DriveDiff
```

### Option 2: Download ZIP
Download and extract the ZIP file from GitHub

### Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

## 🚀 Usage

### Quick Start
```bash
# Navigate to project directory
cd DriveDiff

# Activate virtual environment (if using)
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the application
python src/main.py
```

### Alternative Launch Methods
```bash
# Using the convenience script (Unix/macOS)
./run.sh

# Using the convenience script (Windows)
run.bat
```

### Basic Workflow
1. **Select Directories**: Choose left and right directories to compare
2. **Set Panel Names** (Optional): Customize labels like "Production SD" and "Backup SD"
3. **Configure Scan** (Optional): Use "File → Scan Configuration" to set selective paths
4. **Start Comparison**: Click "Compare Directories"
5. **Review Results**: Navigate through identical, modified, added, and removed files
6. **View File Details**: Double-click files to see side-by-side content comparison
7. **Export Reports**: Use "File → Export Report" to save results

## 📁 Project Structure

```
DriveDiff/
├── src/
│   ├── main.py                 # Application entry point
│   ├── core/
│   │   ├── directory_scanner.py    # Directory scanning and comparison logic
│   │   ├── file_comparator.py      # File-level comparison and hashing
│   │   └── report_generator.py     # Export functionality (HTML, CSV, JSON, Text)
│   ├── gui/
│   │   ├── main_window.py          # Main application window
│   │   ├── file_viewer.py          # Side-by-side file content viewer
│   │   └── configuration_dialog.py # Scan configuration interface
│   └── utils/
│       ├── config_manager.py       # YAML configuration management
│       └── file_utils.py           # File system utilities
├── requirements.txt            # Python dependencies
├── default.yaml               # Default configuration
├── .gitignore                 # Git ignore patterns
└── README.md                  # This file
```

## ⚙️ Configuration

### YAML Configuration File
The application uses `scan_config.yaml` for configuration:

```yaml
scan_paths:
  - "/path/to/important/directory"
  - "/another/path"

ignore_patterns:
  - "*.tmp"
  - "*.log"
  - ".DS_Store"

ui_settings:
  panel_names:
    left: "Production SD"
    right: "Backup SD"
```

### Scan Configuration Dialog
Access via "File → Scan Configuration" to:
- Add/remove scan paths
- Modify ignore patterns
- Configure file type exclusions

## 📊 Export Formats

### HTML Reports
- Professional styling with color-coded sections
- Interactive navigation
- Embedded CSS for offline viewing

### CSV Reports
- Spreadsheet-compatible format
- Detailed file information columns
- Easy data analysis

### JSON Reports
- Machine-readable format
- Complete metadata inclusion
- API integration friendly

### Text Reports
- Plain text format
- Console-friendly output
- Simple sharing and viewing

## 🔧 Development

### Running Tests
```bash
# Run test suite
python -m pytest tests/

# Run specific test
python -m pytest tests/test_file_comparator.py
```

### Code Structure
- **Core Logic**: File comparison, hashing, and scanning
- **GUI Components**: Modular interface components
- **Configuration**: YAML-based settings management
- **Utilities**: Helper functions and file operations

## 🐛 Troubleshooting

### Common Issues

**"Read-only file system" error when saving reports**
- Save to your home directory, Desktop, or Documents folder instead of mounted volumes

**Slow comparison on large directories**
- Use scan configuration to exclude unnecessary subdirectories
- Binary files are automatically excluded from content comparison

**Permission errors accessing directories**
- Ensure you have read permissions for both directories
- On macOS, you may need to grant Full Disk Access to Terminal

### Getting Help
1. Check the [Issues](https://github.com/yourusername/DriveDiff/issues) page
2. Review the troubleshooting section above
3. Create a new issue with detailed error information

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Built with Python and tkinter
- SHA256 hashing for reliable file comparison
- YAML configuration for flexible setup
│   ├── core/
│   │   ├── __init__.py
│   │   ├── file_comparator.py    # File comparison logic
│   │   ├── directory_scanner.py  # Directory scanning
│   │   └── report_generator.py   # Report generation
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py        # Main application window
│   │   ├── comparison_tree.py    # Tree view component
│   │   ├── file_viewer.py        # File content viewer
│   │   └── dialogs.py            # Various dialogs
│   └── utils/
│       ├── __init__.py
│       ├── file_utils.py         # File system utilities
│       └── config.py             # Configuration management
└── tests/                        # Unit tests
    ├── __init__.py
    ├── test_file_comparator.py
    ├── test_directory_scanner.py
    └── test_file_utils.py
```

## License

This project is licensed under the MIT License.
