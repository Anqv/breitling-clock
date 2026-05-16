# Breitling AeroSpace Evo Desktop Watch

A realistic analog desktop watch with a Breitling AeroSpace Evo-inspired design, featuring:

- **3D watch case and bezel** with titanium brushed metal appearance
- **Analog hands** showing local time
- **Dual LCD displays**: Date/Day (upper) and UTC time (lower)
- **Rotating bezel** - interactive bezel that can be rotated with mouse/touch
- **Multiple LCD color themes**: Green (default), Orange/Gold, Cyan, Amber
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
│   ├── renderer.py            # 3D watch rendering
│   ├── bezel.py               # Bezel rotation logic
│   ├── settings.py            # Configuration management
│   └── weather.py             # Weather placeholder
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
│   BREITLING AEROSPACE       │
│   ┌─────────────────────┐   │
│   │  LCD: Date/Day      │   │
│   ├─────────────────────┤   │
│   │    ANALOG HANDS     │   │
│   ├─────────────────────┤   │
│   │  LCD: UTC Time      │   │
│   └─────────────────────┘   │
│   ╭════════════════════╮   │
│   ╰════════════════════╯   │
└─────────────────────────────┘  ← Lower 512x768 (future weather)
```

## Theme Colors

| Theme | LCD Color |
|-------|-----------|
| green | Classic green (#00ff00) |
| orange_gold | Breitling gold (#ffaa00) |
| cyan | Modern cyan (#00ffff) |
| amber | Warm amber (#ffbf00) |

## Requirements

- **Windows**: Python 3.8+, PyQt5
- **Raspberry Pi**: Python 3.8+, PyQt5, display

## Get Started

**Windows**: Run `setup\setup_windows.bat` then `venv\Scripts\python main.py`

**Raspberry Pi**: Run `setup\setup_pi.sh` and reboot

See platform-specific README files for detailed instructions.