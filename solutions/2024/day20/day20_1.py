from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D
from handy_dandy_library.string_manipulations import make_blue

from collections import defaultdict
from heapq import heappush, heappop

from typing import Self


class State:
    def __init__(self, f_score: int, coordinate: Vector2D, cut_count: int):
        self.f = f_score
        self.node = coordinate
        self.cut_count = cut_count

    def __lt__(self, other: Self) -> bool:
        return self.f < other.f

    def __le__(self, other: Self) -> bool:
        return self.f <= other.f


class Racetrack:
    INF = 10 ** 10
    UP = Vector2D((0, -1))
    DOWN = Vector2D((0, 1))
    LEFT = Vector2D((-1, 0))
    RIGHT = Vector2D((1, 0))

    directions = (UP, RIGHT, DOWN, LEFT)

    def __init__(self, lines: list[str]):
        self.lines = lines

        self.n = len(self.lines)
        self.m = len(self.lines[0])

        self.start, self.end, self.walls = self.__parse_lines(lines)

        self.__walls_list = list(self.walls)

        self.h = {Vector2D((i, j)): self.end.manhattan_distance(Vector2D((i, j)))
                  for j in range(self.n)
                  for i in range(self.m)}

    def is_wall(self, coordinate: Vector2D) -> bool:
        return coordinate in self.walls

    def is_within_grid(self, coordinate: Vector2D) -> bool:
        return 0 <= coordinate.x < self.m and 0 <= coordinate.y < self.n

    def reconstruct_path(self, best_previous: dict[Vector2D, Vector2D], coordinate: Vector2D) -> list[Vector2D]:
        total_path = [coordinate]
        current = coordinate
        while current in best_previous and current != self.start:
            current = best_previous[current]
            total_path.append(current)
        total_path.reverse()
        return total_path

    def print_path(self, path: list[Vector2D]) -> None:
        grid = [[' ' for _ in range(self.m)] for _ in range(self.n)]

        for wall in self.__walls_list:
            grid[wall.y][wall.x] = '#'

        c = 1
        for coordinate in path:
            if self.is_wall(coordinate):
                grid[coordinate.y][coordinate.x] = str(c)
                c += 1
            else:
                grid[coordinate.y][coordinate.x] = make_blue('•')

        grid[self.end.y][self.end.x] = make_blue('E')

        print('\n'.join(''.join(row) for row in grid))
        return None

    def shortest_path(self) -> int:
        g_scores = defaultdict(lambda: self.INF)
        best_previous = {self.start: None}

        g_scores[self.start] = 0
        to_check = [State(self.h[self.start], self.start, -1)]

        while to_check:
            state = heappop(to_check)

            if state.node == self.end:
                path_back = self.reconstruct_path(best_previous, self.end)
                self.print_path(path_back)
                return state.f

            neighbours = [(neighbour, self.is_wall(neighbour)) for direction in self.directions
                          if self.is_within_grid((neighbour := state.node + direction))
                          and not self.is_wall(neighbour)]

            tentative_g_score = g_scores[state.node] + 1
            for (neighbour, is_wall) in neighbours:
                if tentative_g_score >= g_scores[neighbour]:
                    continue

                best_previous[neighbour] = state.node
                g_scores[neighbour] = tentative_g_score
                f_score = tentative_g_score + self.h[neighbour]

                heappush(to_check, State(f_score, neighbour, -1))

        return -1

    def shortest_two_consecutive_cut_path(self) -> int:
        # Dijkstra without the 2-cut is (V+E)log(V)
        # State: (f_score, node, cut_count)
        # If cut_count is 0, consider the surrounding neighbours
        #   that are also walls, but they set cut count = 1
        # If cut_count is 1, consider the surrounding neighbours
        #   all neighbours set cut count = 2
        # If cut_count is 2, it's regular a* algo, blocked by walls

        # Can be hugely optimised by excluding walls that are
        #   directly pointing to the outside of the map with
        #       no non-walls between them

        g_scores = defaultdict(lambda: self.INF)
        best_previous = {self.start: None}

        g_scores[self.start] = 0
        ends = []

        to_check = [State(self.h[self.start], self.start, 0)]

        while to_check:
            state = heappop(to_check)

            if state.node == self.end:
                ends.append(state)
                continue

            neighbours = [(neighbour, self.is_wall(neighbour)) for direction in self.directions
                          if (neighbour := state.node + direction)
                          and self.is_within_grid(neighbour)]

            if state.cut_count == 2:
                neighbours = [neighbour for neighbour in neighbours if not neighbour[1]]

            tentative_g_score = g_scores[state.node] + 1
            for (neighbour, is_wall) in neighbours:
                if tentative_g_score >= g_scores[neighbour]:
                    continue

                if state.cut_count == 2 and is_wall:
                    continue

                best_previous[neighbour] = state.node
                g_scores[neighbour] = tentative_g_score
                f_score = tentative_g_score + self.h[neighbour]

                neighbour_cut_count = state.cut_count
                if state.cut_count == 1:
                    neighbour_cut_count = 2
                elif is_wall:
                    neighbour_cut_count += 1

                heappush(to_check, State(f_score, neighbour, neighbour_cut_count))

        best_end_state = min(ends)
        path_back = self.reconstruct_path(best_previous, self.end)
        self.print_path(path_back)
        return best_end_state.f

    def maximum_time_saved(self) -> int:
        biggest = self.shortest_path()
        print('-' * 50)
        smallest = self.shortest_two_consecutive_cut_path()
        print(f"small, big: ({smallest}, {biggest})")
        return biggest - smallest

    @staticmethod
    def __parse_lines(lines: list[str]) -> (Vector2D, Vector2D, set[Vector2D]):
        start = Vector2D((-1, -1))
        end = Vector2D((-1, -1))
        walls = set()

        width = len(lines[0])

        for j in range(len(lines)):
            for i in range(width):
                char = lines[j][i]
                if char == 'S':
                    start = Vector2D((i, j))
                elif char == 'E':
                    end = Vector2D((i, j))
                elif char == '#':
                    walls.add(Vector2D((i, j)))

        return start, end, walls


def tests():
    racetrack = Racetrack(read_lines("puzzle20_1_test_input1.txt"))

    t1 = racetrack.maximum_time_saved()
    print(t1)
    assert t1 == 64


def main():
    tests()


if __name__ == "__main__":
    main()
