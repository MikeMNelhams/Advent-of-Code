from __future__ import annotations
from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import pad_with_horizontal_rules, make_blue

from queue import PriorityQueue

import cProfile
import re


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

    @classmethod
    def UP(cls):
        return cls((0, -1))

    @classmethod
    def RIGHT(cls):
        return cls((1, 0))

    @classmethod
    def DOWN(cls):
        return cls((0, 1))

    @classmethod
    def LEFT(cls):
        return cls((-1, 0))


class Vector(UnitVector):
    def __init__(self, values: tuple[int, int]):
        super().__init__(values)

    def __add__(self, other: Vector) -> Vector:
        return Vector((self.x + other.x, self.y + other.y))

    def __sub__(self, other: Vector) -> Vector:
        return Vector((self.x - other.x, self.y - other.y))

    @classmethod
    def zero(cls):
        return cls((0, 0))

    @property
    def rotated_right(self) -> Vector:
        return Vector((self.y * -abs(self.y), self.x))

    @property
    def rotated_left(self) -> Vector:
        return Vector((self.y, self.x * -abs(self.x)))

    def manhattan_distance(self, other: Vector) -> int:
        return abs(self.x - other.x, self.y - other.y)


class Square:
    ZERO = Vector.zero()

    def __init__(self, coordinate: Vector, distance_to_end_node: int, heat_loss: int, parent: Square = None):
        self.coordinate = coordinate
        self.parent = parent
        self.distance_to_end_node = distance_to_end_node

        self.heat_loss = heat_loss
        self.forward_direction = self.ZERO
        self.forwards_count = 0
        if parent is not None:
            self.heat_loss = heat_loss + parent.heat_loss
            self.forward_direction = coordinate - parent.coordinate
            if parent.forward_direction == self.forward_direction:
                self.forwards_count = self.parent.forwards_count + 1

    def __repr__(self) -> str:
        return f"{make_blue("Sqr")}({self.coordinate}, (g, h, f): ({self.heat_loss},{self.distance_to_end_node},{self.f}))"

    def __lt__(self, other: Square) -> bool:
        return self.f < other.f or (self.f == other.f and self.heat_loss < other.heat_loss) or ()

    @property
    def f(self) -> int:
        return self.heat_loss + self.distance_to_end_node

    def path_to_root_parent(self) -> tuple[Vector]:
        parent = self.parent
        path = [self]
        while parent is not None:
            path.append(parent)
            parent = parent.parent
        return tuple(reversed(path))

    def is_valid_next(self, next_coordinate: Vector) -> bool:
        if self.parent is None:
            return True
        direction = next_coordinate - self.coordinate
        return self.forward_direction != direction or self.forwards_count != 2


class LavaGrid:
    def __init__(self, grid: Grid):
        self.grid = grid

        self.n = len(grid)
        self.m = len(grid[0])
        print(f"Grid size: ({self.m}, {self.n})")
        self.distances_to_end_node = self.__distances_to_end_node(grid)

    def __edge_checks(self, coordinate: Vector) -> (bool, bool, bool, bool):
        return coordinate.y < self.m - 1, coordinate.x < self.n - 1, coordinate.x > 0, coordinate.y > 0

    def __repr__(self) -> str:
        lines = '\n'.join(['\t' + ''.join(str(char) for char in line) for line in self.grid])
        return pad_with_horizontal_rules(lines)

    @staticmethod
    def __distances_to_end_node(grid: Grid) -> Grid:
        m = len(grid[0])
        n = len(grid)
        return [[m - j + n - i - 2 for j in range(m)] for i in range(n)]

    @classmethod
    def from_lines(cls, lines: list[str]):
        grid = [[int(char) for char in line] for line in lines]
        return cls(grid)

    def potential_squares(self, square: Square) -> list[Square]:
        previous_square_coordinate = None
        previous_square = square.parent
        if previous_square is not None:
            previous_square_coordinate = previous_square.coordinate
        coordinate = square.coordinate
        coordinate_indices = ((coordinate.x, coordinate.y + 1),
                              (coordinate.x + 1, coordinate.y),
                              (coordinate.x - 1, coordinate.y),
                              (coordinate.x, coordinate.y - 1),
                              )
        edge_checks = self.__edge_checks(coordinate)
        squares = []
        for edge_check, coordinate_indices in zip(edge_checks, coordinate_indices):
            potential_coordinate = Vector(coordinate_indices)
            if potential_coordinate != previous_square_coordinate and edge_check:
                next_square = self.square_from_grid(potential_coordinate, parent=square)
                if square.is_valid_next(potential_coordinate):
                    squares.append(next_square)
        return squares

    def square_from_grid(self, coordinate: Vector, parent: Square) -> Square:
        try:
            _square = Square(coordinate,
                             self.distances_to_end_node[coordinate.x][coordinate.y],
                             self.grid[coordinate.x][coordinate.y],
                             parent=parent)
        except IndexError as e:
            print(f"Bad coordinate: {coordinate}")
            print(f"Grid size: ({self.n},{self.m})")
            raise e
        return _square

    def minimal_route_heat_loss(self) -> (int, list[Vector]):
        # Definitely a pathfinding problem.
        start_square = self.square_from_grid(Vector((0, 0)), parent=None)
        start_square.heat_loss = 0  # We don't include the starting heat loss

        open_squares = PriorityQueue()
        open_squares.put(start_square)

        final_coordinate = Vector((self.n - 1, self.m - 1))
        checked_grid = [[False for _ in range(self.m)] for _ in range(self.n)]

        while not open_squares.empty():
            square = open_squares.get()
            if square.coordinate == final_coordinate:
                return square.heat_loss, square.path_to_root_parent()

            checked_grid[square.coordinate.x][square.coordinate.y] = 1

            potential_next_squares = self.potential_squares(square)
            for potential_next_square in potential_next_squares:
                next_square_coord = potential_next_square.coordinate
                if checked_grid[next_square_coord.x][next_square_coord.y]:
                    continue

                open_squares.put(potential_next_square)


def tests1():
    up = Vector.UP()
    left = Vector.LEFT()
    down = Vector.DOWN()
    right = Vector.RIGHT()

    assert right.rotated_right == down
    assert down.rotated_right == left
    assert left.rotated_right == up
    assert up.rotated_right == right

    assert up.rotated_left == left
    assert left.rotated_left == down
    assert down.rotated_left == right
    assert right.rotated_left == up


def tests2():
    # Correctness check
    lava_grid = LavaGrid.from_lines(read_lines("day_17_1_test_input.txt"))
    print(lava_grid)
    e, path = lava_grid.minimal_route_heat_loss()
    for p in path:
        print(p)
    assert e == 102


def tests3():
    # Profiling (493 answer)
    # cProfile.run("re.compile(LavaGrid.from_lines(read_lines(\"day_17_1_test_input2.txt\")).minimal_route_heat_loss())")
    lava_grid = LavaGrid.from_lines(read_lines("day_17_1_test_input2.txt"))
    e, path = lava_grid.minimal_route_heat_loss()
    assert e == 493


def main():
    tests2()
    tests3()

    lava_grid = LavaGrid.from_lines(read_lines("day_17_1_input.txt"))
    print(lava_grid)

    e, path = lava_grid.minimal_route_heat_loss()
    print(e)


if __name__ == "__main__":
    main()
