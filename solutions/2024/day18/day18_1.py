from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D

from typing import Self
from heapq import heappop, heappush
from collections import defaultdict

CameFromDict = dict[Vector2D, Vector2D]


class FallingByteGrid:
    UP = Vector2D((0, -1))
    RIGHT = Vector2D((1, 0))
    DOWN = Vector2D((0, 1))
    LEFT = Vector2D((-1, 0))

    INF = 10 ** 10

    directions = (UP, RIGHT, DOWN, LEFT)

    def __init__(self, lines: list[str], width: int, height: int):
        self.n = len(lines)
        self.width = width
        self.height = height
        self.fallen_bytes = self.__fallen_bytes(lines)
        self.fallen_bytes_set = set()

        self.start = Vector2D((0, 0))
        self.end = Vector2D((self.width - 1, self.height - 1))

        self.g_scores = defaultdict(lambda: self.INF)
        self.h_scores = {Vector2D((i, j)): self.end.manhattan_distance(Vector2D((i, j))) for j in range(self.width) for i in range(self.height)}

    def print_path(self, path: list[Vector2D], fallen_bytes: set[Vector2D]) -> None:
        grid = [['.' for _ in range(self.height)] for _ in range(self.width)]

        for fallen_byte in fallen_bytes:
            grid[fallen_byte.y][fallen_byte.x] = '#'

        for coordinate in path:
            grid[coordinate.y][coordinate.x] = 'o'

        print('\n'.join(''.join(row) for row in grid))
        return None

    @staticmethod
    def __fallen_bytes(lines: list[str]) -> list[Vector2D]:
        falling_bytes = [[int(x) for x in line.split(',')] for line in lines]
        return [Vector2D((x[0], x[1])) for x in falling_bytes]

    def minimum_steps(self, number_of_bytes: int) -> int:
        if number_of_bytes == 0:
            return self.width + self.height
        self.g_scores = defaultdict(lambda: self.INF)
        self.fallen_bytes_set = set()

        for coordinate in self.fallen_bytes[:number_of_bytes]:
            self.fallen_bytes_set.add(coordinate)
            self.g_scores[coordinate] = -1
            self.h_scores[coordinate] = -1

        best_previous: CameFromDict = {self.start: (Vector2D((-1, -1)))}

        self.__set_g_score(self.start, 0)

        to_check = [State(self.h(self.start), self.start)]

        while to_check:
            state = heappop(to_check)

            node = state.coordinate
            f_score = state.f

            if node == self.end:
                # path_back = self.reconstruct_path(best_previous, self.end)
                # self.print_path(path_back, set(self.fallen_bytes[:number_of_bytes]))

                return f_score

            neighbours = [neighbour for direction in self.directions
                          if (neighbour := node + direction) not in self.fallen_bytes_set and self.is_within_grid(neighbour)]

            tentative_g_score = self.__get_g_score(node) + 1

            for neighbour in neighbours:
                if tentative_g_score < self.__get_g_score(neighbour):
                    best_previous[neighbour] = node
                    self.__set_g_score(neighbour, tentative_g_score)
                    f_score = tentative_g_score + self.h(neighbour)

                    heappush(to_check, State(f_score, neighbour))
        return -1

    def binary_search_failure_byte(self) -> (int, Vector2D):
        left = 0
        right = len(self.fallen_bytes) - 1
        middle = (left + right) // 2
        while left < right:
            middle = (left + right) // 2
            middle_passes = self.minimum_steps(middle) != -1

            if middle_passes:
                left = middle + 1
            else:
                right = middle

        return middle, self.fallen_bytes[middle]

    @staticmethod
    def reconstruct_path(best_previous: CameFromDict, coordinate: Vector2D) -> list[Vector2D]:
        total_path = [coordinate]
        current = coordinate
        while current in best_previous:
            current = best_previous[current]
            total_path.append(current)
        total_path.reverse()
        return total_path

    def is_within_grid(self, coordinate: Vector2D) -> bool:
        return (0 <= coordinate.x < self.width) and (0 <= coordinate.y < self.height)

    def is_fallen_byte(self, coordinate: Vector2D) -> bool:
        return

    def __get_g_score(self, coordinate: Vector2D) -> int:
        return self.g_scores[coordinate]

    def __set_g_score(self, coordinate: Vector2D, g_score: int) -> None:
        assert coordinate not in self.fallen_bytes_set, ValueError("cannot change the score of a wall!")

        self.g_scores[coordinate] = g_score
        return None

    def h(self, coordinate: Vector2D) -> int:
        return self.h_scores[coordinate]


class State:
    def __init__(self, f_score: int, coordinate: Vector2D):
        self.f = f_score
        self.coordinate = coordinate

    def __repr__(self) -> str:
        return f"State[{self.f}, {self.coordinate}]"

    def __lt__(self, other: Self) -> bool:
        return self.f < other.f

    def __eq__(self, other: Self) -> bool:
        return self.f == other.f


def tests():
    fallen_byte_grid = FallingByteGrid(read_lines("puzzle18_1_test_input1.txt"), 7, 7)

    t1 = fallen_byte_grid.minimum_steps(12)
    assert t1 == 22


def main():
    tests()

    fallen_byte_grid = FallingByteGrid(read_lines("puzzle18_1.txt"), 71, 71)

    t1 = fallen_byte_grid.minimum_steps(1024)
    assert t1 == 292


if __name__ == "__main__":
    main()
