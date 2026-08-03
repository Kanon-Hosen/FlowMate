#!/bin/bash
# FlowMate Automated Setup Script for New Computers

echo "⚡ Setting up FlowMate on new computer..."

# 1. Update system packages & ensure Python 3 & pip exist
sudo apt update && sudo apt install -y python3 python3-pip python3-venv

# 2. Create virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# 3. Install dependencies
echo "Installing requirements..."
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

# 4. Create desktop shortcut launcher
echo "Creating desktop shortcut..."
DESKTOP_FILE="$HOME/Desktop/FlowMate.desktop"
APP_DIR=$(pwd)

cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=FlowMate
GenericName=Automatic File Renamer & Organizer
Comment=Automatically detect completed video downloads, rename them sequentially, and move them into project folders.
Exec=python3 $APP_DIR/main.py
Icon=$APP_DIR/assets/logo.png
Path=$APP_DIR
Terminal=false
Categories=Utility;FileManager;
StartupWMClass=FlowMate
EOF

chmod +x "$DESKTOP_FILE"
gio trust "$DESKTOP_FILE" 2>/dev/null || true

echo "✅ Setup complete! You can now run FlowMate using:"
echo "   python3 main.py"
echo "or double-click the FlowMate icon on your desktop!"
