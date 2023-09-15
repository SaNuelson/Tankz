import tkinter as tk
from typing import List

from toolkit.vector import Vector2


def draw_x(canvas: tk.Canvas, point: Vector2, size: int, color: str, **kwargs) -> List[int]:
    point = point.as_int()
    top = point.y - size
    bot = point.y + size
    left = point.x - size
    right = point.x + size
    return [
        canvas.create_line(left, top, right, bot, fill=color, **kwargs),
        canvas.create_line(left, bot, right, top, fill=color, **kwargs)
    ]


def draw_box(canvas: tk.Canvas, point: Vector2, size: Vector2, color: str, **kwargs) -> List[int]:
    point = point.as_int()
    size = size.as_int()
    top = point.y
    bot = point.y + size.y
    left = point.x
    right = point.x + size.x
    return [
        canvas.create_line(left, top, right, top, fill=color, **kwargs),
        canvas.create_line(right, top, right, bot, fill=color, **kwargs),
        canvas.create_line(right, bot, left, bot, fill=color, **kwargs),
        canvas.create_line(left, bot, left, top, fill=color, **kwargs),
    ]


def draw_grid(canvas: tk.Canvas, size: Vector2, spacing: Vector2, color: str, **kwargs) -> List[int]:
    size = size.as_int()
    spacing = spacing.as_int()
    return [
        *[canvas.create_line(0, spacing.y * y, size.x, spacing.y * y)
          for y in range(size.y // spacing.y)],
        *[canvas.create_line(spacing.x * x, 0, spacing.x * x, size.y)
          for x in range(size.x // spacing.x)]
    ]
