import math
import random

import numpy as np
from matplotlib import pyplot as plt

EMPTY_TILE = 8*8*8
FULL_TILE = 0


def constant_map(w, h, x=None) -> np.ndarray:
    if x is None:
        x = h // 2

    field = np.zeros((h, w, 4))
    field[:x, :, 2] = 255
    field[x:h, :, 1] = 255
    field[:, :, 3] = 255

    return field


def random_walk_map(w, h, start_y=None, step_func=None, plot=False) -> np.ndarray:
    if start_y is None:
        start_y = h // 2

    if step_func is None:
        step_func = lambda y, h, x, w: y

    field = np.zeros((h, w, 4))
    field[:, :, 3] = 255

    last_y = start_y
    field[start_y:h, 0, 1] = 255
    for x in range(2, w):
        last_y = h - step_func(h - last_y, h, x, w)
        field[last_y:h, x, 1] = 255

    if plot:
        plt.imshow(field)
        plt.show()

    return field


def wave_sum_map(w, h):
    waves = [(np.zeros((w,) for _ in range(10)))]
    for i in range(10):
        a = random.random() * 2 - 1
        b = random.random() * math.pi
        waves[i] = np.sin(a * waves[i] + b)

    wave_sum = np.sum(waves, axis=0).astype(int)

    field = np.zeros((h, w, 4))
    field[wave_sum:]

def random_step_func(y, h, x, w):
    return random.choice([y - 1, y, y + 1])
