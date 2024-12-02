from bisect import insort

from handy_dandy_library.file_processing import read_lines


def pair_from_line(line: str) -> (int, int):
    pair = line.split('   ')
    return int(pair[0]), int(pair[1])


def sorted_pairs_from_lines(lines: list[str]) -> (list[int], list[int]):
    x = []
    y = []
    for line in lines:
        pair = pair_from_line(line)
        insort(x, pair[0])
        insort(y, pair[1])
    return x, y


def total_pairwise_distances(x: list[int], y: list[int]) -> int:
    return sum(abs(a - b) for a, b in zip(x, y))


def tests():
    lines = read_lines("puzzle1_test_input1.txt")
    assert total_pairwise_distances(*sorted_pairs_from_lines(lines)) == 11


def main():
    tests()
    total = total_pairwise_distances(*sorted_pairs_from_lines(read_lines("puzzle1_1.txt")))
    assert total == 3569916


if __name__ == "__main__":
    main()
