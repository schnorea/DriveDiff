# DriveDiff - Project Overview

## Current Version: 1.3.0

### Project Description
DriveDiff is an advanced directory comparison tool with dual comparison modes, intelligent mounted volume support, and a comprehensive configuration system. The application provides both deep file content analysis and fast directory structure comparison with an intuitive GUI interface.

## Key Features

### Dual Comparison System
- **Directory Comparison**: SHA256-based file content comparison with detailed analysis
- **Structure Comparison**: Fast directory tree analysis focusing on structure only
- **Independent Configuration**: Separate settings and optimization for each comparison type

### Advanced Path Intelligence
- **Mounted Volume Support**: Intelligent handling of `/Volumes/rootfs/usr/share` → `/usr/share` path matching
- **Smart Exclusion Patterns**: Context-aware pattern matching for complex directory structures
- **Cross-Platform Compatibility**: Works across macOS, Windows, and Linux mounted filesystems

### Configuration Management
- **YAML-Based Configuration**: Clean, readable dual configuration structure
- **GUI Configuration Dialog**: User-friendly interface with validation and real-time preview
- **Import/Export**: Save and load configuration presets
- **Performance Tuning**: Configurable threading, memory usage, and processing limits

## Architecture

### Core Components

#### `/src/core/`
- **`directory_scanner.py`**: Enhanced scanner with dual comparison modes and intelligent path matching
- **`file_comparator.py`**: SHA256-based file content comparison engine
- **`report_generator.py`**: Multi-format report generation (HTML, CSV, JSON, Text)

#### `/src/gui/`
- **`main_window.py`**: Primary application interface with tabbed comparison views
- **`config_dialog.py`**: Comprehensive configuration interface with dual configuration support
- **`comparison_tree.py`**: Color-coded tree view for navigation and result display
- **`file_viewer.py`**: Side-by-side file content comparison with diff highlighting

#### `/src/utils/`
- **`yaml_config.py`**: Dual configuration management with validation and import/export
- **`config.py`**: Application-wide configuration constants and settings
- **`file_utils.py`**: File system utilities and path handling

### Configuration Structure
```yaml
logging:
  level: INFO

directory_comparison:    # Full file content comparison
  paths:
    scan: []            # Specific directories (empty = all)
    exclude: []         # Directories to skip
    include: []         # File patterns to include
    exclude_patterns: [] # File/directory patterns to exclude

structure_comparison:    # Directory structure only
  paths:
    scan: []            # Specific directories (empty = all)  
    exclude: []         # Directories to skip
    exclude_patterns: [] # Directory patterns to exclude

performance:
  worker_threads: 4      # Parallel processing
  hash_chunk_size: 65536 # Memory vs speed optimization
  max_files: 0          # Processing limit (0 = unlimited)
```

## Recent Developments (v1.3.0)

### Major Enhancements
1. **Dual Configuration System**: Complete separation of Directory vs Structure comparison settings
2. **Intelligent Mounted Volume Support**: Advanced path matching for mounted filesystems
3. **Enhanced Configuration Dialog**: Four-tab interface with validation and YAML editing
4. **Configuration Loading Fix**: Resolved issue with YAML editor not updating from loaded files

### Technical Improvements
- Removed legacy configuration support for cleaner codebase
- Organized test structure with proper separation of unit, integration, and GUI tests
- Enhanced path exclusion logic for complex mounted volume scenarios
- Improved memory management and configuration handling

### Code Quality
- Comprehensive test coverage for mounted volume scenarios
- Clean separation of concerns between comparison types
- Proper error handling and validation throughout
- Documentation updates reflecting new architecture

## Testing Structure

### `/tests/`
- **Unit Tests**: Core functionality testing (scanner, comparator, utils)
- **`/tests/integration/`**: End-to-end workflow testing
- **`/tests/gui/`**: User interface and dialog testing

### Test Coverage
- Mounted volume exclusion scenarios
- Dual configuration system validation
- Configuration loading and saving
- Path matching and normalization
- Performance optimization validation

## Usage Patterns

### Typical Workflows
1. **Quick Structure Check**: Use Structure Comparison for fast directory tree analysis
2. **Content Verification**: Use Directory Comparison for deep file content validation
3. **Mounted Volume Analysis**: Automatic handling of complex mounted filesystem paths
4. **Configuration Management**: Save/load presets for different scanning scenarios

### Performance Optimization
- Structure Comparison: Optimized for speed with minimal exclusions
- Directory Comparison: Configurable for thoroughness vs performance
- Smart Threading: Automatic scaling based on system capabilities
- Memory Management: Configurable chunk sizes for different hardware

## Future Roadmap
- Real-time monitoring and incremental comparison
- Plugin system for custom comparison algorithms
- Network directory comparison support
- Advanced reporting with trend analysis
