from handy_dandy_library.file_processing import read_lines
from day16_1 import MirrorGrid


def tests():
    mirror_grid = MirrorGrid.from_lines(read_lines("day_16_1_test_input1.txt"))
    assert mirror_grid.max_energy() == 51


def main():
    tests()

    mirror_grid = MirrorGrid.from_lines(read_lines("day_16_1_input.txt"))
    t = mirror_grid.max_energy()
    print(t)


if __name__ == "__main__":
    main()
