from typing import Iterable

from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import are_equal


class XmasCounter:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.n = len(lines)
        self.m = len(lines[0])

    @property
    def total_xmas_count(self) -> int:
        if self.n < 4:
            if self.m < 4:
                return 0
            return sum(self.total_xmas_count_per_line(line) for line in self.lines)
        if self.m < 4:
            return sum(self.total_xmas_count_per_line(line) for line in self.lines_vertical)

        total = 0
        total += sum(self.total_xmas_count_per_line(line) for line in self.lines)
        total += sum(self.total_xmas_count_per_line(line) for line in self.lines_vertical)
        total += sum(self.total_xmas_count_per_line(line) for line in self.lines_diagonal_down_right)
        total += sum(self.total_xmas_count_per_line(line) for line in self.lines_diagonal_down_left)
        return total

    @staticmethod
    def total_xmas_count_per_line(line: str) -> int:
        total = 0
        line_length = len(line)
        i = 0
        while i < line_length - 3:
            if are_equal(line[i:i + 4], "XMAS"):
                total += 1
                i += 3
                continue
            if are_equal(line[i:i + 4], "SAMX"):
                total += 1
                i += 3
                continue
            i += 1
        return total

    @property
    def lines_vertical(self) -> tuple[str]:
        return tuple(''.join([self.lines[i][j] for i in range(self.n)]) for j in range(self.m))

    @property
    def lines_diagonal_down_right(self) -> list[str]:
        lines_diagonal = [None for _ in range(self.m - 3 + self.n - 4)]
        line_counter = 0

        offset = 0
        while offset < self.m - 3:
            line = ""
            max_iterations = min(self.m - offset, self.n)
            for i in range(max_iterations):
                line += self.lines[i][i + offset]

            lines_diagonal[line_counter] = line
            line_counter += 1
            offset += 1

        offset = 1
        while offset < self.n - 3:
            line = ""
            max_iterations = min(self.m, self.n - offset)
            for i in range(max_iterations):
                line += self.lines[i + offset][i]

            lines_diagonal[line_counter] = line
            line_counter += 1
            offset += 1

        return lines_diagonal

    @property
    def lines_diagonal_down_left(self) -> list[str]:
        lines_diagonal = [None for _ in range(self.m - 3 + self.n - 4)]
        line_counter = 0

        offset = 0
        while offset < self.m - 3:
            line = ""
            max_iterations = min(self.m - offset, self.n)
            for i in range(max_iterations - 1, -1, -1):
                a, b = max_iterations - i - 1, i
                line += self.lines[a][b]

            lines_diagonal[line_counter] = line
            line_counter += 1
            offset += 1

        offset = 1
        while offset < self.n - 3:
            line = ""
            max_iterations = min(self.m, self.n - offset)
            for i in range(max_iterations - 1, -1, -1):
                a, b = max_iterations - 1 - i + offset, i + offset
                line += self.lines[a][b]

            lines_diagonal[line_counter] = line
            line_counter += 1
            offset += 1
        return lines_diagonal


def tests():
    xmas_counter = XmasCounter(read_lines("puzzle4_1_test_input1.txt"))
    assert xmas_counter.total_xmas_count_per_line("MAMXMASAMX") == 2
    assert sum(xmas_counter.total_xmas_count_per_line(line) for line in xmas_counter.lines) == 5
    assert sum(xmas_counter.total_xmas_count_per_line(line) for line in xmas_counter.lines_vertical) == 3
    t1 = xmas_counter.total_xmas_count
    assert t1 == 18


def main():
    tests()

    xmas_counter = XmasCounter(read_lines("puzzle4_1.txt"))
    t2 = xmas_counter.total_xmas_count
    assert t2 == 2406


if __name__ == "__main__":
    main()
