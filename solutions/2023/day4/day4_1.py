from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.string_manipulations import find_first_char_index


def get_separator_indices(line: str) -> (int, int):
    colon_index = find_first_char_index(line, ':')
    pipe_index = find_first_char_index(line[colon_index + 2:], '|')
    pipe_index += colon_index + 2
    return colon_index, pipe_index


def parse_card(line: str, colon_index: int, pipe_index: int) -> (set[int], list[int]):
    winning_values = {int(value) for value in line[colon_index + 1:pipe_index - 1].split(' ') if value != ''}
    chosen_values = tuple(int(value) for value in line[pipe_index + 1:].split(' ') if value != '')
    return winning_values, chosen_values


def card_points(winning_values: set[int], chosen_values: tuple[int]) -> int:
    match_count = number_of_matches(winning_values, chosen_values)
    if match_count == 0:
        return 0
    return 2 ** (match_count - 1)


def number_of_matches(winning_values: set[int], chosen_values: tuple[int]) -> int:
    match_count = 0
    for value in chosen_values:
        if value in winning_values:
            match_count += 1
    return match_count


def total_points(lines: list[str]) -> int:
    start_index, end_index = get_separator_indices(lines[0])
    return sum(card_points(*parse_card(line, start_index, end_index)) for line in lines)


def tests():
    assert card_points({13, 32, 20, 16, 61}, (61, 30, 68, 82, 17, 32, 24, 19)) == 2
    assert total_points(read_lines("day_4_1_test_input.txt")) == 13


def main():
    tests()

    t = total_points(read_lines("day_4_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
