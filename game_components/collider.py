from __future__ import annotations

from typing import TYPE_CHECKING, List

import numpy as np

import toolkit.canvas
import utils
from config import Config
from game_components.renderer import SpriteRenderer
from toolkit.event import Event
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
        self.collided = Event()
        _active_colliders.append(self)

    def __del__(self):
        assert self in _active_colliders
        _active_colliders.remove(self)

    def custom_update(self, delta: float):
        if self.gizmo is not None:
            if Config.debug_mode and self.gizmo.enabled:
                self.gizmo.position = self.position
                self.gizmo.custom_update(delta)
            elif Config.debug_mode and not self.gizmo.enabled:
                self.gizmo.enable()
            elif not Config.debug_mode and self.gizmo.enabled:
                self.gizmo.disable()

        if not self.is_trigger:
            return
        for other in _active_colliders:
            if self is other:
                continue
            if self.is_colliding(other):
                print("Collision between", self, other)
                self.collided(other)

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

    @staticmethod
    def _collision_rect_v_pixel(rect: RectCollider, pixel: PixelCollider) -> bool:
        tl = (rect.position - rect.size / 2).as_int()
        br = (rect.position + rect.size / 2).as_int()
        tr = Vector2(br.x, tl.y).as_int()
        bl = Vector2(tl.x, br.y).as_int()
        # common edge-points check for efficiency
        if pixel.map[tl.y, tl.x] \
                or pixel.map[tr.y, tr.x] \
                or pixel.map[bl.y, bl.x] \
                or pixel.map[br.y, br.x]:
            return True
        return np.any(pixel.map[tl.y:tr.y, tl.x:bl.x])

    @staticmethod
    def _collision_circle_v_pixel(circle: CircleCollider, pixel: PixelCollider) -> bool:
        top = (circle.position - Vector2(0, circle.radius)).as_int()
        bot = (circle.position + Vector2(0, circle.radius)).as_int()
        left = (circle.position - Vector2(circle.radius, 0)).as_int()
        right = (circle.position + Vector2(circle.radius, 0)).as_int()
        if pixel.map[top.y, top.x] \
                or pixel.map[left.y, left.x] \
                or pixel.map[bot.y, bot.x] \
                or pixel.map[right.y, right.x]:
            return True
        # TODO: Proper check
        return np.any(pixel.map[left.y:right.y, top.x:bot.x])


class RectCollider(Collider):
    def __init__(self, game: GamePlay, position: Vector2, size: Vector2, is_trigger: bool = False, **kwargs):
        super().__init__(game, position, is_trigger)
        self.size = size
        self.gizmo = SpriteRenderer(game.canvas,
                                    self.__draw_gizmo,
                                    position=self.position,
                                    size=PartialVector2(self.size),
                                    anchor=Vector2(),
                                    **kwargs)

    def custom_update(self, delta: float):
        super().custom_update(delta)

    def is_colliding(self, other: Collider):
        if not self.is_trigger:
            return False
        if isinstance(other, RectCollider):
            return Collider._collision_rect_v_rect(self, other)
        elif isinstance(other, CircleCollider):
            return Collider._collision_rect_v_circle(self, other)
        elif isinstance(other, PixelCollider):
            return Collider._collision_rect_v_pixel(self, other)
        else:
            return False

    def __draw_gizmo(self, renderer: SpriteRenderer, old_ids: List[int]) -> List[int]:
        if old_ids is not None:
            for old_id in old_ids:
                renderer.canvas.delete(old_id)

        tl = renderer.position
        br = renderer.position + self.size
        renderer.size = self.size
        return [
            *toolkit.canvas.draw_xbox(renderer.canvas, renderer.position, self.size, Config.gizmo_color_primary)
        ]


class CircleCollider(Collider):
    def __init__(self, game: GamePlay, position: Vector2, radius: float, is_trigger: bool = False, **kwargs):
        super().__init__(game, position, is_trigger)
        self.radius = radius
        self.gizmo = SpriteRenderer(game.canvas,
                                    self.__draw_gizmo,
                                    position=self.position,
                                    size=Vector2(1, 1) * self.radius * 2,
                                    anchor=Vector2(),
                                    **kwargs)

    def custom_update(self, delta: float):
        super().custom_update(delta)

    def is_colliding(self, other: Collider):
        if not self.is_trigger:
            return False
        if isinstance(other, RectCollider):
            return Collider._collision_rect_v_circle(other, self)
        elif isinstance(other, CircleCollider):
            return Collider._collision_circle_v_circle(self, other)
        elif isinstance(other, PixelCollider):
            return Collider._collision_circle_v_pixel(self, other)
        else:
            return False

    def __draw_gizmo(self, renderer: SpriteRenderer, old_ids: List[int]) -> List[int]:
        if old_ids is not None:
            for old_id in old_ids:
                renderer.canvas.delete(old_id)

        tl = renderer.position - self.radius
        br = renderer.position + self.radius
        renderer.size = Vector2(1, 1) * self.radius * 2
        return [
            renderer.canvas.create_oval(tl.x, tl.y, br.x, br.y, outline=Config.gizmo_color_primary),
            *toolkit.canvas.draw_x(renderer.canvas, renderer.position, int(self.radius / 2),
                                   Config.gizmo_color_secondary)
        ]


class PixelCollider(Collider):

    def __init__(self, game: GamePlay, pixelmap: np.ndarray, is_trigger: bool = False, **kwargs):
        super().__init__(game, Vector2(0, 0), is_trigger)
        self.map = pixelmap
        self.gizmo = SpriteRenderer(game.canvas,
                                    self.__draw_gizmo,
                                    position=Vector2(0, 0),
                                    size=PartialVector2(Config.screen_w, Config.screen_h),
                                    anchor=Vector2(),
                                    **kwargs)

    def __del__(self):
        assert self in _active_colliders
        _active_colliders.remove(self)

    def custom_update(self, delta: float):
        super().custom_update(delta)

    def is_colliding(self, other: Collider):
        if not self.is_trigger:
            return False
        if isinstance(other, RectCollider):
            return Collider._collision_rect_v_pixel(other, self)
        elif isinstance(other, CircleCollider):
            return Collider._collision_circle_v_pixel(other, self)
        elif isinstance(other, PixelCollider):
            raise NotImplementedError("PixelCollider v PixelCollider not implemented.")
        else:
            return False

    def __draw_gizmo(self, renderer: SpriteRenderer, old_ids: List[int]) -> List[int]:
        if old_ids is not None:
            for old_id in old_ids:
                renderer.canvas.delete(old_id)

        print("pixel collider rerender")
        gizmo_map = np.ones((self.map.shape[0], self.map.shape[1], 4))
        gizmo_map[:, :, 1] = 255
        gizmo_map[:, :, 3] = self.map * 63
        self.gizmo_photo = utils.as_photo(gizmo_map)
        return [
            renderer.canvas.create_image(0, 0, image=self.gizmo_photo, anchor="nw")
        ]
