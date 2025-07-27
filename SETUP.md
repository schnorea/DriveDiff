# SD Card Comparison Tool - Setup Guide

## Prerequisites

### System Requirements
- Python 3.7 or higher
- Operating System: Windows, macOS, or Linux
- Memory: At least 512 MB RAM (more recommended for large comparisons)
- Storage: 50 MB free space for application and temporary files

### External Dependencies
- **Paragon extfs** (for SD card mounting on macOS/Windows)
  - Download from: https://www.paragon-software.com/home/extfs-mac/
  - Required for reading Linux ext2/ext3/ext4 filesystems on macOS and Windows

## Installation

### Option 1: Direct Python Execution (Recommended for Development)

1. **Clone or Download the Application**
   ```bash
   cd /path/to/your/projects
   # If using git:
   git clone <repository-url> DriveDiff
   # Or extract downloaded ZIP file
   ```

2. **Install Python Dependencies**
   ```bash
   cd DriveDiff
   pip install -r requirements.txt
   ```

3. **Run the Application**
   
   **On macOS/Linux:**
   ```bash
   ./run.sh
   ```
   
   **On Windows:**
   ```cmd
   run.bat
   ```
   
   **Or directly with Python:**
   ```bash
   python main.py
   ```

### Option 2: Using Virtual Environment (Recommended for Production)

1. **Create Virtual Environment**
   ```bash
   cd DriveDiff
   python -m venv venv
   ```

2. **Activate Virtual Environment**
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```cmd
   venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

## Configuration

### First Launch
- The application will create a configuration directory on first launch:
  - **Windows:** `%APPDATA%\SDCardComparison\`
  - **macOS:** `~/Library/Application Support/SDCardComparison/`
  - **Linux:** `~/.config/sdcardcomparison/`

### Settings
Access settings through the menu: `Edit > Settings...`

Key settings to configure:
- **Ignore Patterns:** File patterns to exclude from comparison
- **Performance:** Thread pool size and maximum file size for comparison
- **Appearance:** Font settings and color scheme
- **Behavior:** Auto-refresh and metadata comparison options

## SD Card Mounting

### macOS with Paragon extfs
1. Install Paragon extfs for macOS
2. Insert SD card
3. The card should appear in Finder as a mounted volume
4. Use the mounted path (e.g., `/Volumes/SD_CARD_NAME`) in the application

### Windows with Paragon extfs
1. Install Paragon extfs for Windows
2. Insert SD card
3. The card should appear in File Explorer with a drive letter
4. Use the drive path (e.g., `E:\`) in the application

### Linux (Native support)
1. Insert SD card
2. Most Linux distributions will auto-mount the card
3. Check `/media/username/` or `/mnt/` for the mount point
4. Use the mount path in the application

### Manual Mounting (Linux)
```bash
# Identify the device
lsblk

# Create mount point
sudo mkdir /mnt/sdcard

# Mount the device (replace /dev/sdX1 with actual device)
sudo mount /dev/sdX1 /mnt/sdcard

# Use /mnt/sdcard as the path in the application
```

## Troubleshooting

### Common Issues

#### "Permission Denied" Errors
- Ensure you have read permissions for the directories
- On Linux/macOS, you may need to adjust mount permissions:
  ```bash
  sudo mount -o uid=$(id -u),gid=$(id -g) /dev/sdX1 /mnt/sdcard
  ```

#### "Module Not Found" Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.7+)
- If using virtual environment, ensure it's activated

#### Slow Performance
- Reduce the number of files being compared by using ignore patterns
- Increase thread pool size in settings (but not beyond CPU core count)
- Ensure sufficient RAM is available

#### GUI Issues on Linux
- Install tkinter if not included: `sudo apt-get install python3-tk`
- For better appearance: `sudo apt-get install python3-tk-dev`

### File System Compatibility

| File System | Windows | macOS | Linux |
|-------------|---------|-------|-------|
| FAT32       | ✓       | ✓     | ✓     |
| exFAT       | ✓       | ✓     | ✓*    |
| NTFS        | ✓       | ✓*    | ✓*    |
| ext2/3/4    | ✓**     | ✓**   | ✓     |
| HFS+        | ✗       | ✓     | ✗     |

- ✓ = Native support
- ✓* = Requires additional software
- ✓** = Requires Paragon extfs
- ✗ = Not supported

## Usage Tips

### Best Practices
1. **Always safely eject SD cards** before removing them
2. **Use ignore patterns** to exclude temporary and system files
3. **Regular backups** of important data before making changes
4. **Verify mount points** before starting comparison

### Performance Optimization
- Close other applications when comparing large directories
- Use SSD storage for temporary files if available
- Increase virtual memory if comparing very large files

### Security Considerations
- The application only reads files during comparison
- No data is transmitted over the network
- Configuration files may contain recent directory paths
- Use caution when copying files between locations

## Support

### Log Files
- Application logs are stored in the configuration directory
- Include log files when reporting issues

### Reporting Issues
When reporting issues, please include:
- Operating system and version
- Python version
- Error messages or screenshots
- Steps to reproduce the problem
- SD card file system type

### Getting Help
1. Check this setup guide
2. Review error messages in the application
3. Check the configuration directory for log files
4. Consult the README.md file for additional information
