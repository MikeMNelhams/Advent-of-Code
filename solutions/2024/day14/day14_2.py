from handy_dandy_library.file_processing import read_lines

from day14_1 import EasterBunnyHQBathroom


def tests():
    pass
    # No meaningful tests can be constructed.


def main():
    tests()

    ebhq_bathroom = EasterBunnyHQBathroom(read_lines("puzzle14_1.txt"))
    ebhq_bathroom.attempt_secret_xmas(101, 103)


if __name__ == "__main__":
    main()
