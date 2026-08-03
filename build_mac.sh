#!/usr/bin/env bash
# ===================================================
# ClipPilot Automated macOS Installer & Application Builder
# ===================================================

echo "[1/3] Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install pyinstaller

echo "[2/3] Building standalone macOS Application (ClipPilot.app)..."
pyinstaller --noconfirm --onedir --windowed \
    --name "ClipPilot" \
    --add-data "assets:assets" \
    --add-data "config:config" \
    --icon "assets/logo.png" \
    main.py

echo ""
echo "==================================================="
echo "SUCCESS! macOS App Bundle created at: dist/ClipPilot.app"
echo "You can double-click dist/ClipPilot.app on macOS!"
echo "==================================================="
