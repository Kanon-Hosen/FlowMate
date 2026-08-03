#!/bin/bash
# ClipPilot Automated Setup Script for New Computers

echo "⚡ Setting up ClipPilot on new computer..."

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

# 4. Create desktop shortcut & system application menu launcher
echo "Creating desktop shortcut and app menu entry..."
DESKTOP_FILE="$HOME/Desktop/ClipPilot.desktop"
SYSTEM_APP_FILE="$HOME/.local/share/applications/ClipPilot.desktop"
APP_DIR=$(pwd)

cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=ClipPilot
GenericName=Automatic Video & File Pilot
Comment=Automatically detect completed video downloads, rename them sequentially, and move them into project folders.
Exec=python3 $APP_DIR/main.py
Icon=$APP_DIR/assets/logo.png
Path=$APP_DIR
Terminal=false
Categories=Utility;FileManager;
StartupWMClass=ClipPilot
EOF

chmod +x "$DESKTOP_FILE"
gio trust "$DESKTOP_FILE" 2>/dev/null || true

mkdir -p "$HOME/.local/share/applications"
cp "$DESKTOP_FILE" "$SYSTEM_APP_FILE"
chmod +x "$SYSTEM_APP_FILE"
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true

echo "✅ Setup complete! You can now run ClipPilot using:"
echo "   python3 main.py"
echo "or click the ClipPilot icon in your applications menu!"
