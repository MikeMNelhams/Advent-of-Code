from __future__ import annotations


class UnitVector:
    UNIT_VECTOR_NAMES_FROM_VECTOR = {(1, 0): "right", (0, 1): "down", (-1, 0): "left", (0, -1): "up"}

    def __init__(self, values: tuple[int, int]):
        self.x = values[0]
        self.y = values[1]

    def __eq__(self, other: UnitVector) -> bool:
        if not isinstance(other, UnitVector):
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    @property
    def direction_name(self) -> str:
        return self.UNIT_VECTOR_NAMES_FROM_VECTOR.get((self.x, self.y), "not_unit_vector")


class Vector(UnitVector):
    def __init__(self, values: tuple[int, int]):
        super().__init__(values)

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other: Vector) -> Vector:
        return Vector((self.x + other.x, self.y + other.y))

    def __sub__(self, other: Vector) -> Vector:
        return Vector((self.x - other.x, self.y - other.y))

    def __mul__(self, other: int) -> Vector:
        return Vector((self.x * other, self.y * other))

    def __rmul__(self, other: int) -> Vector:
        return self.__mul__(other)

    def __mod__(self, other: int) -> Vector:
        return Vector((self.x % other, self.y % other))

    @classmethod
    def zero(cls):
        return cls((0, 0))
