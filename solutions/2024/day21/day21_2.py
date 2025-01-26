from handy_dandy_library.file_processing import read_lines

from day21_1 import total_complexity


def tests():
    pass
    # No test cases :(


def main():
    tests()

    t1 = total_complexity(read_lines("puzzle21_1.txt"), 25)
    assert t1 == 129551515895690


if __name__ == "__main__":
    main()
