# Path Exclusion Feature

## Overview

The DriveDiff tool now supports **separate configuration systems** for different comparison types, providing precise control over exclusions for each operation:

1. **Directory Comparison Configuration** - For detailed file content comparison
2. **Structure Comparison Configuration** - For directory structure analysis only

Each comparison type supports two complementary exclusion approaches:
- **Path-based exclusions** - Exclude specific absolute or relative paths
- **Pattern-based exclusions** - Exclude files/directories matching glob patterns

## Configuration Types

### Directory Comparison (`directory_comparison`)

Used for detailed file content comparison. Includes file inclusion patterns to filter which files are analyzed for content differences.

```yaml
directory_comparison:
  paths:
    scan: []              # Directories to scan (empty = scan entire directory)
    exclude:              # Specific paths to exclude
      - "/proc"
      - "/sys" 
      - "/tmp"
    include:              # File patterns to include for content analysis
      - "*.conf"
      - "*.json"
      - "*.yaml"
    exclude_patterns:     # File/directory patterns to exclude
      - "*/tmp/*"
      - "*/.git/*"
      - "*.pyc"
```

### Structure Comparison (`structure_comparison`)

Used for directory structure analysis only. Focuses on what directories exist, not file contents. Typically has more aggressive exclusions to provide cleaner structural views.

```yaml
structure_comparison:
  paths:
    scan: []              # Directories to scan (empty = scan entire directory)
    exclude:              # Specific paths to exclude (more aggressive than directory comparison)
      - "/proc"
      - "/sys"
      - "/tmp"
      - "/var/log"        # Additional exclusions for cleaner structure view
      - "/var/spool"
    exclude_patterns:     # Directory patterns to exclude
      - "*/tmp/*"
      - "*/.git/*"
      - "*/build/*"
```

**Note**: Structure comparison does not use include patterns since it analyzes directory structure, not file contents.

## Enhanced Mounted Volume Support

The exclusion system now intelligently handles mounted volumes and different filesystem roots:

```yaml
# These path exclusions:
exclude:
  - "/usr/share"
  - "/tmp"
  - "/var/cache"

# Now automatically match mounted volume paths:
# ✅ /Volumes/rootfs/usr/share
# ✅ /mnt/backup/tmp
# ✅ /media/disk/var/cache
```

**How it works**: The system uses intelligent pattern matching that recognizes when system paths appear in mounted volume contexts, ensuring exclusions work regardless of mount point.
## Configuration Examples

### Directory Comparison Configuration

For detailed file comparison with content analysis:

```yaml
directory_comparison:
  paths:
    scan: []
    exclude:
      - "/proc"
      - "/sys" 
      - "/dev"
      - "/tmp"
      - "/var/cache"
    include:
      - "*.conf"
      - "*.config"
      - "*.json"
      - "*.yaml"
      - "*.xml"
      - "*.txt"
      - "*.log"
    exclude_patterns:
      - "*/tmp/*"
      - "*/.git/*"
      - "*/node_modules/*"
      - "*/__pycache__/*"
      - "*.pyc"
      - "*/build/*"
      - "*/dist/*"
```

### Structure Comparison Configuration

For directory structure analysis (more aggressive exclusions):

```yaml
structure_comparison:
  paths:
    scan: []
    exclude:
      - "/proc"
      - "/sys"
      - "/dev" 
      - "/tmp"
      - "/var/cache"
      - "/var/log"        # Additional exclusions for structure analysis
      - "/var/spool"
      - "/opt"
      - "/media"
      - "/mnt"
    exclude_patterns:
      - "*/tmp/*"
      - "*/.git/*"
      - "*/node_modules/*"
      - "*/__pycache__/*"
      - "*/build/*"
      - "*/cache/*"
      - "*/media/*"
      - "*/mnt/*"
```

## Usage Examples

### Configuring via GUI

1. Open DriveDiff
2. Go to `Edit` → `Scan Configuration...`
3. Use the **📁 Directory Comparison** tab for file comparison exclusions
4. Use the **🌳 Structure Comparison** tab for structure analysis exclusions
5. Configure each type independently
6. Click **Apply** or **OK** to save changes

### Common Exclusion Patterns

**For System Directories (both comparison types):**
```yaml
exclude:
  - "/proc"
  - "/sys" 
  - "/dev"
  - "/run"
```

**For Development Projects (directory comparison):**
```yaml
include:
  - "*.js"
  - "*.ts"
  - "*.py"
  - "*.json"
exclude_patterns:
  - "*/node_modules/*"
  - "*/.git/*"
  - "*/build/*"
  - "*/__pycache__/*"
```

**For Structure Analysis (structure comparison):**
```yaml
exclude:
  - "/var/log"      # Exclude log directories from structure view
  - "/var/spool"    # Exclude spool directories
  - "/opt"          # Exclude optional software
exclude_patterns:
  - "*/cache/*"     # More aggressive cache exclusion
  - "*/build/*"     # Exclude all build directories
```

### Testing Exclusions

You can test your exclusion patterns using the Python API:

```python
from src.utils.yaml_config import YamlConfigManager
from src.core.directory_scanner import DirectoryScanner

# Load configuration manager
config_manager = YamlConfigManager()

# Test directory comparison exclusions
dir_scanner = DirectoryScanner.from_config(config_manager, "directory")
test_paths = ["/tmp/test", "/var/cache/test", "normal/path"]
for path in test_paths:
    excluded = dir_scanner._should_exclude_path(path)
    print(f"Directory comparison - {path}: {'EXCLUDED' if excluded else 'included'}")

# Test structure comparison exclusions  
struct_scanner = DirectoryScanner.from_config(config_manager, "structure")
for path in test_paths:
    excluded = struct_scanner._should_exclude_path(path)
    print(f"Structure comparison - {path}: {'EXCLUDED' if excluded else 'included'}")
```

## Configuration File Structure

The YAML configuration supports this dual structure:

```yaml
# Logging configuration (shared)
logging:
  level: "INFO"

# Directory comparison configuration
directory_comparison:
  paths:
    scan: []              # Directories to scan (empty = scan entire directory)
    exclude:              # Specific paths to exclude
      - "/proc"
      - "/sys"
      - "/tmp"
    include:              # File patterns to include (for content analysis)
      - "*.conf"
      - "*.json"
      - "*.yaml"
    exclude_patterns:     # File/directory patterns to exclude
      - "*/tmp/*"
      - "*/.git/*"
      - "*.pyc"

# Structure comparison configuration
structure_comparison:
  paths:
    scan: []              # Directories to scan (empty = scan entire directory)
    exclude:              # Specific paths to exclude (typically more aggressive)
      - "/proc"
      - "/sys"
      - "/tmp"
      - "/var/log"        # Additional exclusions for cleaner structure view
      - "/var/spool"
    exclude_patterns:     # Directory patterns to exclude
      - "*/tmp/*"
      - "*/.git/*"
      - "*/build/*"

# Performance settings (shared)
performance:
  worker_threads: 4
  hash_chunk_size: 65536
  max_files: 0
```

## Benefits of Dual Configuration

1. **Precise Control**: Different exclusion rules for different comparison types
2. **Cleaner Structure Analysis**: More aggressive exclusions for structure comparison
3. **Flexible File Analysis**: Include patterns only apply to directory comparison
4. **Better Performance**: Each comparison type optimized for its specific purpose
5. **Simplified Management**: Two focused tabs in GUI for clear configuration

The path exclusion feature provides powerful, flexible control over what gets scanned and compared, leading to faster, more focused directory comparisons.
