import time

from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D

from heapq import heappop, heappush

from typing import Self


CameFromDict = dict[Vector2D, tuple[Vector2D, Vector2D]]


class ReindeerMaze:
    UP = Vector2D((0, -1))
    RIGHT = Vector2D((1, 0))
    DOWN = Vector2D((0, 1))
    LEFT = Vector2D((-1, 0))

    INF = 10 ** 10

    def __init__(self, lines: list[str]):
        self.lines = lines
        self.m = len(lines[0])
        self.n = len(lines)

        self.start = Vector2D((1, self.n - 2))
        self.start_direction = self.RIGHT
        self.end = Vector2D((self.m - 2, 1))

        self.g_scores = [[-1 if x == '#' else self.INF for x in row] for row in lines]
        self.f_scores = [[-1 if x == '#' else self.INF for x in row] for row in lines]
        self.h_scores = [[-1 if x == '#' else self.end.manhattan_distance(Vector2D((i, j))) for i, x in enumerate(row)] for j, row in enumerate(lines)]

        self.directions = (self.UP, self.RIGHT, self.DOWN, self.LEFT)

    def minimum_path_cost(self) -> int:
        best_previous: CameFromDict = {self.start: (Vector2D((-1, -1)), self.start_direction)}

        self.__set_g_score(self.start, best_previous)
        self.__set_f_score(self.start, 0)

        to_check = [State(self.h(self.start), self.start)]
        to_check_set = {self.start}

        while to_check:
            state = heappop(to_check)
            to_check_set.remove(state.coordinate)
            current_coordinate = state.coordinate
            if current_coordinate == self.end:
                # path_back = self.reconstruct_path(best_previous, self.end)
                # self.print_path(path_back)

                previous_coordinate, _ = best_previous[current_coordinate]
                return self.__get_f_score(self.end) + 1

            neighbours = [neighbour for direction in self.directions if not self.is_wall(neighbour := current_coordinate + direction)]

            for neighbour in neighbours:
                tentative_g_score = self.__get_g_score(current_coordinate)
                if tentative_g_score < self.__get_g_score(neighbour):
                    current_direction = neighbour - current_coordinate
                    best_previous[neighbour] = (current_coordinate, current_direction)
                    self.__set_g_score(neighbour, best_previous)
                    neighbour_h_score = self.h(neighbour)
                    self.__set_f_score(neighbour, tentative_g_score + neighbour_h_score)

                    if neighbour not in to_check_set:
                        heappush(to_check, State(tentative_g_score + neighbour_h_score, neighbour))
                        to_check_set.add(neighbour)

        return -1

    def h(self, coordinate: Vector2D) -> int:
        return self.h_scores[coordinate.y][coordinate.x]

    @staticmethod
    def reconstruct_path(best_previous: CameFromDict, coordinate: Vector2D) -> list[Vector2D]:
        total_path = [coordinate]
        current = coordinate
        while current in best_previous:
            current = best_previous[current][0]
            total_path.append(current)
        total_path.reverse()
        return total_path

    def print_path(self, path: list[Vector2D]):
        coordinates = set(path)
        grid = [['.' for _ in range(self.m)] for _ in range(self.n)]
        for j in range(self.m):
            for i in range(self.n):
                x = Vector2D((i, j))
                if x in coordinates:
                    grid[j][i] = 'x'
                elif self.is_wall(x):
                    grid[j][i] = '#'
        print('\n'.join(''.join(row) for row in grid))
        return None

    def is_wall(self, coordinate: Vector2D) -> bool:
        return self.__get_g_score(coordinate) == -1

    def __set_f_score(self, coordinate: Vector2D, new_score: int) -> None:
        assert not self.is_wall(coordinate), ValueError("cannot change the score of a wall!")
        self.f_scores[coordinate.y][coordinate.x] = new_score
        return None

    def __get_f_score(self, coordinate: Vector2D) -> int:
        return self.f_scores[coordinate.y][coordinate.x]

    def __set_g_score(self, coordinate: Vector2D, best_previous: CameFromDict) -> None:
        assert not self.is_wall(coordinate), ValueError("cannot change the score of a wall!")
        if coordinate == self.start:
            self.g_scores[coordinate.y][coordinate.x] = 0
            return None

        previous_coordinate, current_direction = best_previous[coordinate]
        _, previous_direction = best_previous[previous_coordinate]

        angle_rounded = abs(round(previous_direction.angle_to(current_direction)))
        previous_g_score = self.__get_g_score(previous_coordinate)

        if angle_rounded == 90:
            self.g_scores[coordinate.y][coordinate.x] = previous_g_score + 1_001
            return None
        elif angle_rounded == 180:
            self.g_scores[coordinate.y][coordinate.x] = previous_g_score + 2_001
            return None
        self.g_scores[coordinate.y][coordinate.x] = previous_g_score + 1
        return None

    def __get_g_score(self, coordinate: Vector2D) -> int:
        return self.g_scores[coordinate.y][coordinate.x]


class State:
    def __init__(self, h_score: int, coordinate: Vector2D):
        self.h = h_score
        self.coordinate = coordinate

    def __repr__(self) -> str:
        return f"State[{self.h}, {self.coordinate}]"

    def __lt__(self, other: Self) -> bool:
        return self.h < other.h

    def __eq__(self, other: Self) -> bool:
        return self.h == other.h


def tests():
    maze = ReindeerMaze(read_lines("puzzle16_1_test_input1.txt"))

    t1 = maze.minimum_path_cost()
    assert t1 == 7036

    maze2 = ReindeerMaze(read_lines("puzzle16_1_test_input2.txt"))

    t2 = maze2.minimum_path_cost()
    assert t2 == 11048


def main():
    tests()

    maze = ReindeerMaze(read_lines("puzzle16_1.txt"))

    t1 = maze.minimum_path_cost()
    assert t1 == 93436


if __name__ == "__main__":
    main()
