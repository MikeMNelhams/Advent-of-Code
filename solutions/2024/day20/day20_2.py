from handy_dandy_library.file_processing import read_lines

from day20_1 import Racetrack


def tests():
    racetrack = Racetrack(read_lines("puzzle20_1_test_input1.txt"))

    t1 = racetrack.best_cheats_count(20, 50)
    assert t1 == 285


def main():
    tests()

    racetrack = Racetrack(read_lines("puzzle20_1.txt"))

    t1 = racetrack.best_cheats_count(20, 100)
    assert t1 == 1017615


if __name__ == "__main__":
    main()
