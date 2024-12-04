from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import are_equal


class MASxCounter:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.n = len(lines)
        self.m = len(lines[0])

    @property
    def total_masx_count(self) -> int:
        if self.n < 3 and self.m < 3:
            return 0

        total = 0
        for i in range(1, self.n - 1):
            for j in range(1, self.m - 1):
                centre = self.lines[i][j]
                if centre != 'A':
                    continue

                ul = self.lines[i - 1][j - 1]
                ur = self.lines[i - 1][j + 1]
                dr = self.lines[i + 1][j + 1]
                dl = self.lines[i + 1][j - 1]
                dr_diagonal = ul + centre + dr
                dr_valid = are_equal(dr_diagonal, "MAS") or are_equal(dr_diagonal, "SAM")

                if not dr_valid:
                    continue

                dl_diagonal = ur + centre + dl
                dl_valid = (are_equal(dl_diagonal, "MAS") or are_equal(dl_diagonal, "SAM"))

                total += int(dl_valid)

        return total


def tests():
    mas_x_counter = MASxCounter(read_lines("puzzle4_1_test_input1.txt"))
    assert mas_x_counter.total_masx_count == 9


def main():
    tests()

    mas_x_counter = MASxCounter(read_lines("puzzle4_1.txt"))
    t2 = mas_x_counter.total_masx_count
    assert t2 == 1807


if __name__ == "__main__":
    main()
