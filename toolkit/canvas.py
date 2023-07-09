import tkinter as tk
from typing import List

from logic.vector import Vector2


def draw_x(canvas: tk.Canvas, point: Vector2, size: int, color: str) -> List[int]:
    return [
        canvas.create_line(int(point.x - size),
                           int(point.y - size),
                           int(point.x + size),
                           int(point.y + size),
                           fill=color),
        canvas.create_line(int(point.x - size),
                           int(point.y + size),
                           int(point.x + size),
                           int(point.y - size),
                           fill=color),
    ]