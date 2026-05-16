#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "========================================"
echo "Breitling AeroSpace Evo Clock - Setup"
echo "========================================"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Install with: sudo apt install python3"
    exit 1
fi

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/4] Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
deactivate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[3/4] Creating autostart entry..."

mkdir -p ~/.config/autostart

cat > ~/.config/autostart/breitling-clock.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Breitling Clock
Comment=Breitling AeroSpace Evo Desktop Watch
Exec=/home/pi/clock/start.sh
Terminal=false
Hidden=false
X-GNOME-Autostart-enabled=true
EOF

echo "[4/4] Creating start script..."
cat > start.sh << 'EOF'
#!/bin/bash
cd /home/pi/clock
source venv/bin/activate
python3 main.py
EOF

chmod +x start.sh

echo
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo
echo "The watch will start automatically on next boot."
echo
echo "To run manually:"
echo "  ./start.sh"
echo
echo "To test now:"
echo "  source venv/bin/activate"
echo "  python3 main.py"
echo
echo "To change LCD color, right-click on the watch"
echo "or edit: ~/.config/clock/settings.json"
echo
read -p "Press Enter to continue..."