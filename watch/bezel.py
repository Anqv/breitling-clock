import math


class BezelController:
    def __init__(self, settings):
        self.settings = settings
        self.angle = settings.get_bezel_rotation()
        self.is_dragging = False
        self.last_mouse_angle = 0
        self.center_x = 0
        self.center_y = 0

    def start_drag(self, x, y, cx, cy):
        self.is_dragging = True
        self.center_x = cx
        self.center_y = cy
        self.last_mouse_angle = math.atan2(y - cy, x - cx)
        return True

    def update_drag(self, x, y):
        if not self.is_dragging:
            return

        current_angle = math.atan2(y - self.center_y, x - self.center_x)
        delta = math.degrees(current_angle - self.last_mouse_angle)
        self.angle = (self.angle + delta) % 360
        self.last_mouse_angle = current_angle

    def end_drag(self):
        if self.is_dragging:
            self.is_dragging = False
            self.settings.set_bezel_rotation(self.angle)

    def is_on_bezel(self, x, y, cx, cy, radius):
        distance = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        inner_r = radius * 0.75
        outer_r = radius * 1.1
        return inner_r <= distance <= outer_r

    def get_angle(self):
        return self.angle