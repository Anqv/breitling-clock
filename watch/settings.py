import json
import os
import sys
from pathlib import Path


class Settings:
    DEFAULT_CONFIG = {
        "display": {
            "width": 1024,
            "height": 768,
            "watch_width": 512,
            "watch_height": 768,
            "offset_x": 0,
            "offset_y": 0
        },
        "theme": {
            "lcd_color": "amber",
            "available_colors": ["green", "orange_gold", "cyan", "amber"]
        },
        "background": {
            "image": ""
        },
        "bezel_rotation": 0
    }

    LCD_COLORS = {
        "green": {
            "primary": "#00ff00",
            "dim": "#004400",
            "background": "#0a1a0a"
        },
        "orange_gold": {
            "primary": "#ffaa00",
            "dim": "#553300",
            "background": "#1a1100"
        },
        "cyan": {
            "primary": "#00ffff",
            "dim": "#004444",
            "background": "#001a1a"
        },
        "amber": {
            "primary": "#ffdd00",
            "dim": "#665500",
            "background": "#000000"
        }
    }

    def __init__(self):
        self.config = self.DEFAULT_CONFIG.copy()
        self.config_file = self._get_config_path()
        self.load()

    def _get_config_path(self):
        project_config = Path(__file__).parent.parent / "config.json"
        if project_config.exists():
            return project_config
        if os.name == "nt":
            base = Path(os.environ.get("APPDATA", "."))
        else:
            base = Path.home() / ".config" / "clock"
        base.mkdir(parents=True, exist_ok=True)
        return base / "settings.json"

    def load(self):
        try:
            with open(self.config_file, "r") as f:
                loaded = json.load(f)
                self._merge_config(loaded)
        except Exception:
            pass

    def _merge_config(self, loaded):
        for key in self.DEFAULT_CONFIG:
            if key in loaded:
                if isinstance(self.DEFAULT_CONFIG[key], dict):
                    self.config[key].update(loaded[key])
                else:
                    self.config[key] = loaded[key]

    def save(self):
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass

    def get_lcd_colors(self):
        theme = self.config.get("theme", {}).get("lcd_color", "amber")
        return self.LCD_COLORS.get(theme, self.LCD_COLORS["green"])

    def set_lcd_color(self, color):
        if color in self.LCD_COLORS:
            self.config["theme"]["lcd_color"] = color
            self.save()

    def get_display_config(self):
        return self.config.get("display", self.DEFAULT_CONFIG["display"])

    def get_bezel_rotation(self):
        return self.config.get("bezel_rotation", 0)

    def set_bezel_rotation(self, angle):
        self.config["bezel_rotation"] = angle % 360
        self.save()


settings = Settings()