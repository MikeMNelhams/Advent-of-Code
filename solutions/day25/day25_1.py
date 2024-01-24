from __future__ import annotations
from handy_dandy_library.file_processing import read_lines

from collections import defaultdict
from itertools import pairwise
from heapq import heappop, heappush


type Adjacency_set2d = dict[str, set[str]]


def graph_edge_code(lines: list[str]) -> None:
    for line in lines:
        phrase_halves = line.split(": ")
        key = phrase_halves[0]
        values = phrase_halves[1].split(' ')
        for value in values:
            print(f"{key} -- {value};")
    return None


class Node:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent


class DirectedGraph2D:
    def __init__(self, adjacency_set: Adjacency_set2d):
        self.adjacency_set = adjacency_set
        self.dfs_counter = 1

    def __repr__(self) -> str:
        return f"{self.adjacency_set}"

    def __len__(self) -> int:
        return len(self.adjacency_set)

    @classmethod
    def from_lines(cls, lines: list[str]):
        adjacency_set = defaultdict(set)

        for line in lines:
            phrase_halves = line.split(": ")
            key = phrase_halves[0]
            values = phrase_halves[1].split(' ')
            for value in values:
                adjacency_set[key].add(value)
                adjacency_set[value].add(key)
        return cls(dict(adjacency_set))

    def minimal_cuts_3_edge_connected_graph(self) -> set[tuple[str, str]]:
        # I cannot get this algorithm to work:
        # I cannot find any implementation of this algorithm.
        # In theory, the maths is correct, but it's too hard
        # The paper:
        # https://pdf.sciencedirectassets.com/272975/1-s2.0-S1570866709X0002X/1-s2.0-S1570866708000415/main.pdf?
        # X-Amz-Security-Token=IQoJb3JpZ2luX2VjEC4aCXVzLWVhc3QtMSJGMEQCIHGrSI064yyL4f%2FRfKVNZ7qxpvg3m4vdNeJ0OSM9Wrz%
        # 2FAiBNBx0Ay2O2c7AU9QdT5qpgFK7GTX2ABJAYhVguaxK5kCq7BQjX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAUaDDA1OTAwMzU0Njg2NS
        # IMEdXKEJn5%2Fg55joszKo8F1XeOhNTgW5zL%2Fx0uOpYTzaFLRn%2BK5PwYnIkBxIzwFjJm48Lv3R%2Bp1urYm0Z7aOJxNqEmrPM8zxexSo
        # MQgEnGiBSqT0Vy4iR9Csn6WvqRTqkk4hrmpCTxg%2FZtUFMpH1BfbVz5IrdQVDlA4pknOgcdaSuZfrA3fJ8DCAgty1mfLHkAPUo%2BW0eh8Wh
        # YcvXdBzlKVuQYhiYhXKnqxapCshoR2Ybw5C%2FM%2BGNHfHh9zozC46l2WqMzuAKx50cuyPYiBkEoaMB7n5PawQr94ibWvKl7JUgCz5biFzx3
        # VK4p6XdPWn0rjv6fj4oharKxXuEnQQ2XBeKX39qBdPCvN1o2lXvZA8o8raw0V7770Rq4vow%2FxvkcfZTpmHnBUBrCZcXyzqD%2B6eIkOQ%2F
        # 9OcpOwg60T7uAP%2B82MB%2FLI1zz4UKqbM3CbhTwmnY4MmtW1W6lm%2F4v4DOwSI%2Ba%2FQs4MuTk8iwo%2F5s4ZFTjuD1jSX3R0HGLhjT1
        # FYxQXbFWQc32hIoRqcBZGXWcY%2BNdF69eZ543F%2FdYIJqL1t%2FhAFOpZ1u7cv0vU09h6bHVxYOkG6G5weEnBcj1C2iFfrYMgx4zF4SgULX
        # 0FqhiqDvMWHcZrgfrqo37Nq4tvWiKRt89c%2FHDcOs3emeK08zlAUt%2BTJgT2XnE58mEPk0rd%2FI0Wha%2F2OY52vPGbWu9MaQoPD%2F96J
        # GvtKkosN%2Frf%2BnW8F14CpklyfgwfI5IeR6ariLwtLMUB11%2BUoI8oidTOrhXuv%2BJTE%2F9ccnEaNzhZ76xDZgJAZeZsRQXYVhat3YND
        # B4kPDQQ0Jd4BgIjcKuBgSxu94zInryOgluc38nMnSjZg1w9Fa1SCdM18mVSLDhrqbG81A%2B271152OkEN3xtbDDa26StBjqyATyYXtfxWe9h
        # yRtbEvJBPjDROvdXJM%2FXtV3DS5EK2S82t5fjBbywaxJhSmf5WcPwvPvs21GA94ro8Kcn%2Fe4piH8BczgwSXU6zVet3r2xPGxI971RK9tTB
        # GTgu%2B5F1vy2MzdDhIUGKFiJF9z%2FY1Ikv5VjTUbxJzb8dsgFRXKoDpU3se1r7VRwRxy38EBpifNeRpro0RjJl4WZl54VqYQjdfljsDAvCa
        # 3qNVsc0XVji0ue7fo%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240118T145537Z&X-Amz-SignedHeaders=host&X-
        # Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTY3HCZSO2K%2F20240118%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-
        # Signature=0c66b6737154cf98b51f8f47a948e197f5db08f3fa2c0fcd92802e33a9e3e8ce&hash=431e9707f3adca0d444982db9bb2d
        # 6b0d1b4f5b301a47a101cf10b2a1ce88490&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii
        # =S1570866708000415&tid=spdf-424f75a8-9a6e-4d5f-a1aa-85e1e32a1298&sid=40a930c14555f44e8f49d3d7873a4a72110egxrq
        # b&type=client&tsoh=d3d3LnNjaWVuY2VkaXJlY3QuY29t&ua=1d025a56515005045152&rr=8477ae135e10531a&cc=gb
        G = self.adjacency_set
        visited = set()

        V = list(G.keys())

        dfs = {V[0]: 1}

        stack = {v: [] for v in V}

        to_low = {}

        cut_edges = set()

        nd = {}
        low_point = {}
        second_low_point = {}
        low = {}
        second_low = {}
        tree_edges = defaultdict(set)
        pre = {v: 0 for v in V}
        post = {v: 0 for v in V}

        def is_ancestor(a, b):
            return pre[a] < pre[b] and post[a] > post[b]

        def is_descendant(a, b):
            return is_ancestor(b, a)

        def find_cut_pairs(v):
            visited.add(v)

            pre[v] = self.dfs_counter
            dfs[v] = self.dfs_counter
            self.dfs_counter += 1

            nd[v] = 1

            low_point[v] = dfs[v]
            low[v] = v

            second_low_point[v] = dfs[v]
            second_low[v] = v

            for w in G[v]:
                tree_edges[v].add(w)
                if w not in visited:
                    find_cut_pairs(w)
                    if stack[w] and w == stack[w][-1][1][1]:
                        (x, y), (p, _) = stack[w].pop()
                        cut_edges.add((x, y))
                        cut_edges.add((v, w))
                        if len(cut_edges) == 3:
                            return cut_edges

                        if v != p:
                            stack[w].append([(x, y), (p, v)])
                    nd[v] += nd[w]
                    if low_point[w] < low_point[v]:
                        second_low_point[v] = low_point[v]
                        low_point[v] = low_point[w]

                        second_low[v] = low[v]
                        low[v] = low[w]

                        stack[v] = stack[w]
                        to_low[v] = w
                    elif low_point[w] < second_low_point[v]:
                        second_low_point[v] = low_point[w]
                        second_low[v] = low[w]
                        stack[w] = []
                elif v not in G[w]:
                    if dfs[w] <= low_point[v]:
                        second_low_point[w] = low_point[v]
                        low_point[v] = dfs[w]
                        second_low[v] = low[v]
                        low[v] = w
                        stack[v] = []
                        to_low[v] = w
                    elif dfs[w] < second_low_point[v]:
                        second_low_point[v] = dfs[w]
                        second_low[v] = w

            if not stack[v]:
                if second_low_point[v] > low_point[v]:
                    stack[v].append([(v, to_low[v]), (low[v], second_low[v])])
            elif second_low_point[v] > dfs[stack[v][-1][1][1]]:
                q = stack[v][-1][1][1]
                stack[v].append([(v, to_low[v]), [q, second_low[v]]])
            else:
                while stack[v] and second_low_point[v] <= dfs[stack[v][-1][1][0]]:
                    stack[v].pop()
                    if stack[v] and second_low_point[v] < dfs[stack[v][-1][1][1]]:
                        (x, y), (p, _) = stack[v].pop()
                        stack[v].append([(x, y), (p, second_low[v])])

            post[v] = self.dfs_counter

            for u in G[v]:
                if v not in tree_edges[u]:
                    while stack[v] and stack[v][-1][0][1] in tree_edges[stack[v][-1][0][0]] and is_descendant(u, stack[v][-1][0][1]):
                        stack[v].pop()

            return cut_edges

        e_cut = find_cut_pairs(V[0])
        print(e_cut)
        return e_cut

    def minimal_cuts_3_brute_force_disjoint_product(self) -> int:
        G = self.adjacency_set
        G_len = len(G)
        # Thanks to reddit for the set-masking optimisation ^^

        def bfs(start, exclusions={}):
            visited = {start: (0, [start])}
            heap = [(0, start, [start])]
            while len(heap) > 0:
                dist, node, path = heappop(heap)
                for de in G[node]:
                    if (node, de) in exclusions:
                        continue
                    if de not in visited:
                        visited[de] = (dist + 1, path + [de])
                        heappush(heap, (dist + 1, de, path + [de]))
            return len(visited), visited, node

        start = next(k for k in G)
        _, visited, stop = bfs(start)
        for x1, y1 in pairwise(visited[stop][1]):
            exclusions = {(x1, y1), (y1, x1)}
            _, visited2, _ = bfs(start, exclusions)
            for x2, y2 in pairwise(visited2[stop][1]):
                exclusions = {(x1, y1), (y1, x1), (x2, y2), (y2, x2)}
                _, visited3, _ = bfs(start, exclusions)
                for x3, y3 in pairwise(visited3[stop][1]):
                    exclusions = {(x1, y1), (y1, x1), (x2, y2), (y2, x2), (x3, y3), (y3, x3)}
                    lena, _, _ = bfs(start, exclusions)
                    if G_len != lena:
                        return lena * (G_len - lena)


def tests():
    directed_graph = DirectedGraph2D.from_lines(read_lines("day_25_1_test_input1.txt"))
    edge_cut_product = directed_graph.minimal_cuts_3_brute_force_disjoint_product()
    assert edge_cut_product == 54


def main():
    tests()

    directed_graph = DirectedGraph2D.from_lines(read_lines("day_25_1_input.txt"))
    edge_cut_product = directed_graph.minimal_cuts_3_brute_force_disjoint_product()
    print(edge_cut_product)


if __name__ == "__main__":
    main()
