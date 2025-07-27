@echo off
REM SD Card Comparison Tool Launch Script for Windows

REM Change to the script directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python 3 is required but not found in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

REM Check if required packages are installed
echo Checking dependencies...
python -c "
import sys
missing_packages = []

try:
    import tkinter
except ImportError:
    missing_packages.append('tkinter (should be included with Python)')

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

if %errorlevel% neq 0 (
    pause
    exit /b 1
)

REM Launch the application
echo Starting SD Card Comparison Tool...
python main.py %*

REM Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)
