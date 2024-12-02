import operator

from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import find_first_char_index, parse_ints
from functools import reduce

import math


def number_of_ints_between_two_floats(lower: int, higher: int) -> int:
    lower_floor = math.floor(lower)
    higher_ceiling = math.floor(higher)
    return max(higher_ceiling - lower_floor, 0)


def is_approximately_an_integer(x: float, precision: int = 8) -> bool:
    return x - round(x, precision) == 0


def distance_raced(time_spent_charging: int, race_time_limit: int) -> int:
    return time_spent_charging * (race_time_limit - time_spent_charging)


def number_of_ways_to_beat_race(race_time_limit: int, race_record: int) -> int:
    b = race_time_limit / 2.0
    determinant = 0.5 * math.sqrt(race_time_limit ** 2 - 4 * race_record)
    c1 = b - determinant
    c2 = b + determinant
    count = number_of_ints_between_two_floats(c1, c2)
    if is_approximately_an_integer(c1) or is_approximately_an_integer(c2):
        count -= 1
    return count


def product_ways(lines: list[str]):
    colon_index = find_first_char_index(lines[0], ':')
    time_limits = parse_ints(lines[0][colon_index + 1:])
    colon_index = find_first_char_index(lines[1], ':')
    distance_records = parse_ints(lines[1][colon_index + 1:])
    return reduce(operator.mul, (number_of_ways_to_beat_race(t, r) for t, r in zip(time_limits, distance_records)))


def tests():
    assert number_of_ways_to_beat_race(7, 9) == 4
    assert number_of_ways_to_beat_race(15, 40) == 8
    assert number_of_ways_to_beat_race(30, 200) == 9

    assert product_ways(read_lines("day_6_1_test_input.txt")) == 288


def main():
    tests()

    t = product_ways(read_lines("day_6_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
