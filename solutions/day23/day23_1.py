from __future__ import annotations
from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import pad_with_horizontal_rules

from collections import deque, defaultdict


type Grid = list[list[int]]
type adjacency_set2d = list[list[set[Vector]]]

INF = 10**20


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

    def __mul__(self, other: int) -> Vector:
        return Vector((self.x * other, self.y * other))

    def __rmul__(self, other: int) -> Vector:
        return self.__mul__(other)

    def __mod__(self, other: int) -> Vector:
        return Vector((self.x % other, self.y % other))

    @classmethod
    def zero(cls):
        return cls((0, 0))


class SnowIsland:
    encodings = {'.': 0, '#': 1, '>': 2, '^': 3, 'v': 4, '<': 5, 'S': 6, 'E': 7}
    reverse_encodings = {0: '.', 1: '#', 2: '>', 3: '^', 4: 'v', 5: '<', 6: 'S', 7: 'E'}
    slope_chars = ('<', 'v', '^', '>')
    UP = Vector((-1, 0))
    RIGHT = Vector((0, 1))
    DOWN = Vector((1, 0))
    LEFT = Vector((0, -1))

    def __init__(self, encoded_grid: list[list[int]], start_position: Vector, end_position: Vector):
        self.grid = encoded_grid
        self.n = len(encoded_grid)
        self.m = len(encoded_grid[0])
        self.start_position = start_position
        self.end_position = end_position

    def __getitem__(self, item: Vector) -> int:
        return self.grid[item.x][item.y]

    def __setitem__(self, key: Vector, value: int) -> None:
        self.grid[key.x][key.y] = value
        return None

    def __repr__(self) -> str:
        start_position_encoding = self[self.start_position]
        end_position_encoding = self[self.end_position]
        self[self.start_position] = 6
        self[self.end_position] = 7
        lines = '\n'.join(''.join(self.reverse_encodings[encoding] for encoding in line) for line in self.grid)
        self[self.start_position] = start_position_encoding
        self[self.end_position] = end_position_encoding
        return pad_with_horizontal_rules(lines)

    @classmethod
    def from_lines(cls, lines: list[str], start_position: Vector, end_position: Vector):
        return cls([[cls.encodings[char] for char in line] for line in lines], start_position, end_position)

    def __edge_checks(self, coordinate: Vector) -> (bool, bool, bool, bool):
        return coordinate.y < self.m - 1, coordinate.x > 0, coordinate.x < self.n - 1, coordinate.y > 0

    def __blocking_slope_checks(self, potential_neighbours, outside_grid_checks):
        is_not_blocking_slope = (edge_check if not edge_check
                                 else self.reverse_encodings[self[potential_neighbours[i]]] != self.slope_chars[i]
                                 for i, edge_check in enumerate(outside_grid_checks))
        return is_not_blocking_slope

    def __potential_neighbours(self, coordinate: Vector) -> (Vector, Vector, Vector, Vector):
        return coordinate + self.RIGHT, coordinate + self.UP, coordinate + self.DOWN, coordinate + self.LEFT

    def __coord_checks(self, coordinate: Vector, potential_neighbours) -> (bool, bool, bool, bool):
        is_not_outside_grid = self.__edge_checks(coordinate)
        is_not_forest = (is_not_outside_grid[i] if not is_not_outside_grid[i]
                         else not self.is_forest(potential_neighbours[i])
                         for i in range(4))
        is_not_blocking_slope = self.__blocking_slope_checks(potential_neighbours, is_not_outside_grid)
        return (all(checks) for checks in zip(is_not_forest, is_not_blocking_slope))

    def is_forest(self, coordinate: Vector) -> bool:
        return self[coordinate] == 1

    def neighbours(self, coordinate: Vector) -> set[Vector]:
        # Right, Up, Down, Left
        potential_neighbours = self.__potential_neighbours(coordinate)
        for i in range(4):
            if self[coordinate] == i + 2:
                return {potential_neighbours[i]}
        coord_checks = self.__coord_checks(coordinate, potential_neighbours)
        valid_neighbours = {neighbour for i, (neighbour, is_valid) in enumerate(zip(potential_neighbours, coord_checks)) if is_valid}
        return valid_neighbours

    def to_adjacency_set(self) -> list[list[set[Vector]]]:
        adjacency_set = [[set() for _ in range(self.m)] for _ in range(self.n)]
        nodes_to_visit = [self.start_position]
        while nodes_to_visit:
            node = nodes_to_visit.pop()
            potential_neighbours = self.neighbours(node)
            for potential_neighbour in potential_neighbours:
                if node not in adjacency_set[potential_neighbour.x][potential_neighbour.y]:
                    adjacency_set[node.x][node.y].add(potential_neighbour)
                    nodes_to_visit.append(potential_neighbour)
        return adjacency_set


