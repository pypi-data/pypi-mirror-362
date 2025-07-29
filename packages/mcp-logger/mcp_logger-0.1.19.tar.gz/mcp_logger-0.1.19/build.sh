#!/bin/bash

# Exit on error
set -e

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed"
    exit 1
fi

# Check if pip3 is available
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

# Install required packages if not already installed
pip3 install build twine

# Clean up any existing builds
rm -rf build/ dist/ *.egg-info/

# Build the package
python3 -m build

# If you want to publish, uncomment the following line and make sure you have your PyPI credentials set up
# python3 -m twine upload dist/* 