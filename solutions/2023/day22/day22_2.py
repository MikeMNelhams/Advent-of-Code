from handy_dandy_library.file_processing import read_lines

from day22_1 import BrickFactory, FallingBricks


def tests():
    falling_bricks = FallingBricks([BrickFactory.from_line(line) for line in read_lines("day_22_1_test_input.txt")])
    assert falling_bricks.number_of_falls_from_vital_blocks() == 7


def main():
    tests()

    falling_bricks = FallingBricks([BrickFactory.from_line(line) for line in read_lines("day_22_1_input.txt")])
    t = falling_bricks.number_of_falls_from_vital_blocks()
    print(t)


if __name__ == "__main__":
    main()