class DirectedGraph2D:
    def __init__(self, adjacency_set: adjacency_set2d):
        self.adjacency_set = adjacency_set
        self.n = len(adjacency_set)
        self.m = len(adjacency_set[0])

    def __repr__(self) -> str:
        return str(self.adjacency_set)

    def __getitem__(self, item: Vector) -> set[Vector]:
        return self.adjacency_set[item.x][item.y]

    @property
    def visually_sorted(self) -> list[Vector]:
        # TODO DOESN'T INCLUDE ANY CONNECTED NODES THAT HAVE 0 OUTDEGREE
        return [c for i in range(self.n) for j in range(self.m) if self[(c := Vector((i, j)))]]

    def is_acyclic(self, known_source: Vector) -> bool:
        return not self.is_cyclic(known_source)

    def is_cyclic(self, known_source: Vector) -> bool:
        visited = defaultdict(lambda: False)
        on_stack = defaultdict(lambda: False)
        stack = [known_source]

        while stack:
            node = stack[-1]

            if not visited[node]:
                visited[node] = True
                on_stack[node] = True
            else:
                on_stack[node] = False
                stack.pop()

            for neighbour in self[node]:
                if not visited[neighbour]:
                    stack.append(neighbour)
                elif on_stack[neighbour]:
                    return True

        return False

    def longest_hamiltonian_path(self, start_position: Vector) -> list[Vector]:
        assert self.is_acyclic(start_position)
        topological_sort = self.visually_sorted
        distances = {node: -INF for node in topological_sort}
        distances[topological_sort[0]] = 0
        print(distances.keys())
        for i, node in enumerate(topological_sort):
            successors = self[node]
            for successor in successors:
                distances[successor] = max(distances[successor], distances[node] + 1)
        return max(reversed(distances.values()))


def tests():
    start_position = Vector((0, 1))
    end_position = Vector((22, 21))
    snow_island = SnowIsland.from_lines(read_lines("day_23_1_test_input.txt"), start_position, end_position)
    print(snow_island)
    assert snow_island.neighbours(start_position) == {start_position + snow_island.DOWN}
    assert snow_island.neighbours(end_position) == {end_position + snow_island.UP}
    x1 = Vector((9, 20))
    x2 = x1 + snow_island.RIGHT + snow_island.DOWN
    assert snow_island.neighbours(x1) == {x1 + snow_island.LEFT, x1 + snow_island.RIGHT}
    assert snow_island.neighbours(x1 + snow_island.RIGHT) == {x1, x2}
    assert snow_island.neighbours(x2) == {x2 + snow_island.DOWN}
    assert snow_island.neighbours(x2 + snow_island.DOWN) == {x2 + 2 * snow_island.DOWN}
    snow_island_graph = DirectedGraph2D(snow_island.to_adjacency_set())

    print(snow_island_graph.visually_sorted)
    print(f"Is the graph acyclic?: {snow_island_graph.is_acyclic(start_position)}")

    print(snow_island_graph.longest_hamiltonian_path(start_position))

    # TODO visual topological sort is wrong.



def main():
    tests()


if __name__ == "__main__":
    main()
