from __future__ import annotations
from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D, polygon_area, integer_border_points_count


def sign(x: int) -> int:
    if x > 0:
        return 1
    return -1


class ColorVector:
    UP = Vector2D((0, 1))
    RIGHT = Vector2D((1, 0))
    DOWN = Vector2D((0, -1))
    LEFT = Vector2D((-1, 0))
    DIRECTION_TO_UNIT_VECTORS = {'U': UP, 'R': RIGHT,
                                 'D': DOWN, 'L': LEFT}
    INT_TO_DIRECTION = ['R', 'D', 'L', 'U']

    def __init__(self, direction_vector: Vector2D, color: str):
        self.direction_vector = direction_vector
        self.color = color

    def __repr__(self) -> str:
        return f"ColorVector(({self.direction_vector.x}, {self.direction_vector.y}), {self.color})"

    @classmethod
    def from_direction_magnitude(cls, direction: str, magnitude: int):
        return cls.DIRECTION_TO_UNIT_VECTORS[direction] * magnitude

    @classmethod
    def from_hexadecimal_line(cls, line: str):
        line_thirds = line.split(' ')
        color = line_thirds[2][2:-1]
        direction = cls.INT_TO_DIRECTION[int(color[-1])]
        return cls.from_direction_magnitude(direction, int(color[:-1], 16))

    @classmethod
    def from_line(cls, line: str):
        line_thirds = line.split(' ')
        direction = line_thirds[0]
        magnitude = int(line_thirds[1])
        color = line_thirds[2]
        direction_vector = cls.from_direction_magnitude(direction, magnitude)
        return cls(direction_vector, color)

    @classmethod
    def from_line_but_hexadecimal_twist(cls, line: str):
        return cls(cls.from_hexadecimal_line(line), '')


class Shape:
    def __init__(self, coordinates: list[Vector2D]):
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

    @classmethod
    def from_lines(cls, lines: list[str]):
        return cls([ColorVector.from_line(line) for line in lines])

    @property
    def area(self):
        return self.shape.dug_area

    @staticmethod
    def __grid_corner_coordinates(color_vectors: list[ColorVector]) -> list[Vector2D]:
        coordinates = [Vector2D.zero() for _ in range(len(color_vectors))]
        for i, color_vector in enumerate(color_vectors[:-1], 1):
            coordinates[i] = coordinates[i-1] + color_vector.direction_vector
        return coordinates


def tests():
    digger = Digger.from_lines(read_lines("day_18_1_test_input1.txt"))
    assert digger.area == 62


def main():
    tests()

    digger = Digger.from_lines(read_lines("day_18_1_input.txt"))
    t = digger.area
    print(t)


if __name__ == "__main__":
    main()
