import operator

from handy_dandy_library.file_processing import read_lines
from day3_1 import adjacent_indices
from functools import reduce


class Star:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def __repr__(self):
        return f"Star({self.row}, {self.column})"


def find_stars(lines: list[str]) -> list[Star]:
    stars_found = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '*':
                stars_found.append(Star(i, j))
    return stars_found


def total_gear_ratios(lines: list[str]) -> int:
    all_stars = find_stars(lines)
    total_gear_ratio = 0

    for star in all_stars:
        adjacent_parts = set()
        adjacents_indices_to_star = adjacent_indices(star.row, star.column)
        for indices in adjacents_indices_to_star:
            if lines[indices[0]][indices[1]].isdigit():
                adjacent_parts.add(part_from_digit_indices(lines, indices))
        if len(adjacent_parts) == 2:
            total_gear_ratio += reduce(operator.mul, adjacent_parts)

    return total_gear_ratio


def part_from_digit_indices(lines: list[str], digit_indices: list[int]) -> int:
    row = lines[digit_indices[0]]
    m = len(row) - 1
    pivot_index = digit_indices[1]
    start_index = -1
    end_index = -1

    for i, char in enumerate(row[pivot_index:]):
        if not char.isdigit():
            end_index = i
            break
        if i + pivot_index == m:
            end_index = m
            break

    for i, char in enumerate(row[pivot_index::-1]):
        if not char.isdigit():
            start_index = i - 1
            break

        if pivot_index - i == 0:
            start_index = i
            break

    part = int(row[pivot_index - start_index:pivot_index + end_index])
    return part


def tests():
    assert total_gear_ratios(read_lines("day_3_2_test_input.txt")) == 467835


def main():
    tests()

    t = total_gear_ratios(read_lines("day_3_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
