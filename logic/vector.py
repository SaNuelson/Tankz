from __future__ import annotations

import math


class Vector2:
    x: float
    """X coordinate of the vector"""

    y: float
    """Y coordinate of the vector"""

    def __init__(self, x: float | Vector2 = 0, y: float = 0):
        if isinstance(x, Vector2):
            self.x = x.x
            self.y = x.y
        else:
            self.x = x
            self.y = y

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __add__(self, other: Vector2):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2):
        return self + -other

    def __mul__(self, other: Vector2 | float):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        return Vector2(self.x * other, self.y * other)

    def __matmul__(self, other: Vector2):
        return self.x * other.x + self.y * other.y

    def __mod__(self, other: float):
        return Vector2(self.x % other, self.y % other)

    def __floordiv__(self, other: Vector2 | float):
        return Vector2(self.x // other, self.y // other)

    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))

    def __truediv__(self, other: Vector2 | float):
        return Vector2(self.x / other, self.y / other)

    def __eq__(self, other: Vector2):
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __ne__(self, other: Vector2):
        return not self.__eq__(other)

    def __gt__(self, other: Vector2):
        return self.x > other.x and self.y > other.y

    def __ge__(self, other: Vector2):
        return self.x >= other.x and self.y >= other.y

    def __lt__(self, other: Vector2):
        return other.__gt__(self)

    def __le__(self, other: Vector2):
        return other.__ge__(self)

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    @property
    def sqr_magnitude(self) -> float:
        return self.x * self.x + self.y * self.y

    @property
    def normalized(self) -> Vector2:
        if self.magnitude == 0:
            return None
        return self / self.magnitude

    @property
    def area(self) -> float:
        return self.x * self.y

    def rotated(self, degrees: float) -> Vector2:
        radians = math.radians(degrees)
        return Vector2(
            self.x * math.cos(radians) - self.y * math.sin(radians),
            self.x * math.sin(radians) + self.y * math.cos(radians)
        )

    def __repr__(self):
        return f"Vector2({self.x},{self.y})"


class PartialVector2(Vector2):
    x: float | None
    """X coordinate of the vector"""

    y: float | None
    """Y coordinate of the vector"""

    def __init__(self, x: float | Vector2 | None = 0, y: float | None = 0):
        super().__init__(x, y)

    def __neg__(self):
        return Vector2(-self.x if self.x is not None else None,
                       -self.y if self.y is not None else None)

    def __add__(self, other: Vector2):
        result = PartialVector2(
            (self.x + other.x) if (self.x is not None and other.x is not None) else None,
            (self.y + other.y) if (self.y is not None and other.y is not None) else None
        )
        return result

    def __sub__(self, other: Vector2):
        result = PartialVector2(
            (self.x - other.x) if (self.x is not None and other.x is not None) else None,
            (self.y - other.y) if (self.y is not None and other.y is not None) else None
        )
        return result

    def __mul__(self, other: float):
        result = PartialVector2(
            (self.x * other) if (self.x is not None) else None,
            (self.y * other) if (self.y is not None) else None
        )
        return result

    def __matmul__(self, other: Vector2):
        if not self.is_valid or (other is PartialVector2 and not other.is_valid):
            return None
        return self.x * other.x + self.y * other.y

    def __mod__(self, other: float):
        return Vector2(
            self.x % other if self.x is not None else None,
            self.y % other if self.y is not None else None
        )

    def __floordiv__(self, other: Vector2 | float):
        if other is float:
            return Vector2(
                self.x // other if self.x is not None else None,
                self.y // other if self.y is not None else None
            )

        result = PartialVector2(
            (self.x // other.x) if (self.x is not None and other.x is not None) else None,
            (self.y // other.y) if (self.y is not None and other.y is not None) else None
        )
        return result

    def __abs__(self):
        return Vector2(
            abs(self.x) if self.x is not None else None,
            abs(self.y) if self.y is not None else None
        )

    def __truediv__(self, other: Vector2 | float):
        if other is float:
            return Vector2(self.x / other if self.x is not None else None,
                           self.y / other if self.y is not None else None)

        result = PartialVector2(
            (self.x / other.x) if (self.x is not None and other.x is not None) else None,
            (self.y / other.y) if (self.y is not None and other.y is not None) else None
        )
        return result

    def partially_compatible(self, other: Vector2):
        return not((self.x is None and other.x is not None) or
                   (self.x is not None and other.x is None) or
                   (self.y is None and other.y is not None) or
                   (self.y is not None and other.y is None))

    @property
    def magnitude(self) -> float | None:
        if not self.is_valid:
            return None
        return math.sqrt(self.x * self.x + self.y * self.y)

    @property
    def sqr_magnitude(self) -> float | None:
        if not self.is_valid:
            return None
        return self.x * self.x + self.y * self.y

    @property
    def normalized(self) -> Vector2 | None:
        if self.magnitude == 0:
            return None
        return self / self.magnitude

    @property
    def is_valid(self) -> bool:
        return self.x is not None and self.y is not None

    def rotated(self, degrees: float) -> Vector2 | None:
        if not self.is_valid:
            return None
        radians = math.radians(degrees)
        return Vector2(
            self.x * math.cos(radians) - self.y * math.sin(radians),
            self.x * math.sin(radians) + self.y * math.cos(radians)
        )

    def __repr__(self):
        return f"Vector2({self.x},{self.y})"