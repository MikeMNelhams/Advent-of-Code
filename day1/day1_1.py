def read_lines(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        content = [line[:-1] if line[-1] == '\n' else line for line in file]
    return content


def calibration_value(phrase: str) -> int:
    total = 10 * first_digit(phrase) + first_digit(reversed(phrase))
    return total


def first_digit(phrase: str) -> int:
    for char in phrase:
        if char.isdigit():
            return int(char)
    raise TypeError


def sum_calibration_values(file_path: str) -> int:
    return sum(calibration_value(phrase) for phrase in read_lines(file_path))


def tests():
    assert calibration_value("1abc2") == 12
    assert calibration_value("pqr3stu8vwx") == 38
    assert calibration_value("a1b2c3d4e5f") == 15
    assert calibration_value("treb7uchet") == 77
    assert sum_calibration_values("puzzle1_test_input.txt") == 142


def main():
    t = sum_calibration_values("puzzle1_input.txt")
    print(t)


if __name__ == "__main__":
    main()
