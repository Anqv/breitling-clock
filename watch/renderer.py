import math
import os
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import (
    QPainter, QColor, QPen, QBrush, QLinearGradient, QRadialGradient,
    QFont, QPainterPath, QFontMetrics, QPixmap, QImage
)
from PyQt5.Qt import QPen


def _c(hex_color):
    hex_color = hex_color.lstrip('#')
    return QColor(int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))


class WatchRenderer:
    def __init__(self, settings):
        self.settings = settings
        self.lcd_colors = self.settings.get_lcd_colors()
        self.background_image = None
        self._load_background()

    def _load_background(self):
        bg_config = self.settings.config.get("background", {})
        image_path = bg_config.get("image", "")
        if image_path:
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            full_path = os.path.join(project_dir, image_path)
            if os.path.exists(full_path):
                self.background_image = QPixmap(full_path)

    def reload_background(self):
        self.background_image = None
        self._load_background()

    def render(self, painter, width, height, time_data, bezel_angle):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        cx, cy = width / 2, height / 2
        outer_radius = min(width, height) * 0.45
        bezel_width = outer_radius * 0.12

        if self.background_image and not self.background_image.isNull():
            scaled = self.background_image.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled)
        else:
            self._draw_3d_case(painter, cx, cy, outer_radius + bezel_width)
            self._draw_3d_bezel(painter, cx, cy, outer_radius, bezel_width, bezel_angle)
            self._draw_dial(painter, cx, cy, outer_radius - bezel_width * 0.5)
            self._draw_hour_markers(painter, cx, cy, outer_radius - bezel_width * 0.7)

        self._draw_lcd_displays(painter, cx, cy, outer_radius, time_data)
        self._draw_analog_hands(painter, cx, cy, outer_radius - bezel_width * 0.8, time_data)
        self._draw_center_cap(painter, cx, cy, outer_radius * 0.06)

    def _draw_3d_case(self, painter, cx, cy, radius):
        gradient = QRadialGradient(cx, cy, radius)
        gradient.setColorAt(0, _c("#4a4a4a"))
        gradient.setColorAt(0.7, _c("#2a2a2a"))
        gradient.setColorAt(0.85, _c("#1a1a1a"))
        gradient.setColorAt(1, _c("#0a0a0a"))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(cx, cy), radius, radius)

        shadow = QRadialGradient(cx, cy + radius * 0.1, radius * 1.2)
        shadow.setColorAt(0, QColor(0, 0, 0, 60))
        shadow.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(shadow))
        painter.drawEllipse(QPointF(cx, cy), radius, radius)

    def _draw_3d_bezel(self, painter, cx, cy, radius, bezel_width, rotation):
        inner_r = radius - bezel_width * 0.3
        outer_r = radius + bezel_width * 0.7

        gradient = QRadialGradient(cx - radius * 0.3, cy - radius * 0.3, radius * 1.5)
        gradient.setColorAt(0, _c("#888888"))
        gradient.setColorAt(0.3, _c("#666666"))
        gradient.setColorAt(0.5, _c("#444444"))
        gradient.setColorAt(0.7, _c("#333333"))
        gradient.setColorAt(1, _c("#222222"))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(cx, cy), outer_r, outer_r)

        painter.setBrush(QBrush(_c("#1a1a1a")))
        painter.drawEllipse(QPointF(cx, cy), inner_r, inner_r)

        self._draw_bezel_markers(painter, cx, cy, inner_r, outer_r, rotation)

        highlight = QRadialGradient(cx - radius * 0.4, cy - radius * 0.4, radius * 0.8)
        highlight.setColorAt(0, QColor(255, 255, 255, 40))
        highlight.setColorAt(0.5, QColor(255, 255, 255, 10))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(highlight))
        painter.drawEllipse(QPointF(cx, cy), outer_r * 0.95, outer_r * 0.95)

    def _draw_bezel_markers(self, painter, cx, cy, inner_r, outer_r, rotation):
        painter.setPen(QPen(_c("#aaaaaa"), 2))
        for i in range(60):
            angle = math.radians(i * 6 + rotation)
            is_major = i % 5 == 0
            len_factor = 0.15 if is_major else 0.08

            x1 = cx + math.sin(angle) * (inner_r)
            y1 = cy - math.cos(angle) * (inner_r)
            x2 = cx + math.sin(angle) * (inner_r + (outer_r - inner_r) * len_factor)
            y2 = cy - math.cos(angle) * (inner_r + (outer_r - inner_r) * len_factor)

            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

    def _draw_dial(self, painter, cx, cy, radius):
        gradient = QLinearGradient(cx - radius, cy - radius, cx + radius, cy + radius)
        gradient.setColorAt(0, _c("#3a3a3a"))
        gradient.setColorAt(0.5, _c("#252525"))
        gradient.setColorAt(1, _c("#3a3a3a"))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(cx, cy), radius, radius)

        inner_r = radius * 0.85
        painter.setBrush(QBrush(_c("#1a1a1a")))
        painter.drawEllipse(QPointF(cx, cy), inner_r, inner_r)

    def _draw_hour_markers(self, painter, cx, cy, radius):
        font = QFont("Arial")
        font.setPointSize(int(radius * 0.12))
        font.setWeight(QFont.Bold)
        font.setLetterSpacing(QFont.PercentageSpacing, 120)
        painter.setFont(font)

        major_nums = {12: "12", 3: "3", 6: "6", 9: "9"}
        for hour in range(1, 13):
            angle = math.radians(hour * 30 - 90)
            if hour in major_nums:
                dist = radius * 0.75
                painter.setPen(QPen(_c("#ffffff"), 2))
                fm = QFontMetrics(font)
                w = fm.horizontalAdvance(major_nums[hour])
                h = fm.height()
                px = cx + math.cos(angle) * dist - w / 2
                py = cy + math.sin(angle) * dist + h / 4
                painter.drawText(QPointF(px, py), major_nums[hour])
            else:
                len_factor = 0.12
                x1 = cx + math.cos(angle) * (radius * (1 - len_factor))
                y1 = cy + math.sin(angle) * (radius * (1 - len_factor))
                x2 = cx + math.cos(angle) * (radius)
                y2 = cy + math.sin(angle) * (radius)
                painter.setPen(QPen(_c("#888888"), 2))
                painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        for i in range(60):
            if i % 5 != 0:
                angle = math.radians(i * 6 - 90)
                len_factor = 0.06
                x1 = cx + math.cos(angle) * (radius * (1 - len_factor))
                y1 = cy + math.sin(angle) * (radius * (1 - len_factor))
                x2 = cx + math.cos(angle) * (radius)
                y2 = cy + math.sin(angle) * (radius)
                gradient = QRadialGradient(x2 - len_factor * radius * 0.3, y2 - len_factor * radius * 0.3, radius * 0.1)
                gradient.setColorAt(0, _c("#cccccc"))
                gradient.setColorAt(0.5, _c("#999999"))
                gradient.setColorAt(1, _c("#666666"))
                painter.setPen(QPen(_c("#888888"), 1))
                painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

    def _draw_lcd_displays(self, painter, cx, cy, radius, time_data):
        lcd = self.settings.get_lcd_colors()
        primary = _c(lcd["primary"])
        bg = _c(lcd["background"])

        upper_y = cy - radius * 0.20
        lower_y = cy + radius * 0.25
        lcd_width = radius * 1.3 * 0.67
        lcd_height = radius * 0.25

        date_str = time_data.get("date", "16:05")
        utc_str = time_data.get("utc", "14:32:45")

        self._draw_7segment_lcd(painter, cx - lcd_width / 2, upper_y - lcd_height / 2,
                               lcd_width, lcd_height, bg, primary, date_str)

        self._draw_7segment_lcd(painter, cx - lcd_width / 2, lower_y - lcd_height / 2,
                               lcd_width, lcd_height, bg, primary, utc_str)

    SEGMENT_MAP = {
    '0': [1, 1, 1, 1, 1, 1, 0],
    '1': [0, 1, 1, 0, 0, 0, 0],
    '2': [1, 1, 0, 1, 1, 0, 1],
    '3': [1, 1, 1, 1, 0, 0, 1],
    '4': [0, 1, 1, 0, 0, 1, 1],
    '5': [1, 0, 1, 1, 0, 1, 1],
    '6': [1, 0, 1, 1, 1, 1, 1],
    '7': [1, 1, 1, 0, 0, 0, 0],
    '8': [1, 1, 1, 1, 1, 1, 1],
    '9': [1, 1, 1, 1, 0, 1, 1],
    'A': [1, 1, 1, 0, 1, 1, 1],
    'B': [0, 0, 1, 1, 1, 1, 1],
    'C': [1, 0, 0, 1, 1, 1, 0],
    'D': [0, 1, 1, 1, 1, 0, 1],
    'E': [1, 0, 0, 1, 1, 1, 1],
    'F': [1, 0, 0, 0, 1, 1, 1],
    'G': [1, 0, 1, 1, 1, 1, 0],
    'H': [0, 1, 1, 0, 1, 1, 1],
    'I': [0, 0, 1, 0, 0, 1, 0],
    'J': [0, 1, 1, 1, 0, 0, 0],
    'K': [0, 1, 1, 0, 1, 1, 1],
    'L': [0, 0, 0, 1, 1, 1, 0],
    'M': [1, 1, 1, 0, 1, 1, 0],
    'N': [1, 1, 1, 0, 1, 0, 1],
    'O': [1, 1, 1, 1, 1, 1, 0],
    'P': [1, 1, 0, 0, 1, 1, 1],
    'Q': [1, 1, 1, 1, 1, 0, 1],
    'R': [1, 1, 0, 0, 1, 0, 1],
    'S': [1, 0, 1, 1, 0, 1, 1],
    'T': [0, 0, 0, 0, 1, 1, 1],
    'U': [0, 1, 1, 1, 1, 1, 0],
    'V': [0, 1, 1, 1, 1, 1, 0],
    'W': [0, 1, 1, 1, 1, 1, 1],
    'X': [0, 1, 1, 0, 1, 1, 1],
    'Y': [0, 1, 1, 0, 0, 1, 1],
    'Z': [1, 1, 0, 1, 1, 0, 1],
    '/': [0, 0, 0, 0, 0, 0, 1],
    '-': [0, 0, 0, 0, 0, 0, 1],
    ':': [0, 0, 0, 0, 0, 0, 0],
    ' ': [0, 0, 0, 0, 0, 0, 0],
}

    def _draw_7segment_lcd(self, painter, x, y, w, h, bg, primary, value):
        xi, yi, wi, hi = int(x), int(y), int(w), int(h)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(bg))
        painter.drawRoundedRect(xi, yi, wi, hi, 4, 4)

        inner_bg = QColor(bg.red() + 8, bg.green() + 8, bg.blue() + 8)
        painter.setBrush(QBrush(inner_bg))
        painter.drawRoundedRect(xi + 3, yi + 3, wi - 6, hi - 6, 2, 2)

        if value:
            self._draw_7segment_text(painter, xi + 3, yi + 3, wi - 6, hi - 6, primary, value)

    def _draw_7segment_text(self, painter, x, y, w, h, color, text):
        text = text.upper()
        display_len = sum(2 if c == ':' else 1 for c in text)
        if display_len == 0:
            return

        available_w = w - w * 0.1
        char_w = available_w / display_len

        start_x = x + w * 0.05
        pos = 0
        for char in text:
            char_x = start_x + pos * char_w
            if char == ':':
                self._draw_7segment_colon(painter, char_x, y, char_w, h, color)
            else:
                self._draw_7segment_char(painter, char_x, y, char_w, h, color, char)
            pos += 2 if char == ':' else 1

    def _draw_7segment_colon(self, painter, x, y, w, h, color):
        dot_r = w * 0.15
        dot1_y = y + h * 0.35
        dot2_y = y + h * 0.65

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(color))
        painter.drawEllipse(QPointF(x + w * 0.5, dot1_y), dot_r, dot_r)
        painter.drawEllipse(QPointF(x + w * 0.5, dot2_y), dot_r, dot_r)

    def _draw_7segment_char(self, painter, x, y, w, h, color, char):
        segments = self.SEGMENT_MAP.get(char, [0] * 7)

        gap = w * 0.04
        left = x + w * 0.18
        right = x + w * 0.82
        top = y + h * 0.12
        middle = y + h * 0.5
        bottom = y + h * 0.88

        path = QPainterPath()

        if segments[0]:
            path.moveTo(left + gap, top)
            path.lineTo(right - gap, top)
            path.lineTo(right - gap - gap, top + w * 0.08)
            path.lineTo(left + gap + gap, top + w * 0.08)
            path.closeSubpath()

        if segments[5]:
            path.moveTo(left, top + gap)
            path.lineTo(left + w * 0.08, top + gap + gap)
            path.lineTo(left + w * 0.08, middle - gap - gap)
            path.lineTo(left, middle - gap)
            path.lineTo(left, top + gap)

        if segments[6]:
            path.moveTo(left + gap, middle)
            path.lineTo(right - gap, middle)
            path.lineTo(right - gap - gap, middle + w * 0.04)
            path.lineTo(left + gap + gap, middle + w * 0.04)
            path.closeSubpath()

        if segments[4]:
            path.moveTo(left, middle + gap)
            path.lineTo(left + w * 0.08, middle + gap + gap)
            path.lineTo(left + w * 0.08, bottom - gap - gap)
            path.lineTo(left, bottom - gap)
            path.lineTo(left, middle + gap)

        if segments[3]:
            path.moveTo(left + gap, bottom)
            path.lineTo(right - gap, bottom)
            path.lineTo(right - gap - gap, bottom - w * 0.08)
            path.lineTo(left + gap + gap, bottom - w * 0.08)
            path.closeSubpath()

        if segments[2]:
            path.moveTo(right - w * 0.08, middle + gap + gap)
            path.lineTo(right, middle + gap)
            path.lineTo(right, bottom - gap)
            path.lineTo(right - w * 0.08, bottom - gap - gap)
            path.lineTo(right - w * 0.08, middle + gap + gap)

        if segments[1]:
            path.moveTo(right - w * 0.08, top + gap + gap)
            path.lineTo(right, top + gap)
            path.lineTo(right, middle - gap)
            path.lineTo(right - w * 0.08, middle - gap - gap)
            path.lineTo(right - w * 0.08, top + gap + gap)

        painter.fillPath(path, QBrush(color))

    def _draw_analog_hands(self, painter, cx, cy, max_radius, time_data):
        hour = time_data["hour"] % 12
        minute = time_data["minute"]
        second = time_data["second"]

        hour_angle = math.radians((hour + minute / 60) * 30 - 90)
        minute_angle = math.radians(minute * 6 - 90)
        second_angle = math.radians(second * 6 - 90)

        self._draw_3d_hour_hand(painter, cx, cy, hour_angle, max_radius * 0.55)
        self._draw_3d_minute_hand(painter, cx, cy, minute_angle, max_radius * 0.75)
        self._draw_3d_second_hand(painter, cx, cy, second_angle, max_radius * 0.85)

    def _draw_3d_hour_hand(self, painter, cx, cy, angle, length):
        cx_face = cx + math.cos(angle) * length
        cy_face = cy + math.sin(angle) * length

        path = QPainterPath()
        path.moveTo(cx, cy)
        path.lineTo(cx_face + math.cos(angle + math.pi / 2) * 8,
                   cy_face + math.sin(angle + math.pi / 2) * 8)
        path.lineTo(cx_face, cy_face)
        path.lineTo(cx_face + math.cos(angle - math.pi / 2) * 8,
                   cy_face + math.sin(angle - math.pi / 2) * 8)
        path.closeSubpath()

        gradient = QLinearGradient(cx, cy, cx_face, cy_face)
        gradient.setColorAt(0, _c("#666666"))
        gradient.setColorAt(0.5, _c("#cccccc"))
        gradient.setColorAt(1, _c("#888888"))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

        highlight = QLinearGradient(cx + 2, cy, cx_face, cy_face)
        highlight.setColorAt(0, QColor(255, 255, 255, 0))
        highlight.setColorAt(0.5, QColor(255, 255, 255, 80))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(highlight))
        painter.drawPath(path)

    def _draw_3d_minute_hand(self, painter, cx, cy, angle, length):
        cx_face = cx + math.cos(angle) * length
        cy_face = cy + math.sin(angle) * length

        path = QPainterPath()
        path.moveTo(cx, cy)
        path.lineTo(cx_face + math.cos(angle + math.pi / 2) * 6,
                   cy_face + math.sin(angle + math.pi / 2) * 6)
        path.lineTo(cx_face, cy_face)
        path.lineTo(cx_face + math.cos(angle - math.pi / 2) * 6,
                   cy_face + math.sin(angle - math.pi / 2) * 6)
        path.closeSubpath()

        gradient = QLinearGradient(cx, cy, cx_face, cy_face)
        gradient.setColorAt(0, _c("#555555"))
        gradient.setColorAt(0.5, _c("#bbbbbb"))
        gradient.setColorAt(1, _c("#777777"))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

    def _draw_3d_second_hand(self, painter, cx, cy, angle, length):
        x2 = cx + math.cos(angle) * length
        y2 = cy + math.sin(angle) * length
        x3 = cx - math.cos(angle) * 20
        y3 = cy - math.sin(angle) * 20

        painter.setPen(QPen(_c("#cc0000"), 2))
        painter.drawLine(QPointF(cx, cy), QPointF(x2, y2))

        painter.setPen(QPen(_c("#ff3333"), 1))
        painter.drawLine(QPointF(cx, cy), QPointF(x3, y3))

    def _draw_center_cap(self, painter, cx, cy, radius):
        gradient = QRadialGradient(cx - radius * 0.3, cy - radius * 0.3, radius)
        gradient.setColorAt(0, _c("#dddddd"))
        gradient.setColorAt(0.5, _c("#888888"))
        gradient.setColorAt(1, _c("#555555"))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(cx, cy), radius, radius)

        painter.setBrush(QBrush(_c("#333333")))
        painter.drawEllipse(QPointF(cx, cy), radius * 0.3, radius * 0.3)