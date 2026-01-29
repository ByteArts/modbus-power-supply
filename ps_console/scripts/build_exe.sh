#!/bin/bash
# This script builds the Windows executable for the ps_console program using PyInstaller.

# Navigate to the source directory
cd ../src

# Use PyInstaller to create the executable
pyinstaller --onefile ps_console.py

# Move the generated executable to the scripts directory
mv dist/ps_console ../scripts/

# Clean up build artifacts
rm -rf build dist ps_console.spec

echo "Executable built successfully and moved to the scripts directory."