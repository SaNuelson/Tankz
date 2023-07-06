import numpy as np


def constant(w, h, x=None) -> np.ndarray:
    if x is None:
        x = h // 2

    field = np.zeros((h, w, 4))
    field[:x, :, 2] = 255
    field[x:h, :, 1] = 255
    field[:, :, 3] = 255

    return field
