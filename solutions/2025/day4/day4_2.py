from handy_dandy_library.file_processing import read_lines

from day4_1 import PaperRollGrid


def count_future_accessible_rolls(puzzle_path: str) -> int:
    lines = read_lines(puzzle_path)
    grid = PaperRollGrid(lines)
    return grid.count_future_accessible_rolls()


def main():
    assert count_future_accessible_rolls("puzzle4_1_test_input.txt") == 43
    t = count_future_accessible_rolls("puzzle4_1.txt")
    print(t)


if __name__ == "__main__":
    main()
