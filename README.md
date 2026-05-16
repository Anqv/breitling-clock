# Breitling AeroSpace Evo Desktop Watch

A realistic analog desktop watch with a Breitling AeroSpace Evo-inspired design, featuring:

- **Photo-realistic watch face** with custom background image support
- **Rotating bezel** - interactive bezel that rotates with mouse/touch drag
- **Smooth analog hands** - hour, minute, and second hands with millisecond precision
- **Dual LCD displays** using DSEG7 Classic font:
  - Upper: Date + Day (e.g., "16:05 sat")
  - Lower: Configurable timezone time (UTC or ±1-12h offset)
- **Multiple LCD color themes**: Amber (default), Green, Orange/Gold, Cyan
- **Cross-platform**: Works on Windows 11 and Raspberry Pi 4/5

## Quick Links

- **[Windows Setup](README_WINDOWS.md)**
- **[Raspberry Pi Setup](README_RASPBERRYPI.md)**

## Project Structure

```
clock/
├── main.py                    # Entry point
├── config.json                # Display and theme settings
├── requirements.txt           # Python dependencies
├── watch/
│   ├── main_window.py         # Window configuration
│   ├── watch_face.py          # Main watch widget
│   ├── renderer.py            # Watch rendering with LCD
│   ├── bezel.py               # Bezel rotation logic
│   ├── settings.py            # Configuration management
│   └── weather.py             # Weather placeholder
├── assets/
│   ├── watch_face.png         # Watch face background image
│   ├── watch_bezel_without_face.png  # Rotating bezel image
│   ├── fonts/
│   │   └── DSEG7Classic-Bold.ttf     # 7-segment LCD font
├── setup/
│   ├── setup_windows.bat      # Windows installer
│   └── setup_pi.sh           # Raspberry Pi installer
├── autostart/
│   └── clock.desktop         # Pi autostart entry
└── README_*.md               # Platform-specific docs
```

## Display Layout

```
┌─────────────────────────────┐  ← Upper 512x768 (watch)
│   ╭════════════════════╮   │  ← Rotating bezel
│   │   BREITLING        │   │
│   │   ┌────────────┐   │   │  ← Upper LCD: Date + Day
│   │   │ 16:05 sat  │   │   │
│   │   └────────────   │   │
│   │    ANALOG HANDS    │   │  ← Smooth sweeping hands
│   │   ┌────────────┐   │   │
│   │   │ 14:32:45   │   │   │  ← Lower LCD: UTC time
│   │   └────────────┘   │   │
│   ╰════════════════════╯   │
└─────────────────────────────┘  ← Lower 512x768 (future weather)
```

## Theme Colors

| Theme | LCD Color |
|-------|-----------|
| amber | Warm amber (#ffdd00) - default |
| green | Classic green (#00ff00) |
| orange_gold | Breitling gold (#ffaa00) |
| cyan | Modern cyan (#00ffff) |

## Configuration

Edit `config.json` to customize:

```json
{
  "display": {
    "width": 1024,
    "height": 768,
    "watch_width": 512,
    "watch_height": 768,
    "offset_x": 0,
    "offset_y": 0
  },
  "theme": {
    "lcd_color": "amber"
  },
  "background": {
    "image": "assets/watch_face_clean_blue.png"
  },
  "lower_lcd": {
    "timezone": "UTC"
  },
  "bezel_rotation": 0
}
```

## Features

### Watch Face
- Custom background image support (PNG, JPG, BMP)
- Rotating bezel with mouse/touch drag
- Bezel rotation angle saved between sessions

### LCD Displays
- DSEG7 Classic 7-segment font for authentic LCD look
- Upper LCD: Date (DD:MM) + 3-letter English day name
- Lower LCD: Configurable timezone time (HH:MM:SS)
  - Set `"timezone": "UTC"` in config for UTC time (shows "UTC" label)
  - Set `"timezone": "+1"` to `"+12"` or `"-1"` to `"-12"` for hour offsets
- No background fill - uses image's black LCD areas

### Analog Hands
- Smooth sweeping motion with millisecond precision
- Hour hand: 12-hour cycle with minute/second interpolation
- Minute hand: 60-minute cycle with second interpolation
- Second hand: Continuous smooth movement

## Requirements

- **Windows**: Python 3.8+, PyQt5
- **Raspberry Pi**: Python 3.8+, PyQt5, display

## Get Started

**Windows**: Run `setup\setup_windows.bat` then `venv\Scripts\python main.py`

**Raspberry Pi**: Run `setup\setup_pi.sh` and reboot

See platform-specific README files for detailed instructions.

## Controls

- **Right-click**: Open context menu to change LCD color theme
- **Drag bezel**: Click and drag on the outer bezel to rotate it
- **Drag window**: Click and drag on the watch face to reposition
