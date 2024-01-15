from handy_dandy_library.file_processing import read_lines
from day10_1 import PipeGrid


def tests():
    pipe_grid = PipeGrid.from_lines(read_lines("day_10_1_test_input1.txt"))
    assert pipe_grid.area_enclosed == 1

    pipe_grid2 = PipeGrid.from_lines(read_lines("day_10_1_test_input2.txt"))
    assert pipe_grid2.area_enclosed == 1

    pipe_grid3 = PipeGrid.from_lines(read_lines("day_10_1_test_input3.txt"))
    assert pipe_grid3.area_enclosed == 1

    pipe_grid4 = PipeGrid.from_lines(read_lines("day_10_2_test_input1.txt"))
    assert pipe_grid4.area_enclosed == 4

    pipe_grid5 = PipeGrid.from_lines(read_lines("day_10_2_test_input2.txt"))
    assert pipe_grid5.area_enclosed == 8

    pipe_grid6 = PipeGrid.from_lines(read_lines("day_10_2_test_input3.txt"))
    assert pipe_grid6.area_enclosed == 10


def main():
    tests()

    pipe_grid = PipeGrid.from_lines(read_lines("day_10_1_input.txt"))
    t = pipe_grid.area_enclosed

    assert t == 511


if __name__ == "__main__":
    main()
