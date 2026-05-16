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
- **Photo-realistic background** - Custom watch face image
- **Rotating bezel** - Click and drag on the outer bezel to rotate
- **Smooth analog hands** - Hour, minute, and second hands with millisecond precision
- **Dual LCD displays** with DSEG7 Classic 7-segment font:
  - Upper LCD: Date + Day (e.g., "16:05 sat")
  - Lower LCD: UTC time (e.g., "14:32:45")

### Controls
- **Left-click + drag on bezel**: Rotate the bezel
- **Left-click + drag on dial**: Move the watch window
- **Right-click**: Open context menu with options
- **Right-click menu**:
  - LCD Color: Select amber (default), green, orange_gold, or cyan
  - Close: Exit the application

### Theme Colors
The watch supports multiple LCD color themes:
| Theme | Color |
|-------|-------|
| amber | Warm amber (#ffdd00) - default |
| green | Classic green (#00ff00) |
| orange_gold | Breitling-inspired gold/orange |
| cyan | Modern cyan |

Change colors via right-click menu or edit:
```
%APPDATA%\clock\settings.json
```

## Configuration

Edit `config.json` to customize display settings, background image, and theme.

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

**LCD not visible**
- Ensure the background image has black LCD areas
- Check that DSEG7 font is in `assets/fonts/`

## Technical Details

- Window type: Frameless, always-on-top, transparent
- Display area: 512 x 768 pixels (upper portion of 1024x768 portrait display)
- Update rate: 200ms (5 updates per second for smooth hand movement)
- Settings stored in: `%APPDATA%\clock\settings.json`

## Uninstall

1. Delete the `clock` folder
2. Delete `%APPDATA%\clock\` folder (settings)
3. Remove any desktop shortcuts
