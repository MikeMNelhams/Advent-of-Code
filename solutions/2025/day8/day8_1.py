from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector3D

from itertools import combinations
from functools import reduce
from heapq import nlargest
import operator


class ElectricJunctionBoxes:
    INF = 10 ** 20

    def __init__(self, puzzle_path: str):
        lines = read_lines(puzzle_path)
        self.junctions = [Vector3D(tuple(map(int, line.split(",")))) for line in lines]
        self.n = len(self.junctions)
        self.distances = self.__sorted_distances(self.junctions)

    @staticmethod
    def __sorted_distances(junctions: list[Vector3D]) -> list[tuple[int, int, int]]:
        n = len(junctions)
        distances = [((junctions[i] - junctions[j]).magnitude_squared, i, j)
                     for i, j in combinations(range(n), 2)]
        distances.sort(key=lambda x: x[0])
        return distances

    def largest_circuits_product(self, connection_limit: int,
                                 top_count: int=3) -> int:
        circuits = [{i} for i in range(self.n)]
        junctions_to_circuits = {i: i for i in range(self.n)}
        for _, i, j in self.distances[:connection_limit]:
            i_circuit_index = junctions_to_circuits[i]
            j_circuit_index = junctions_to_circuits[j]
            if i_circuit_index == j_circuit_index:
                continue
            circuits[i_circuit_index] |= circuits[j_circuit_index]
            for k in circuits[j_circuit_index]:
                junctions_to_circuits[k] = i_circuit_index
            circuits[j_circuit_index].clear()

        top_n = nlargest(top_count, (len(x) for x in circuits))
        return reduce(operator.mul, top_n, 1)

    def final_circuit_connection_x_product(self) -> int:
        circuits = [{i} for i in range(self.n)]
        junctions_to_circuits = {i: i for i in range(self.n)}

        for _, i, j in self.distances:
            i_circuit_index = junctions_to_circuits[i]
            j_circuit_index = junctions_to_circuits[j]
            if i_circuit_index == j_circuit_index:
                continue
            circuits[i_circuit_index] |= circuits[j_circuit_index]
            for k in circuits[j_circuit_index]:
                junctions_to_circuits[k] = i_circuit_index
            circuits[j_circuit_index].clear()
            if len(circuits[junctions_to_circuits[0]]) == self.n:
                return self.junctions[i].x * self.junctions[j].x

        raise ValueError("We electrocuted the elves :(")


def main():
    test_junction_boxes = ElectricJunctionBoxes("puzzle8_1_test_input.txt")
    assert test_junction_boxes.largest_circuits_product(10, 3) == 40

    junction_boxes = ElectricJunctionBoxes("puzzle8_1.txt")
    t = junction_boxes.largest_circuits_product(997, 3)
    print(t)


if __name__ == "__main__":
    main()
