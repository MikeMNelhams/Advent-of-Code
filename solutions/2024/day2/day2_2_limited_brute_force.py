from handy_dandy_library.file_processing import read_lines

from day2_1 import levels_from_line, is_safe


def is_safe_with_cut_brute_force(levels: list[int]) -> bool:
    # O(n^2)
    m = len(levels)
    assert m >= 3, ValueError("Invalid levels")

    if is_safe(levels):
        return True

    return any(is_safe(tuple(x for j, x in enumerate(levels) if j != i)) for i in range(m))


def number_of_safe_levels(lines: str) -> int:
    return sum((is_safe_with_cut_brute_force(levels_from_line(line)) for line in lines))


def tests():
    t1 = number_of_safe_levels(read_lines("puzzle1_test_input1.txt"))
    print(t1)
    assert t1 == 4

    assert is_safe_with_cut_brute_force(levels=[10, 6, 4, 2, 1])
    assert is_safe_with_cut_brute_force(levels=[1, 2, 5, 8, 9, 13])
    assert not is_safe_with_cut_brute_force(levels=[1, 3, 1, 1, 4, 5])

    t2 = number_of_safe_levels(read_lines("puzzle1_1.txt"))
    print(t2)


def main():
    tests()


if __name__ == "__main__":
    main()
