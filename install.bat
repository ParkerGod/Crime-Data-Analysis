@echo off
echo ==========================================
echo Crime Data Analysis - Installation Script
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing required packages...
echo This may take a few minutes...
pip install -r requirements.txt

REM Check installation
echo.
echo Verifying installation...
python -c "import pandas; import matplotlib; import seaborn; print('All packages installed successfully!')"

if errorlevel 1 (
    echo.
    echo Error: Some packages failed to install
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Installation completed successfully!
echo ==========================================
echo.
echo To run the analysis:
echo   1. Activate the virtual environment: venv\Scripts\activate.bat
echo   2. Run: python main.py -i your_data.csv
echo.
pause
