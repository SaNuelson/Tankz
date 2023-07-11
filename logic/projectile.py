from __future__ import annotations

from typing import TYPE_CHECKING

from config import Config
from logic.collider import CircleCollider
from logic.renderer import SpriteRenderer
from logic.vector import Vector2, PartialVector2

if TYPE_CHECKING:
    from frames.game_play import GamePlay


class Projectile:
    # region position: Vector2 { get; set }
    _pos: Vector2

    @property
    def pos(self) -> Vector2:
        return self._pos

    @pos.setter
    def pos(self, value: Vector2):
        if self._pos == value:
            return
        self._pos = value
        self.projectile.position = self._pos
        self.collider.position = self._pos

    # endregion

    def __init__(self, game: GamePlay, pos: Vector2, force: Vector2):
        self._pos = pos
        self.force = force
        self.projectile = SpriteRenderer(game.canvas,
                                         Config.res_path_ball,
                                         position=self._pos,
                                         size=PartialVector2(Config.ball_w, None))
        self.collider = CircleCollider(game,
                                       position=self._pos,
                                       radius=Config.ball_w / 2,
                                       is_trigger=True)

    def custom_update(self, delta: float):
        gravity = Config.phys_gravity * Config.pixels_per_meter * delta
        self.force += gravity
        # print("gravity", gravity)

        drag = Config.cannonball_k * self.force.sqr_magnitude * self.projectile.size.area * delta
        drag = -self.force.normalized * drag
        self.force += drag
        # print("drag", drag)

        self.pos += self.force * delta
        self.projectile.custom_update(delta)
