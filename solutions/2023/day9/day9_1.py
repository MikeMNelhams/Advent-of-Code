from handy_dandy_library.file_processing import read_lines


def line_to_sequence(line: str) -> list[int]:
    return [int(x) for x in line.split(' ')]


def differences(sequence: list[int]) -> list[int]:
    return [sequence[i] - sequence[i - 1] for i in range(1, len(sequence))]


def oasis(sequence: list[int]) -> int:
    difference_sequences = [sequence.copy()]
    for _ in range(len(sequence) - 2):
        if difference_sequences[-1][-1] == 0:
            break
        difference_sequences.append(differences(difference_sequences[-1]))

    print(difference_sequences)

    total = 0
    for sequence in difference_sequences[:-1]:
        total += sequence[-1]
        print(total)

    return total


def oasis_total(lines: list[str]) -> int:
    return sum(oasis(line_to_sequence(line)) for line in lines)


def tests():
    assert oasis_total(read_lines("day_9_1_test_input.txt")) == 114


def main():
    tests()

    # t = oasis_total(read_lines("day_9_1_input.txt"))
    # print(t)


if __name__ == "__main__":
    main()
