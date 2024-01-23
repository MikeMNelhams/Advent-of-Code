from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import DIGIT_NUMERALS, DIGIT_NUMERAL_REPLACEMENTS
from typing import Callable


NUMERAL_FIRST_LETTERS = {"o", "t", "f", "s", "e", "n"}
NUMERAL_LAST_LETTERS = {"e", "o", "r", "part_list", "n", "t"}


def digit_or_numeral_first_match(phrase: str, match_pattern: Callable) -> int:
    m = len(phrase) - 1
    for i, char in enumerate(phrase):
        if char in NUMERAL_LAST_LETTERS:
            for numeral in DIGIT_NUMERALS:
                is_valid_length = m - i >= len(numeral)
                if is_valid_length and match_pattern(i, numeral, phrase):
                    return int(DIGIT_NUMERAL_REPLACEMENTS[numeral])

        if char.isdigit():
            return int(char)

    raise TypeError


def substring_match_forwards(start_index: int, numeral: str, phrase: str) -> bool:
    return phrase[start_index:start_index + len(numeral)] == numeral


def substring_match_backwards(start_index: int, numeral: str, phrase: str) -> bool:
    return phrase[start_index:start_index + len(numeral)] == numeral[::-1]


def calibration_value(phrase: str) -> int:
    first_digit = digit_or_numeral_first_match(phrase, substring_match_forwards)
    total = 10 * first_digit + digit_or_numeral_first_match(phrase[::-1], substring_match_backwards)
    return total


def sum_calibration_values(file_path: str) -> int:
    return sum(calibration_value(phrase) for phrase in read_lines(file_path))


def tests():
    assert calibration_value("eightwothree") == 83  # noqa
    assert sum_calibration_values("puzzle1_2_test_input.txt") == 281


def main():
    tests()

    t = sum_calibration_values("puzzle1_input.txt")
    print(t)


if __name__ == "__main__":
    main()
