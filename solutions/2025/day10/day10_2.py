from handy_dandy_library.file_processing import read_lines

from day10_1 import MachineOperator


def fewest_joltage_valid_button_presses(puzzle_path: str) -> int:
    lines = read_lines(puzzle_path)
    return sum(MachineOperator(line).fewest_joltage_valid_button_presses() for line in lines)


def main():
    assert fewest_joltage_valid_button_presses("day10_1_test_input.txt") == 33

    t = fewest_joltage_valid_button_presses("day10_1.txt")
    assert t == 16663


if __name__ == "__main__":
    main()
