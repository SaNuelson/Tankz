import tkinter as tk
from tkinter import ttk

from logic.player import Player


class PlayerInfo(tk.Frame):
    def __init__(self, master: tk.Misc, player: Player):
        super().__init__(master)
        self.player = player

        self.info = tk.Label(self, text="PLAYER")
        self.info.pack()

        self.health = ttk.Progressbar(self, variable=player.health, maximum=100)
        self.health.pack()
