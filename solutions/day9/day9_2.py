from handy_dandy_library.file_processing import read_lines
from day9_1 import differences, line_to_sequence


def oasis_backwards(sequence: list[int]) -> int:
    difference_sequences = [sequence.copy()]
    n = len(sequence)
    for _ in range(n - 2):
        if difference_sequences[-1][-1] == 0:
            break
        difference_sequences.append(differences(difference_sequences[-1]))

    total = 0
    for i in range(len(difference_sequences) - 1, -1, -1):
        total = difference_sequences[i][0] - total

    return total


def oasis_backwards_total(lines: list[str]) -> int:
    return sum(oasis_backwards(line_to_sequence(line)) for line in lines)


def tests():
    assert oasis_backwards_total(read_lines("day_9_1_test_input.txt")) == 2


def main():
    tests()

    t = oasis_backwards_total(read_lines("day_9_1_input.txt"))
    print(t)


if __name__ == "__main__":
    main()
