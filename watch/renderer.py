import math
import os
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import (
    QPainter, QColor, QPen, QBrush, QLinearGradient, QRadialGradient,
    QFont, QPainterPath, QFontMetrics, QPixmap, QImage, QFontDatabase
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
        self.bezel_image = None
        self.seg_font = None
        self._load_background()
        self._load_bezel()
        self._load_seven_segment_font()

    def _load_bezel(self):
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bezel_path = os.path.join(project_dir, "assets", "watch_bezel_without_face.png")
        if os.path.exists(bezel_path):
            self.bezel_image = QPixmap(bezel_path)

    def _load_seven_segment_font(self):
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_path = os.path.join(project_dir, "assets", "fonts", "DSEG7Classic-Bold.ttf")
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    self.seg_font = QFont(families[0])

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

        # Draw bezel first (background layer) - scaled to fill widget
        if self.bezel_image and not self.bezel_image.isNull():
            bezel_scaled = self.bezel_image.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            b_w = bezel_scaled.width()
            b_h = bezel_scaled.height()
            b_offset_x = (width - b_w) // 2
            b_offset_y = (height - b_h) // 2
            
            painter.save()
            painter.translate(cx, cy)
            painter.rotate(bezel_angle)
            painter.translate(-cx, -cy)
            painter.drawPixmap(b_offset_x, b_offset_y, bezel_scaled)
            painter.restore()

        # Draw watch face on top of bezel - scaled to fit inside bezel
        if self.background_image and not self.background_image.isNull():
            # Scale watch face to fit within the bezel's inner area
            watch_scaled = self.background_image.scaled(int(width * 0.75), int(height * 0.75), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            w_w = watch_scaled.width()
            w_h = watch_scaled.height()
            w_offset_x = (width - w_w) // 2
            w_offset_y = (height - w_h) // 2
            painter.drawPixmap(w_offset_x, w_offset_y, watch_scaled)
            bg_config = self.settings.config.get("background", {})
            cx = (width // 2) + bg_config.get("center_x", 0)
            cy = (height // 2) + bg_config.get("center_y", 0)
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

        date_str = time_data.get("date", "16:05")
        utc_str = time_data.get("utc", "14:32:45")
        utc_label = time_data.get("utc_label", "utc")

        # Use different positions based on whether background image is used
        if self.background_image and not self.background_image.isNull():
            # Scale factor: watch face (613) / bezel (817) = 0.75
            scale = 0.75
            
            # Exact positions from watch_face.png (292x292)
            # Upper LCD: y=52-87, center offset -0.524, height 0.247
            # Make 20% smaller
            upper_y = cy - radius * 0.524 * scale
            upper_lcd_height = radius * 0.247 * 0.80 * scale
            upper_lcd_width = radius * 1.15 * 0.80 * scale
            
            # Lower LCD: box x=75, y=195, w=143, h=40
            # Make 10% smaller, move left 10px, down 20px (scaled)
            lower_y = cy + radius * 0.473 * scale + 20 * scale
            lower_lcd_height = radius * 0.274 * 0.90 * scale
            lower_lcd_width = radius * 0.98 * 0.90 * scale
            
            self._draw_7segment_lcd(painter, cx - upper_lcd_width / 2, upper_y - upper_lcd_height / 2 - 2,
                                   upper_lcd_width, upper_lcd_height, bg, primary, date_str, -3)

            self._draw_7segment_lcd(painter, cx - lower_lcd_width / 2 - 10 + 14, lower_y - lower_lcd_height / 2,
                                   lower_lcd_width, lower_lcd_height, bg, primary, utc_str)
            
            # Draw timezone label in lower-left corner if UTC
            if utc_label == "utc":
                self._draw_timezone_label(painter, cx - lower_lcd_width / 2 - 10 + 14 - 20 - 5, lower_y - lower_lcd_height / 2 - 15 - 2,
                                         lower_lcd_width, lower_lcd_height, primary)
        else:
            # Default positions for generated watch face
            upper_y = cy - radius * 0.20
            lower_y = cy + radius * 0.25
            lcd_width = radius * 1.3 * 0.67
            lcd_height = radius * 0.25
            
            self._draw_7segment_lcd(painter, cx - lcd_width / 2, upper_y - lcd_height / 2,
                                   lcd_width, lcd_height, bg, primary, date_str)

            self._draw_7segment_lcd(painter, cx - lcd_width / 2, lower_y - lcd_height / 2,
                                   lcd_width, lcd_height, bg, primary, utc_str)
            
            if utc_label == "utc":
                self._draw_timezone_label(painter, cx - lcd_width / 2 - 20 - 5, lower_y - lcd_height / 2 - 15 - 2,
                                         lcd_width, lcd_height, primary)

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

    def _draw_7segment_lcd(self, painter, x, y, w, h, bg, primary, value, y_offset=0):
        xi, yi, wi, hi = int(x), int(y), int(w), int(h)
        # No black background - LCD areas are already black in the image

        if value:
            self._draw_7segment_text(painter, xi, yi + y_offset, wi, hi, primary, value)

    def _draw_timezone_label(self, painter, x, y, w, h, primary):
        font = QFont("Arial", int(h * 0.2))
        painter.setFont(font)
        painter.setPen(QPen(primary, 1))
        painter.drawText(QPointF(x + 2, y + h * 0.25), "UTC")

    def _draw_7segment_text(self, painter, x, y, w, h, color, text):
        if not self.seg_font:
            return
            
        text = text.upper()
        
        # Create font with size to fill the LCD area
        font = QFont(self.seg_font)
        font.setPixelSize(int(h * 0.95))
        
        painter.setFont(font)
        painter.setPen(QPen(color, 1))
        
        # Calculate text position to center it
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(text)
        text_x = x + (w - text_width) / 2
        text_y = y + h * 0.85  # Baseline position
        
        painter.drawText(QPointF(text_x, text_y), text)

    def _draw_7segment_colon(self, painter, x, y, w, h, color):
        # Two circular dots like in the 6x7seg.png image
        dot_r = h * 0.07
        dot1_y = y + h * 0.32
        dot2_y = y + h * 0.62

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(color))
        painter.drawEllipse(QPointF(x + w * 0.5, dot1_y), dot_r, dot_r)
        painter.drawEllipse(QPointF(x + w * 0.5, dot2_y), dot_r, dot_r)

    def _draw_7segment_char(self, painter, x, y, w, h, color, char):
        segments = self.SEGMENT_MAP.get(char, [0] * 7)

        # Segment geometry matching 6x7seg.png style exactly
        # Thick segments with angled/diamond ends
        seg_thickness = w * 0.15  # Segment width/thickness
        gap = seg_thickness * 0.35  # Gap between segments
        
        # Character boundaries
        char_left = x + w * 0.05
        char_right = x + w * 0.95
        char_top = y
        char_middle = y + h * 0.5
        char_bottom = y + h
        
        # Horizontal segment positions
        h_seg_y_top = char_top
        h_seg_y_mid = char_middle - seg_thickness / 2
        h_seg_y_bot = char_bottom - seg_thickness
        
        # Vertical segment positions
        v_seg_x_left = char_left
        v_seg_x_right = char_right - seg_thickness
        
        # Vertical segment heights
        v_seg_top_start = char_top + seg_thickness + gap
        v_seg_top_end = char_middle - gap - seg_thickness / 2
        v_seg_bot_start = char_middle + gap + seg_thickness / 2
        v_seg_bot_end = char_bottom - seg_thickness - gap
        
        path = QPainterPath()
        
        # Helper to draw horizontal segment with angled ends
        def add_h_segment(left_x, right_x, top_y, thickness):
            path.moveTo(left_x + gap, top_y)
            path.lineTo(right_x - gap, top_y)
            path.lineTo(right_x - gap - gap, top_y + thickness)
            path.lineTo(left_x + gap + gap, top_y + thickness)
            path.closeSubpath()
        
        # Helper to draw vertical segment with angled ends
        def add_v_segment(x_pos, top_y, bottom_y, thickness, is_left=True):
            if is_left:
                path.moveTo(x_pos, top_y + gap)
                path.lineTo(x_pos + thickness, top_y + gap + gap)
                path.lineTo(x_pos + thickness, bottom_y - gap - gap)
                path.lineTo(x_pos, bottom_y - gap)
                path.closeSubpath()
            else:
                path.moveTo(x_pos, top_y + gap + gap)
                path.lineTo(x_pos + thickness, top_y + gap)
                path.lineTo(x_pos + thickness, bottom_y - gap)
                path.lineTo(x_pos, bottom_y - gap - gap)
                path.closeSubpath()

        # Segment A (top horizontal)
        if segments[0]:
            add_h_segment(char_left, char_right, h_seg_y_top, seg_thickness)
        
        # Segment F (top-left vertical)
        if segments[5]:
            add_v_segment(v_seg_x_left, v_seg_top_start, v_seg_top_end, seg_thickness, True)
        
        # Segment B (top-right vertical)
        if segments[1]:
            add_v_segment(v_seg_x_right, v_seg_top_start, v_seg_top_end, seg_thickness, False)
        
        # Segment G (middle horizontal)
        if segments[6]:
            add_h_segment(char_left, char_right, h_seg_y_mid, seg_thickness)
        
        # Segment E (bottom-left vertical)
        if segments[4]:
            add_v_segment(v_seg_x_left, v_seg_bot_start, v_seg_bot_end, seg_thickness, True)
        
        # Segment C (bottom-right vertical)
        if segments[2]:
            add_v_segment(v_seg_x_right, v_seg_bot_start, v_seg_bot_end, seg_thickness, False)
        
        # Segment D (bottom horizontal)
        if segments[3]:
            add_h_segment(char_left, char_right, h_seg_y_bot, seg_thickness)

        painter.fillPath(path, QBrush(color))

    def _draw_analog_hands(self, painter, cx, cy, max_radius, time_data):
        hour = time_data["hour"] % 12
        minute = time_data["minute"]
        second = time_data["second"]
        millisecond = time_data.get("millisecond", 0)

        # Smooth movement with millisecond precision
        hour_angle = math.radians((hour + minute / 60 + second / 3600 + millisecond / 3600000) * 30 - 90)
        minute_angle = math.radians((minute + second / 60 + millisecond / 60000) * 6 - 90)
        second_angle = math.radians((second + millisecond / 1000) * 6 - 90)

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