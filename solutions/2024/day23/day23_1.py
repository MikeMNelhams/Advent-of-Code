from handy_dandy_library.file_processing import read_lines

from collections import defaultdict


class LanParty:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.edges = self.__edge_sets(lines)

    @staticmethod
    def __edge_sets(lines: list[str]) -> dict[str, set[str]]:
        edges = defaultdict(set)
        for line in lines:
            a, b = line.split('-')
            edges[a].add(b)
            edges[b].add(a)
        return edges

    @property
    def t_triangle_count(self) -> int:
        triples = set()
        for u, edges in self.edges.items():
            if len(edges) == 1:
                continue

            for v in edges:
                for w in self.edges.keys():
                    if w in self.edges[v] and w in self.edges[u]:
                        triples.add(tuple(sorted((u, v, w))))

        total = 0
        for triple in triples:
            for node in triple:
                if node[0] == 't':
                    total += 1
                    break

        return total


def tests():
    lan_party = LanParty(read_lines("puzzle23_1_test_input1.txt"))
    assert lan_party.t_triangle_count == 7


def main():
    tests()

    lan_party = LanParty(read_lines("puzzle23_1.txt"))
    assert lan_party.t_triangle_count == 1327


if __name__ == "__main__":
    main()
