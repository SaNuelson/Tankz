import numpy as np

from config import Config


def constant(w, h, x=None) -> np.ndarray:
    if x is None:
        x = h // 2

    field = np.zeros((h, w))
    field[x:h, :] = 255

    return field


def random_walk(w, h, start_y=None, step_func=None) -> np.ndarray:
    if start_y is None:
        start_y = h // 2

    if step_func is None:
        step_func = lambda y, h, x, w: y

    field = np.zeros((h, w, 4))

    last_y = start_y
    field[start_y:start_y+10, 0] = Config.rgba_earth_top
    field[start_y+10:h, 0] = Config.rgba_earth_bot
    for x in range(2, w):
        last_y = h - step_func(h - last_y, h, x, w)
        field[last_y:last_y+10, x] = Config.rgba_earth_top
        field[last_y+10:h, x] = Config.rgba_earth_bot

    return field


def height_at(map: np.ndarray, x: int) -> int:
    slice = map[:, x, 3]
    return np.argmax(slice > 0)
