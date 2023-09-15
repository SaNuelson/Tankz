import random
import tkinter as tk

import numpy as np

import utils
from config import Config
from game_components.collider import PixelCollider
from logic import terrain
from logic.player import Human
from logic.tank import Tank
from tkinter_components.PlayerInfo import PlayerInfo
from toolkit.vector import Vector2
from utils import as_photo


class GamePlay(tk.Frame):
    def __init__(self, master, player_count=2):
        super().__init__(master, )

        self.menu = tk.Frame(self)
        self.menu.pack()

        self.canvas = tk.Canvas(self, width=Config.screen_w, height=Config.screen_h)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=utils.load_photo(Config.res_path_skytex, width=Config.screen_w),
                                 anchor="nw")

        self.map_array = terrain.random_walk(Config.screen_w, Config.screen_h,
                                             step_func=lambda y, h, x, w: y + random.randint(-1, 1))
        self.map_photo = as_photo(self.map_array)
        self.map_photo_id = self.canvas.create_image(0, 0, image=self.map_photo, anchor="nw")
        self.map_mask = np.sign(self.map_array[:, :, 3]).astype(np.bool)
        self.map_collider = PixelCollider(self, self.map_mask)

        player_dist = Config.screen_w // (player_count + 1)
        self.tanks = [Tank(self) for _ in range(player_count)]
        self.players = [Human(self, tank) for tank in self.tanks]
        self.player_infos = [PlayerInfo(self.menu, player) for player in self.players]
        for i in range(player_count):
            x = player_dist * (i + 1)
            y = terrain.height_at(self.map_array, x)
            self.tanks[i].pos = Vector2(x, y)
        for info in self.player_infos:
            info.pack(side=tk.LEFT)
        self.active_player = 0

    def custom_update(self, delta: float):
        self.map_collider.custom_update(delta)

        for player in self.players:
            player.custom_update(delta)

        self.players[self.active_player].start_turn()
