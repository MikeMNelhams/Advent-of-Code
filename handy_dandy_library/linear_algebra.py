from __future__ import annotations

from handy_dandy_library.list_operations import consecutive_pairs


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

    def __eq__(self, other: Vector) -> bool:
        return hash(self) == hash(other)

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

    def manhattan_distance(self, other: Vector) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def cross_product(self, other: Vector) -> int:
        return self.x * other.y - other.x * self.y

    @classmethod
    def zero(cls):
        return cls((0, 0))


def polygon_area(polygon: list[Vector]) -> float:
    return 0.5 * abs(sum(a.cross_product(b) for a, b in consecutive_pairs(polygon)))


def integer_border_points_count(polygon: list[Vector]) -> int:
    return sum(a.manhattan_distance(b) for a, b in consecutive_pairs(polygon)) + 1
