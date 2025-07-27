# Panel Names Feature Documentation

## Overview
The File Viewer now supports customizable panel names, allowing users to label the left and right panels with meaningful names that reflect their specific comparison context.

## Features

### 1. **Custom Panel Names**
- Replace generic "Left File" and "Right File" labels with custom names
- Names appear in the LabelFrame headers above each file panel
- Useful for context-specific comparisons (e.g., "Original" vs "Modified")

### 2. **Easy-to-Use Dialog**
- Click "Panel Names..." button in the file viewer controls
- Simple dialog with text fields for left and right panel names
- Real-time preview of changes

### 3. **Built-in Presets**
Six useful preset combinations:
- **Original / Modified** - For version comparisons
- **Source / Target** - For deployment comparisons  
- **Before / After** - For change tracking
- **Old / New** - For update comparisons
- **Local / Remote** - For synchronization comparisons
- **Default** - Reset to "Left File" / "Right File"

### 4. **Persistent Settings**
- Panel names are automatically saved to YAML configuration
- Settings persist between application sessions
- Integrated with existing configuration system

### 5. **Programmatic API**
```python
# Set custom names
file_viewer.set_panel_names("Source Code", "Production Code")

# Get current names
left_name, right_name = file_viewer.get_panel_names()

# Reset to defaults
file_viewer.reset_panel_names()
```

## Usage Examples

### Example 1: Code Review
```
Left Panel: "Current Branch"
Right Panel: "Feature Branch"
```

### Example 2: Configuration Management
```
Left Panel: "Development Config"
Right Panel: "Production Config"
```

### Example 3: Backup Comparison
```
Left Panel: "Original Files"
Right Panel: "Backup Files"
```

### Example 4: Document Revision
```
Left Panel: "Draft v1.0"
Right Panel: "Draft v2.0"
```

## Configuration File Integration

Panel names are stored in the YAML configuration under the `ui` section:

```yaml
ui:
  panel_names:
    left: "Source"
    right: "Target"
  file_viewer:
    sync_scrolling: true
    font_size: 10
    default_view: "side_by_side"
```

## Benefits

1. **Improved Context**: Clear labels help users understand what they're comparing
2. **Professional Appearance**: Custom names make the interface more polished
3. **Workflow Integration**: Names can reflect specific business processes
4. **User Experience**: Reduces cognitive load by providing meaningful labels
5. **Flexibility**: Easily change names for different comparison scenarios

## Technical Implementation

- **Backend**: Enhanced FileViewer class with panel name management
- **Frontend**: Intuitive dialog with preset buttons and custom text fields
- **Persistence**: YAML configuration integration with automatic saving
- **Validation**: Automatic fallback to defaults for empty names
- **Error Handling**: Graceful handling of configuration loading/saving issues

This feature enhances the user experience by providing contextual clarity for file comparisons, making the tool more professional and user-friendly for various comparison scenarios.
