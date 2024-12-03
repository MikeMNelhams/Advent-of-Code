from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import sign

from day2_1 import levels_from_line, is_safe


from collections import defaultdict


def is_safe_edge_case_checking(levels: list[int] | tuple[int]) -> (bool, int, int, int):
    m = len(levels)
    assert m >= 3, ValueError("Invalid levels")

    bad_gradient_signs_count = 0
    bad_gradients_count = 0

    is_definitely_safe = True
    first_bad_index = -1
    gradient_signs_count = defaultdict(int)

    first_difference = levels[1] - levels[0]
    first_gradient_sign = sign(first_difference)
    first_displacement = abs(first_difference)
    gradient_signs_count[first_gradient_sign] += 1

    if first_displacement > 3 or first_displacement < 1:
        is_definitely_safe = False
        first_bad_index = 0
        bad_gradients_count += 1

    for i in range(1, m - 1):
        current_difference = levels[i+1] - levels[i]

        gradient_sign = sign(current_difference)
        gradient_signs_count[gradient_sign] += 1
        if gradient_sign != first_gradient_sign:
            if first_bad_index == -1:
                first_bad_index = i
            is_definitely_safe = False

        current_displacement = abs(current_difference)
        if current_displacement > 3 or current_displacement < 1:
            if first_bad_index == -1:
                first_bad_index = i
            is_definitely_safe = False
            bad_gradients_count += 1

    if len(gradient_signs_count) > 1:
        bad_gradient_signs_count = min(gradient_signs_count.values())

    return is_definitely_safe, first_bad_index, bad_gradient_signs_count, bad_gradients_count


def is_safe_with_cut(levels: list[int]) -> bool:
    m = len(levels)
    # O(kn) where k is the number of bad indices to cut
    # Instead of checking every possible cut and seeing which one works:
    #   Try to check if it's safe. If it's not, then remember the bad difference index.
    #   Try checking the safety of the levels with the cuts:
    #       - left of bad index
    #       - current bad index
    #       - right of bad index
    # This works, because if there is MORE than one bad difference index, the levels are definitely bad, otherwise...
    #   the bad element MUST be within 1 index of the bad difference index

    assert m >= 3, ValueError("Invalid levels")

    is_definitely_safe, first_bad_index, bad_signs_count, bad_gradients_count = is_safe_edge_case_checking(levels)
    if is_definitely_safe:
        return True

    if bad_signs_count > 1:
        return False

    if bad_gradients_count > 1:
        return False

    if first_bad_index == 0 and is_safe(levels[1:]):
        return True

    if first_bad_index == m - 1 and is_safe(levels[:-1]):
        return is_definitely_safe

    # Must be a middle element that's bad! Let's cut the left, current, and right element!
    if any(is_safe([x for i, x in enumerate(levels) if i != first_bad_index + j]) for j in range(-1, 2)):
        return True

    return False


def number_of_safe_levels(lines: str) -> int:
    return sum((is_safe_with_cut(levels_from_line(line)) for line in lines))


def tests():
    t1 = number_of_safe_levels(read_lines("puzzle2_test_input1.txt"))
    print(t1)
    assert t1 == 4

    assert is_safe_with_cut(levels=[10, 6, 4, 2, 1])
    assert is_safe_with_cut(levels=[1, 2, 5, 8, 9, 13])

    t2 = number_of_safe_levels(read_lines("puzzle2_1.txt"))
    print(t2)
    assert t2 == 301


def main():
    tests()


if __name__ == "__main__":
    main()
