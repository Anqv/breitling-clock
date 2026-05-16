# Breitling AeroSpace Evo Desktop Watch - Raspberry Pi Setup

## Requirements

- Raspberry Pi 4 or Raspberry Pi 5
- Raspberry Pi OS (Desktop or Lite with desktop)
- 1024x768 portrait display recommended (or adjust in config)
- Internet connection for installation

## Quick Start (Automated)

1. Copy the `clock` folder to your Raspberry Pi:
   ```
   scp -r clock pi@raspberrypi.local:/home/pi/
   ```

2. SSH into your Pi and run setup:
   ```
   cd /home/pi/clock
   chmod +x setup/setup_pi.sh
   ./setup_pi.sh
   ```

3. **Reboot** - the watch will start automatically:
   ```
   sudo reboot
   ```

## Quick Start (Manual)

If you prefer to run without autostart:

```bash
cd /home/pi/clock
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Features

### Watch Face
- **Photo-realistic background** - Custom watch face image
- **Rotating bezel** - Touch/drag on the outer bezel to rotate
- **Smooth analog hands** - Hour, minute, and second hands with millisecond precision
- **Dual LCD displays** with DSEG7 Classic 7-segment font:
  - Upper LCD: Date + Day (e.g., "16:05 sat")
  - Lower LCD: UTC time (e.g., "14:32:45")

### Controls
- **Touch/drag on bezel**: Rotate the bezel
- **Touch/drag on dial**: Move the watch window
- **Right-click**: Open context menu (mouse or touch-and-hold)
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
~/.config/clock/settings.json
```

## Auto-Start Configuration

The setup script creates:
- Virtual environment: `~/clock/venv/`
- Start script: `~/clock/start.sh`
- Desktop entry: `~/.config/autostart/breitling-clock.desktop`

### Check if autostart is working:
```bash
cat ~/.config/autostart/breitling-clock.desktop
```

### Disable autostart:
```bash
rm ~/.config/autostart/breitling-clock.desktop
```

## Display Configuration

Edit `config.json` to adjust display:

```json
{
  "display": {
    "width": 1024,
    "height": 768,
    "watch_width": 512,
    "watch_height": 768,
    "offset_x": 0,
    "offset_y": 0
  }
}
```

- `watch_width` x `watch_height`: Size of the watch window
- `offset_x` x `offset_y`: Position on screen

For a 1024x768 portrait display showing watch in upper half:
- Watch area: 512x768 at position (0, 0)
- Lower area (512x768) reserved for future weather display

## Troubleshooting

**No display visible:**
- Check HDMI connection
- Ensure display resolution matches config.json

**Watch doesn't start on boot:**
```bash
# Check if desktop entry is enabled
cat ~/.config/autostart/breitling-clock.desktop

# Test manually
/home/pi/clock/start.sh
```

**Touch not working:**
- Ensure touchscreen drivers are installed
- Try right-click with long press

**LCD colors appear wrong:**
- Edit settings: `nano ~/.config/clock/settings.json`
- Change `"lcd_color"` to your preferred theme

**LCD not visible:**
- Ensure the background image has black LCD areas
- Check that DSEG7 font is in `assets/fonts/`

## Technical Details

- Window type: Frameless, always-on-top, transparent
- Display area: 512 x 768 pixels
- Update rate: 200ms (5 updates per second for smooth hand movement)
- Settings stored in: `~/.config/clock/settings.json`

## Future Features

The lower half of the display (512x768) is reserved for:
- Weather information display
- Integration with weather APIs (OpenWeatherMap)

## Uninstall

```bash
# Remove autostart
rm ~/.config/autostart/breitling-clock.desktop

# Remove settings
rm -rf ~/.config/clock/

# Remove clock folder
rm -rf ~/clock
```

## Support

For issues, check:
1. Python is installed: `python3 --version`
2. PyQt5 installed: `source ~/clock/venv/bin/activate && pip list`
3. Display connection: Check `/dev/fb0` or HDMI output
