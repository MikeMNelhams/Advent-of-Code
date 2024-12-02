from __future__ import annotations
from handy_dandy_library.file_processing import read_lines


type Grid = list[list[int]]

START_CHAR = 'S'


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


class Garden:
    encodings = {'.': 0, '#': 1, START_CHAR: 0}
    reverse_encodings = {0: '.', 1: '#', 2: 'O', 3: 'S'}
    UP = Vector((0, -1))
    RIGHT = Vector((1, 0))
    DOWN = Vector((0, 1))
    LEFT = Vector((-1, 0))

    def __init__(self, encoded_grid: Grid, start_square: Vector):
        self.grid = encoded_grid
        self.n = len(encoded_grid)
        self.m = len(encoded_grid[0])
        self.start_square = start_square

    @classmethod
    def from_lines(cls, lines: list[str]):
        start_square = Vector.zero()
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == START_CHAR:
                    start_square = Vector((i, j))
                    break
            if start_square != Vector.zero():
                break
        encoded_grid = [[cls.encodings[char] for char in line] for line in lines]
        return cls(encoded_grid, start_square)

    def __repr__(self):
        return '\n'.join([''.join([self.reverse_encodings[x] for x in line]) for line in self.grid])

    def is_rock(self, coordinate: Vector) -> bool:
        return self.grid[coordinate.x % self.n][coordinate.y % self.m]

    def neighbours(self, coordinate: Vector) -> set[Vector]:
        # Right, Up, Down, Left
        potential_neighbours = (coordinate + self.RIGHT,
                                coordinate + self.UP,
                                coordinate + self.DOWN,
                                coordinate + self.LEFT)
        coord_checks = (not self.is_rock(potential_neighbours[0]),
                        not self.is_rock(potential_neighbours[1]),
                        not self.is_rock(potential_neighbours[2]),
                        not self.is_rock(potential_neighbours[3]))

        valid_neighbours = {neighbour for i, (neighbour, is_valid) in enumerate(zip(potential_neighbours, coord_checks)) if is_valid}
        return valid_neighbours

    def reachable_plots(self, number_of_steps: int, starting_square: Vector=Vector((-1, -1))) -> list[Vector]:
        reachable_plots = {self.start_square}
        if starting_square != Vector((-1, -1)):
            reachable_plots = {starting_square}
        for _ in range(number_of_steps):
            coords_to_add = set()
            for coordinate in reachable_plots:
                coords_to_add |= self.neighbours(coordinate)
            reachable_plots = coords_to_add
        return list(reachable_plots)

    def update_to_circles(self, coordinates: list[Vector]) -> None:
        for coordinate in coordinates:
            self.grid[coordinate.x][coordinate.y] = 2
        return None

    def update_to_s(self, coordinate: list[Vector]) -> None:
        for coordinate in coordinate:
            self.grid[coordinate.x][coordinate.y] = 3
        return None

    def reachable_plot_count(self, number_of_steps: int, starting_square: Vector=Vector((-1, -1))) -> list[Vector]:
        return len(self.reachable_plots(number_of_steps, starting_square))

    def filter_by_edges(self, reachable_plots: list[Vector]) -> list[Vector]:
        return [reachable_plot for reachable_plot in reachable_plots if (reachable_plot.x == 0 or reachable_plot.y == 0 or reachable_plot.x == self.n-1 or reachable_plot.y == self.m-1)]


def tests():
    garden = Garden.from_lines(read_lines("day_21_1_test_input.txt"))
    reachable_plots = garden.reachable_plots(6)

    assert len(reachable_plots) == 16
    print(reachable_plots)


def main():
    tests()

    garden = Garden.from_lines(read_lines("day_21_1_input.txt"))
    t = len(garden.reachable_plots(64))
    print(t)
    assert t == 3814


if __name__ == "__main__":
    main()
