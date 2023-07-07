import math
from typing import Tuple

from config import Config, InputKey
import utils
import tkinter as tk

from frames.game_play import GamePlay
from logic import terrain
from logic.input import Input


class Tank:
    cannon_angle: int = 0
    cannon_speed: int = 0.1
    tank_speed: int = 1

    pos: Tuple[int, int]

    @property
    def pos_x(self) -> int:
        """ X position of the tank on the map. """
        return self.pos[0]

    @property
    def pos_y(self) -> int:
        """ Y position of the tank on the map. """
        return self.pos[1]

    cannon_offset: Tuple[int, int] = (0, 0)

    @property
    def cannon_x(self) -> int:
        """ X position of the tank's cannon on the map. """
        return self.pos[0] + Config.cannon_offset[0] + self.cannon_offset[0]

    @property
    def cannon_y(self) -> int:
        """ Y position of the tank's cannon on the map. """
        return self.pos[1] + Config.cannon_offset[1] + self.cannon_offset[1]

    cannon_dirty: bool = True
    tank_dirty: bool = True

    def __init__(self, game: GamePlay, x=100, y=100):
        self.game = game
        self.canvas = game.canvas
        self.pos = (x, y)
        self.cannon_offset = (0.5 * Config.cannon_w * math.cos(math.radians(-self.cannon_angle)),
                              0.5 * Config.cannon_w * math.sin(math.radians(-self.cannon_angle)))

        tank_base = utils.load_photo(Config.res_path_tank_base, width=Config.tank_w)
        self.tank_base = self.canvas.create_image(self.pos_x, self.pos_y, image=tank_base)

        tank_cannon = utils.load_photo(Config.res_path_tank_cannon, width=Config.cannon_w)
        self.tank_cannon = self.canvas.create_image(self.cannon_x, self.cannon_y, image=tank_cannon)

    def custom_update(self):
        if self.cannon_dirty:
            self.cannon_dirty = False
            # Delete old cannon, load new cannon and place it on canvas
            self.canvas.delete(self.tank_cannon)
            self.cannon_angle %= 360
            tank_cannon = utils.load_photo(Config.res_path_tank_cannon, width=Config.cannon_w, rotate=self.cannon_angle)
            self.cannon_offset = (0.5 * Config.cannon_w * math.cos(math.radians(-self.cannon_angle)),
                                  0.5 * Config.cannon_w * math.sin(math.radians(-self.cannon_angle)))
            self.tank_cannon = self.canvas.create_image(self.cannon_x, self.cannon_y, image=tank_cannon)
            self.canvas.tag_raise(self.tank_base)

    def aim_plus(self):
        self.cannon_angle += self.cannon_speed
        self.cannon_dirty = True

    def aim_minus(self):
        self.cannon_angle -= self.cannon_speed
        self.cannon_dirty = True

    def move_right(self):
        nx = self.pos_x + self.tank_speed
        ny = terrain.height_at(self.game.map_array, nx)
        self.pos = (nx, ny)
        self.tank_dirty = True
        self.cannon_dirty = True

    def move_left(self):
        nx = self.pos_x - self.tank_speed
        ny = terrain.height_at(self.game.map_array, nx)
        self.pos = (nx, ny)
        self.tank_dirty = True
        self.cannon_dirty = True


class PlayerTank(Tank):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        Input.key_down[InputKey.RIGHT].append(lambda: print("RIGHT"))