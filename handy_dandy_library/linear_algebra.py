from __future__ import annotations

from handy_dandy_library.list_operations import consecutive_pairs


class UnitVector2D:
    UNIT_VECTOR_NAMES_FROM_VECTOR = {(1, 0): "right", (0, 1): "down", (-1, 0): "left", (0, -1): "up"}

    def __init__(self, values: tuple[int, int]):
        self.x = values[0]
        self.y = values[1]

    def __eq__(self, other: UnitVector2D) -> bool:
        if not isinstance(other, UnitVector2D):
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"({str(self)})"

    def __str__(self) -> str:
        return f"{self.x},{self.y}"

    @property
    def direction_name(self) -> str:
        return self.UNIT_VECTOR_NAMES_FROM_VECTOR.get((self.x, self.y), "not_unit_vector")


class Vector2D(UnitVector2D):
    def __init__(self, values: tuple[float, float]):
        super().__init__(values)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other: Vector2D) -> bool:
        return hash(self) == hash(other)

    def __add__(self, other: Vector2D) -> Vector2D:
        return Vector2D((self.x + other.x, self.y + other.y))

    def __sub__(self, other: Vector2D) -> Vector2D:
        return Vector2D((self.x - other.x, self.y - other.y))

    def __mul__(self, other: float) -> Vector2D:
        return Vector2D((self.x * other, self.y * other))

    def __floordiv__(self, other: int) -> Vector2D:
        return Vector2D((self.x // other, self.y // other))

    def __rmul__(self, other: float) -> Vector2D:
        return self.__mul__(other)

    def __mod__(self, other: int) -> Vector2D:
        return Vector2D((self.x % other, self.y % other))

    def manhattan_distance(self, other: Vector2D) -> float:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def cross_product(self, other: Vector2D) -> float:
        return self.x * other.y - other.x * self.y

    @classmethod
    def zero(cls):
        return cls((0, 0))


class Vector3D:
    def __init__(self, values: tuple[float, float, float]):
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

    def __mul__(self, other: float) -> Vector3D:
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

    def xy_projected_cross_product(self, other: Vector3D) -> int:
        return self.x * other.y - other.x * self.y

    @property
    def manhattan_distance_from_zero(self) -> float:
        return self.x + self.y + self.z

    @property
    def first_non_zero_dim_index(self) -> int:
        for i, value in enumerate(self.values):
            if value != 0:
                return i
        raise TypeError

    @property
    def values(self) -> list[float]:
        return [self.x, self.y, self.z]

    @classmethod
    def zero(cls):
        return cls((0, 0, 0))

    def linearly_independent(self, other: Vector3D) -> bool:
        return any(v != 0 for v in self.cross(other).values)

    def cross(self, other: Vector3D) -> Vector3D:
        return Vector3D((self.y * other.z - self.z * other.y,
                         self.z * other.x - self.x * other.z,
                         self.x * other.y - self.y * other.x))

    def dot(self, other: Vector3D) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def triple_product(self, other: Vector3D, other2: Vector3D) -> float:
        return self.dot(other.cross(other2))


def polygon_area(polygon: list[Vector2D]) -> float:
    return 0.5 * abs(sum(a.cross_product(b) for a, b in consecutive_pairs(polygon)))


def integer_border_points_count(polygon: list[Vector2D]) -> int:
    return sum(a.manhattan_distance(b) for a, b in consecutive_pairs(polygon)) + 1


def sign(x: float) -> int:
    return x and (-1 if x < 0 else 1)
