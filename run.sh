#!/bin/bash

# SD Card Comparison Tool Launch Script

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python 3 is required but not found in PATH"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.7"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
$PYTHON_CMD -c "
import sys
missing_packages = []

try:
    import tkinter
except ImportError:
    missing_packages.append('tkinter (usually included with Python)')

try:
    import chardet
except ImportError:
    missing_packages.append('chardet')

try:
    import PIL
except ImportError:
    missing_packages.append('Pillow')

if missing_packages:
    print('Missing required packages:')
    for pkg in missing_packages:
        print(f'  - {pkg}')
    print()
    print('Please install missing packages with:')
    print('  pip install -r requirements.txt')
    sys.exit(1)
else:
    print('All dependencies found.')
"

if [ $? -ne 0 ]; then
    exit 1
fi

# Launch the application
echo "Starting SD Card Comparison Tool..."
$PYTHON_CMD main.py "$@"
