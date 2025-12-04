from handy_dandy_library.file_processing import read_lines


def dozen_joltage(bank: str):
    bank2 = [int(battery) for battery in bank]
    joltages = [0 for _ in range(12)]
    for i in range(12):
        index_to_remove = -1
        bank_cut = bank2[:-(11 - i)]
        if -(11 - i) == 0:
            bank_cut = bank2
        for j, battery in enumerate(bank_cut):
            if battery > joltages[i]:
                index_to_remove = j
                joltages[i] = battery
        bank2 = [x for i, x in enumerate(bank2) if i > index_to_remove]
    y = int("".join([str(x) for x in joltages]))
    return y


def sum_dozen_joltage(puzzle_path: str) -> int:
    lines = read_lines(puzzle_path)
    return sum([dozen_joltage(bank) for bank in lines])


def main():
    assert sum_dozen_joltage("puzzle3_1_test_input.txt") == 3121910778619
    t = sum_dozen_joltage("puzzle3_1.txt")


if __name__ == "__main__":
    main()
