@echo off
REM This batch script uses PyInstaller to create an executable for the ps_console.py script.

REM Navigate to the directory containing the script
cd ..\src

REM Use PyInstaller to create the executable
pyinstaller --onefile ps_console.py

REM Move the generated executable to the scripts directory
move dist\ps_console.exe ..\scripts

REM Clean up build files
rmdir /s /q build
rmdir /s /q dist
del ps_console.spec

echo Build complete! The executable is located in the scripts directory.