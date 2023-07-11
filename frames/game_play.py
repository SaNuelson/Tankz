import random
import tkinter as tk

import utils
from config import Config
from logic import terrain
from logic.player import Human
from logic.tank import Tank
from utils import as_photo


class GamePlay(tk.Frame):
    def __init__(self, master, player_count=2):
        super().__init__(master)

        self.canvas = tk.Canvas(self, width=Config.screen_w, height=Config.screen_h)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=utils.load_photo(Config.res_path_skytex, width=Config.screen_w), anchor="nw")

        self.map_array = terrain.random_walk(Config.screen_w, Config.screen_h, step_func=lambda y, h, x, w: y + random.randint(-1, 1))
        self.map_photo = as_photo(self.map_array)
        self.map_photo_id = self.canvas.create_image(0, 0, image=self.map_photo, anchor="nw")

        player_dist = Config.screen_w // (player_count + 1)
        self.players = []
        for i in range(player_count):
            x = player_dist * (i + 1)
            y = terrain.height_at(self.map_array, x)
            tank = Tank(self, x, y)
            player = Human(self, tank)
            self.players.append(player)
        self.active_player = 0

    def custom_update(self, delta: float):
        for player in self.players:
            player.custom_update(delta)

        self.players[self.active_player].start_turn()