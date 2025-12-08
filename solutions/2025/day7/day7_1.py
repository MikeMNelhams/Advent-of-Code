from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import make_blue

import bisect
from collections import defaultdict


class TachyonGrid:
    def __init__(self, puzzle_path: str):
        lines = read_lines(puzzle_path)
        self.splitters = self.__find_splitters(lines)
        self.start_point = self.__find_start_coordinate(lines)
        self.n = len(lines)
        self.m = len(lines[0])

    def __find_splitters(self, lines: list[str]) -> dict[list[int]]:
        n = len(lines)
        m = len(lines[0])
        splitters = {j: [i for i in range(n) if lines[i][j] == "^"] for j in range(m)}
        splitters = {key: value for key, value in splitters.items() if value}
        return splitters

    def __find_start_coordinate(self, lines: list[str]) ->tuple[int]:
        start_point = [0, -1]
        for j in range(len(lines[0])):
            if lines[0][j] == "S":
                start_point[1] = j
                break
        return tuple(start_point)

    def simulate_split_beams_count(self) -> int:
        beams = [self.start_point]
        beam_split_count = 0
        already_split = set()
        for _ in range(self.n):
            if not beams:
                return beam_split_count
            new_beams = set()
            for beam in beams:
                if beam[1] not in self.splitters:
                    continue
                splitters_in_column = self.splitters[beam[1]]

                splitter_index = bisect.bisect(splitters_in_column, beam[0])
                if splitter_index == len(splitters_in_column):
                    continue

                splitter_x = splitters_in_column[splitter_index]
                if (splitter_x, beam[1]) in already_split:
                    continue
                beam_split_count += 1
                already_split.add((splitter_x, beam[1]))

                if beam[1] > 0:
                    new_beams.add((splitter_x, beam[1] - 1))
                if beam[1] < self.m - 1:
                    new_beams.add((splitter_x, beam[1] + 1))
            beams = list(new_beams)
        raise ValueError("AHHH THERE'S TACHYON BEAMS EVERYWHERE!")

    def simulate_paths_count(self) -> int:
        paths = defaultdict(int)
        paths[(self.start_point[0], self.start_point[1])] = 1
        paths_count = 0
        for _ in range(self.n):
            if not paths:
                return paths_count
            new_paths = defaultdict(int)
            for path, count in paths.items():
                if path[1] not in self.splitters:
                    paths_count += count
                    continue

                splitters_in_column = self.splitters[path[1]]

                splitter_index = bisect.bisect(splitters_in_column, path[0])
                if splitter_index == len(splitters_in_column):
                    paths_count += count
                    continue

                splitter_x = splitters_in_column[splitter_index]

                if path[1] > 0:
                    new_paths[(splitter_x, path[1] - 1)] += count
                if path[1] < self.m - 1:
                    new_paths[(splitter_x, path[1] + 1)] += count
            paths = new_paths
        raise ValueError("AHHH THERE'S TACHYON BEAMS EVERYWHERE!")


def main():
    test_tachyon_grid = TachyonGrid("puzzle7_1_test_input.txt")
    assert test_tachyon_grid.simulate_split_beams_count() == 21

    tachyon_grid = TachyonGrid("puzzle7_2.txt")
    print(tachyon_grid.simulate_split_beams_count())


if __name__ == "__main__":
    main()
