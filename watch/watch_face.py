from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QPainter, QColor
from .renderer import WatchRenderer
from .bezel import BezelController
from .settings import settings


class WatchFace(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.setMouseTracking(True)

        self.renderer = WatchRenderer(settings)
        self.bezel = BezelController(settings)
        self.weather = None

        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(200)
        self.update_time()

    def update_time(self):
        self.current_time = QDateTime.currentDateTime()
        self.local_time = {
            "hour": self.current_time.time().hour(),
            "minute": self.current_time.time().minute(),
            "second": self.current_time.time().second(),
            "millisecond": self.current_time.time().msec()
        }
        
        # Calculate time based on timezone offset
        tz_offset = settings.get_timezone_offset()
        if tz_offset == 0:
            # UTC time
            base_time = self.current_time.toUTC()
            self.display_time = {
                "hour": base_time.time().hour(),
                "minute": base_time.time().minute(),
                "second": base_time.time().second(),
                "label": "utc"
            }
        else:
            # Offset from UTC
            base_time = self.current_time.toUTC()
            offset_time = base_time.addSecs(tz_offset * 3600)
            self.display_time = {
                "hour": offset_time.time().hour(),
                "minute": offset_time.time().minute(),
                "second": offset_time.time().second(),
                "label": f"{tz_offset:+d}"
            }
        
        self.date = self.current_time.date()
        # Force English day names
        day_names = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        self.day_name = day_names[self.date.dayOfWeek() - 1]
        self.update()

    def paintEvent(self, event):
        w = self.width()
        h = self.height()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        painter.fillRect(0, 0, w, h, QColor(0, 0, 0, 0))

        time_display = self.local_time.copy()
        time_display["date"] = f"{self.date.day():02d}:{self.date.month():02d} {self.day_name}"
        time_display["utc"] = f"{self.display_time['hour']:02d}:{self.display_time['minute']:02d}:{self.display_time['second']:02d}"
        time_display["utc_label"] = self.display_time["label"]

        self.renderer.lcd_colors = settings.get_lcd_colors()
        self.renderer.render(painter, w, h, time_display, self.bezel.get_angle())

    def mousePressEvent(self, event):
        cx, cy = self.width() / 2, self.height() / 2
        radius = min(self.width(), self.height()) * 0.45

        if self.bezel.is_on_bezel(event.x(), event.y(), cx, cy, radius):
            self.bezel.start_drag(event.x(), event.y(), cx, cy)
        else:
            self._drag_start = event.pos()
            self._dragging = True

    def mouseMoveEvent(self, event):
        if self.bezel.is_dragging:
            self.bezel.update_drag(event.x(), event.y())
            self.update()
        elif hasattr(self, '_dragging') and self._dragging:
            pass

    def mouseReleaseEvent(self, event):
        if self.bezel.is_dragging:
            self.bezel.end_drag()
            self.update()
        self._dragging = False

    def touchEvent(self, event):
        if event.type() == event.TouchBegin:
            touch = event.touches()[0]
            self.mousePressEvent(touch)
            return True
        elif event.type() == event.TouchUpdate:
            touch = event.touches()[0]
            self.mouseMoveEvent(touch)
            return True
        elif event.type() == event.TouchEnd:
            self.mouseReleaseEvent(event.touches()[0] if event.touches() else None)
            return True
        return super().touchEvent(event)