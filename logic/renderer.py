from __future__ import annotations

import tkinter as tk
from enum import Enum
from typing import Tuple, Callable

import utils
from logic.vector import Vector2, PartialVector2


class SpriteDrawMode(Enum):
    FROM_FILE = 1
    DIRECT = 2
    CALLBACK = 3


class SpriteRenderer:
    # region dirty: bool = False { get; set_dirty }
    _dirty: bool = False

    @property
    def dirty(self) -> bool:
        """Flag whether gizmo needs to be reloaded"""
        return self._dirty

    def set_dirty(self):
        """Force renderer to refresh the gizmo during next update"""
        self._dirty = True

    # endregion

    # region enabled: bool = True { get; set }
    _enabled: bool = True

    @property
    def enabled(self) -> bool:
        """Flag whether gizmo is drawn on canvas"""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        if self.enabled == value:
            return
        self.enabled = value
        if self.enabled:
            self.enable()
        else:
            self.disable()

    # endregion

    # region canvas: tk.Canvas { get; set }
    _canvas: tk.Canvas = None
    """Canvas on which to be drawn"""

    @property
    def canvas(self) -> tk.Canvas:
        return self._canvas

    @canvas.setter
    def canvas(self, value: tk.Canvas):
        if self._canvas == value:
            return
        if self._sprite_id is not None and self._canvas.find_withtag(self._sprite_id):
            self._canvas.delete(self._sprite_id)
        self._canvas = value
        self.set_dirty()

    # endregion

    # region sprite_path: str | Callable[[SpriteRenderer], int] (PathLike) { get; set }
    _sprite_path: str | Callable[[SpriteRenderer], int] = None
    """
    Path in project to the _sprite to be loaded. 
    Alternatively, callable that creates an image and returns its canvas ID.
    """

    @property
    def sprite_path(self) -> str:
        return self._sprite_path

    @sprite_path.setter
    def sprite_path(self, value: str):
        if self._sprite_path == value:
            return
        # TODO: Check path exists & is good
        self._sprite_path = value
        self.__load_sprite()
        self.set_dirty()

    # endregion

    # region gizmo: tk.PhotoImage { get; private set (via sprite_path) }
    _sprite: tk.PhotoImage = None
    """Sprite drawn onto _canvas"""

    @property
    def sprite(self) -> tk.PhotoImage:
        return self._sprite

    # endregion

    # region sprite_id: int | None { get; private set (via sprite_path) }
    _sprite_id: int | None = None
    """ID of _sprite on _canvas"""

    @property
    def sprite_id(self) -> int | None:
        return self._sprite_id

    # endregion

    # region position: Vector2 { get; set }
    _position: Vector2

    @property
    def position(self) -> Vector2:
        """Position of gizmo on canvas, specifically its center"""
        return Vector2(self._position)

    @position.setter
    def position(self, value: Vector2):
        if self._position == value:
            return
        self._position = value
        self.set_dirty()

    # endregion

    # region anchor: Vector2 { get; set }
    _anchor: Vector2
    """Vector specifying pivot point of _sprite, (0,0) being top-left corner and (1,1) being bottom-right corner"""
    _anchor_position: Vector2 = Vector2(0, 0)
    """Offset in pixels from the center of gizmo to the anchor"""

    # When gizmo rotates/scales, center stays the same, so it serves well as reference point.
    # New anchor needs to be where old anchor was
    # New anchor == center + rotated/scaled offset
    # Old anchor == old center + old offset

    @property
    def anchor(self) -> Vector2:
        return self._anchor

    @anchor.setter
    def anchor(self, value: Vector2):
        if self._anchor == value:
            return
        self.anchor = value
        self.set_dirty()

    # endregion

    # region rotation: Vector2 { get; set }
    _rotation: float
    """Rotation of the _sprite in degrees"""

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, value: float):
        if self._rotation == value:
            return
        self._rotation = value
        self.set_dirty()

    # endregion

    # region size: Vector2 { get; set }
    _size: Vector2
    """Size of the _sprite in pixels"""

    @property
    def size(self) -> Vector2:
        return self._size

    @size.setter
    def size(self, value: Vector2):
        if self._size == value:
            return
        self._size = value
        self.set_dirty()

    # endregion

    # region flip: Tuple[bool, bool] { get; set }
    _flip: Tuple[bool, bool]
    """Flags specifying whether _sprite is flipped horizontally/vertically"""

    @property
    def flip(self) -> Tuple[bool, bool]:
        return self._flip

    @flip.setter
    def flip(self, value: Tuple[bool, bool]):
        if self._flip == value:
            return
        self._flip = value
        self.set_dirty()

    # endregion

    _draw_mode: SpriteDrawMode

    def __init__(self,
                 canvas: tk.Canvas,
                 sprite_path: str | tk.PhotoImage | Callable[[SpriteRenderer], int],
                 position: Vector2 = Vector2(0, 0),
                 rotation: float = 0,
                 size: PartialVector2 = PartialVector2(None, None),
                 flip: Tuple[bool, bool] = (False, False),
                 anchor: Vector2 = Vector2(0.5, 0.5)):
        self._canvas = canvas

        self._position = position
        self._rotation = rotation
        self._size = Vector2(0, 0)
        self._flip = flip
        self._anchor = anchor

        if isinstance(sprite_path, str):
            self._draw_mode = SpriteDrawMode.FROM_FILE
            self._sprite_path = sprite_path
        elif isinstance(sprite_path, Callable):
            self._draw_mode = SpriteDrawMode.CALLBACK
            self._sprite_path = sprite_path
        else:
            self._draw_mode = SpriteDrawMode.DIRECT
            self._sprite = sprite_path

        self.__load_sprite(size)
        self._dirty = True

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def custom_update(self, delta: float):
        if self._dirty:
            self._dirty = False

            if self._anchor != Vector2(0.5, 0.5):
                self._anchor_position = (Vector2(0.5, 0.5) - self.anchor) * self.size
                self._anchor_position = utils.rotate_vec(self._anchor_position, -self.rotation)

            if self._sprite_id is not None and self._canvas.find_withtag(self._sprite_id):
                self._canvas.delete(self._sprite_id)

            self.__load_sprite()

    def __load_sprite(self, override_size: PartialVector2 | None = None):
        if self._draw_mode == SpriteDrawMode.DIRECT:
            return

        width = override_size.x if override_size is not None else self._size.x if self._size is not None else None
        height = override_size.y if override_size is not None else self._size.y if self._size is not None else None

        if self._draw_mode == SpriteDrawMode.CALLBACK:
            self._sprite_id = self._sprite_path(self)
            assert self.size is not None, "SpriteRenderer onSpriteDrawn callback must set renderer.size"
            print("SpriteRenderer.__load_sprite _size set via callable to", self._size)
        else:
            self._sprite = utils.load_photo(self._sprite_path,
                                            int(height) if height is not None else None,
                                            int(width) if width is not None else None,
                                            self._flip[0] if self._flip is not None else False,
                                            self._flip[1] if self._flip is not None else False,
                                            int(self._rotation) if self._rotation is not None else 0)
            delta = self._anchor_position - (Vector2(0.5, 0.5) - self.anchor) * self.size
            self._sprite_id = self._canvas.create_image(self._position.x + delta.x,
                                                        self._position.y + delta.y,
                                                        image=self._sprite)
            if override_size is not None:
                self._size = Vector2(self._sprite.width(), self._sprite.height())
                print("SpriteRenderer.__load_sprite _size deduced to", self._size)

    def abs_pos(self, rel_point: Vector2):
        return self.position + (rel_point - Vector2(0.5, 0.5)) * utils.rotate_vec(self.size / 2, -self.rotation)
