from __future__ import annotations
from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import polygon_area, integer_border_points_count


type Coordinate = Vector


def sign(x: int) -> int:
    if x > 0:
        return 1
    return -1


class UnitVectors:
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)


class Vector:
    DIRECTION_TO_UNIT_VECTORS = {'U': UnitVectors.UP, 'R': UnitVectors.RIGHT,
                                 'D': UnitVectors.DOWN, 'L': UnitVectors.LEFT}
    INT_TO_DIRECTION = ['R', 'D', 'L', 'U']

    def __init__(self, values: tuple[int, int]):
        if len(values) != 2:
            raise TypeError
        self.x = values[0]
        self.y = values[1]

    def __eq__(self, other: Vector) -> bool:
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.x
        return self.y

    def __mul__(self, other: int) -> Vector:
        return Vector((self.x * other, self.y * other))

    def __add__(self, other: Vector) -> Vector:
        return Vector((self.x + other.x, self.y + other.y))

    def manhattan_distance(self, other: Vector) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def cross_product(self, other: Vector) -> int:
        return self.x * other.y - other.x * self.y

    @classmethod
    def from_direction_magnitude(cls, direction: str, magnitude: int):
        return cls(cls.DIRECTION_TO_UNIT_VECTORS[direction]) * magnitude

    @classmethod
    def from_hexadecimal_line(cls, line: str):
        line_thirds = line.split(' ')
        color = line_thirds[2][2:-1]
        direction = cls.INT_TO_DIRECTION[int(color[-1])]
        return cls.from_direction_magnitude(direction, int(color[:-1], 16))

    @classmethod
    def zero(cls):
        return cls((0, 0))


class ColorVector:
    def __init__(self, direction_vector: Vector, color: str):
        self.direction_vector = direction_vector
        self.color = color

    def __repr__(self) -> str:
        return f"ColorVector(({self.direction_vector.x}, {self.direction_vector.y}), {self.color})"

    @classmethod
    def from_line(cls, line: str):
        line_thirds = line.split(' ')
        direction = line_thirds[0]
        magnitude = int(line_thirds[1])
        color = line_thirds[2]
        direction_vector = Vector.from_direction_magnitude(direction, magnitude)
        return cls(direction_vector, color)

    @classmethod
    def from_line_but_hexadecimal_twist(cls, line: str):
        return cls(Vector.from_hexadecimal_line(line), '')


class Shape:
    def __init__(self, coordinates: list[Vector]):
        self.coordinates = coordinates
        self.__coordinates_repr = [(coordinate.x, coordinate.y) for coordinate in coordinates]

    @property
    def num_border_points(self) -> int:
        return integer_border_points_count(self.coordinates)

    def __repr__(self) -> str:
        return str(self.__coordinates_repr)

    def __len__(self) -> int:
        return len(self.coordinates)

    @property
    def area(self) -> float:
        return polygon_area(self.coordinates)

    @property
    def dug_area(self) -> int:
        return int(self.area) + 1 + self.num_border_points // 2


class Digger:
    def __init__(self, color_vectors: list[ColorVector]):
        self.color_vectors = color_vectors
        self.shape = Shape(self.__grid_corner_coordinates(color_vectors))

    @property
    def area(self):
        return self.shape.dug_area

    @staticmethod
    def __grid_corner_coordinates(color_vectors: list[ColorVector]) -> list[Coordinate]:
        coordinates = [Vector.zero() for _ in range(len(color_vectors))]
        for i, color_vector in enumerate(color_vectors[:-1], 1):
            coordinates[i] = coordinates[i-1] + color_vector.direction_vector
        return coordinates


def read_coordinates(lines: list[str]) -> list[ColorVector]:
    return [ColorVector.from_line(line) for line in lines]


def tests():
    color_vectors = read_coordinates(read_lines("day_18_1_test_input1.txt"))
    print(color_vectors)

    digger = Digger(color_vectors)
    assert digger.area == 62


def main():
    tests()

    color_vectors = read_coordinates(read_lines("day_18_1_input.txt"))
    digger = Digger(color_vectors)
    t = digger.area
    print(t)


if __name__ == "__main__":
    main()
