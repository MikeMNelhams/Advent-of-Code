from handy_dandy_library.file_processing import read_lines
from handy_dandy_library.linear_algebra import Vector2D

from day18_1 import FallingByteGrid


def tests():
    fallen_bytes_grid = FallingByteGrid(read_lines("puzzle18_1_test_input1.txt"), 7, 7)

    t1, bad_byte = fallen_bytes_grid.binary_search_failure_byte()
    assert bad_byte == Vector2D((6, 1))


def main():
    tests()

    fallen_bytes_grid = FallingByteGrid(read_lines("puzzle18_1.txt"), 71, 71)

    t1, bad_byte = fallen_bytes_grid.binary_search_failure_byte()
    assert bad_byte == Vector2D((58, 44))


if __name__ == "__main__":
    main()
