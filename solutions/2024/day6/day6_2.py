import profile
import time

from handy_dandy_library.file_processing import read_lines

from day6_1 import GuardPredictor


def tests():
    guard_predictor = GuardPredictor(read_lines("puzzle6_1_test_input1.txt"))

    t1 = guard_predictor.unique_obstacles_that_create_loop_count()

    assert t1 == 6


def main():
    tests()

    guard_predictor = GuardPredictor(read_lines("puzzle6_1.txt"))

    t2 = guard_predictor.unique_obstacles_that_create_loop_count()
    assert t2 == 1976


if __name__ == "__main__":
    main()
