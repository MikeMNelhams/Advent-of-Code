from handy_dandy_library.file_processing import read_lines

type RockCoordinates = list[list[int]]


class MirrorMapper:
    dimension_weights = [100, 1]

    def __init__(self, lines: list[str]):
        self.rocks = self.__rock_coordinates(lines)
        self.n = len(lines)
        self.m = len(lines[0])

    @staticmethod
    def __rock_coordinates(lines: list[str]) -> RockCoordinates:
        rocks = [[1 if char == '#' else 0 for char in line] for line in lines]
        return rocks

    def rock_column(self, index: int) -> list[int]:
        return [self.rocks[i][index] for i in range(self.n)]

    def shape(self, dimension: int) -> int:
        if dimension == 0:
            return self.n
        return self.m

    def get_rock_row_or_column(self, index: int, dimension: int) -> list[int]:
        if dimension == 0:
            return self.rocks[index]
        return self.rock_column(index)

    def is_mirrored(self, index: int, dimension: int) -> bool:
        dim_length = self.shape(dimension)
        if index > dim_length - 2:
            return False

        above_index = index + 1
        below_index = index

        while below_index >= 0 and above_index < dim_length:
            above = self.get_rock_row_or_column(above_index, dimension)
            below = self.get_rock_row_or_column(below_index, dimension)
            if above != below:
                return False
            above_index += 1
            below_index -= 1
        return True

    def is_smudged_mirrored(self, index: int, dimension: int) -> bool:
        dim_length = self.shape(dimension)
        if index > dim_length - 2:
            return False

        above_index = index + 1
        below_index = index
        incorrect_count = 0
        while below_index >= 0 and above_index < dim_length:
            above = self.get_rock_row_or_column(above_index, dimension)
            below = self.get_rock_row_or_column(below_index, dimension)
            if above != below:
                incorrect_count = sum(1 if a != b else 0 for a, b in zip(above, below))
            if incorrect_count > 1:
                return False
            above_index += 1
            below_index -= 1
        return incorrect_count == 1

    def mirror_summary(self, smudged: bool=False) -> int:
        is_reflected = self.is_mirrored
        if smudged:
            is_reflected = self.is_smudged_mirrored

        for dimension in range(2):
            dimension_length = self.shape(dimension)
            for i in range(dimension_length):
                if is_reflected(i, dimension):
                    return self.dimension_weights[dimension] * (i + 1)

        raise ZeroDivisionError


def read_puzzles(lines: list[str]) -> list[list[str]]:
    puzzles = []
    indices = [i for i, line in enumerate(lines) if line == ''] + [len(lines)]

    start = 0
    for index in indices:
        puzzle = lines[start:index]
        puzzles.append(puzzle)
        start = index + 1

    return puzzles


def test2():
    mirror_mapper2 = MirrorMapper(read_lines("day_13_1_test_input1.txt"))
    assert mirror_mapper2.mirror_summary() == 5

    mirror_mapper1 = MirrorMapper(read_lines("day_13_1_test_input2.txt"))
    assert mirror_mapper1.mirror_summary() == 400

    assert mirror_mapper1.mirror_summary() + mirror_mapper2.mirror_summary() == 405


def test1():
    mirror_mapper = MirrorMapper(read_lines("day_13_1_test_input1.txt"))

    assert not mirror_mapper.is_mirrored(0, 0)
    assert not mirror_mapper.is_mirrored(1, 0)
    assert not mirror_mapper.is_mirrored(2, 0)
    assert not mirror_mapper.is_mirrored(3, 0)
    assert not mirror_mapper.is_mirrored(4, 0)
    assert not mirror_mapper.is_mirrored(5, 0)
    assert not mirror_mapper.is_mirrored(6, 0)

    assert not mirror_mapper.is_mirrored(0, 1)
    assert not mirror_mapper.is_mirrored(1, 1)
    assert not mirror_mapper.is_mirrored(2, 1)
    assert not mirror_mapper.is_mirrored(3, 1)
    assert mirror_mapper.is_mirrored(4, 1)
    assert not mirror_mapper.is_mirrored(5, 1)
    assert not mirror_mapper.is_mirrored(6, 1)
    assert not mirror_mapper.is_mirrored(7, 1)
    assert mirror_mapper.mirror_summary() == 5


def main():
    test1()
    test2()

    puzzles = read_puzzles(read_lines("day_13_1_input.txt"))

    total = sum(MirrorMapper(puzzle).mirror_summary() for puzzle in puzzles)
    print(total)


if __name__ == "__main__":
    main()
