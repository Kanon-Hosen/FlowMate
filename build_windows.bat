@echo off
REM ===================================================
REM ClipPilot Automated Windows Installer & Executable Builder
REM ===================================================

echo [1/3] Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo [2/3] Building standalone Windows executable (ClipPilot.exe)...
pyinstaller --noconfirm --onefile --windowed --name "ClipPilot" --add-data "assets;assets" --add-data "config;config" --icon "assets/logo.png" main.py

echo.
echo ===================================================
echo SUCCESS! Executable created at: dist\ClipPilot.exe
echo You can run dist\ClipPilot.exe on any Windows 10/11 PC!
echo ===================================================
pause
