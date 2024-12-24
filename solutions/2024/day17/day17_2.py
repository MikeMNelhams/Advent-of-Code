from handy_dandy_library.file_processing import read_lines

from day17_1 import ChronospatialComputer


def tests():
    chrono_computer = ChronospatialComputer(read_lines("puzzle17_2_test_input1.txt"))

    a1 = chrono_computer.determine_tauto_a()
    assert a1 == 117440


def main():
    # tests()
    chrono_computer = ChronospatialComputer(read_lines("puzzle17_1.txt"))

    print(a2)


if __name__ == "__main__":
    main()
