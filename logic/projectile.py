from config import Config


class Projectile:
    def __init__(self, x, y, fx, fy):
        self.pos = (x, y)
        self.force = (fx, fy)

    def custom_update(self, delta: float):
        x, y = self.pos
        fx, fy = self.force
        gx, gy = Config.phys_gravity
        nx = x + (fx + gx) * delta
        ny = y + (fy + gy) * delta
        self.pos = nx, ny
