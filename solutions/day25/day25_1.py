from __future__ import annotations
from handy_dandy_library.file_processing import read_lines

from collections import defaultdict


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
        # We need to use tarjan's bridge finding algorithm with chained decomposition.
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


def tests():
    directed_graph = DirectedGraph2D.from_lines(read_lines("day_25_1_test_input1.txt"))
    print(directed_graph)
    edge_cuts = directed_graph.minimal_cuts_3_edge_connected_graph()



def main():
    tests()


if __name__ == "__main__":
    main()
