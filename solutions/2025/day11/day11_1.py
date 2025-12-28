from handy_dandy_library.file_processing import read_lines

from collections import defaultdict, deque


class Grid:
    def __init__(self, puzzle_path: str):
        lines = read_lines(puzzle_path)
        self.adjacency_graph = self.__adjacency_graph(lines)

    @staticmethod
    def __adjacency_graph(lines: list[str]) -> dict[str, list[str]]:
        graph = {}
        for line in lines:
            phrases = line.split(": ")
            x = phrases[0]
            y = phrases[1].split(" ")
            graph[x] = y
        return graph

    def unique_path_count(self, start: str, end: str) -> int:
        parents = defaultdict(set)
        for key, values in self.adjacency_graph.items():
            for value in values:
                parents[value].add(key)

        to_check = deque([])
        to_check_set = set()
        for key in self.adjacency_graph:
            if key not in parents:
                to_check.append(key)
                to_check_set.add(key)
        checked = set()
        path_count = defaultdict(lambda: 0)
        path_count[start] += 1

        while to_check:
            x = to_check.popleft()
            neighbours = self.adjacency_graph.get(x, [])
            for child in neighbours:
                if child in checked:
                    continue
                parents[child].remove(x)
            to_check_set.remove(x)
            x_count = path_count[x]
            for neighbour in neighbours:
                path_count[neighbour] += x_count
                if neighbour not in checked and neighbour not in to_check_set and not parents[neighbour]:
                    to_check.append(neighbour)
                    to_check_set.add(neighbour)

            checked.add(x)

        return path_count.get(end, 0) // path_count.get(start, 1)

    def path_svr_fft_or_dac_out_count(self) -> int:
        svr_to_fft_count = self.unique_path_count("svr", "fft")
        svr_to_dac_count = self.unique_path_count("svr", "dac")

        if svr_to_fft_count == 0 or svr_to_dac_count == 0:
            raise ValueError("Graph does not contain valid inner nodes FFT or DAC")
        if svr_to_fft_count == svr_to_dac_count:
            raise ValueError("Graph contains cycle or is disconnected!")

        if svr_to_fft_count < svr_to_dac_count:
            return svr_to_fft_count * self.unique_path_count("fft", "dac") * self.unique_path_count("dac", "out")
        return svr_to_dac_count * self.unique_path_count("dac", "fft") * self.unique_path_count("fft", "out")


def main():
    test_grid = Grid("day11_1_test_input.txt")
    assert test_grid.unique_path_count("you", "out") == 5

    grid = Grid("day11_1.txt")
    t = grid.unique_path_count("you", "out")
    print(t)
    # 21 is just wrong kekw


if __name__ == "__main__":
    main()
