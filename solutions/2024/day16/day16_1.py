from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D

from heapq import heappop, heappush

from collections import deque, defaultdict

from typing import Self

from enum import Enum


CameFromDict = dict[Vector2D, tuple[Vector2D, Vector2D]]


class Orientation(Enum):
    VERTICAL = 0
    HORIZONTAL = 1

    def __lt__(self, other: "Orientation") -> bool:
        return self.value < other.value


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

        self.walls = {Vector2D((i, j)) for i in range(self.m) for j in range(self.n) if lines[j][i] == '#'}
        self.start = Vector2D((1, self.n - 2))
        self.start_direction = self.RIGHT
        self.end = Vector2D((self.m - 2, 1))

        self.g_scores = defaultdict(lambda: self.INF)
        self.h_scores = [[-1 if x == '#' else self.end.manhattan_distance(Vector2D((i, j))) for i, x in enumerate(row)] for j, row in enumerate(lines)]

        self.directions = (self.UP, self.RIGHT, self.DOWN, self.LEFT)

    def h(self, coordinate: Vector2D) -> int:
        return self.h_scores[coordinate.y][coordinate.x]

    def print_path(self, path: list[Vector2D]):
        coordinates = set(path)
        grid = [[' ' for _ in range(self.m)] for _ in range(self.n)]
        for j in range(self.m):
            for i in range(self.n):
                x = Vector2D((i, j))
                if x in coordinates:
                    grid[j][i] = '.'
                elif self.is_wall(x):
                    grid[j][i] = '#'
        print('\n'.join(''.join(row) for row in grid))
        return None

    def is_wall(self, coordinate: Vector2D) -> bool:
        return coordinate in self.walls

    def __set_g_score(self, state: tuple[Vector2D, Vector2D], new_value: int) -> None:
        assert not self.is_wall(state[0]), ValueError("cannot change the score of a wall!")
        self.g_scores[state] = new_value
        return None

    def __get_g_score(self, state: tuple[Vector2D, Vector2D]) -> int:
        return self.g_scores[state]

    @property
    def best_path_scores(self) -> (int, int):
        best_previous = {self.start: (Vector2D((-1, -1)), self.start_direction)}
        best_edges = defaultdict(set)

        self.__set_g_score((self.start, self.start_direction), 0)

        to_check = [(State(self.h(self.start), self.start, self.RIGHT))]

        end_states = set()
        best = self.INF

        while to_check:
            state = heappop(to_check)
            node = state.coordinate
            previous_direction = state.direction

            if node == self.end:
                g_score = self.__get_g_score((node, previous_direction))
                end_states.add((node, previous_direction, g_score))
                best = min(best, g_score)
                continue

            for direction in self.directions:
                neighbour = node + direction

                if self.is_wall(neighbour):
                    continue

                cost = 1

                angle_rounded = abs(round(previous_direction.angle_to(direction)))
                if angle_rounded == 180:
                    continue

                elif angle_rounded == 90:
                    cost += 1_000

                tentative_g_score = self.__get_g_score((node, previous_direction)) + cost
                neighbour_g_score = self.__get_g_score((neighbour, direction))

                if tentative_g_score == neighbour_g_score:
                    best_edges[(neighbour, direction)].add((node, previous_direction, tentative_g_score))

                elif tentative_g_score < neighbour_g_score:
                    best_previous[(neighbour, direction)] = (node, previous_direction)

                    self.__set_g_score((neighbour, direction), tentative_g_score)
                    neighbour_h_score = self.h(neighbour)

                    best_edges[(neighbour, direction)] = {(node, previous_direction, tentative_g_score)}

                    heappush(to_check, (State(tentative_g_score + neighbour_h_score, neighbour, direction)))

        return best, self.__best_tiles(best_edges, end_states, best)

    def __best_tiles(self, best_edges, end_states, best_end_score: int) -> set:
        tiles = set()

        to_check = deque([(self.end, end_state[1]) for end_state in end_states if end_state[2] == best_end_score])
        while to_check:
            node, direction = to_check.popleft()
            tiles.add(node)
            for previous in best_edges[(node, direction)]:
                to_check.append((previous[0], previous[1]))

        self.print_path(tiles)
        return len(tiles)


class State:
    def __init__(self, h_score: int, coordinate: Vector2D, direction: Vector2D = None):
        self.h = h_score
        self.coordinate = coordinate
        self.direction = direction

    def __repr__(self) -> str:
        return f"State[{self.h}, {self.coordinate}, D:{self.direction}]"

    def __lt__(self, other: Self) -> bool:
        return self.h < other.h

    def __eq__(self, other: Self) -> bool:
        return self.h == other.h


def tests():
    maze = ReindeerMaze(read_lines("puzzle16_1_test_input1.txt"))

    t1, _ = maze.best_path_scores
    assert t1 == 7036

    maze2 = ReindeerMaze(read_lines("puzzle16_1_test_input2.txt"))

    t2, _ = maze2.best_path_scores
    assert t2 == 11048


def main():
    tests()

    maze = ReindeerMaze(read_lines("puzzle16_1.txt"))

    t1, _ = maze.best_path_scores
    assert t1 == 93436


if __name__ == "__main__":
    main()
