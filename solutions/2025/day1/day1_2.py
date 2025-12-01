from handy_dandy_library.file_processing import read_lines
from day1_1 import DIRECTIONS


def count_zero_remainder_crosses(puzzle_path: str) -> int:
    rotations = read_lines(puzzle_path)
    x = 50
    total_zero_remainder_intersects = 0
    for rotation in rotations:
        x0 = x
        x += int(rotation[1:]) * DIRECTIONS[rotation[0]]
        total_zero_remainder_intersects += abs(x) // 100
        if rotation[0] == "L" and x0 > 0:
            total_zero_remainder_intersects += int(x <= 0)
        x %= 100
    return total_zero_remainder_intersects


def main():
    assert count_zero_remainder_crosses("puzzle1_1_test_input.txt") == 6
    t = count_zero_remainder_crosses("puzzle1_1.txt")
    assert t == 6305


if __name__ == "__main__":
    main()
