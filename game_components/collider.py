from __future__ import annotations

from typing import TYPE_CHECKING

import utils
from config import Config
from game_components.renderer import SpriteRenderer
from toolkit.vector import Vector2, PartialVector2

if TYPE_CHECKING:
    from frames.game_play import GamePlay

_active_colliders = []


class Collider:

    def __init__(self, game: GamePlay, position: Vector2, is_trigger: bool = False):
        self.game = game
        self.gizmo = None
        self.position = position
        self.is_trigger = is_trigger
        self.debug = Config.debug_mode
        _active_colliders.append(self)

    def __del__(self):
        assert self in _active_colliders
        _active_colliders.remove(self)

    def custom_update(self, delta: float):
        if self.debug and self.gizmo is not None:
            self.gizmo.position = self.position
        if not self.is_trigger:
            return
        for other in _active_colliders:
            if self.is_colliding(other):
                # TODO: COllision
                pass

    def is_colliding(self, other: Collider):
        return False

    @staticmethod
    def _collision_rect_v_rect(a: RectCollider, b: RectCollider) -> bool:
        if a.position.x + a.size.x < b.position.x:
            return False
        if a.position.y + a.size.y < b.position.y:
            return False
        if b.position.x + b.size.x < a.position.x:
            return False
        if b.position.y + b.size.y < a.position.y:
            return False
        return True

    @staticmethod
    def _collision_rect_v_circle(rect: RectCollider, circle: CircleCollider) -> bool:
        interpoint = utils.clamp(circle.position, rect.position - rect.size / 2, rect.position + rect.size / 2)
        return (interpoint - circle.position).sqr_magnitude <= circle.radius * circle.radius

    @staticmethod
    def _collision_circle_v_circle(a: CircleCollider, b: CircleCollider) -> bool:
        sqr_dist = (a.position - b.position).sqr_magnitude
        max_dist = a.radius + b.radius
        return sqr_dist <= max_dist * max_dist


class RectCollider(Collider):
    def __init__(self, game: GamePlay, position: Vector2, size: Vector2, is_trigger: bool = False):
        super().__init__(game, position, is_trigger)
        self.size = size

        if self.debug:
            self.gizmo = SpriteRenderer(game.canvas,
                                        RectCollider.__draw_gizmo,
                                        position=self.position,
                                        size=PartialVector2(self.size))

    def custom_update(self, delta: float):
        super().custom_update(delta)

    def is_colliding(self, other: Collider):
        if not self.is_trigger:
            return False
        if isinstance(other, RectCollider):
            return Collider._collision_rect_v_rect(self, other)
        elif isinstance(other, CircleCollider):
            return Collider._collision_rect_v_circle(self, other)
        else:
            return False

    @staticmethod
    def __draw_gizmo(renderer: SpriteRenderer) -> int:
        tl = renderer.position - renderer.size / 2
        br = renderer.position + renderer.size / 2
        return renderer.canvas.create_rectangle(int(tl.x), int(tl.y), int(tl.x), int(tl.y), fill=Config.gizmo_color)


class CircleCollider(Collider):
    def __init__(self, game: GamePlay, position: Vector2, radius: float, is_trigger: bool = False):
        super().__init__(game, position, is_trigger)
        self.radius = radius

        if self.debug:
            self.sprite = SpriteRenderer(game.canvas,
                                         self.__draw_gizmo,
                                         position=self.position,
                                         size=Vector2(1, 1) * self.radius * 2)

    def custom_update(self, delta: float):
        super().custom_update(delta)

    def is_colliding(self, other: Collider):
        if not self.is_trigger:
            return False
        if isinstance(other, RectCollider):
            return Collider._collision_rect_v_circle(other, self)
        elif isinstance(other, CircleCollider):
            return Collider._collision_circle_v_circle(self, other)
        else:
            return False

    def __draw_gizmo(self, renderer: SpriteRenderer) -> int:
        tl = renderer.position - renderer.size / 2
        br = renderer.position + renderer.size / 2
        renderer.size = Vector2(1, 1) * self.radius * 2
        print("CircleCollider.__draw_gizmo", tl, br, renderer.size)
        return renderer.canvas.create_oval(int(tl.x), int(tl.y), int(br.x), int(br.y), fill=Config.gizmo_color)
