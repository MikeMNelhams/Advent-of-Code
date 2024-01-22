from handy_dandy_library.file_processing import read_lines


type Grid = list[list[int, int]]


def empty_grid(number_of_rows: int, number_of_columns: int) -> Grid:
    return [[0 for _ in range(number_of_columns)] for _ in range(number_of_rows)]


class RockNRoller:
    HARD_ROCK_CHAR = '#'
    SMOOTH_ROCK_CHAR = 'O'
    EMPTY_CHAR = '.'
    ROCK_ENCODINGS = {EMPTY_CHAR: 0, HARD_ROCK_CHAR: 1, SMOOTH_ROCK_CHAR: 2}
    ROCK_ENCODINGS_REVERSED = {0: EMPTY_CHAR, 1: HARD_ROCK_CHAR, 2: SMOOTH_ROCK_CHAR}

    def __init__(self, encoded_grid: Grid):
        self.encoded_grid = encoded_grid
        self.encoded_grid_transposed = self.__grid_transposed(encoded_grid)
        self.n = len(encoded_grid)
        self.m = len(encoded_grid[0])

    def __repr__(self) -> str:
        return '\n'.join(''.join(self.ROCK_ENCODINGS_REVERSED[encoding] for encoding in line)
                         for line in self.encoded_grid)

    @property
    def hard_rock_encoding(self) -> int:
        return self.ROCK_ENCODINGS[self.HARD_ROCK_CHAR]

    @property
    def smooth_rock_encoding(self) -> int:
        return self.ROCK_ENCODINGS[self.SMOOTH_ROCK_CHAR]

    @classmethod
    def from_lines(cls, lines: list[str]):
        n = len(lines)
        m = len(lines[0])
        encoded_grid = empty_grid(n, m)

        for i, row in enumerate(lines):
            for j, char in enumerate(row):
                encoded_grid[i][j] = cls.ROCK_ENCODINGS[char]

        return cls(encoded_grid)

    @staticmethod
    def __grid_transposed(grid: Grid) -> Grid:
        n = len(grid)
        m = len(grid[0])
        transposed_grid = empty_grid(m, n)

        for i, row in enumerate(grid):
            for j, encoding in enumerate(row):
                transposed_grid[j][i] = encoding

        return transposed_grid

    def roll_north(self) -> None:
        hard_rock_encoding = self.hard_rock_encoding
        smooth_rock_encoding = self.smooth_rock_encoding
        hard_rock_positions = [[i for i, encoding in enumerate(self.encoded_grid_transposed[col_idx])
                                        if encoding == hard_rock_encoding] + [self.n] for col_idx in range(self.m)]
        smooth_rock_positions = [[i for i, encoding in enumerate(self.encoded_grid_transposed[col_idx])
                                        if encoding == smooth_rock_encoding] for col_idx in range(self.m)]

        new_grid = empty_grid(self.n, self.m)

        for j, hard_rocks in enumerate(hard_rock_positions):
            for hard_rock in hard_rocks[:-1]:
                new_grid[hard_rock][j] = hard_rock_encoding

        for col_idx in range(self.m):
            hard_idx = 0
            current_smooth_rock_idx = 0
            for smooth_rock in smooth_rock_positions[col_idx]:
                hard_rock = hard_rock_positions[col_idx][hard_idx]
                while smooth_rock > hard_rock:
                    current_smooth_rock_idx = hard_rock + 1
                    hard_idx += 1
                    hard_rock = hard_rock_positions[col_idx][hard_idx]
                new_grid[current_smooth_rock_idx][col_idx] = smooth_rock_encoding
                current_smooth_rock_idx += 1

        self.encoded_grid = new_grid
        self.encoded_grid_transposed = self.__grid_transposed(new_grid)
        return None

    @property
    def total_load(self) -> int:
        total = 0
        smooth_rock_encoding = self.smooth_rock_encoding

        for i, row in enumerate(reversed(self.encoded_grid), 1):
            for j, encoding in enumerate(row):
                if encoding == smooth_rock_encoding:
                    total += i
        return total


def test1():
    rock_roller = RockNRoller.from_lines(read_lines("day_14_1_test_input1.txt"))
    rock_roller.roll_north()
    assert rock_roller.total_load == 136


def test2():
    rock_roller = RockNRoller.from_lines(read_lines("day_14_1_test_input2.txt"))
    assert rock_roller.total_load == 136


def tests():
    test1()
    test2()


def main():
    tests()

    rock_roller = RockNRoller.from_lines(read_lines("day_14_1_input.txt"))
    rock_roller.roll_north()
    t = rock_roller.total_load
    assert t == 108889


if __name__ == "__main__":
    main()
