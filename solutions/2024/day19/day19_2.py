from handy_dandy_library.file_processing import read_lines

from day19_1 import TowelPatternChecker


def tests():
    toweler = TowelPatternChecker(read_lines("puzzle19_1_test_input1.txt"))

    t1 = toweler.possible_towel_combinations()
    print(t1)
    assert t1 == 16


def main():
    tests()

    toweler = TowelPatternChecker(read_lines("puzzle19_1.txt"))
    t1 = toweler.possible_towel_combinations()
    print(t1)


if __name__ == "__main__":
    main()
