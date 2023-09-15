import tkinter as tk
from typing import List

from config import Config
from tkinter_components.ImageButton import ImageButton


class RangeSelector(tk.Frame):
    def __init__(self, master: tk.Misc, values: List, initial_value: any = None, width: int | None = None):
        super().__init__(master, width=200)

        self.value = tk.Variable(self, initial_value)
        self.possible_values = values
        self.value_index = -1 if initial_value is None else values.index(initial_value)
        self.initial_value = initial_value

        self.width = width
        label_width = None
        if self.width is not None:
            label_width = max(0, self.width - 2 * Config.arrow_w)
            print("W", label_width)

        self.grid_columnconfigure(1, weight=1)

        self.btn_player_minus = ImageButton.PackArrowRedLeft(self, "-", self.on_minus_press)
        self.btn_player_minus.grid(row=0, column=0, sticky="nswe")
        self.player_count_label = tk.Label(self, textvariable=self.value)
        self.player_count_label.grid(row=0, column=1, sticky="nswe")
        self.btn_player_minus = ImageButton.PackArrowGreenRight(self, "+", self.on_plus_press)
        self.btn_player_minus.grid(row=0, column=2, sticky="nswe")

        self.grid_columnconfigure(1, minsize=label_width)

    def on_minus_press(self):
        if self.value_index <= 0:
            return
        self.value.set(self.possible_values[self.value_index - 1])
        self.value_index -= 1

    def on_plus_press(self):
        if self.value_index >= len(self.possible_values):
            return
        self.value.set(self.possible_values[self.value_index + 1])
        self.value_index += 1
