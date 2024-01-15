from __future__ import annotations
from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import make_blue
from handy_dandy_library.linear_algebra import Vector, polygon_area, integer_border_points_count

from collections import deque


Grid = list[list]


class PipeGrid:
    UP = Vector((0, -1))
    DOWN = Vector((0, 1))
    LEFT = Vector((-1, 0))
    RIGHT = Vector((1, 0))
    PIPE_NEIGHBOURS = {'|': (UP, DOWN), '-': (RIGHT, LEFT),
                       'L': (RIGHT, UP), 'J': (UP, LEFT),
                       '7': (DOWN, LEFT), 'F': (RIGHT, DOWN),
                       'S': (RIGHT, UP, DOWN, LEFT)}
    CARTESIAN_PIPES = {'|', '-'}

    def __init__(self, grid: Grid):
        self.grid = grid
        self.n = len(grid[0])
        self.m = len(grid)
        self._pipes = self._pipe_chars(grid)
        self.starting_coordinate = self._starting_coordinate(grid)

    def __repr__(self) -> str:
        lines = '\n'.join(''.join(char for char in line) for line in self.grid)
        return lines

    def __getitem__(self, item: Vector) -> set[Vector]:
        return self.grid[item.y][item.x]

    def coloured_squares(self, square_coordinates: set[Vector]) -> None:
        representation = '\n'.join(''.join(make_blue(encoding) if Vector((j, i)) in square_coordinates
                                           else encoding
                                           for j, encoding in enumerate(line))
                                   for i, line in enumerate(self.grid))
        return representation

    @staticmethod
    def _pipe_chars(grid: Grid) -> Grid:
        return [[1 if char != '.' else 0 for char in row] for row in grid]

    @staticmethod
    def _starting_coordinate(grid: Grid) -> (int, int):
        n = len(grid)
        m = len(grid[0])
        for j in range(n):
            for i in range(m):
                if grid[j][i] == 'S':
                    return Vector((i, j))
        raise TypeError

    @classmethod
    def from_lines(cls, lines: list[str]):
        return cls(lines)

    def _edge_checks(self, coordinate: Vector) -> (bool, bool, bool, bool):
        return coordinate.x < self.n - 1, coordinate.y > 0, coordinate.y < self.m - 1, coordinate.x > 0

    def _potential_neighbours(self, coordinate: Vector) -> (Vector, Vector, Vector, Vector):
        # R U D L
        return coordinate + self.RIGHT, coordinate + self.UP, coordinate + self.DOWN, coordinate + self.LEFT

    def is_pipe(self, coordinate: Vector) -> bool:
        return self._pipes[coordinate.y][coordinate.x]

    def _surrounding_squares(self, coordinate: Vector) -> set[Vector]:
        # Right, Up, Down, Left
        potential_neighbours = self._potential_neighbours(coordinate)
        coord_checks = self._edge_checks(coordinate)
        valid_neighbours = {neighbour for neighbour, is_valid in zip(potential_neighbours, coord_checks) if is_valid}

        if self.is_pipe(coordinate):
            pipe_neighbours = {coordinate + unit_vector for unit_vector in self.PIPE_NEIGHBOURS[self[coordinate]]}
            valid_neighbours &= pipe_neighbours

        return valid_neighbours

    def neighbours(self, coordinate: Vector) -> set[Vector]:
        valid_neighbours = self._surrounding_squares(coordinate)
        return valid_neighbours

    def s_neighbours(self) -> set[Vector]:
        valid_neighbours = self._surrounding_squares(self.starting_coordinate)
        invalid_neighbours = set()
        for neighbour in tuple(valid_neighbours):
            if self[neighbour] == '.':
                invalid_neighbours.add(neighbour)
            if self.starting_coordinate not in self.neighbours(neighbour):
                invalid_neighbours.add(neighbour)
        valid_neighbours -= invalid_neighbours
        return valid_neighbours

    @property
    def main_loop(self) -> (set[Vector], int):
        pipes_connecting_to_start = self.s_neighbours()
        visited = {self.starting_coordinate}
        coordinates_to_visit = deque([(pipe, 1) for pipe in pipes_connecting_to_start])
        max_distance = 0
        while coordinates_to_visit:
            coordinate, distance = coordinates_to_visit.popleft()
            max_distance = max(max_distance, distance)
            visited.add(coordinate)

            neighbours = self.neighbours(coordinate)
            neighbours -= visited

            for neighbour in neighbours:
                coordinates_to_visit.append((neighbour, distance + 1))
        return visited, max_distance

    @property
    def main_loop_furthest_distance(self) -> int:
        _, max_distance = self.main_loop
        return max_distance

    @property
    def main_loop_shortened_coordinates(self) -> list[Vector]:
        """ Remove all vertical and horizontal pipes """
        pipes_connecting_to_start = self.s_neighbours()
        coordinates_to_visit = [list(pipes_connecting_to_start)[0]]
        previous = self.starting_coordinate
        path = [self.starting_coordinate]

        while coordinates_to_visit:
            coordinate = coordinates_to_visit.pop()
            path.append(coordinate)
            neighbours = self.neighbours(coordinate)
            neighbours -= {self.starting_coordinate, previous}

            previous = coordinate
            for neighbour in neighbours:
                coordinates_to_visit.append(neighbour)

        contracted_path = [coordinate for coordinate in path if self[coordinate] not in self.CARTESIAN_PIPES]
        return contracted_path

    @property
    def area_enclosed(self) -> int:
        main_loop = self.main_loop_shortened_coordinates
        # Using Pick's theorem. Quicker than raytracing, since all points are on the integer grid.
        total_area = polygon_area(main_loop)
        border_points = integer_border_points_count(main_loop)
        interior_points = int(total_area) + 1 - border_points // 2
        return interior_points


def tests():
    pipe_grid = PipeGrid.from_lines(read_lines("day_10_1_test_input1.txt"))
    assert pipe_grid.main_loop_furthest_distance == 4

    pipe_grid2 = PipeGrid.from_lines(read_lines("day_10_1_test_input2.txt"))
    assert pipe_grid2.main_loop_furthest_distance == 4

    pipe_grid3 = PipeGrid.from_lines(read_lines("day_10_1_test_input3.txt"))
    assert pipe_grid3.main_loop_furthest_distance == 8


def main():
    tests()

    pipe_grid = PipeGrid.from_lines(read_lines("day_10_1_input.txt"))
    t = pipe_grid.main_loop_furthest_distance

    assert t == 6613


if __name__ == "__main__":
    main()
