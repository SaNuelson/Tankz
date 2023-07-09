from __future__ import annotations

import math
from typing import Tuple

from config import Config, InputKey
import utils
import tkinter as tk

from logic import terrain
from logic.input import Input

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from frames.game_play import GamePlay


class Tank:

    tank_dirty: bool = True
    """Flag whether tank base needs re-rendering"""
    tank_base_id: int = None
    """Canvas ID of tank base _sprite."""
    tank_speed: int = 2
    """Speed of tank (in pixels per movement button press)"""
    prev_pos: Tuple[int, int]
    """Previous _position (used to compute delta)"""
    pos: Tuple[int, int]
    """Current _position on _canvas of tank (0,0) being the top left corner"""

    @property
    def pos_x(self) -> int:
        """ X _position of the tank on the map. """
        return self.pos[0]

    @property
    def pos_y(self) -> int:
        """ Y _position of the tank on the map. """
        return self.pos[1]

    cannon_dirty: bool = True
    """Flag specifying whether cannon needs to be re-rendered"""
    tank_cannon_id: int = None
    """Canvas ID of tank cannon _sprite."""
    cannon_offset: Tuple[int, int] = (0, 0)
    """Vector to offset cannon _sprite from base (i.e., vector from center of tank base to center of cannon)."""
    cannon_angle: int = 0
    """Angle of the cannon in degrees, 0 being horizontally to the right."""
    cannon_speed: int = 1
    """Speed at which cannon turns (in degrees per button press)."""

    @property
    def cannon_x(self) -> int:
        """ X _position of the tank's cannon on the map. """
        return self.pos[0] + Config.cannon_offset[0] + self.cannon_offset[0]

    @property
    def cannon_y(self) -> int:
        """ Y _position of the tank's cannon on the map. """
        return self.pos[1] + Config.cannon_offset[1] + self.cannon_offset[1]

    def __init__(self, game: GamePlay, x=100, y=100):
        self.game = game
        self.canvas = game.canvas
        self.prev_pos = (x, y)
        self.pos = (x, y)
        self.cannon_offset = (0.5 * Config.cannon_w * math.cos(math.radians(-self.cannon_angle)),
                              0.5 * Config.cannon_w * math.sin(math.radians(-self.cannon_angle)))

        tank_base = utils.load_photo(Config.res_path_tank_base, width=Config.tank_w)
        self.tank_base_id = self.canvas.create_image(self.pos_x, self.pos_y, image=tank_base)
        assert self.canvas.find_withtag(self.tank_base_id)

        tank_cannon = utils.load_photo(Config.res_path_tank_cannon, width=Config.cannon_w)
        self.tank_cannon_id = self.canvas.create_image(self.cannon_x, self.cannon_y, image=tank_cannon)
        assert self.canvas.find_withtag(self.tank_cannon_id)

    def custom_update(self):
        if self.cannon_dirty:
            self.cannon_dirty = False
            self.place_cannon()
        if self.tank_dirty:
            self.tank_dirty = False
            self.place_base()

    def place_cannon(self):
        # Delete old cannon, load new cannon and place it on _canvas
        assert self.canvas.find_withtag(self.tank_cannon_id) != ()
        self.canvas.delete(self.tank_cannon_id)
        self.cannon_angle %= 360
        tank_cannon = utils.load_photo(Config.res_path_tank_cannon, width=Config.cannon_w, rotate=self.cannon_angle)
        self.cannon_offset = (0.5 * Config.cannon_w * math.cos(math.radians(-self.cannon_angle)),
                              0.5 * Config.cannon_w * math.sin(math.radians(-self.cannon_angle)))
        self.tank_cannon_id = self.canvas.create_image(self.cannon_x, self.cannon_y, image=tank_cannon)
        self.canvas.tag_raise(self.tank_base_id)

    def place_base(self):
        assert self.canvas.find_withtag(self.tank_base_id) != ()
        self.canvas.move(self.tank_base_id, self.pos_x - self.prev_pos[0], self.pos_y - self.prev_pos[1])

    def aim_plus(self):
        self.cannon_angle += self.cannon_speed
        self.cannon_dirty = True

    def aim_minus(self):
        self.cannon_angle -= self.cannon_speed
        self.cannon_dirty = True

    def move_right(self):
        nx = self.pos_x + self.tank_speed
        ny = terrain.height_at(self.game.map_array, nx)
        self.prev_pos = self.pos
        self.pos = (nx, ny)
        self.tank_dirty = True
        self.cannon_dirty = True

    def move_left(self):
        nx = self.pos_x - self.tank_speed
        ny = terrain.height_at(self.game.map_array, nx)
        self.prev_pos = self.pos
        self.pos = (nx, ny)
        self.tank_dirty = True
        self.cannon_dirty = True
