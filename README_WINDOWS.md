# Breitling AeroSpace Evo Desktop Watch - Windows Setup

## Requirements

- Windows 10 or Windows 11
- Python 3.8 or later (download from python.org)

## Quick Start

1. **Run the setup script:**
   ```
   double-click setup\setup_windows.bat
   ```

2. **Launch the watch:**
   ```
   venv\Scripts\python main.py
   ```

   Or create a desktop shortcut with this target:
   ```
   "C:\path\to\clock\venv\Scripts\python.exe" "C:\path\to\clock\main.py"
   ```

## Features

### Watch Face
- **Analog display**: Shows local time with hour, minute, and second hands
- **Upper LCD**: Shows date and day of week
- **Lower LCD**: Shows UTC time
- **Rotating bezel**: Click and drag on the outer bezel ring to rotate it

### Controls
- **Left-click + drag on dial**: Move the watch window
- **Right-click**: Open context menu with options
- **Right-click menu**:
  - LCD Color: Select green, orange_gold, cyan, or amber
  - Close: Exit the application

### Theme Colors
The watch supports multiple LCD color themes:
| Theme | Color |
|-------|-------|
| green | Classic green LCD (default) |
| orange_gold | Breitling-inspired gold/orange |
| cyan | Modern cyan |
| amber | Warm amber |

Change colors via right-click menu or edit:
```
%APPDATA%\clock\settings.json
```

## Troubleshooting

**"python not found"**
- Install Python from python.org
- Make sure to check "Add Python to PATH" during installation

**Window doesn't show**
- Make sure no other Qt applications are conflicting
- Try running from Command Prompt to see error messages

**Display issues**
- The watch is fixed to the upper-left 512x768 area of the screen
- Edit `config.json` to change position or size

## Technical Details

- Window type: Frameless, always-on-top, transparent
- Display area: 512 x 768 pixels (upper portion of 1024x768 portrait display)
- Update rate: 1 second intervals
- Settings stored in: `%APPDATA%\clock\settings.json`

## Uninstall

1. Delete the `clock` folder
2. Delete `%APPDATA%\clock\` folder (settings)
3. Remove any desktop shortcuts