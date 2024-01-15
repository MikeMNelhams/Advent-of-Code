import time

from handy_dandy_library.file_processing import read_lines
from day12_1 import combinations_from_puzzle


def unfold_line(line: str) -> str:
    input_halves = line.split(' ')
    nonogram_numbers = input_halves[1].split(',') * 5
    nonogram_string = (input_halves[0] + '?') * 5
    nonogram_string = nonogram_string[:-1]

    nonogram_numbers_string = ",".join(nonogram_numbers)
    return f"{nonogram_string} {nonogram_numbers_string}"


def unfold(lines: list[str]) -> list[str]:
    return [unfold_line(line) for line in lines]


def tests():
    assert unfold_line(read_lines("day_12_1_test_input.txt")[0]) == "???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3"
    assert combinations_from_puzzle(unfold(read_lines("day_12_1_test_input.txt"))) == 525152


def main():
    tests()

    # t = combinations_from_puzzle(unfold(read_lines("day_12_1_input.txt")))
    # print(t)


if __name__ == "__main__":
    main()
