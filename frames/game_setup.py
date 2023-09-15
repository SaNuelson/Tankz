import tkinter as tk

from tkinter_components.RangeSelector import RangeSelector


class GameSetup(tk.Frame):
    player_count: tk.IntVar

    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.player_count_selector = RangeSelector(self, list(range(2, 9)), 2)
        self.player_count_selector.grid(column=0, row=0, sticky="nswe")

        self.ai_difficulty_selector = RangeSelector(self, ["Easy", "Medium", "Hard"], "Easy", width=120)
        self.ai_difficulty_selector.grid(column=1, row=0, sticky="nswe")