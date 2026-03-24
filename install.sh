#!/bin/bash

echo "=========================================="
echo "Crime Data Analysis - Installation Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing required packages..."
echo "This may take a few minutes..."
pip install -r requirements.txt

# Check installation
echo ""
echo "Verifying installation..."
python3 -c "import pandas; import matplotlib; import seaborn; print('All packages installed successfully!')"

if [ $? -ne 0 ]; then
    echo ""
    echo "Error: Some packages failed to install"
    exit 1
fi

echo ""
echo "=========================================="
echo "Installation completed successfully!"
echo "=========================================="
echo ""
echo "To run the analysis:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run: python main.py -i your_data.csv"
echo ""
