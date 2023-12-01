from day1_1 import read_lines
from handy_dandy_string_manipulations.string_manipulations import DIGIT_NUMERALS, DIGIT_NUMERAL_REPLACEMENTS


NUMERAL_FIRST_LETTERS = {"o", "t", "f", "s", "e", "n"}


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


def tests():
    test_lines = read_lines("puzzle2_test_input.txt")
    assert first_digit_or_numeral(test_lines[0]) == 2
    assert first_digit_or_numeral(test_lines[1]) == 8
    assert first_digit_or_numeral(test_lines[2]) == 1
    assert first_digit_or_numeral(test_lines[3]) == 2
    assert first_digit_or_numeral(test_lines[4]) == 4


def main():
    tests()


if __name__ == "__main__":
    main()
