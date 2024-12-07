from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import make_blue, pad_with_horizontal_rules

from day23_1 import SnowIsland, DirectedGraph2D, Vector, Adjacency_set2d, Adjacency_weights

from collections import defaultdict, deque


class SnowIslandNoSlopes(SnowIsland):
    encodings = {'.': 0, '#': 1, '>': 0, '^': 0, 'v': 0, '<': 0, 'S': 2, 'E': 3}
    reverse_encodings = {0: '.', 1: '#', 2: 'S', 3: 'E'}

    def _coord_checks(self, coordinate: Vector, potential_neighbours) -> (bool, bool, bool, bool):
        is_not_outside_grid = self._edge_checks(coordinate)
        is_not_forest = (is_not_outside_grid[i] if not is_not_outside_grid[i]
                         else not self.is_forest(potential_neighbours[i])
                         for i in range(4))
        return is_not_forest

    def coloured_squares(self, square_coordinates: set[Vector]) -> None:
        start_position_encoding = self[self.start_position]
        end_position_encoding = self[self.end_position]
        self[self.start_position] = self.encodings['S']
        self[self.end_position] = self.encodings['E']
        representation = '\n'.join(''.join(make_blue('O') if Vector((i, j)) in square_coordinates
                                           else self.reverse_encodings[encoding]
                                           for j, encoding in enumerate(line))
                                   for i, line in enumerate(self.grid))
        self[self.start_position] = start_position_encoding
        self[self.end_position] = end_position_encoding
        representation = pad_with_horizontal_rules(representation, rule_length=self.m)
        return representation

    def neighbours(self, coordinate: Vector) -> set[Vector]:
        # Right, Up, Down, Left
        potential_neighbours = self._potential_neighbours(coordinate)
        coord_checks = self._coord_checks(coordinate, potential_neighbours)
        valid_neighbours = {neighbour
                            for i, (neighbour, is_valid) in enumerate(zip(potential_neighbours, coord_checks))
                            if is_valid}
        return valid_neighbours

    def to_adjacency_set_condensed(self) -> (Adjacency_set2d, Adjacency_weights):
        adjacency_set = defaultdict(set)
        adjacency_weights = defaultdict(lambda: 1)

        start = [self.start_position, self.start_position, 0]

        nodes_to_visit = deque([start])

        visited_nodes = set()

        adjacency_set[self.start_position] = set()  # So it's indexed first
        while nodes_to_visit:
            parent_node, node, distance = nodes_to_visit.popleft()
            visited_nodes.add(node)

            potential_neighbours = self.neighbours(node)
            potential_neighbours -= visited_nodes

            # Divide into 2
            if len(potential_neighbours) >= 2:
                print(f"Split node: {node}")
                adjacency_set[parent_node].add(node)
                adjacency_weights[(parent_node, node)] = distance
                for potential_neighbour in potential_neighbours:
                    nodes_to_visit.append([node, potential_neighbour, 0])

            # Continue path
            if len(potential_neighbours) == 1:
                nodes_to_visit.append([parent_node, list(potential_neighbours)[0], distance + 1])

            # Dead end
            if len(potential_neighbours) == 0:
                print(f"Dead end on node: {node}")
                adjacency_set[parent_node].add(node)
                adjacency_weights[(parent_node, node)] = distance

        print(adjacency_set)
        print(adjacency_weights)
        return adjacency_set, adjacency_weights


def tests():
    snow_island = SnowIslandNoSlopes.from_lines(read_lines("day_23_1_test_input.txt"))
    print(snow_island)

    snow_island_graph = DirectedGraph2D(*snow_island.to_adjacency_set_condensed())
    print(snow_island.coloured_squares({value for values in snow_island_graph.adjacency_set.values() for value in values} | (snow_island_graph.adjacency_set.keys())))
    grid_size = (snow_island.n, snow_island.m)
    start_position = snow_island.guard_position

    t = snow_island_graph.longest_acyclic_path_size(start_position, grid_size)
    print(t)
    assert t == 154


def main():
    tests()


if __name__ == "__main__":
    main()
