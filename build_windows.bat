@echo off
REM ===================================================
REM FlowMate Automated Windows Installer & Executable Builder
REM ===================================================

echo [1/3] Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo [2/3] Building standalone Windows executable (FlowMate.exe)...
pyinstaller --noconfirm --onefile --windowed --name "FlowMate" --add-data "assets;assets" --add-data "config;config" --icon "assets/logo.png" main.py

echo.
echo ===================================================
echo SUCCESS! Executable created at: dist\FlowMate.exe
echo You can run dist\FlowMate.exe on any Windows 10/11 PC!
echo ===================================================
pause
