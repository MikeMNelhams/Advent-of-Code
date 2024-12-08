from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D

from collections import defaultdict
from itertools import combinations


class AntennaTracker:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.n = len(lines)
        self.m = len(lines)
        self.antennas = self.__antennas_from_lines(lines)

    def __antennas_from_lines(self, lines: list[str]) -> dict[str, Vector2D]:
        antennas = defaultdict(set)
        for i in range(self.n):
            for j in range(self.m):
                char = lines[i][j]
                if char == '.':
                    continue
                antennas[char].add(Vector2D((i, j)))
        return antennas

    def is_within_bounds(self, coordinate: Vector2D) -> bool:
        return (0 <= coordinate.x < self.n) and (0 <= coordinate.y < self.m)

    @property
    def unique_antinodes_count(self) -> int:
        locations = set()

        for _, coordinates in self.antennas.items():
            for a, b in combinations(coordinates, 2):
                displacement = b - a
                antinode0 = a + displacement * 2
                antinode1 = a - displacement
                if self.is_within_bounds(antinode0):
                    locations.add(antinode0)
                if self.is_within_bounds(antinode1):
                    locations.add(antinode1)

        return len(locations)

    @property
    def unique_t_antinodes_count(self) -> int:
        locations = set()

        for _, coordinates in self.antennas.items():
            for a, b in combinations(coordinates, 2):
                displacement: Vector2D = b - a

                y_abs = abs(displacement.y)
                x_abs = abs(displacement.x)

                if y_abs >= x_abs and y_abs % x_abs == 0:
                    displacement //= x_abs

                elif x_abs > y_abs and x_abs % y_abs == 0:
                    displacement //= y_abs

                hit_wall = False
                p = Vector2D((a.x, a.y))
                while not hit_wall:
                    locations.add(p)
                    p -= displacement
                    hit_wall = not self.is_within_bounds(p)

                hit_wall = False
                p = Vector2D((a.x, a.y)) + displacement
                while not hit_wall:
                    locations.add(p)
                    p += displacement
                    hit_wall = not self.is_within_bounds(p)

        return len(locations)


def tests():
    antenna_tracker = AntennaTracker(read_lines("puzzle8_1_test_input1.txt"))

    t1 = antenna_tracker.unique_antinodes_count
    assert t1 == 14


def main():
    tests()

    antenna_tracker = AntennaTracker(read_lines("puzzle8_1.txt"))

    t2 = antenna_tracker.unique_antinodes_count
    assert t2 == 249


if __name__ == "__main__":
    main()
