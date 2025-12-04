from handy_dandy_library.file_processing import read_lines


def joltage(bank: str) -> int:
    first_digit_index = -1
    maximum = -1
    for i, battery in enumerate(bank[:-1]):
        x = int(battery)
        if x > maximum:
            first_digit_index = i
            maximum = x
    adjusted_bank = [x for i, x in enumerate(bank) if i > first_digit_index]
    second_maximum = max(adjusted_bank)
    return int(str(maximum) + str(second_maximum))


def total_output_joltage(puzzle_path: str) -> int:
    lines = read_lines(puzzle_path)
    return sum([joltage(bank) for bank in lines])


def main():
    assert total_output_joltage("puzzle3_1_test_input.txt") == 357
    t = total_output_joltage("puzzle3_1.txt")


if __name__ == "__main__":
    main()
