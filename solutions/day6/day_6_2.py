import operator
from functools import reduce

from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import find_first_char_index, parse_int_ignore_spaces
from day_6_1 import number_of_ways_to_beat_race


def product_ways2(lines: list[str]):
    colon_index = find_first_char_index(lines[0], ':')
    time_limit = parse_int_ignore_spaces(lines[0][colon_index + 1:])
    colon_index = find_first_char_index(lines[1], ':')
    distance_record = parse_int_ignore_spaces(lines[1][colon_index + 1:])
    print(time_limit, distance_record)
    return number_of_ways_to_beat_race(time_limit, distance_record)


def tests():
    assert product_ways2(read_lines("day_6_1_test_input.txt")) == 71503


def main():
    tests()
    print('-'*100)
    t = product_ways2(read_lines("day_6_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
