from collections import Counter

from handy_dandy_library.file_processing import read_lines

from day1_1 import pair_from_line


def pairs_from_lines(lines: list[str]) -> (list[int], list[int]):
    n = len(lines)
    x = [0 for _ in range(n)]
    y = [0 for _ in range(n)]
    for i, line in enumerate(lines):
        pair = pair_from_line(line)
        x[i], y[i] = pair[0], pair[1]
    return x, y


def total_frequency_pairwise_sums(lines: list[str]) -> int:
    x, y = pairs_from_lines(lines)
    y_counts = Counter(y)
    return sum(a * y_counts[a] for a in x)


def tests():
    assert total_frequency_pairwise_sums(read_lines("puzzle1_test_input1.txt")) == 31


def main():
    tests()
    total = total_frequency_pairwise_sums(read_lines("puzzle1_1.txt"))
    assert total == 26407426


if __name__ == "__main__":
    main()
