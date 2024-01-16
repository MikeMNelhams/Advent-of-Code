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


class Vector3D:
    def __init__(self, values: tuple[int, int, int]):
        self.x = values[0]
        self.y = values[1]
        self.z = values[2]

    def __eq__(self, other: Vector3D) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, other: Vector3D) -> Vector3D:
        return Vector3D((self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other: Vector3D) -> Vector3D:
        return Vector3D((self.x - other.x, self.y - other.y, self.z - other.z))

    def __mul__(self, other: int) -> Vector3D:
        return Vector3D((self.x * other, self.y * other, self.z * other))

    def copy(self):
        return Vector3D((self.x, self.y, self.z))

    @property
    def magnitude(self) -> int:
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    @property
    def unit_vector(self) -> Vector3D:
        magnitude = self.xy_projection.magnitude
        if magnitude == 0:
            raise ZeroDivisionError
        return self * (1 / magnitude)

    @property
    def xy_projection(self) -> Vector3D:
        return Vector3D((self.x, self.y, 0))

    @property
    def manhattan_distance_from_zero(self) -> int:
        return self.x + self.y + self.z

    @property
    def first_non_zero_dim_index(self) -> int:
        for i, value in enumerate(self.values):
            if value != 0:
                return i
        raise TypeError

    @property
    def values(self) -> list[int]:
        return [self.x, self.y, self.z]

    @classmethod
    def zero(cls):
        return cls((0, 0, 0))


def polygon_area(polygon: list[Vector]) -> float:
    return 0.5 * abs(sum(a.cross_product(b) for a, b in consecutive_pairs(polygon)))


def integer_border_points_count(polygon: list[Vector]) -> int:
    return sum(a.manhattan_distance(b) for a, b in consecutive_pairs(polygon)) + 1
