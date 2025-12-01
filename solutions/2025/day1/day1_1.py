from handy_dandy_library.file_processing import read_lines

DIRECTIONS = {"L": -1, "R": 1}


def count_zero_remainders(puzzle_path: str) -> int:
    rotations = read_lines(puzzle_path)
    x = 50
    total_zeroes = 0
    for rotation in rotations:
        x += int(rotation[1:]) * DIRECTIONS[rotation[0]]
        x %= 100
        if x == 0:
            total_zeroes += 1
    return total_zeroes


def main():
    assert count_zero_remainders("puzzle1_1_test_input.txt") == 3
    t = count_zero_remainders("puzzle1_1.txt")
    assert t == 1059


if __name__ == "__main__":
    main()
