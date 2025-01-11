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
    def _three_cliques(self) -> set[tuple]:
        triples = set()
        for u, edges in self.edges.items():
            if len(edges) == 1:
                continue

            for v in edges:
                for w in self.edges.keys():
                    if w in self.edges[v] and w in self.edges[u]:
                        triples.add(tuple(sorted((u, v, w))))
        return triples

    @property
    def t_triangle_count(self) -> int:
        triples = self._three_cliques

        total = 0
        for triple in triples:
            for node in triple:
                if node[0] == 't':
                    total += 1
                    break

        return total

    @property
    def lan_password(self) -> str:
        # Find the max clique.
        # Brute force the list of 4 cliques, repeat until not possible to expand.
        # Use the 3 cliques, get the list of all vertices involved in 3 cliques.
        triples = self._three_cliques
        cliques = set()

        for triple in triples:
            for node in triple:
                if node[0] == 't':
                    cliques.add(triple)
                    break

        is_possible = True
        i = 4
        while is_possible:
            print(f"Attempting to form clique of size: {i}")
            is_possible, cliques = self._attempt_increase_clique_size(cliques)
            i += 1

        return ','.join(cliques.pop())

    def _attempt_increase_clique_size(self, cliques: set[tuple]) -> (bool, set[tuple]):
        possible_vertices = {u for clique in cliques for u in clique}

        cliques_bigger = set()
        for clique in cliques:
            clique_set = set(clique)
            remaining_vertices = possible_vertices - clique_set

            for v in remaining_vertices:
                if all(v in self.edges[u] for u in clique):
                    cliques_bigger.add(tuple(sorted(clique_set | {v})))

        is_possible = len(cliques_bigger) != 0

        if is_possible:
            return True, cliques_bigger

        return False, cliques


def tests():
    lan_party = LanParty(read_lines("puzzle23_1_test_input1.txt"))
    assert lan_party.t_triangle_count == 7


def main():
    tests()

    lan_party = LanParty(read_lines("puzzle23_1.txt"))
    assert lan_party.t_triangle_count == 1327


if __name__ == "__main__":
    main()
