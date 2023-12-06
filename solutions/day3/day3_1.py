from handy_dandy_library.file_processing import read_lines
import numpy as np

index_filter = np.array([[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]])


def total_parts(lines: list[str]) -> int:
    intersection_indices = symbol_adjacent_indices(lines)
    total = 0

    m = len(lines[0])

    for i, line in enumerate(lines):
        digit_start_index = -1
        valid_part = False
        print(f"line: {i}")
        for j, char in enumerate(line):
            if digit_start_index == -1 and char.isdigit():
                digit_start_index = j

            if digit_start_index != -1:
                if char.isdigit() and intersection_indices[i, j] == 1:
                    valid_part = True

                if not char.isdigit():
                    if valid_part:
                        number_found = int(line[digit_start_index:j])
                        print(f"Found: {number_found}")
                        total += number_found
                    digit_start_index = -1
                    valid_part = False

                if j == m - 1 and valid_part:
                    number_found = int(line[digit_start_index:])
                    print(f"Found: {number_found}")
                    total += number_found
        print('-'*50)
    return total


def symbol_adjacent_indices(lines: list[str]) -> np.array:
    n = len(lines)
    m = len(lines[0])

    all_indices = np.zeros((n, m))

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char != '.' and not char.isdigit():
                mark_valid_indices(all_indices, i, j)

    return all_indices


def mark_valid_indices(indices: np.array, row: int, column: int) -> None:
    adjacents = adjacent_indices(row, column)
    for row in adjacents:
        indices[row[0], row[1]] = 1
    return None


def adjacent_indices(row: int, column: int) -> np.array:
    indices = index_filter.copy()
    indices[:, 0] += row
    indices[:, 1] += column
    return indices


def tests():
    lines = read_lines("day_3_1_test_input.txt")
    assert total_parts(lines) == 4361


def main():
    # tests()

    t = total_parts(read_lines("day_3_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
