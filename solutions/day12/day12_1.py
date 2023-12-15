from handy_dandy_library.file_processing import read_lines
import math
from itertools import accumulate


def contiguous_permutations_collective(capacity: int, ordered_contiguous_lengths: list[int]) -> int:
    total_elements = sum(ordered_contiguous_lengths)

    if total_elements > capacity:
        raise ValueError

    number_of_contiguous_lengths = len(ordered_contiguous_lengths)
    space_required = total_elements + number_of_contiguous_lengths - 1

    if space_required == capacity:
        return 1

    # Nonogram formula
    return math.comb(capacity - total_elements + 1, number_of_contiguous_lengths)


def contiguous_permutations(capacity: int, number_of_elements: int) -> int:
    return capacity - number_of_elements + 1


def combinations_from_puzzle_line(line: str) -> int:
    input_halves = line.split(' ')
    nonogram_numbers = [int(char) for char in input_halves[1].split(',')]
    nonogram_string = input_halves[0] + '.'
    total_combinations = 0

    chars_to_check = [[nonogram_string, 0, nonogram_numbers]]
    while chars_to_check:
        step = chars_to_check.pop()
        if not step[0]:
            total_combinations += int(not step[1] and not step[2])
            continue

        potential_chars = [".", "#"]
        if step[0][0] != '?':
            potential_chars = step[0][0]

        for char in potential_chars:
            if char == "#":
                chars_to_check.append([step[0][1:], step[1] + 1, step[2]])
                continue
            if not step[1]:
                chars_to_check.append([step[0][1:], 0, step[2]])
                continue
            if step[2] and step[2][0] == step[1]:
                chars_to_check.append([step[0][1:], 0, step[2][1:]])

    return total_combinations


def combinations_from_puzzle(lines: list[str]) -> int:
    return sum(combinations_from_puzzle_line(line) for line in lines)


def tests():
    assert contiguous_permutations(3, 1) == 3
    assert contiguous_permutations(3, 2) == 2
    assert contiguous_permutations(4, 1) == 4
    assert contiguous_permutations(4, 2) == 3
    assert contiguous_permutations(4, 3) == 2
    assert contiguous_permutations(5, 1) == 5
    assert contiguous_permutations(5, 2) == 4
    assert contiguous_permutations(5, 3) == 3
    assert contiguous_permutations(5, 5) == 1
    assert contiguous_permutations(1, 1) == 1

    assert contiguous_permutations_collective(3, [1, 1]) == 1
    assert contiguous_permutations_collective(4, [1, 1]) == 3
    assert contiguous_permutations_collective(4, [1, 2]) == 1
    assert contiguous_permutations_collective(4, [2, 1]) == 1
    assert contiguous_permutations_collective(5, [1, 1]) == 6
    assert contiguous_permutations_collective(5, [2, 1]) == 3
    assert contiguous_permutations_collective(5, [1, 2]) == 3
    assert contiguous_permutations_collective(5, [2, 2]) == 1
    assert contiguous_permutations_collective(5, [3, 1]) == 1
    assert contiguous_permutations_collective(6, [1, 1]) == 10
    assert contiguous_permutations_collective(500, [34, 68]) == contiguous_permutations_collective(500, [68, 34])
    assert contiguous_permutations_collective(5, [1, 1, 1]) == 1
    assert contiguous_permutations_collective(6, [1, 1, 1]) == 4

    assert combinations_from_puzzle_line("???.### 1,1,3") == 1
    assert combinations_from_puzzle_line(".??..??...?##. 1,1,3") == 4
    assert combinations_from_puzzle_line("?#?#?#?#?#?#?#? 1,3,1,6") == 1
    assert combinations_from_puzzle_line("????.#...#... 4,1,1") == 1
    assert combinations_from_puzzle_line("????.######..#####. 1,6,5") == 4

    assert combinations_from_puzzle(read_lines("day_12_1_test_input.txt")) == 21


def main():
    tests()

    t = combinations_from_puzzle(read_lines("day_12_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
