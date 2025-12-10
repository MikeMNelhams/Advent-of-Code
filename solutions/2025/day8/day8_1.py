from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector3D

from itertools import combinations
from functools import reduce
import operator


class ElectricJunctionBoxes:
    INF = 10 ** 20

    def __init__(self, puzzle_path: str):
        lines = read_lines(puzzle_path)
        self.junctions = [Vector3D(tuple(map(int, line.split(",")))) for line in lines]
        self.n = len(self.junctions)

    def largest_circuits_product(self, connection_limit: int,
                                 top_count: int=3) -> int:
        distances = []
        n = len(self.junctions)
        for i, j in combinations(range(n), 2):
            x0 = self.junctions[i]
            x1 = self.junctions[j]
            if i == j:
                continue
            d = (x1 - x0).magnitude_squared
            distances.append((d, i, j))

        distances.sort(key=lambda x: x[0])

        circuits = [{i} for i in range(n)]
        junctions_to_circuits = {i: i for i in range(n)}
        for _, i, j in distances[:connection_limit]:
            i_circuit_index = junctions_to_circuits[i]
            j_circuit_index = junctions_to_circuits[j]
            if i_circuit_index == j_circuit_index:
                continue
            circuits[i_circuit_index] |= circuits[j_circuit_index]
            for k in circuits[j_circuit_index]:
                junctions_to_circuits[k] = i_circuit_index
            circuits[j_circuit_index].clear()

        w = sorted((len(x) for x in circuits), reverse=True)[:top_count]
        return reduce(operator.mul, w, 1)


def main():
    test_junction_boxes = ElectricJunctionBoxes("puzzle8_1_test_input.txt")
    assert test_junction_boxes.largest_circuits_product(10, 3) == 40

    junction_boxes = ElectricJunctionBoxes("puzzle8_1.txt")
    t = junction_boxes.largest_circuits_product(997, 3)

    assert t == 330786
    print(t)


if __name__ == "__main__":
    main()
