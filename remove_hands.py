from PyQt5.QtGui import QImage, QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QPointF
import math
import os

# Load image
img = QImage('assets/watch_face.png')
w, h = img.width(), img.height()
cx, cy = w // 2, h // 2

print(f'Image size: {w}x{h}')

# Sample dial background color
samples = []
for y in range(120, 170):
    for x in range(20, 70):
        color = img.pixel(x, y)
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        if 40 < r < 70 and 40 < g < 70 and 40 < b < 70:
            samples.append((r, g, b))

if samples:
    avg_r = int(sum(s[0] for s in samples) / len(samples))
    avg_g = int(sum(s[1] for s in samples) / len(samples))
    avg_b = int(sum(s[2] for s in samples) / len(samples))
else:
    avg_r, avg_g, avg_b = 55, 55, 55

print(f'Background color: RGB({avg_r},{avg_g},{avg_b})')
bg_color = QColor(avg_r, avg_g, avg_b)

# Create painter
painter = QPainter(img)
painter.setRenderHint(QPainter.Antialiasing)
painter.setPen(Qt.NoPen)
painter.setBrush(QBrush(bg_color))

# Cover hands with thin rotated rectangles
# Hour hand: ~10:30 position (315 degrees from 12 o'clock clockwise)
painter.save()
painter.translate(cx, cy)
painter.rotate(315)  # Rotate to match hour hand direction
painter.drawRect(-5, -70, 10, 70)  # Thin rectangle covering hour hand
painter.restore()

# Minute hand: ~2:10 position (65 degrees from 12 o'clock clockwise)
painter.save()
painter.translate(cx, cy)
painter.rotate(65)  # Rotate to match minute hand direction
painter.drawRect(-4, -80, 8, 80)  # Thin rectangle covering minute hand
painter.restore()

# Cover center cap
painter.drawEllipse(QPointF(cx, cy), 10, 10)

painter.end()
print('Hands removed')

# Save
output_path = 'assets/watch_face_clean.png'
try:
    success = img.save(output_path)
    print(f'Save success: {success}')
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f'File size: {size} bytes')
except Exception as e:
    print(f'Error saving: {e}')
