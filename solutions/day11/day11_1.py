import sys

from handy_dandy_library.file_processing import read_lines
from itertools import combinations


GalaxyCoordinates = list[list[int, int]]


class Cosmos:
    def __init__(self, lines: list[str]):
        self.galaxy_coordinates = self.__galaxy_coordinates(lines)
        self.n = len(lines)
        self.m = len(lines[0])

    def __repr__(self) -> str:
        return f"Galaxies: {self.galaxy_coordinates} | Size: ({self.n}, {self.m})"

    @staticmethod
    def __galaxy_coordinates(lines: list[str]) -> GalaxyCoordinates:
        galaxy = [[i, j] for i, line in enumerate(lines) for j, char in enumerate(line) if char == '#']
        return galaxy

    def empty_row_indices(self) -> list[int]:
        available_rows = set(range(self.n))
        found_rows = {x[0] for x in self.galaxy_coordinates}
        return list(available_rows - found_rows)

    def empty_column_indices(self) -> list[int]:
        available_columns = set(range(self.m))
        found_columns = {x[1] for x in self.galaxy_coordinates}
        return list(available_columns - found_columns)

    def expand(self) -> None:
        empty_rows_indices = sorted(self.empty_row_indices()) + [sys.maxsize]
        empty_column_indices = sorted(self.empty_column_indices()) + [sys.maxsize]
        row_accumulator = 0
        column_accumulator = 0

        self.galaxy_coordinates.sort(key=lambda x: x[0])
        for i, galaxy in enumerate(self.galaxy_coordinates):
            if galaxy[0] > empty_rows_indices[row_accumulator]:
                row_accumulator += 1
            self.galaxy_coordinates[i][0] += row_accumulator

        self.galaxy_coordinates.sort(key=lambda x: x[1])
        for i, galaxy in enumerate(self.galaxy_coordinates):
            if galaxy[1] > empty_column_indices[column_accumulator]:
                column_accumulator += 1
            self.galaxy_coordinates[i][1] += column_accumulator

        self.n += row_accumulator
        self.m += column_accumulator
        return None


def coordinate_distance(coordinate1: list[int, int], coordinate2: list[int, int]) -> int:
    return abs(coordinate1[0] - coordinate2[0]) + abs(coordinate1[1] - coordinate2[1])


def galaxy_brain_sum(lines: list[str]) -> int:
    cosmos = Cosmos(lines)
    cosmos.expand()
    galaxy_coordinates = cosmos.galaxy_coordinates
    total = sum(coordinate_distance(coordinate1, coordinate2)
                for coordinate1, coordinate2 in combinations(galaxy_coordinates, 2))
    return total


def tests():
    # set([[0, 4], [1, 9], [2, 0], [5, 8], [6, 1], [7, 12], [10, 9], [11, 0], [11, 5]])
    assert coordinate_distance([6, 1], [11, 5]) == 9
    assert galaxy_brain_sum(read_lines("day_11_1_test_input.txt")) == 374


def main():
    tests()

    t = galaxy_brain_sum(read_lines("day_11_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
