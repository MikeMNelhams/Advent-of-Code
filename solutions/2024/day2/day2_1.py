from handy_dandy_library.file_processing import read_lines


def levels_from_line(line: str) -> list[int]:
    return [int(x) for x in line.split(' ')]


def is_safe(levels: list[int] | tuple[int]) -> bool:
    m = len(levels)

    assert m >= 3, ValueError("Invalid levels")

    first_difference = levels[1] - levels[0]
    is_increasing = first_difference > 0
    first_displacement = abs(first_difference)
    if first_displacement > 3 or first_displacement < 1:
        return False

    for i in range(1, m - 1):
        current_difference = levels[i+1] - levels[i]
        if (current_difference > 0) != is_increasing:
            return False
        current_displacement = abs(current_difference)
        if current_displacement > 3 or current_displacement < 1:
            return False

    return True


def number_of_safe_levels(lines: str) -> int:
    return sum((is_safe(levels_from_line(line)) for line in lines))


def tests():
    t1 = number_of_safe_levels(read_lines("puzzle2_test_input1.txt"))
    assert t1 == 2

    t2 = number_of_safe_levels(read_lines("puzzle2_1.txt"))
    print(t2)


def main():
    tests()


if __name__ == "__main__":
    main()
