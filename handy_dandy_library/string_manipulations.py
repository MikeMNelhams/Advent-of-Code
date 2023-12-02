import re


DIGIT_NUMERALS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")

DIGIT_NUMERAL_REPLACEMENTS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
                              "six": "6", "seven": "7", "eight": "8", "nine": "9"}


def convert_numeric_in_text_to_digits(phrase: str) -> str:
    """ One pass literal numeric to digit numeric """
    digit_replacements_escaped = map(re.escape, DIGIT_NUMERAL_REPLACEMENTS)

    # OR regex to match any digit replacement strings
    pattern = re.compile("|".join(digit_replacements_escaped), 0)

    def digit_matching(match):
        return DIGIT_NUMERAL_REPLACEMENTS[match.group(0)]

    return pattern.sub(digit_matching, phrase)


def find_first_char_index(phrase: str, target_char: str) -> int:
    for i, char in enumerate(phrase):
        if char == target_char:
            return i

    if len(target_char) > 1:
        raise TypeError(f"target_char: \'{target_char}\' is more than 1 character long!")

    return -1


if __name__ == "__main__":
    print("This is a library file. Import, but don't run.")
