from handy_dandy_library.file_processing import read_lines
from day4_1 import get_separator_indices, parse_card, number_of_matches
from collections import deque


def total_scratchcards(lines: list[str]) -> int:
    # Given that cards cannot cause overflow victories. Card 6 must have 0 matches.
    n = len(lines)
    start_index, end_index = get_separator_indices(lines[0])
    number_of_winning_values_per_card = len(parse_card(lines[0], start_index, end_index)[0])
    total = 0
    window = deque([1 for _ in range(number_of_winning_values_per_card + 1)])

    window_cutoff = n - number_of_winning_values_per_card
    print(f"cutoff: {window_cutoff}")
    for i, line in enumerate(lines):
        match_count = number_of_matches(*parse_card(line, start_index, end_index))

        print(f"total: {total} | i: {i} | match_count: {match_count} | window: {window}")
        current_number_of_scorecards = window.popleft()
        total += current_number_of_scorecards

        if i < window_cutoff:
            window.append(1)

        for j in range(match_count):
            window[j] += current_number_of_scorecards

    return total


def tests():
    assert total_scratchcards(read_lines("day_4_2_test_input.txt")) == 30


def main():
    tests()

    t = total_scratchcards(read_lines("day_4_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
