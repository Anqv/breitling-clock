from PyQt5.QtWidgets import QMainWindow, QFrame
from PyQt5.QtCore import Qt, Qt
from PyQt5.QtGui import QCursor
from .watch_face import WatchFace
from .settings import settings


class WatchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._drag_position = None

        display_config = settings.get_display_config()
        self.watch_width = display_config.get("watch_width", 512)
        self.watch_height = display_config.get("watch_height", 768)
        self.offset_x = display_config.get("offset_x", 0)
        self.offset_y = display_config.get("offset_y", 0)

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_AcceptTouchEvents)

        self.watch_face = WatchFace()
        self.setCentralWidget(self.watch_face)

        self.setGeometry(
            self.offset_x,
            self.offset_y,
            self.watch_width,
            self.watch_height
        )

        self.setCursor(QCursor(Qt.OpenHandCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.setCursor(QCursor(Qt.ClosedHandCursor))
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event.globalPos())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_position:
            self.move(event.globalPos() - self._drag_position)

    def mouseReleaseEvent(self, event):
        self._drag_position = None
        self.setCursor(QCursor(Qt.OpenHandCursor))

    def show_context_menu(self, pos):
        from PyQt5.QtWidgets import QMenu
        menu = QMenu(self)

        colors = settings.config["theme"]["available_colors"]
        current = settings.config["theme"]["lcd_color"]

        color_menu = menu.addMenu("LCD Color")
        for color in colors:
            action = color_menu.addAction(color.replace("_", " ").title())
            action.setCheckable(True)
            action.setChecked(color == current)
            action.triggered.connect(lambda checked, c=color: self._change_color(c))

        menu.addSeparator()
        menu.addAction("Close").triggered.connect(self.close)

        menu.exec_(pos)

    def _change_color(self, color):
        settings.set_lcd_color(color)
        self.watch_face.update()