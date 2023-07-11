from __future__ import annotations

from typing import List, TYPE_CHECKING

from config import Config
from logic import terrain
from logic.projectile import Projectile
from logic.renderer import SpriteRenderer
from logic.vector import Vector2, PartialVector2

if TYPE_CHECKING:
    from frames.game_play import GamePlay


class Tank:
    tank_speed: int = 2
    """Speed of tank (in pixels per movement button press)"""
    cannon_speed: int = 1
    """Speed at which cannon turns (in degrees per button press)."""
    projectile_speed: int = 100

    # region _pos: Vector2 { get; set }
    _pos: Vector2
    """Position within the canvas"""

    @property
    def pos(self) -> Vector2:
        return self._pos

    @pos.setter
    def pos(self, value: Vector2):
        if self._pos == value:
            return
        self._pos = value
        self.tank_base.position = self._pos
        self.tank_cannon.position = self._pos + Vector2(Config.cannon_offset[0], Config.cannon_offset[1])

    # endregion

    # region cannon_angle: float { get; set }
    _cannon_angle: float = 0

    @property
    def cannon_angle(self) -> float:
        """Angle of the cannon in degrees, 0 being horizontally to the right."""
        return self._cannon_angle

    @cannon_angle.setter
    def cannon_angle(self, value):
        if self._cannon_angle == value:
            return
        self._cannon_angle = value
        self.tank_cannon.rotation = value

    # endregion

    tank_base: SpriteRenderer
    tank_cannon: SpriteRenderer
    projectiles: List[Projectile]

    def __init__(self, game: GamePlay, x=100, y=100):
        self.projectiles = []
        self.game = game
        self.canvas = game.canvas
        self._pos = Vector2(x, y)

        self.tank_base = SpriteRenderer(self.canvas,
                                        Config.res_path_tank_base,
                                        position=self._pos,
                                        size=PartialVector2(Config.tank_w, None))

        self.tank_cannon = SpriteRenderer(self.canvas,
                                          Config.res_path_tank_cannon,
                                          position=self._pos + Vector2(Config.cannon_offset[0], Config.cannon_offset[1]),
                                          size=PartialVector2(Config.cannon_w, None),
                                          anchor=Vector2(0, 0.5))

    def custom_update(self, delta: float):
        self.tank_base.custom_update(delta)
        self.tank_cannon.custom_update(delta)
        for proj in self.projectiles:
            proj.custom_update(delta)

    def aim_plus(self):
        self.cannon_angle += self.cannon_speed

    def aim_minus(self):
        self.cannon_angle -= self.cannon_speed

    def move_right(self):
        nx = self.pos.x + self.tank_speed
        ny = terrain.height_at(self.game.map_array, int(nx))
        self.pos = Vector2(nx, ny)

    def move_left(self):
        nx = self.pos.x - self.tank_speed
        ny = terrain.height_at(self.game.map_array, int(nx))
        self.pos = Vector2(nx, ny)

    def fire(self):
        force = Vector2(self.projectile_speed, 0).rotated(-self.cannon_angle)
        self.projectiles.append(Projectile(self.game, self.pos, force))
