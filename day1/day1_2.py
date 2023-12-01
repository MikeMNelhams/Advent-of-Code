from day1_1 import read_lines
from handy_dandy_string_manipulations.string_manipulations import DIGIT_NUMERALS, DIGIT_NUMERAL_REPLACEMENTS


NUMERAL_FIRST_LETTERS = {"o", "t", "f", "s", "e", "n"}
NUMERAL_LAST_LETTERS = {"e", "o", "r", "x", "n", "t"}


def first_digit_or_numeral(phrase: str) -> int:
    m = len(phrase) - 1
    for i, char in enumerate(phrase):
        if char in NUMERAL_FIRST_LETTERS:
            for numeral in DIGIT_NUMERALS:
                numeral_length = len(numeral)
                is_valid_length = m - i >= numeral_length
                if is_valid_length and phrase[i:i + numeral_length] == numeral:
                    return int(DIGIT_NUMERAL_REPLACEMENTS[numeral])
        if char.isdigit():
            return int(char)

    raise TypeError


def last_digit_or_numeral(phrase: str) -> int:
    m = len(phrase) - 1
    for i, char in enumerate(reversed(phrase)):
        if char in NUMERAL_LAST_LETTERS:
            for numeral in DIGIT_NUMERALS:
                numeral_length = len(numeral)
                is_valid_length = m - i >= numeral_length
                if is_valid_length and phrase[-i - 1:-i - 1 - numeral_length:-1] == numeral[::-1]:
                    return int(DIGIT_NUMERAL_REPLACEMENTS[numeral])

        if char.isdigit():
            return int(char)

    raise TypeError


def calibration_value(phrase: str) -> int:
    total = 10 * first_digit_or_numeral(phrase) + last_digit_or_numeral(phrase)
    return total


def sum_calibration_values(file_path: str) -> int:
    return sum(calibration_value(phrase) for phrase in read_lines(file_path))


def tests():
    test_lines = read_lines("puzzle2_test_input.txt")
    assert first_digit_or_numeral(test_lines[0]) == 2
    assert first_digit_or_numeral(test_lines[1]) == 8
    assert first_digit_or_numeral(test_lines[2]) == 1
    assert first_digit_or_numeral(test_lines[3]) == 2
    assert first_digit_or_numeral(test_lines[4]) == 4

    assert last_digit_or_numeral(test_lines[0]) == 9
    assert last_digit_or_numeral(test_lines[1]) == 3
    assert last_digit_or_numeral(test_lines[2]) == 3
    assert last_digit_or_numeral(test_lines[3]) == 4
    assert last_digit_or_numeral(test_lines[4]) == 2

    assert sum_calibration_values("puzzle2_test_input.txt") == 281


def main():
    tests()

    t = sum_calibration_values("puzzle1_input.txt")
    print(t)


if __name__ == "__main__":
    main()
