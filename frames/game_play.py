import tkinter as tk

import numpy as np
from PIL.Image import Image
from matplotlib import pyplot as plt

from logic import terrain
from logic.tank import Tank, PlayerTank
from utils import as_photo, as_image


class GamePlay(tk.Frame):
    def __init__(self, master, width, height):
        super().__init__(master)

        self.canvas = tk.Canvas(width=width, height=height)
        self.canvas.pack()

        map_array = terrain.constant(width, height)
        map_photo = as_photo(map_array)
        map_image = as_image(np.random.uniform(0, 255, (300, 300, 4)))
        plt.imshow(map_image)
        plt.show()
        map_photo = as_photo(np.random.uniform(0, 255, (300, 300, 4)))
        self.map = self.canvas.create_image(100, 100, image=map_photo)
        return
        self.tank = Tank(self.canvas)
        self.tank2 = PlayerTank(self.canvas)

    def custom_update(self):
        return
        self.tank.custom_update()
        self.tank2.custom_update()