from __future__ import annotations
from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import pad_with_horizontal_rules


type Grid = list[list[int]]


class UnitVector:
    UNIT_VECTOR_CODENAMES = {"up": 0, "right": 1, "down": 2, "left": 3}
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

    def __mod__(self, other: int) -> Vector:
        return Vector((self.x % other, self.y % other))

    @classmethod
    def zero(cls):
        return cls((0, 0))


class SnowIsland:
    encodings = {'.': 0, '#': 1, '>': 2, '^': 3, 'v': 4, '<': 5, 'S': 6}
    reverse_encodings = {0: '.', 1: '#', 2: '>', 3: '^', 4: 'v', 5: '<', 6: 'S'}
    UP = Vector((-1, 0))
    RIGHT = Vector((0, 1))
    DOWN = Vector((1, 0))
    LEFT = Vector((0, -1))

    def __init__(self, encoded_grid: list[list[int]], start_position: Vector):
        self.grid = encoded_grid
        self.n = len(encoded_grid)
        self.m = len(encoded_grid[0])
        self.start_position = start_position

    def __getitem__(self, item: Vector) -> int:
        return self.grid[item.x][item.y]

    def __setitem__(self, key: Vector, value: int) -> None:
        self.grid[key.x][key.y] = value
        return None

    def __repr__(self) -> str:
        start_position_encoding = self[self.start_position]
        self[self.start_position] = 6
        lines = '\n'.join(''.join(self.reverse_encodings[encoding] for encoding in line) for line in self.grid)
        self[self.start_position] = start_position_encoding
        return pad_with_horizontal_rules(lines)

    @classmethod
    def from_lines(cls, lines: list[str], start_position: Vector):
        return cls([[cls.encodings[char] for char in line] for line in lines], start_position)

    def __edge_checks(self, coordinate: Vector) -> (bool, bool, bool, bool):
        return coordinate.y < self.m - 1, coordinate.x > 0, coordinate.x < self.n - 1, coordinate.y > 0

    def is_forest(self, coordinate: Vector) -> bool:
        return self[coordinate] == 1

    def neighbours(self, coordinate: Vector) -> set[Vector]:
        # Right, Up, Down, Left
        potential_neighbours = (coordinate + self.RIGHT,
                                coordinate + self.UP,
                                coordinate + self.DOWN,
                                coordinate + self.LEFT)
        for i in range(4):
            if self[coordinate] == i + 2:
                return {potential_neighbours[i]}
        edge_checks = self.__edge_checks(coordinate)
        coord_checks = tuple(edge_checks[i] and not self.is_forest(potential_neighbours[i]) for i in range(4))
        valid_neighbours = {neighbour for i, (neighbour, is_valid) in enumerate(zip(potential_neighbours, coord_checks)) if is_valid}
        return valid_neighbours


def tests():
    snow_island = SnowIsland.from_lines(read_lines("day_23_1_test_input.txt"), Vector((0, 1)))
    print(snow_island)
    print(snow_island.neighbours(snow_island.start_position))


def main():
    tests()


if __name__ == "__main__":
    main()
