import sys

from handy_dandy_library.file_processing import read_lines
from itertools import combinations


type GalaxyCoordinates = list[list[int, int]]


class Cosmos:
    def __init__(self, lines: list[str]):
        self.galaxy_coordinates = self.__galaxy_coordinates(lines)
        self.n = len(lines)
        self.m = len(lines[0])

    def __repr__(self) -> str:
        return f"Galaxies: {self.galaxy_coordinates} | Size: ({self.n}, {self.m})"

    def get_dimension_length(self, dimension: int) -> int:
        if dimension == 0:
            return self.n
        return self.m

    def set_dimension_length(self, dimension: int, value: int) -> int:
        if dimension == 0:
            self.n = value
            return None
        self.m = value
        return None

    @staticmethod
    def __galaxy_coordinates(lines: list[str]) -> GalaxyCoordinates:
        galaxy = [[i, j] for i, line in enumerate(lines) for j, char in enumerate(line) if char == '#']
        return galaxy

    def _empty_dimension_indices(self, dimension: int) -> list[int]:
        available_rows = set(range(self.get_dimension_length(dimension)))
        found_rows = {x[dimension] for x in self.galaxy_coordinates}
        return list(available_rows - found_rows)

    def _expand_dim(self, dimension: int, expansion_rate: int=1):
        empty_indices = sorted(self._empty_dimension_indices(dimension=dimension)) + [sys.maxsize]
        accumulator = 0
        threshold_index = 0

        self.galaxy_coordinates.sort(key=lambda x: x[dimension])
        for i, galaxy in enumerate(self.galaxy_coordinates):
            if galaxy[dimension] > empty_indices[threshold_index]:
                accumulator += expansion_rate
                threshold_index += 1
            self.galaxy_coordinates[i][dimension] += accumulator

        self.set_dimension_length(dimension, self.get_dimension_length(dimension) + accumulator)
        return None

    def expand(self, expansion_rate=1) -> None:
        for i in range(2):
            self._expand_dim(dimension=i, expansion_rate=expansion_rate)
        return None


def coordinate_distance(coordinate1: list[int, int], coordinate2: list[int, int]) -> int:
    return abs(coordinate1[0] - coordinate2[0]) + abs(coordinate1[1] - coordinate2[1])


def galaxy_brain_sum(lines: list[str], expansion_rate=1) -> int:
    cosmos = Cosmos(lines)
    cosmos.expand(expansion_rate=expansion_rate)
    galaxy_coordinates = cosmos.galaxy_coordinates
    total = sum(coordinate_distance(coordinate1, coordinate2)
                for coordinate1, coordinate2 in combinations(galaxy_coordinates, 2))
    return total


def tests():
    assert coordinate_distance([6, 1], [11, 5]) == 9
    assert galaxy_brain_sum(read_lines("day_11_1_test_input.txt")) == 374


def main():
    tests()

    t = galaxy_brain_sum(read_lines("day_11_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
