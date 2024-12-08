from handy_dandy_library.file_processing import read_lines

from day8_1 import AntennaTracker


def tests():
    antenna_tracker = AntennaTracker(read_lines("puzzle8_1_test_input1.txt"))

    t1 = antenna_tracker.unique_t_antinodes_count
    assert t1 == 34


def main():
    tests()

    antenna_tracker = AntennaTracker(read_lines("puzzle8_1.txt"))

    t2 = antenna_tracker.unique_t_antinodes_count
    assert t2 == 905


if __name__ == "__main__":
    main()
