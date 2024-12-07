from handy_dandy_library.file_processing import read_lines

from day7_1 import Calibrator


def tests():
    calibrator = Calibrator(read_lines("puzzle7_1_test_input1.txt"))

    assert calibrator.operation_challenges[3].is_possible2()

    assert calibrator.possible_challenges_sum3() == 11387


def main():
    tests()

    calibrator = Calibrator(read_lines("puzzle7_1.txt"))

    t2 = calibrator.possible_challenges_sum3()
    assert t2 == 424977609625985


if __name__ == "__main__":
    main()
