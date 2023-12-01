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


if __name__ == "__main__":
    print("This is a library file. Import, but don't run.")
